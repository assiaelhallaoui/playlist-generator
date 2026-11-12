from ai.scenario_analyzer import analyze_scenario

SCENARIOS = [
    "I had feelings for someone but never told them. Now they've moved on with someone else.",
    "My best friend and I drifted apart after I moved cities, and I miss who we used to be.",
    "I finally left a job that was destroying me, but I feel guilty and weirdly lost.",
]

if __name__ == "__main__":
    for s in SCENARIOS:
        print("=" * 60)
        print(s)
        result = analyze_scenario(s)
        print(result.model_dump_json(indent=2))