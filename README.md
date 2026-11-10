# Between the Lines

**An AI-powered Spotify playlist generator based on lyrical meaning and musical storytelling**

Between the Lines is a web application that generates personalized Spotify playlists based on a user's experiences, emotions, and personal situations.

Instead of recommending songs based solely on genre, popularity, or musical similarity, Between the Lines focuses on what songs are actually about.

Users describe a situation, and the application identifies songs whose lyrics, narratives, and emotional themes reflect that experience.

## Motivation

The idea came to me while I was playing around with my Spotify playlists, trying to build one made of songs I could relate to, so that I wouldn't feel so alone. I thought of two songs, and then I got stuck.

I had used Spotify's AI playlist feature before, but it only recommended songs with broadly similar themes, like love or loss, when I wanted something much more precise. Some of my playlists about very specific situations have collected a lot of likes on Spotify, which shows that this kind of playlist is wanted.

## How It Works

1. **Lyrics Analysis:** An AI model analyzes song lyrics to identify themes, emotions, narratives, relationship dynamics, and meaning.
2. **Scenario Understanding:** Users describe a personal experience, which is then analyzed to extract its context.
3. **Semantic Matching:** The application compares the user's scenario against the lyrical meaning of songs.
4. **Playlist Ranking:** Matching songs are ranked by their relevance to the user's experience, and users can rate how well each song matches.
5. **Spotify Integration:** Users can generate personalized playlists and save them directly to Spotify.

## Tech Stack

| Category | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI (planned API endpoints) |
| AI | Mistral Large 4 via the NVIDIA API |
| AI Integration | OpenAI-compatible Python SDK |
| Data Validation | Pydantic |
| Data Storage | JSON (current prototype) |
| Music Integration | Spotify Web API (planned) |
| Semantic Matching | Text embeddings and similarity scoring (planned) |

## Current Progress

### Implemented

**Project Setup**
- Initialized the React and TypeScript frontend using Vite.
- Created the Python backend and AI module structure.
- Configured Python dependencies and environment variables.
- Created a song catalog containing Spotify track metadata.

**AI Lyrics Analyzer (currently working on)**
- Integrated Mistral Large 4 through the NVIDIA API.
- Implemented AI-powered analysis of supplied song lyrics.
- Extracts structured information, including:
  - Themes
  - Emotions
  - Narrative
  - Relationship dynamics
  - Lyrical meaning
- Validates the AI-generated output with Pydantic.
- Saves analyses to `data/song_themes.json`.
- Replaces existing analyses with the same song ID to avoid duplicate entries.
- Successfully tested the pipeline using original sample lyrics.

### In Development / Planned

**Scenario Analyzer**
- Accept a user's personal situation in natural language.
- Extract emotions, themes, relationship dynamics, and narrative context.
- Produce a structured representation for matching.

**Semantic Song Matching**
- Generate embeddings for song analyses and user scenarios.
- Compare their semantic similarity.
- Prioritize narrative and situational relevance rather than emotion alone.

**Playlist Ranking**
- Rank songs by lyrical relevance.
- Combine semantic similarity with theme and narrative alignment.
- Reduce repetitive recommendations.
- Generate explanations of why each song matches a scenario.

**Backend API**
- Build FastAPI endpoints for scenario analysis and playlist generation.
- Connect the AI pipeline to the frontend.
- Implement error handling and response validation.

**Frontend**
- Create an interface where users can describe their experiences.
- Display recommended songs and their explanations.
- Allow users to preview and customize generated playlists.
- Add loading states and responsive layouts.

**Spotify Integration**
- Implement Spotify OAuth authentication.
- Retrieve relevant track information.
- Create playlists in users' Spotify accounts.
- Allow users to save generated recommendations.

## Planned Features

- Explanations with highlighted lyrics, where licensing permits (otherwise, a paraphrase of the lyrical connection)
- Users can accept or reject songs, and their feedback is stored in a database to improve future recommendations
- Music preferences: artists, language, genre, and era
- Playlist progression: arrange songs to tell a story (for example, enemies to lovers)

## Project Structure

```text
playlist-generator/
├── ai/
│   ├── lyrics_analyzer.py
│   ├── scenario_analyzer.py
│   ├── embeddings.py
│   ├── song_matcher.py
│   └── playlist_ranker.py
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── data/
│   ├── songs.json
│   └── song_themes.json
├── frontend/
│   ├── src/
│   └── package.json
├── tests/
│   └── test_lyrics_analyzer.py
├── .gitignore
└── README.md
```

*Some modules are currently placeholders and will be implemented as development progresses.*

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js and npm
- An NVIDIA API key with access to the selected Mistral model

### 1. Clone the repository

```bash
git clone https://github.com/assiaelhallaoui/playlist-generator.git
cd playlist-generator
```

### 2. Set up the Python environment

```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
NVIDIA_API_KEY=your_nvidia_api_key
NVIDIA_MODEL=mistralai/mistral-large-4-1t-a52b
```

Never commit API keys to version control. Make sure `.env` is listed in `.gitignore`.

### 4. Test the lyrics analyzer

```bash
python -m tests.test_lyrics_analyzer
```

The test analyzes original sample lyrics and saves the resulting structured analysis to `data/song_themes.json`.

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend is currently a development scaffold. The complete playlist-generation interface is not yet implemented.

## Example

**User scenario:**

> "I had feelings for someone but never told them. Now they've moved on with someone else, and I keep thinking about what could have happened."

The planned application would identify songs exploring themes such as unexpressed feelings, regret, missed opportunities, and emotional attachment.

Rather than returning any sad love song, the recommendation system would prioritize songs describing similar experiences and relationship dynamics.

## Development Roadmap

- [x] Initialize frontend and backend project structure
- [x] Configure Mistral Large 4 through the NVIDIA API
- [x] Implement AI lyrics analyzer
- [x] Validate structured AI responses with Pydantic
- [x] Store song analyses in JSON
- [x] Test lyrics analysis with sample lyrics
- [ ] Implement user scenario analyzer
- [ ] Generate semantic embeddings
- [ ] Implement song similarity matching
- [ ] Build playlist ranking algorithm
- [ ] Develop FastAPI endpoints
- [ ] Build interactive React frontend
- [ ] Implement Spotify authentication
- [ ] Generate and save Spotify playlists
- [ ] Add automated tests and improve recommendation quality
- [ ] Deploy the application

## Lyrics and Copyright

The application is designed to analyze lyrics obtained from sources that explicitly authorize their use for AI processing.

Spotify's Web API does not provide full song lyrics. The current prototype uses original sample lyrics for testing. Integrating real song lyrics will require an appropriately licensed or authorized source.

## Project Status

**Active development: AI lyrics analysis prototype completed.**

The next milestone is implementing scenario analysis and semantic matching to connect users' personal experiences with the meaning of songs.