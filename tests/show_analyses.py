import json
import sys

songs = {s["id"]: s for s in json.load(open("data/song_analyses.json", encoding="utf-8"))}
ids = sys.argv[1:] or ["song_006", "song_008", "song_017", "song_020", "song_043"]

for i in ids:
    s = songs.get(i)
    if not s:
        continue
    print("=" * 60)
    print(f"{s['title']} - {s['artist']}  [{s['confidence']}]")
    print("Narrative:", s["narrative"])
    print("Meaning:  ", s["lyrical_meaning"])
    print("Themes:   ", ", ".join(s["themes"]))