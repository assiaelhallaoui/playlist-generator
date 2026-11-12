from ai.reranker import recommend

SCENARIOS = [
    "I had feelings for someone but never told them. Now they've moved on with someone else.",
    "My best friend and I drifted apart after I moved cities, and I miss who we used to be.",
    "I finally left a job that was destroying me, but I feel guilty and weirdly lost.",
]

if __name__ == "__main__":
    for s in SCENARIOS:
        print("=" * 60)
        print(s)
        for song in recommend(s, retrieve_k=8, final_k=3):
            print(
                f"  LLM {song['llm_score']}/10 | sim {song['similarity']:.2f} | "
                f"{song['title']} - {song['artist']}"
            )
            print(f"      {song['reason']}")