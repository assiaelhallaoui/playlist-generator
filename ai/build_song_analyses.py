import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from ai.scenario_analyzer import MODEL, _extract_json, client

SONGS_PATH = Path("data/songs.json")
OUT_PATH = Path("data/song_analyses.json")


class SongAnalysis(BaseModel):
    confidence: Literal["high", "low"]
    themes: list[str] = []
    emotions: list[str] = []
    narrative: str = ""
    relationship_dynamics: str = ""
    lyrical_meaning: str = ""
    key_details: list[str] = []

SYSTEM_PROMPT = """You analyze what a song is about so it can be matched to a person's \
life situation.

You receive a song's title, artist and album, and sometimes "notes": a trusted \
summary written by the user. If notes are given, base your analysis on them and treat \
them as more reliable than your own memory.

Rules:
- A title or a single image is NOT evidence of the meaning. Never infer the story from \
the title alone. Lyrics are often figurative: objects, places and flowers usually stand \
for feelings, not literal events.
- Only describe the song if you can recall its actual content (specific scenes, \
statements or the overall message), or if notes were provided. Otherwise set \
"confidence" to "low" and leave the other fields empty.
- Set "confidence" to "high" ONLY if you are certain. If you are partly unsure, use "low".
- Describe the story in your own words. NEVER quote lyrics.

Return ONLY a JSON object with exactly these keys:
- "confidence": "high" or "low"
- "key_details": 2-3 specific details of the song you are relying on (empty if low)
- "themes": list of 3-6 short strings
- "emotions": list of 3-6 short strings
- "narrative": 2-3 sentences on the story, in the third person
- "relationship_dynamics": one sentence on who is involved and the dynamic
- "lyrical_meaning": 1-2 sentences on what the song is really about, not generic

JSON only, no markdown."""


def analyze_song(song: dict) -> SongAnalysis:
    user_msg = (
        f"Title: {song['title']}\nArtist: {song['artist']}\n"
        f"Album: {song.get('album', '')} ({song.get('release_year', '')})"
    )
    if song.get("notes"):
        user_msg += f"\n\nNotes (trusted summary): {song['notes']}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=8000,
    )
    raw = response.choices[0].message.content
    if not raw:
        raise ValueError(f"empty response (finish_reason={response.choices[0].finish_reason})")
    return SongAnalysis.model_validate_json(_extract_json(raw))


if __name__ == "__main__":
    songs = json.loads(SONGS_PATH.read_text(encoding="utf-8"))
    done = {}
    if OUT_PATH.exists():
        done = {s["id"]: s for s in json.loads(OUT_PATH.read_text(encoding="utf-8"))}

    for i, song in enumerate(songs, 1):
        if song["id"] in done:
            continue
        try:
            analysis = analyze_song(song).model_dump()
            done[song["id"]] = {**song, **analysis}
            print(f"[{i}/{len(songs)}] {analysis['confidence']:4} {song['title']} - {song['artist']}")
        except Exception as e:
            print(f"[{i}/{len(songs)}] FAILED {song['title']}: {str(e)[:100]}")
            continue
        OUT_PATH.write_text(
            json.dumps(list(done.values()), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    low = [s["title"] for s in done.values() if s["confidence"] == "low"]
    print(f"\nDone: {len(done)} songs, {len(low)} low confidence: {low}")