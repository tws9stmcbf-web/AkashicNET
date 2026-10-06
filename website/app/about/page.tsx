import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About AkashicNET — AKASHICNET.ORG",
  description: "The mission, human thread and evidence boundaries behind AkashicNET.",
};

const threads = [
  {
    time: "A threshold",
    place: "Held without private detail",
    title: "A question becomes a practice",
    text: "A profound lived experience opened questions about memory, awareness, identity and reality. It remains personal testimony rather than universal proof.",
  },
  {
    time: "Across communities",
    place: "Science · contemplation · culture",
    title: "Many paths begin to connect",
    text: "Encounters across research, contemplative traditions, community knowledge, art and lived experience gradually formed the interdisciplinary pattern that became AkashicNET.",
  },
  {
    time: "A symbolic thread",
    place: "TAM · Green Tara · Sarnath",
    title: "Symbols become questions",
    text: "A sequence involving a Tibetan TAM symbol, Green Tara and Sarnath became personally meaningful and helped sharpen questions about continuity, compassion and the Dharma without being treated as evidence of fate or causation.",
  },
  {
    time: "A recurring destination",
    place: "Varanasi · Sarnath",
    title: "The journey remains open",
    text: "Repeated connections with Varanasi and Sarnath have become part of the project’s human thread: places associated with death, impermanence, transformation, teaching and inquiry. The meaning remains open to revision.",
  },
];

export default function AboutPage() {
  return (
    <main className="about-page">
      <header className="nav-shell about-nav">
        <a className="wordmark" href="/" aria-label="Return to AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="About navigation"><a href="/">Home</a><a href="/faq">FAQ</a><a href="/community">Community</a><a href="#mission">Mission</a><a href="#constellation">Human thread</a></nav>
      </header>

      <section className="about-hero">
        <div className="about-hero-copy">
          <p className="section-label">About AkashicNET</p>
          <h1>A living library.<br/><em>A long-term human mission.</em></h1>
          <p>AkashicNET is an independent knowledge-stewardship and citizen data-science project exploring difficult questions across consciousness, science, ecology, philosophy, contemplative traditions and human–AI collaboration.</p>
          <p>The public identity remains intentionally anonymous. The work should be judged by its sources, methods, provenance and willingness to remain uncertain—not by the biography of one person.</p>
          <p className="project-attribution"><strong>Original vision and editorial direction:</strong> the AkashicNET founder. Developed and formalised through human–AI collaboration.</p>
        </div>
        <figure className="author-seal">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt=""/>
          <figcaption>Sacred Toroidal Love · compassionate intelligence in relationship</figcaption>
        </figure>
      </section>

      <section className="author-mantra" aria-label="Personal compass">
        <p className="section-label">Personal compass</p>
        <blockquote>“Silence your mind.<br/>Open your heart.<br/><em>Follow your gut.</em>”</blockquote>
        <p>A private compass made public only as a principle: listen inwardly while remaining accountable to evidence, other people and the living world.</p>
      </section>

      <section className="inner-cosmology" id="mission">
        <p className="section-label">Mission</p>
        <h2>Remember without flattening.<br/><em>Connect without collapsing.</em></h2>
        <div>
          <h3>Correct without erasing · Serve rather than persuade</h3>
          <p>AkashicNET is designed as a living, revisable knowledge system. It can hold scientific evidence, interpretation, testimony, hypothesis and speculation together while keeping their differences visible.</p>
        </div>
      </section>

      <section className="constellation" id="constellation">
        <div className="constellation-intro">
          <p className="section-label">The human thread</p>
          <h2>A nonlinear constellation.</h2>
          <p>The project has a human story behind it, but the story is not a credential and not a proof. The public version preserves only the parts needed to explain why certain questions became important.</p>
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
          <h2>Impermanence,<br/>transformation and presence.</h2>
          <p>Varanasi is approached as a living cultural and spiritual context associated with death, continuity and radical presence. AkashicNET does not claim authority over its traditions or reduce them to aesthetic symbols.</p>
        </article>
        <article>
          <p className="section-label">Sarnath</p>
          <h2>The first turning<br/>of the Dharma wheel.</h2>
          <p>Sarnath represents a return to first principles: the Middle Way, disciplined inquiry, ethical conduct, attention and compassion. These traditions are represented with provenance and context rather than treated as scientific evidence by default.</p>
        </article>
      </section>

      <section className="flying-tension">
        <p className="section-label">Possible outcomes</p>
        <h2>A public knowledge commons<br/><em>that improves through use.</em></h2>
        <p>Possible outcomes include better research questions, evidence stewardship, interdisciplinary bridges, provenance-aware tools, a self-correcting public record and more transparent human–AI collaboration.</p>
      </section>

      <aside className="meaning-boundary" aria-label="How AkashicNET knows">
        <span>How AkashicNET knows</span>
        <div><strong>Established Evidence</strong><p>Empirical findings and well-supported claims are kept traceable to public sources and methodological context.</p></div>
        <div><strong>Interpretation</strong><p>Explanatory framing is separated from observation and remains open to competing readings.</p></div>
        <div><strong>Lived Experience / Testimony</strong><p>Human experience can be meaningful phenomenological data without automatically becoming evidence of external ontology.</p></div>
        <div><strong>Hypothesis · Speculation</strong><p>Exploratory ideas may be mapped, but they remain explicitly labelled and reversible.</p></div>
      </aside>

      <aside className="meaning-boundary" aria-label="Project principles">
        <span>Project principles</span>
        <div><strong>Provenance first</strong><p>Sources, uncertainty, corrections and version history should remain visible wherever practical.</p></div>
        <div><strong>Human-governed AI</strong><p>AI can assist retrieval, mapping and synthesis; consequential judgement remains accountable to human review.</p></div>
        <div><strong>Privacy retained</strong><p>Personal names, health details, family information, intimate visionary material and travel logistics are deliberately excluded from the public About page.</p></div>
        <div><strong>Meaning is allowed. Overclaiming is not.</strong><p>AkashicNET can explore extraordinary questions without pretending uncertainty has disappeared.</p></div>
      </aside>

      <aside className="page-provenance" aria-label="Page version and update date">
        <span>About page · Anonymous public edition</span><span>Updated 30 August 2026</span>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
