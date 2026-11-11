
import { useState, type FormEvent } from 'react'
import './App.css'

const examples = [
  'I miss someone I should have moved on from.',
  'Everything is changing, and I feel lost.',
  'I feel like I\'m the only one trying',
  'I\'m growing up too fast'
]


const songsOfTheWeek = [
  {
    id: 1,
    title: 'seasons',
    artist: 'wave to earth',
    cover: '/covers/seasons.jpg',
    meaning: 'a story about self-doubt and hurtng the ones you love ',
    storytelling:
      'it is about the ache of believing you’re a liability to the people you love',
    spotifyUrl: 'https://open.spotify.com/intl-fr/track/0aVd7QiY8BstysHb62c5Fi?si=9fcdc40a675b4b4a',
  },
  {
    id: 2,
    title: 'panic',
    artist: 'beomgyu',
    cover: '/covers/panic.jpg',
    meaning: 'a story about the comfort of music among panic',
    storytelling:
      'the feeling of being left alone in the world that comes when a panic attack hits. when moments that seemed insurmountable, music is a refuge, and beomgyu hopes the song gives listeners hope and resilience.',
    spotifyUrl: 'https://open.spotify.com/intl-fr/track/3PTQ2rPfaPDxqpXOcRlTsZ?si=77f336dc2ccc402e',
  },
  {
    id: 3,
    title: 'nomad',
    artist: 'clairo',
    cover: '/covers/nomad.jpg',
    meaning: 'a story about running away to an idea.',
    storytelling:
      'nomad is about daydreaming about someone or something and the urge to give everything up and chase. but it\'s also about not trusting one self and not letting love except when it comes to that one person. ',
    spotifyUrl: 'https://open.spotify.com/intl-fr/track/4WJPxTsvWIdRZ9vMtqk7fj?si=c6b7e1868b1b406f',
  },
]


function App() {
  const [story, setStory] = useState('')
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!story.trim()) return

    setSubmitted(true)
  }

  return (
    <div className="site-shell">
      <header className="navbar">
        <a className="brand" href="/" aria-label="Between the Lines home">
          <span className="brand-icon">◉</span>
          between the lines<span className="brand-dot">.</span>
        </a>

        <nav>
          <a href="#discover">Discover</a>
          <a href="#weekly">Weekly picks</a>
          <a href="#about">Our story</a>
        </nav>
      </header>

      <main>
        <section className="hero" id="discover">
          <div className="hero-content">
            <div className="eyebrow">
              <span className="eyebrow-line" />
              WELCOME TO THE LISTENING ROOM
            </div>

            <h1>
              Create your own
              <br />
              soundtrack
            </h1>

            <p className="hero-description">
              For everything, every specific feeling, every little moment, there's a song
              that understands. You're never alone.
            </p>

            <a href="#your-story" className="hero-button">
              Tell us what's happening <span>↗</span>
            </a>

            </div> {/* Closes hero-content */}

            <div className="record-scene" aria-hidden="true">

            <div className="record-shadow" />

            <div className="vinyl">
              <div className="vinyl-label">
                <span>BETWEEN</span>
                <span className="label-center" />
                <span>THE LINES</span>
              </div>
            </div>

            <div className="record-caption">
              <span>NOW SPINNING</span>
              <span>your next favorite song ♡</span>
            </div>
          </div>
        </section>

        <section className="story-section" id="your-story">
          <div className="section-heading">
            <span className="section-number">01 / THE BEGINNING</span>

            <h2>So, what's your story?</h2>

            <p>
              explain however you want your story or what you want to
              we'll find what matches and all you have to do is 
              put on earphones, lay in bed and enjoy              
            </p>
          </div>

          <form className="story-card" onSubmit={handleSubmit}>
            <div className="card-top">
              <span>✉ &nbsp; A NOTE FROM YOU</span>
              <span>PRIVATE LISTENING SESSION</span>
            </div>

            <label htmlFor="story" className="input-label">
              Dear music,
            </label>

            <textarea
              id="story"
              value={story}
              onChange={(event) => {
                setStory(event.target.value)
                setSubmitted(false)
              }}
              placeholder="There's this person I never told how I felt. Now they've moved on, but I still think about what could have been..."
              rows={5}
              maxLength={1500}
              required
            />

            <div className="suggestions">
              <span>NEED A LITTLE INSPIRATION?</span>

              <div className="suggestion-list">
                {examples.map((example) => (
                  <button
                    key={example}
                    type="button"
                    className="suggestion"
                    onClick={() => {
                      setStory(example)
                      setSubmitted(false)
                    }}
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>

            <div className="card-bottom">
              <span className="character-count">
                {story.length} / 1500
              </span>

              <button
                type="submit"
                className="submit-button"
                disabled={!story.trim()}
              >
                Find my soundtrack <span>↗</span>
              </button>
            </div>
          </form>

          {submitted && (
            <div className="demo-result" role="status">
              <div className="mini-record" aria-hidden="true" />

              <div className="demo-text">
                <h3>Your story is ready for its soundtrack.</h3>
                <p>
                  The listening room is being built.
                  Soon, we'll match your story with songs
                  through their lyrical meaning.
                </p>
              </div>

              <button
                type="button"
                onClick={() => setSubmitted(false)}
              >
                Close
              </button>
            </div>
          )}
        </section>


      <section className="about-section" id="about">

        
      <section className="weekly-section" id="weekly">
        <div className="weekly-container">
          <div className="weekly-heading">
            <span className="section-number">
              02 / FROM THE RECORD SHELF
            </span>

            <h2>
              Songs of the <em>week.</em>
            </h2>

            <p>
              a little selection of songs i've been listening to
              this week and the stories they tell
            </p>

            <span className="weekly-note">
              handpicked with love ♡
            </span>
          </div>

          <div className="weekly-grid">
            {songsOfTheWeek.map((song) => (
              <article className="song-card" key={song.id}>
                <div className="song-cover">
                  <img
                    src={song.cover}
                    alt={`${song.title} album cover`}
                    loading="lazy"
                  />
                  <span className="song-number">
                    0{song.id}
                  </span>
                </div>

                <div className="song-details">
                  <span className="song-category">
                    THE STORY BEHIND THE SONG
                  </span>

                  <h3>{song.title}</h3>
                  <p className="song-artist">{song.artist}</p>

                  <p className="song-meaning">
                    {song.meaning}
                  </p>

                  <div className="song-story">
                    <span>BETWEEN THE LINES</span>
                    <p>{song.storytelling}</p>
                  </div>

                  {song.spotifyUrl && (
                    <a
                      href={song.spotifyUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="spotify-link"
                    >
                      Listen on Spotify ↗
                    </a>
                  )}
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>


        <span className="section-number">02 / THE STORY BEHIND IT</span>

        <h2>
          From a music fan <em>to another.</em>
        </h2>

        <p>
          between the lines started with a playlist i couldn't finish.
        </p>

        <p>
          i was scrolling through my spotify library, where i hold 100+ playlists, trying to put
          together a playlist of songs that felt like my own story. songs I could relate to, 
          songs that made me feel a little less alone. 
          i found two... then i got stuck
        </p>

        <p>
          i'd tried AI-generated playlists before, but the
          recommendations always felt too broad. songs about love,
          heartbreak, or loss — when i was looking for
          something much more specific. 
        </p>

        <p>
          some of my playlists about very specific experiences
          had already received a lot of love from other listeners.
          it made me realize i wasn't the only one looking
          for this kind of connection through music.
        </p>

        <p>
          so i started building between the lines.
          a little corner of the internet where you can share
          your story, your mood, your highs and lows
          and discover songs that understand it.
        </p>

        <p>
          this is a passion project from an idea i got in the late hours of the night
          i hope music you get from here will comfort you how well it has comforted me ♡
        </p>

        <p className="about-signature">
          with love, from a music fan to another. ♡
        </p>

        <div className="about-divider">✳</div>
      </section>

      </main>

      <footer className="footer">
        <span>between the lines. © 2026</span>
      </footer>
    </div>
  )
}

export default App
