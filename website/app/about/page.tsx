import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About — AkashicNET",
  description: "About AkashicNET: its mission, meaning, boundaries and possible outcomes.",
};

// Public identity is intentionally anonymous: no personal name is published on this page.
export default function AboutPage() {
  return (
    <main className="community-page">
      <header className="nav-shell community-nav">
        <a className="wordmark" href="/" aria-label="Return to AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="About navigation"><a href="/">Home</a><a href="/community">Community</a></nav>
      </header>

      <section className="community-hero">
        <p className="section-label">About AkashicNET</p>
        <h1>A living library.<br/><em>A long-term mission.</em></h1>
        <p>AkashicNET is a citizen data-science and knowledge-stewardship project exploring how scientific research, philosophy, contemplative traditions, lived experience, creativity and community knowledge can be mapped together without pretending that every connection is proven.</p>
      </section>

      <section className="statement">
        <div><p className="section-label">Meaning</p><p className="side-note">Curiosity with provenance.</p></div>
        <div>
          <h2>Both are true.</h2>
          <p>There is a genuine pull toward Varanasi and the wider contemplative traditions connected with it. At the same time, AkashicNET treats that pull as personal and spiritual orientation—not as scientific evidence, destiny, or proof of a metaphysical claim.</p>
          <p>The mission is to follow curiosity while preserving uncertainty: to document sources, relationships, contradictions, experiences and open questions in a form that can be reviewed, corrected and extended by others.</p>
        </div>
      </section>

      <section className="principles">
        <div className="section-heading"><div><p className="section-label">If the mission is completed well</p><h2>What could it result in?</h2></div><p>Possible outcomes, not promises.</p></div>
        <div className="principle-grid">
          <article><span>01</span><h3>A durable public knowledge commons</h3><p>A navigable interdisciplinary library where sources, context, provenance and uncertainty remain visible.</p></article>
          <article><span>02</span><h3>Better questions</h3><p>Patterns across science, philosophy, contemplative traditions and lived experience could reveal useful research questions without being mistaken for proof.</p></article>
          <article><span>03</span><h3>Stronger evidence stewardship</h3><p>Claims could be separated more clearly into established evidence, interpretation, testimony, hypothesis and speculation.</p></article>
          <article><span>04</span><h3>Tools other people can use</h3><p>Open interfaces, provenance-aware search and reviewable knowledge graphs could help researchers, communities and curious readers explore complex topics more responsibly.</p></article>
          <article><span>05</span><h3>A record that can correct itself</h3><p>Git history, explicit uncertainty and reversible decisions could preserve how ideas evolve rather than hiding mistakes or overclaiming certainty.</p></article>
          <article><span>06</span><h3>Service rather than certainty</h3><p>The larger aspiration is not to prove an “Akashic” worldview, but to build something useful enough that greater understanding, compassion and responsible collaboration become more possible.</p></article>
        </div>
      </section>

      <section className="boundary">
        <div className="boundary-title"><p className="section-label">Boundary</p><h2>Meaning is allowed.<br/>Overclaiming is not.</h2></div>
        <div className="boundary-list">
          <div><span className="status public">Public</span><p><strong>Vision:</strong> the mission, public-source links, reviewed outputs and high-level project status.</p></div>
          <div><span className="status governed">Governed</span><p><strong>Interpretation:</strong> spiritual, philosophical and experiential ideas can be represented, but their evidential status must remain explicit.</p></div>
          <div><span className="status private">Protected</span><p><strong>Private corpus:</strong> raw working data and restricted source material remain outside the public website.</p></div>
        </div>
      </section>

      <aside className="page-quotation" aria-label="AkashicNET compass">
        <span>AkashicNET compass</span><blockquote>“Knowledge explains. Wisdom guides. Compassion decides how knowledge should serve.”</blockquote>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
