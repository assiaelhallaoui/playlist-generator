import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)
MODEL = os.environ.get("NVIDIA_MODEL", "mistralai/mistral-large-4-1t-a52b")

class ScenarioAnalysis(BaseModel):
    themes: list[str] = Field(description="Core themes of the situation")
    emotions: list[str] = Field(description="Emotions the person is feeling")
    narrative: str = Field(description="2-3 sentence summary of what happened")
    relationship_dynamics: str = Field(description="Who is involved and how they relate")
    lyrical_meaning: str = Field(description="What a song would need to say to truly mirror this situation")


SYSTEM_PROMPT = """You analyze a personal situation described by a user so it can be \
matched to songs whose lyrics tell a similar story.

Return ONLY a JSON object with exactly these keys:
- "themes": list of 3-6 short strings (e.g. "unspoken feelings", "missed opportunity")
- "emotions": list of 3-6 short strings
- "narrative": 2-3 sentences summarizing the situation in the third person
- "relationship_dynamics": one sentence on who is involved and the dynamic between them
- "lyrical_meaning": 1-2 sentences describing what a song would have to be about to \
mirror this exact situation (be specific, not just "sad love song")

Be specific to the situation. No markdown, no commentary, JSON only."""

def _extract_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in model output: {text[:200]}")
    return text[start : end + 1]

def analyze_scenario(scenario: str) -> ScenarioAnalysis:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": scenario},
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    choice = response.choices[0]
    raw = choice.message.content

    if not raw:
        # Debug: on regarde ce que le modèle a vraiment renvoyé
        print("finish_reason:", choice.finish_reason)
        print("message complet:", choice.message)
        raise ValueError("Le modèle a renvoyé une réponse vide")

    return ScenarioAnalysis.model_validate_json(_extract_json(raw))

if __name__ == "__main__":
    example = (
        "I had feelings for someone but never told them. Now they've moved on "
        "with someone else, and I keep thinking about what could have happened."
    )
    print(analyze_scenario(example).model_dump_json(indent=2))