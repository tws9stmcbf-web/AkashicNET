import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About AkashicNET — AKASHICNET.ORG",
  description: "The anonymous human thread, mission and evidence boundaries behind AkashicNET.",
};

const threads = [
  {
    time: "A threshold",
    place: "Private circumstances withheld",
    title: "An encounter with Akasha",
    text: "A profound lived experience opened the image of Akasha: memory, awareness and reality as something larger than one life-story. The experience is preserved as testimony, while private circumstances remain private.",
  },
  {
    time: "Later gatherings",
    place: "Music · community · altered perspective",
    title: "The witness beyond the ordinary",
    text: "Unusual states of awareness became inner landmarks—personally meaningful testimony, described without publishing intimate visionary detail or turning experience into universal proof.",
  },
  {
    time: "A symbolic thread",
    place: "Encounter · gift · later interpretation",
    title: "TAM becomes Green Tara",
    text: "A Tibetan TAM symbol later became associated with Green Tara and Sarnath. The sequence is presented as retrospective meaning-making, not evidence of external causation or destiny.",
  },
  {
    time: "Contemplative resonance",
    place: "Practice · community · lunar symbolism",
    title: "Cycles become a language",
    text: "Recurring lunar and contemplative motifs became a personal language for reflection. Their significance remains interpretive rather than scientific evidence.",
  },
  {
    time: "An open direction",
    place: "Varanasi · Sarnath",
    title: "Two places keep returning",
    text: "Varanasi and nearby Sarnath recur as symbols of impermanence, transformation, Dharma and inquiry. Any future journey details remain private.",
  },
];

export default function AboutPage() {
  return (
    <main className="about-page">
      <header className="nav-shell about-nav">
        <a className="wordmark" href="/" aria-label="Return to AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="About navigation"><a href="/">Home</a><a href="/community">Community</a><a href="#constellation">The constellation</a></nav>
      </header>

      <section className="about-hero">
        <div className="about-hero-copy">
          <p className="section-label">About AkashicNET</p>
          <h1>Following the pattern<br/><em>without mistaking it for proof.</em></h1>
          <p>AkashicNET grew from sustained curiosity across consciousness, science, contemplative traditions, community knowledge and lived experience. The human contributor remains intentionally anonymous; this page preserves the project’s motivating thread without turning biography into authority.</p>
        </div>
        <figure className="author-seal">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt="The Sacred Toroidal Love emblem of AkashicNET"/>
          <figcaption>Sacred Toroidal Love · compassionate intelligence in relationship</figcaption>
        </figure>
      </section>

      <section className="author-mantra" aria-label="Personal compass">
        <p className="section-label">A personal compass</p>
        <blockquote>“Silence your mind.<br/>Open your heart.<br/><em>Follow your gut.</em>”</blockquote>
        <p>A practice for listening inwardly while remaining accountable to evidence, other people and the living world.</p>
      </section>

      <section className="inner-cosmology">
        <p className="section-label">A lived interpretation</p>
        <h2>From inner experience<br/><em>to a wider field of inquiry.</em></h2>
        <blockquote>“Boundless awareness is infinite love.”</blockquote>
        <div>
          <h3>Interconnection as question, not conclusion</h3>
          <p>AkashicNET leaves room for philosophical ideas such as panpsychism, animism and field-like metaphors of interconnection while keeping their status explicit. Metaphysical imagery, synchronicity and unusual experience are not treated as evidence that quantum physics proves panpsychism, astral perception or a universal field of consciousness.</p>
        </div>
      </section>

      <section className="constellation" id="constellation">
        <div className="constellation-intro">
          <p className="section-label">Across space and time</p>
          <h2>A nonlinear constellation.</h2>
          <p>The meaning is not located in any single event. It emerges retrospectively through symbols, encounters and contemplative practice—threads that appear to bend toward Varanasi and Sarnath when viewed together.</p>
        </div>
        <div className="constellation-grid">
          {threads.map((thread, index) => (
            <article key={thread.title}>
              <span>{String(index + 1).padStart(2,"0")}</span>
              <small>{thread.time}<br/>{thread.place}</small>
              <h3>{thread.title}</h3>
              <p>{thread.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="destination-pair">
        <article>
          <p className="section-label">Varanasi</p>
          <h2>Death, transformation<br/>and radical presence.</h2>
          <p>The city represents an encounter with impermanence, Shiva, the Ganges and living traditions—including curiosity about Aghori paths—without romanticising them or claiming authority over them.</p>
        </article>
        <article>
          <p className="section-label">Sarnath</p>
          <h2>The first turning<br/>of the Dharma wheel.</h2>
          <p>Sarnath represents the Buddha’s first teaching, the Middle Way and a return to practice: wisdom expressed through ethical conduct, attention and compassion.</p>
        </article>
      </section>

      <section className="flying-tension">
        <p className="section-label">The open journey</p>
        <h2>Inquiry can have a direction<br/><em>without becoming destiny.</em></h2>
        <p>Varanasi and Sarnath remain meaningful directions for inquiry. Travel plans, dates, routes and personal logistics are intentionally outside the public record.</p>
      </section>

      <aside className="meaning-boundary" aria-label="How to interpret this account">
        <span>How to read this page</span>
        <div><strong>Lived Experience/Testimony</strong><p>Experiences and patterns may guide reflection and creativity without being universalised.</p></div>
        <div><strong>Interpretation</strong><p>Synchronicity is presented as meaning-making—not evidence of cosmic causation, privileged access or a guaranteed destination.</p></div>
        <div><strong>Open to revision</strong><p>Memory, meaning and theory may deepen, change or dissolve as new context appears.</p></div>
        <div><strong>Privacy retained</strong><p>Names, health records, intimate visions, family and relationship details, and travel logistics are deliberately excluded.</p></div>
      </aside>

      <aside className="page-provenance" aria-label="Page version and update date">
        <span>About page · Anonymous public edition</span><span>AkashicNET v0.10 · Pre-alpha</span><span>Updated 30 August 2026</span>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Boundless awareness is infinite love.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
