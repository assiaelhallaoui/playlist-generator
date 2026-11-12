import json

from pydantic import BaseModel, Field

from ai.scenario_analyzer import MODEL, _extract_json, client


class RankedSong(BaseModel):
    id: str
    score: int = Field(ge=0, le=10)
    reason: str


class RerankResult(BaseModel):
    ranking: list[RankedSong]


SYSTEM_PROMPT = """You help match a user's personal situation to songs whose lyrics \
tell a similar story.

You receive the situation and a list of candidate songs (with id, title, artist and \
a short analysis of each). Score every candidate from 0 to 10 on how well the song's \
story and emotions mirror this specific situation (not just the general mood).

Return ONLY a JSON object:
{"ranking": [{"id": "<song id>", "score": <0-10>, "reason": "<one sentence explaining \
the match>"}, ...]}

Rules:
- Include every candidate exactly once, ordered from best to worst match.
- Each reason must be one sentence, specific to the situation and the song.
- JSON only, no markdown, no commentary."""


def rerank(scenario: str, candidates: list[dict]) -> list[dict]:
    payload = [
        {
            "id": str(c["id"]),
            "title": c.get("title", ""),
            "artist": c.get("artist", ""),
            "narrative": c.get("narrative", ""),
            "lyrical_meaning": c.get("lyrical_meaning", ""),
            "themes": c.get("themes", []),
            "emotions": c.get("emotions", []),
        }
        for c in candidates
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Situation:\n{scenario}\n\nCandidates:\n"
                f"{json.dumps(payload, ensure_ascii=False)}",
            },
        ],
        temperature=0.2,
        max_tokens=8000,
    )
    raw = response.choices[0].message.content
    if not raw:
        raise ValueError(f"Réponse vide (finish_reason={response.choices[0].finish_reason})")

    result = RerankResult.model_validate_json(_extract_json(raw))

    by_id = {str(c["id"]): c for c in candidates}
    final = []
    for item in result.ranking:
        song = by_id.get(item.id)
        if song:  # ignore les ids inventés par le modèle
            final.append({**song, "llm_score": item.score, "reason": item.reason})
    return sorted(final, key=lambda s: s["llm_score"], reverse=True)


def recommend(scenario: str, retrieve_k: int = 8, final_k: int = 5) -> list[dict]:
    from ai.song_matcher import match_songs

    candidates = []
    for song, sim in match_songs(scenario, top_k=retrieve_k):
        candidates.append({**song, "similarity": float(sim)})
    return rerank(scenario, candidates)[:final_k]