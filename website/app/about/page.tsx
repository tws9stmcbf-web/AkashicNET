import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Jatinder — AKASHICNET.ORG",
  description: "The personal mantra and nonlinear constellation of lived experiences behind AkashicNET.",
};

const threads = [
  {
    time: "An early marker",
    place: "A full-moon birth",
    title: "Born beneath a full moon",
    text: "A birth shortly after humanity’s first Moon landing became the earliest point in a pattern recognised only much later.",
  },
  {
    time: "A life-changing threshold",
    place: "Held without clinical detail",
    title: "An encounter with Akasha",
    text: "A profound threshold experience opened the image of Akasha: memory, awareness and reality as something larger than one life-story. Private health circumstances are intentionally omitted.",
  },
  {
    time: "Later gatherings",
    place: "Music · community · altered perspective",
    title: "The witness beyond the ordinary",
    text: "Unusual states of awareness at community gatherings became inner landmarks—meaningful testimony, described without publishing intimate visionary detail or turning experience into universal proof.",
  },
  {
    time: "June 2024 → April 2025",
    place: "Haarlem → Bicycle Day",
    title: "The symbol arrives before its meaning",
    text: "A human connection begun around ICPR in Haarlem was followed by the gift of a Tibetan TAM necklace. Its significance was not yet understood.",
  },
  {
    time: "April 2026",
    place: "India reflected through another journey",
    title: "TAM becomes Green Tara",
    text: "Green Tara entered the story after another person returned from India and Sarnath. Looking backward, the sequence appeared: TAM → Green Tara → Sarnath.",
  },
  {
    time: "A later full-moon birthday",
    place: "O.Z.O.R.A.",
    title: "The lunar thread returns",
    text: "A birthday returned beneath a full moon at O.Z.O.R.A., experienced alongside the contemplative resonance of Āsāḷha Puja and Guru Purnima.",
  },
  {
    time: "Now → what comes next",
    place: "Encounters · festivals · online crossings",
    title: "Varanasi keeps appearing",
    text: "Repeated encounters with people connected to Varanasi—offline, online and at gatherings—have strengthened the felt invitation toward the city and nearby Sarnath.",
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
          <p className="section-label">About Jatinder</p>
          <h1>Following the pattern<br/><em>without mistaking it for proof.</em></h1>
          <p>AkashicNET grew from years of curiosity across consciousness, science, contemplative traditions, community knowledge and lived experience. This page describes the personal constellation behind the project—not a fixed identity, doctrine or claim of destiny.</p>
        </div>
        <figure className="author-seal">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt="The Sacred Toroidal Love emblem of AkashicNET"/>
          <figcaption>Sacred Toroidal Love · compassionate intelligence in relationship</figcaption>
        </figure>
      </section>

      <section className="author-mantra" aria-label="Jatinder's mantra">
        <p className="section-label">Jatinder’s mantra</p>
        <blockquote>“Silence your mind.<br/>Open your heart.<br/><em>Follow your gut.</em>”</blockquote>
        <p>A compass for listening inwardly while remaining accountable to evidence, other people and the living world.</p>
      </section>

      <section className="inner-cosmology">
        <p className="section-label">A personal cosmology</p>
        <h2>From the quantum<br/><em>to the cosmos.</em></h2>
        <blockquote>“A quantum-enhanced panpsychic consciousness—meta-lucid, astrally aware and attentive to thought, energy, frequency and vibration; reaching from quantum possibility to the cosmos, and every conscious being in between.”</blockquote>
        <div>
          <h3>Panpsychic animism · A living field</h3>
          <p>This is Jatinder’s poetic and philosophical language for felt interconnection: consciousness and aliveness woven through reality rather than confined to one isolated self. “Quantum” is used here as metaphysical imagery and an open question—not as evidence that quantum physics proves panpsychism, astral perception or a universal field of consciousness.</p>
        </div>
      </section>

      <section className="constellation" id="constellation">
        <div className="constellation-intro">
          <p className="section-label">Across space and time</p>
          <h2>A nonlinear constellation.</h2>
          <p>The meaning is not located in any single event. It emerges retrospectively through places, symbols, encounters and lunar returns—threads that appear to bend toward Varanasi and Sarnath when viewed together.</p>
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
          <p>The city represents an encounter with impermanence, Shiva, the Ganges and living traditions—including curiosity about Aghori paths—without romanticising or claiming authority over them.</p>
        </article>
        <article>
          <p className="section-label">Sarnath</p>
          <h2>The first turning<br/>of the Dharma wheel.</h2>
          <p>Sarnath represents the Buddha’s first teaching, the Middle Way and a return to practice: wisdom expressed through ethical conduct, attention and compassion.</p>
        </article>
      </section>

      <section className="flying-tension">
        <p className="section-label">The unresolved edge</p>
        <h2>The pull toward the journey<br/><em>and unease about flying.</em></h2>
        <p>Both are true. Jatinder feels drawn toward Varanasi and Sarnath while holding cognitive dissonance about reaching them by air. The tension remains open rather than being hidden or forced into a tidy answer; dates and itinerary details remain private.</p>
      </section>

      <aside className="meaning-boundary" aria-label="How to interpret this account">
        <span>How to read this page</span>
        <div><strong>Personally meaningful</strong><p>These experiences and patterns can guide reflection, creativity and personal choices.</p></div>
        <div><strong>Not proof of fate</strong><p>Synchronicity is presented as lived interpretation—not evidence of cosmic causation, privileged access or a guaranteed destination.</p></div>
        <div><strong>Open to revision</strong><p>Memory, meaning and theory may deepen, change or dissolve as new context appears.</p></div>
        <div><strong>Privacy retained</strong><p>Health records, intimate visions, family and relationship details, and travel logistics are deliberately excluded.</p></div>
      </aside>

      <aside className="page-provenance" aria-label="Page version and update date">
        <span>About page · Iteration 01</span><span>AkashicNET v0.9 · Pre-alpha</span><span>Updated 30 August 2026</span>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Boundless awareness is infinite love.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
