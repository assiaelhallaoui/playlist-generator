
from ai.lyrics_analyzer import analyze_lyrics, save_analysis
import json

# Original fictional lyrics for testing
test_lyrics = """
I see you standing on the other side
We pass each other every night
I wrote the words but never sent
And now I wonder where the summer went

You found somebody, I stayed behind
Replaying moments in my mind
I had the chance but let it go
Now there are things you'll never know
"""

analysis = analyze_lyrics(
    title="Unsent",
    artist="Test Artist",
    lyrics=test_lyrics
)

print(json.dumps(analysis, indent=2, ensure_ascii=False))

save_analysis("test_001", analysis)
