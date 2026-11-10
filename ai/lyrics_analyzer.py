# Receive lyrics from a source authorized for AI processing.
# Send the lyrics to an AI model.
# Extract themes, emotions, and narrative meaning.
# Return structured JSON.
# Save the analysis so you don't have to process the same song repeatedly.


# Receive lyrics from a source authorized for AI processing.
# Send the lyrics to Mistral Large 4 through NVIDIA.
# Extract themes, emotions, and narrative meaning.
# Return structured JSON.
# Save the analysis to avoid processing the same song repeatedly.

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError


# ========== CONFIGURATION ==========

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("NVIDIA_API_KEY")

if not API_KEY:
    raise RuntimeError("NVIDIA_API_KEY is missing from .env")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://integrate.api.nvidia.com/v1",
    timeout=120.0,
)

MODEL = os.getenv(
    "NVIDIA_MODEL",
    "mistralai/mistral-large-4-1t-a52b"
)


# ========== DATA MODEL ==========

class SongAnalysis(BaseModel):
    themes: list[str]
    emotions: list[str]
    narrative: str
    relationship_dynamics: list[str]
    lyrical_meaning: str


# ========== LYRICS ANALYSIS ==========

def analyze_lyrics(title: str, artist: str, lyrics: str) -> dict:

    if not lyrics.strip():
        raise ValueError("Lyrics cannot be empty.")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a music lyrics analyst. "
                    "Analyze only the supplied lyrics. "
                    "Identify the specific situations, emotions, "
                    "themes, narrative and relationship dynamics. "
                    "Do not invent details or quote the lyrics. "
                    "Return ONLY a compact JSON object with "
                    "exactly these fields: "
                    "themes, emotions, narrative, "
                    "relationship_dynamics, lyrical_meaning. "
                    "Themes, emotions and relationship_dynamics "
                    "must be arrays of strings. "
                    "Narrative and lyrical_meaning must be strings. "
                    "Keep the analysis concise. "
                    "Do not include Markdown or additional text."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Song title: {title}\n"
                    f"Artist: {artist}\n\n"
                    f"Lyrics:\n{lyrics}"
                )
            }
        ],
        temperature=0.2,
        max_tokens=8192,
        extra_body={
            "reasoning_effort": "low"
        },
        stream=False
    )

    # ========== RESPONSE HANDLING ==========

    choice = response.choices[0]

    content = choice.message.content
    finish_reason = choice.finish_reason

    print("FINISH REASON:", finish_reason)

    if finish_reason == "length":
        raise RuntimeError(
            "Mistral reached its token limit before completing "
            "the response. Try increasing max_tokens or using "
            "a model with lower reasoning requirements."
        )

    if not content or not isinstance(content, str):
        raise RuntimeError(
            "Mistral returned no text response. "
            f"Finish reason: {finish_reason}"
        )

    # ========== CLEAN JSON ==========

    clean_content = content.strip()

    # Remove Markdown code fences if present
    if clean_content.startswith("```"):
        lines = clean_content.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        clean_content = "\n".join(lines).strip()

    # ========== VALIDATE JSON ==========

    try:
        parsed_json = json.loads(clean_content)

        analysis = SongAnalysis.model_validate(
            parsed_json
        )

    except json.JSONDecodeError as error:
        print("RAW MODEL RESPONSE:")
        print(repr(content))

        raise RuntimeError(
            "Mistral returned invalid JSON."
        ) from error

    except ValidationError as error:
        print("RAW MODEL RESPONSE:")
        print(repr(content))

        raise RuntimeError(
            "Mistral returned JSON that does not match "
            "the required SongAnalysis structure."
        ) from error

    return analysis.model_dump()


# ========== SAVE ANALYSIS ==========


def save_analysis(song_id: str, analysis: dict):
    """
    Save the analysis to data/song_themes.json.
    Replace an existing entry with the same song_id.
    """

    output_path = ROOT_DIR / "data" / "song_themes.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing analyses
    if output_path.exists() and output_path.stat().st_size > 0:
        try:
            with open(output_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "song_themes.json contains invalid JSON. "
                "Fix or back up the file before saving."
            ) from error
    else:
        data = []

    if not isinstance(data, list):
        raise ValueError(
            "song_themes.json must contain a JSON array."
        )

    # Remove any previous analysis for this song
    data = [
        song for song in data
        if song.get("song_id") != song_id
    ]

    # Add the new analysis
    data.append({
        "song_id": song_id,
        "analysis_source": "provided_lyrics",
        "analysis": analysis
    })

    # Save the updated data
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Analysis saved for {song_id}")
