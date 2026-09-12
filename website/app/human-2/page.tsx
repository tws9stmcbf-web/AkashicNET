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
        <figure className="author-seal framework-hero">
          <img src="/images/human2-hero.webp" width="1254" height="1254" fetchPriority="high" alt="A luminous heart-tree joining human awareness, knowledge networks and the living Earth"/>
          <figcaption>HUMAN 2.0 connects inner awareness, shared knowledge and a flourishing biosphere. Artistic metaphor, not scientific evidence.</figcaption>
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
          <h3>Proposed pathway: AkashicNET → Evidence + Provenance → Future Human-Guided Multi-Model Analysis → Seven Lenses → HUMAN 2.0 → Regenerative Society → Biosphere → Flourishing 2100</h3>
          <p>The framework is designed to stay revisable. Better evidence, criticism and community perspectives should be able to change the map.</p>
        </div>
      </section>

      <figure className="framework-figure">
        <div className="framework-image-scroll" tabIndex={0} role="region" aria-label="Scrollable detailed evidence-commons figure">
          <img src="/images/human2-fig1-evidence-commons.webp" width="1536" height="1024" loading="lazy" decoding="async" alt="Evidence-commons concept map using the five canonical labels: Established Evidence, Interpretation, Lived Experience/Testimony, Hypothesis and Speculation. Its archive snapshot describes the approximately 2,000-member r/NeuronsToNirvana community and distinguishes 9,502 source rows from 7,457 structurally unique URLs."/>
        </div>
        <figcaption><span>Figure 1 · Evidence commons</span><p>A visual map of a living knowledge commons. The archive snapshot describes the approximately 2,000-member r/NeuronsToNirvana community, distinguishes 9,502 source rows from 7,457 structurally unique URLs and uses the canonical five-label evidence taxonomy. Connections remain exploratory; they are not validated relationships or accepted evidence.</p></figcaption>
      </figure>

      <section className="constellation" id="lenses">
        <div className="constellation-intro">
          <p className="section-label">Seven lenses</p>
          <h2>Different perspectives.<br/>A more complete picture.</h2>
          <p>These are cross-cutting analytical lenses, not seven commandments or compulsory stages.</p>
          <p>Here, #METAD is the cross-layer interpretive lens. METAD-AK is the separate, proposed technical orchestration layer.</p>
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

      <figure className="framework-figure">
        <div className="framework-image-scroll" tabIndex={0} role="region" aria-label="Scrollable HUMAN 2.0 lenses-and-domains figure">
          <img src="/images/human2-fig2-seven-lenses-domains.webp" width="1536" height="1024" loading="lazy" decoding="async" alt="HUMAN 2.0 heart-tree connecting seven lenses—AWAKEN, HOMESENSE, HIERATIC, ADAPT, TRANSCEND, REGENERATE and #METAD—to seven domains—Self, Relationships, Intelligence, Resilience, Regeneration, Wisdom and Futures."/>
        </div>
        <figcaption><span>Figure 2 · Lenses and domains</span><p>A HUMAN-facing map of seven lenses across seven domains. #METAD is a cross-layer interpretive lens; METAD-AK remains the separate proposed technical orchestration layer.</p></figcaption>
      </figure>

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

      <figure className="framework-figure">
        <div className="framework-image-scroll" tabIndex={0} role="region" aria-label="Scrollable HUMAN 2.0 seven-by-seven matrix">
          <img src="/images/human2-fig3-7x7-matrix.webp" width="1600" height="1100" loading="lazy" decoding="async" alt="Seven AkashicNET lenses crossing seven domains to form a forty-nine-cell HUMAN 2.0 matrix"/>
        </div>
        <figcaption><span>Figure 3 · The 7×7 matrix</span><p>Forty-nine places to ask better questions. Each cell is an analytical intersection, not a hierarchy, score or scientific result.</p></figcaption>
      </figure>

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

      <figure className="framework-figure framework-figure--square">
        <img src="/images/human2-fig4-flourishing-2100.webp" width="1254" height="1254" loading="lazy" decoding="async" alt="Speculative regenerative future where technology, knowledge, communities and ecosystems coexist"/>
        <figcaption><span>Figure 4 · Flourishing 2100</span><p>A speculative regenerative horizon: an invitation to consider which present choices make flourishing futures more likely, not a prediction or delivery promise.</p></figcaption>
      </figure>

      <section className="inner-cosmology">
        <p className="section-label">The BuddhaFly effect</p>
        <h2>Awareness alone<br/><em>is not wisdom.</em></h2>
        <div>
          <h3>Mettā · Karuṇā · Muditā · Upekkhā</h3>
          <p>The four Brahmavihāras — loving-kindness, compassion, sympathetic joy and equanimity — provide an ethical lens for transforming awareness into wiser action.</p>
          <p><strong>Awareness × Discernment × Humility × Compassion × Integration × Action → Wisdom</strong></p>
        </div>
      </section>

      <figure className="framework-figure framework-figure--square">
        <img src="/images/human2-fig5-buddhafly-effect.webp" width="1254" height="1254" loading="lazy" decoding="async" alt="A luminous butterfly containing the four Brahmavihāras: mettā, karuṇā, muditā and upekkhā"/>
        <figcaption><span>Figure 5 · The BuddhaFly effect</span><p>The Brahmavihāras provide ethical inspiration for turning awareness toward wiser action. This is a values framework, not an evidential claim.</p></figcaption>
      </figure>

      <aside className="meaning-boundary evidence-taxonomy" aria-label="Evidence membrane">
        <span>Evidence membrane</span>
        <div><strong>Established Evidence</strong><p>Appropriately reviewed support with explicit provenance, methods, limits and source context.</p></div>
        <div><strong>Interpretation</strong><p>A reasoned reading, synthesis or framework presented as interpretation rather than established fact.</p></div>
        <div><strong>Lived Experience/Testimony</strong><p>First-person or reported experience preserved as testimony without universalising it.</p></div>
        <div><strong>Hypothesis</strong><p>A specific, testable or investigable proposition that remains unconfirmed.</p></div>
        <div><strong>Speculation</strong><p>A possibility or conjecture with insufficient support for hypothesis or established-evidence status.</p></div>
      </aside>

      <section className="constellation" id="horizon">
        <div className="constellation-intro">
          <p className="section-label">Long horizon · exploratory</p>
          <h2>From people<br/><em>to biosphere.</em></h2>
          <p>This is a direction of travel, not a delivery promise.</p>
        </div>
        <div className="constellation-grid">
          <article><span>2026</span><h3>Governed foundations</h3><p>Bounded Question Graph prototypes, provenance, the Living Library and AI-assisted analysis. METAD-AK orchestration is not currently deployed.</p></article>
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
        <span>HUMAN 2.0 · v0.1</span><span>Exploratory framework</span><span>Concept figures · not evidence</span><span>September 2026</span>
      </aside>

      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Know · Awaken · Adapt · Regenerate · Flourish</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
