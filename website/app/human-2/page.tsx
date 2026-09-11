import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "HUMAN 2.0 — AKASHICNET.ORG",
  description: "An exploratory AkashicNET project for human, collective and planetary flourishing.",
};

const lenses = [
  ["AWAKEN", "What are we becoming aware of?", "Attention, transformation, self-knowledge and consequences."],
  ["HOMESENSE", "What actually matters?", "Coherence, relationships, reciprocity, communities and planetary wellbeing."],
  ["HIERATIC", "What wisdom should we preserve and examine?", "Philosophy, contemplative traditions, ethics, ritual, compassion and meaning."],
  ["ADAPT", "How can we become more resilient?", "Health, learning, neurodiversity, resources, climate adaptation and appropriate technology."],
  ["TRANSCEND", "What might we move beyond?", "Compulsive consumption, limiting assumptions, polarisation and destructive habits."],
  ["REGENERATE", "What can we leave better than we found it?", "Ecosystems, communities, knowledge commons and conditions inherited by future generations."],
  ["#METAD", "How does everything connect across layers?", "Mind, body, culture, technology, society, biosphere, time and scale."],
];

const domains = [
  ["Self", "Mind · Body · Awareness · Learning · Meaning"],
  ["Relationships", "Compassion · Cooperation · Communication · Culture · Community"],
  ["Intelligence", "Human intelligence · AI · Collective intelligence · Evidence literacy · Wisdom"],
  ["Resilience", "Health · Adaptation · Neurodiversity · Preparedness · Recovery"],
  ["Regeneration", "Pachamama · Water · Biodiversity · Food · Energy · Circular systems"],
  ["Wisdom", "Science · Philosophy · Contemplative traditions · Lived experience · Big Questions"],
  ["Futures", "Human–AI symbiosis · Regenerative civilisation · Planetary intelligence · Unknown possibilities"],
];

export default function HumanTwoPage() {
  return (
    <main className="about-page">
      <header className="nav-shell about-nav">
        <a className="wordmark" href="/" aria-label="Return to AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="HUMAN 2.0 navigation"><a href="/">Home</a><a href="/metad-ak">METAD-AK</a><a href="#lenses">Seven lenses</a><a href="#domains">Seven domains</a><a href="#garden">The garden</a><a href="#horizon">Long horizon</a></nav>
      </header>

      <section className="about-hero">
        <div className="about-hero-copy">
          <p className="section-label">HUMAN 2.0 · v0.1 · September 2026</p>
          <h1>From self-awareness<br/><em>to a flourishing biosphere.</em></h1>
          <p>HUMAN 2.0 is an exploratory AkashicNET programme asking how humans might flourish more wisely within themselves, with one another, with technology and with the living Earth.</p>
          <p><strong>It is a question, not a destination.</strong> It is not a proposal for a superior species, compulsory enhancement or one ideal kind of human.</p>
        </div>
        <figure className="author-seal">
          <img src="/images/akashicnet-toroidal-love-logo.png" alt=""/>
          <figcaption>AkashicNET provides the knowledge infrastructure. HUMAN 2.0 asks what we do with it.</figcaption>
        </figure>
      </section>

      <section className="author-mantra" aria-label="HUMAN 2.0 compass">
        <p className="section-label">A compass</p>
        <blockquote>“Awareness is a portal,<br/>not a destination.”</blockquote>
        <p>Awareness creates the potential for wisdom. Reflection, discernment, humility, integration, compassion and wiser action determine what that potential becomes.</p>
      </section>

      <section className="inner-cosmology">
        <p className="section-label">The architecture</p>
        <h2>Knowledge infrastructure below.<br/><em>Flourishing above.</em></h2>
        <div>
          <h3>AkashicNET → Evidence + Provenance → Human-guided Multi-AI → Seven Lenses → HUMAN 2.0 → Regenerative Society → Biosphere → Flourishing 2100</h3>
          <p>The framework is designed to stay revisable. Better evidence, criticism and community perspectives should be able to change the map.</p>
        </div>
      </section>

      <section className="constellation" id="lenses">
        <div className="constellation-intro">
          <p className="section-label">Seven lenses</p>
          <h2>Different perspectives.<br/>A more complete picture.</h2>
          <p>These are cross-cutting analytical lenses, not seven commandments or compulsory stages.</p>
        </div>
        <div className="constellation-grid">
          {lenses.map(([title, question, text], index) => (
            <article key={title}>
              <span>{String(index + 1).padStart(2,"0")}</span>
              <small>{question}</small>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="constellation" id="domains">
        <div className="constellation-intro">
          <p className="section-label">Seven domains</p>
          <h2>A matrix,<br/><em>not a pyramid.</em></h2>
          <p>The seven lenses can be applied across seven domains of human and planetary flourishing.</p>
        </div>
        <div className="constellation-grid">
          {domains.map(([title, text], index) => (
            <article key={title}>
              <span>{String(index + 1).padStart(2,"0")}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="destination-pair">
        <article>
          <p className="section-label">Human × AI × Collective Intelligence</p>
          <h2>Many minds.<br/>Many models.</h2>
          <p>AI may help retrieve, compare, model and synthesise. Human judgement remains accountable for values, interpretation, evidence boundaries and consequential decisions.</p>
          <p><a className="text-link" href="/metad-ak">Explore METAD-AK →</a></p>
        </article>
        <article>
          <p className="section-label">The wisdom question</p>
          <h2>Capability is not<br/>the same as wisdom.</h2>
          <p>The deeper question is one of direction: what is intelligence becoming oriented toward, who benefits, what does it serve and what kind of future does it help create?</p>
        </article>
      </section>

      <section className="flying-tension" id="garden">
        <p className="section-label">Community awareness</p>
        <h2>A garden,<br/><em>not a possession.</em></h2>
        <blockquote>“A garden you walk with love, kindness, respect, awe — not possession.”</blockquote>
        <p>We plant seeds of knowledge, curiosity and care, then cultivate the conditions in which they can grow. HUMAN 2.0 is less about engineering a perfect human than cultivating conditions in which people, communities and the living world can flourish together.</p>
      </section>

      <section className="inner-cosmology">
        <p className="section-label">The BuddhaFly effect</p>
        <h2>Awareness alone<br/><em>is not wisdom.</em></h2>
        <div>
          <h3>Mettā · Karuṇā · Muditā · Upekkhā</h3>
          <p>The four Brahmavihāras — loving-kindness, compassion, sympathetic joy and equanimity — provide an ethical lens for transforming awareness into wiser action.</p>
          <p><strong>Awareness × Discernment × Humility × Compassion × Integration × Action → Wisdom</strong></p>
        </div>
      </section>

      <aside className="meaning-boundary" aria-label="Evidence membrane">
        <span>Evidence membrane</span>
        <div><strong>Established Evidence</strong><p>Well-supported findings remain traceable to public sources and methodological context.</p></div>
        <div><strong>Interpretation</strong><p>Reasoned synthesis remains distinguishable from observation.</p></div>
        <div><strong>Lived Experience / Testimony</strong><p>Subjective experience can be meaningful without automatically establishing external ontology.</p></div>
        <div><strong>Hypothesis · Speculation · Imagination</strong><p>Exploratory ideas remain labelled, provisional and reversible.</p></div>
      </aside>

      <section className="constellation" id="horizon">
        <div className="constellation-intro">
          <p className="section-label">Long horizon · exploratory</p>
          <h2>From people<br/><em>to biosphere.</em></h2>
          <p>This is a direction of travel, not a delivery promise.</p>
        </div>
        <div className="constellation-grid">
          <article><span>2026</span><h3>Governed intelligence core</h3><p>Question Graphs, evidence intelligence, provenance, Living Library and human-guided AI.</p></article>
          <article><span>2027–2029</span><h3>Scientific evidence intelligence</h3><p>Replication, methodology, effect sizes, uncertainty and evidence lineage.</p></article>
          <article><span>2030–2036</span><h3>Collaborative knowledge commons</h3><p>Researchers and communities contribute evidence, objections, replications, alternatives and corrections.</p></article>
          <article><span>2040+</span><h3>Biosphere knowledge network</h3><p>Ecology, biodiversity, climate, health, culture, technology and communities examined as interacting systems.</p></article>
          <article><span>2100</span><h3>Flourishing futures</h3><p>A speculative horizon asking what decisions today increase the probability of futures worth inhabiting.</p></article>
        </div>
      </section>

      <section className="author-mantra" aria-label="HUMAN 2.0 constitutional principle">
        <p className="section-label">Constitutional principle</p>
        <blockquote>“There is no ideal HUMAN 2.0.”</blockquote>
        <p>No hierarchy of minds. No compulsory enhancement. No single path to flourishing. Neurodiversity and cultural diversity are not defects to standardise away.</p>
      </section>

      <aside className="page-provenance" aria-label="Page version and status">
        <span>HUMAN 2.0 · v0.1</span><span>Exploratory framework</span><span>Images & figures planned for later revision</span><span>September 2026</span>
      </aside>

      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Know · Awaken · Adapt · Regenerate · Flourish</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
