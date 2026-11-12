from ai.song_matcher import match_songs

SCENARIOS = [
    "I had feelings for someone but never told them. Now they've moved on with someone else.",
    "My best friend and I drifted apart after I moved cities, and I miss who we used to be.",
    "I finally left a job that was destroying me, but I feel guilty and weirdly lost.",
]

if __name__ == "__main__":
    for s in SCENARIOS:
        print("=" * 60)
        print(s)
        for song, score in match_songs(s, top_k=3):
            print(f"  {score:.3f}  {song['title']} - {song['artist']}")