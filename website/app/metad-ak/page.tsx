import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "METAD-AK v0.1 — AKASHICNET.ORG",
  description: "AkashicNET's exploratory meta-intelligence layer: many minds, many models, human judgement remains sovereign.",
};

const stages = [
  ["Input", "Human question, context, sources and analysis intent."],
  ["Orchestration", "Route work across suitable models, tools and evidence-aware workflows."],
  ["Plural analysis", "Invite multiple distinct perspectives rather than a single-model answer."],
  ["Comparison", "Surface agreement, disagreement, uncertainty and model-specific contributions."],
  ["Evidence check", "Trace claims to sources and keep confidence separate from consensus."],
  ["Human review", "A human remains responsible for judgement, framing, values and release."],
];

export default function MetadAkPage() {
  return (
    <main className="about-page">
      <header className="nav-shell about-nav">
        <a className="wordmark" href="/" aria-label="Return to AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="METAD-AK navigation"><a href="/">Home</a><a href="/human-2">HUMAN 2.0</a><a href="#architecture">Architecture</a><a href="#boundary">Human boundary</a><a href="#horizon">Horizon</a></nav>
      </header>

      <section className="about-hero">
        <div className="about-hero-copy">
          <p className="section-label">METAD-AK v0.1 · AkashicNET Meta-Intelligence Layer</p>
          <h1>Many minds.<br/>Many models.<br/><em>Human judgement remains sovereign.</em></h1>
          <p>METAD-AK is an exploratory architecture for comparing multiple machine perspectives while preserving evidence boundaries, provenance, uncertainty and accountable human review.</p>
        </div>
        <figure className="author-seal framework-hero">
          <img src="/images/metad-ak-hero.webp" width="1254" height="1254" fetchPriority="high" alt="A luminous heart-tree divided between a living knowledge commons and a future meta-intelligence layer"/>
          <figcaption>Plural machine intelligence · evidence-aware synthesis · human accountability. Concept only; not currently deployed.</figcaption>
        </figure>
      </section>

      <section className="author-mantra" aria-label="Deployment status">
        <p className="section-label">Future / exploratory · 2026 → 2036 vision</p>
        <blockquote>“Not currently deployed.”</blockquote>
        <p>This page describes a technical horizon, not a promise or guaranteed delivery commitment. Current AkashicNET capabilities remain bounded by the project's published status and evidence-governance rules.</p>
      </section>

      <section className="inner-cosmology" id="architecture">
        <p className="section-label">Technical purpose</p>
        <h2>Plural intelligence.<br/><em>One accountable review boundary.</em></h2>
        <div>
          <h3>Input → Orchestration → Multiple Models → Comparison → Evidence Check → Human Review → Provenance-Rich Output</h3>
          <p>Agreement among models is useful information, but it is not scientific replication and it does not become truth by vote.</p>
        </div>
      </section>

      <figure className="framework-figure">
        <div className="framework-image-scroll" tabIndex={0} role="region" aria-label="Scrollable METAD-AK architecture figure">
          <img src="/images/metad-ak-fig1-multi-ai-architecture.webp" width="1536" height="1024" loading="lazy" decoding="async" alt="Conceptual multi-model workflow from human input through orchestration, comparison, evidence checks and human review"/>
        </div>
        <figcaption><span>Figure 1 · Multi-model architecture</span><p>A provider-neutral conceptual workflow. Models and tools are illustrative components, not confirmed integrations or evidence of deployment.</p></figcaption>
      </figure>

      <section className="constellation">
        <div className="constellation-intro">
          <p className="section-label">Analysis workflow</p>
          <h2>Different models.<br/>Visible disagreement.</h2>
          <p>The objective is not to average away differences. It is to make model contributions, uncertainty and evidential support easier to inspect.</p>
        </div>
        <div className="constellation-grid">
          {stages.map(([title, text], index) => (
            <article key={title}>
              <span>{String(index + 1).padStart(2,"0")}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <aside className="meaning-boundary" aria-label="METAD-AK evidence safeguards">
        <span>Non-negotiable safeguards</span>
        <div><strong>Consensus ≠ proof</strong><p>Several models giving similar answers do not constitute independent empirical confirmation.</p></div>
        <div><strong>Confidence ≠ evidence</strong><p>Model certainty must remain distinguishable from source quality and evidential strength.</p></div>
        <div><strong>Provenance before promotion</strong><p>For any released synthesis, material claims remain traceable to their sources, model contributions and review context.</p></div>
        <div><strong>Uncertainty remains visible</strong><p>Disagreement, missing evidence and unknowns should survive synthesis rather than being smoothed away.</p></div>
      </aside>

      <section className="destination-pair" id="boundary">
        <article>
          <p className="section-label">Human review gate</p>
          <h2>Sovereignty means<br/>accountability.</h2>
          <p>Human judgement remains responsible for accuracy checks, balance, contextual interpretation, values, evidence boundaries and decisions about what is released publicly.</p>
        </article>
        <article>
          <p className="section-label">HUMAN 2.0</p>
          <h2>The engine asks how.<br/>HUMAN 2.0 asks why.</h2>
          <p>METAD-AK explores how multiple intelligences might work together. HUMAN 2.0 explores how that intelligence can be directed wisely: who and what does it serve, and what kind of future does it help create?</p>
          <p><a className="text-link" href="/human-2">Explore HUMAN 2.0 →</a></p>
        </article>
      </section>

      <section className="flying-tension">
        <p className="section-label">Scope boundary</p>
        <h2>Technical architecture.<br/><em>Human purpose.</em></h2>
        <p>METAD-AK remains focused on orchestration, evidence, provenance, disagreement and accountable review. Questions of awareness, wisdom, compassion, community, neurodiversity, the BuddhaFly ethical layer and Flourishing 2100 belong primarily on the HUMAN 2.0 page.</p>
      </section>

      <section className="constellation" id="horizon">
        <div className="constellation-intro">
          <p className="section-label">Exploratory horizon</p>
          <h2>From assisted analysis<br/><em>to a federated knowledge commons.</em></h2>
          <p>These stages are directional and provisional.</p>
        </div>
        <div className="constellation-grid">
          <article><span>2026–2027</span><h3>Model-aware analysis</h3><p>Bounded experiments in routing, attribution and provenance-aware synthesis.</p></article>
          <article><span>2027–2029</span><h3>Evidence-aware orchestration</h3><p>Stronger contradiction handling, uncertainty and research-method context.</p></article>
          <article><span>2030–2032</span><h3>Collaborative intelligence</h3><p>Human and institutional contributions remain attributable and reviewable.</p></article>
          <article><span>2033–2036</span><h3>Federated knowledge commons</h3><p>Interoperable systems preserve provenance across communities and tools.</p></article>
        </div>
      </section>

      <figure className="framework-figure">
        <div className="framework-image-scroll" tabIndex={0} role="region" aria-label="Scrollable METAD-AK roadmap figure">
          <img src="/images/metad-ak-fig2-capabilities-boundaries.webp" width="1536" height="1024" loading="lazy" decoding="async" alt="Exploratory METAD-AK roadmap: Model-aware analysis in 2026–2027, Evidence-aware orchestration in 2027–2029, Collaborative intelligence in 2030–2032, and Federated knowledge commons in 2033–2036."/>
        </div>
        <figcaption><span>Figure 2 · Capabilities and boundaries</span><p>A directional 2026–2036 roadmap. Dates and stages are exploratory rather than delivery commitments; METAD-AK remains not currently deployed.</p></figcaption>
      </figure>

      <aside className="page-provenance" aria-label="Page version and status">
        <span>METAD-AK v0.1</span><span>Future / Exploratory</span><span>Not currently deployed</span><span>Human judgement remains sovereign</span><span>September 2026</span>
      </aside>

      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Many minds · Many models · Human judgement remains sovereign</p><p>Evidence · Provenance · Human review · 2026</p></footer>
    </main>
  );
}
