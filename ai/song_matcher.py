import json
from pathlib import Path

import numpy as np

from ai.embeddings import embed_texts
from ai.scenario_analyzer import analyze_scenario


def analysis_to_text(a: dict) -> str:
    """Même format de texte pour les chansons ET les scénarios."""
    return "\n".join(
        [
            f"Narrative: {a.get('narrative', '')}",
            f"Relationship: {a.get('relationship_dynamics', '')}",
            f"Meaning: {a.get('lyrical_meaning', '')}",
            f"Themes: {', '.join(a.get('themes', []))}",
            f"Emotions: {', '.join(a.get('emotions', []))}",
        ]
    )


def load_songs(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):  # {song_id: {...}} -> liste
        data = [{"id": k, **v} for k, v in data.items()]
    return data


def match_songs(scenario: str, songs_path: str = "data/test_songs.json", top_k: int = 5):
    songs = load_songs(songs_path)

    scenario_analysis = analyze_scenario(scenario).model_dump()
    query_vec = embed_texts([analysis_to_text(scenario_analysis)], input_type="query")[0]
    song_vecs = embed_texts([analysis_to_text(s) for s in songs], input_type="passage")

    # similarité cosinus
    query_vec = query_vec / np.linalg.norm(query_vec)
    song_vecs = song_vecs / np.linalg.norm(song_vecs, axis=1, keepdims=True)
    scores = song_vecs @ query_vec

    ranked = sorted(zip(songs, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]