import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About — AkashicNET",
  description: "About AkashicNET: its human mission, meaning, ethical compass, boundaries and possible outcomes.",
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
        <h1>A living library.<br/><em>A long-term human mission.</em></h1>
        <p>AkashicNET is a citizen data-science and knowledge-stewardship project exploring how scientific research, philosophy, contemplative traditions, lived experience, creativity and community knowledge can be mapped together without pretending that every connection is proven.</p>
      </section>

      <section className="statement">
        <div><p className="section-label">The human thread</p><p className="side-note">Curiosity with provenance.</p></div>
        <div>
          <h2>Both are true.</h2>
          <p>There is a genuine pull toward Varanasi, Sarnath and the wider contemplative traditions connected with them. That pull has emerged through years of reading, travel, music, community encounters, synchronicities and personal reflection.</p>
          <p>At the same time, AkashicNET treats those experiences as biographical and spiritual provenance—not as scientific evidence, destiny, or proof of a metaphysical claim. Their value lies partly in the questions they generate and the paths of inquiry they inspire.</p>
          <p>The mission is therefore not to force every pattern into a single explanation. It is to follow curiosity while preserving uncertainty: to document sources, relationships, contradictions, experiences and open questions in a form that can be reviewed, corrected and extended by others.</p>
        </div>
      </section>

      <section className="manifesto">
        <p className="section-label">Personal compass</p>
        <div className="manifesto-lines"><span>Silence your mind.</span><span>Open your heart.</span><span>Follow your gut.</span></div>
        <p>Awaken within · Serve without</p>
      </section>

      <section className="principles">
        <div className="section-heading"><div><p className="section-label">Why build it?</p><h2>From private curiosity to public service.</h2></div><p>The project is personal in origin, but its value depends on becoming useful beyond one person.</p></div>
        <div className="principle-grid">
          <article><span>01</span><h3>Remember without flattening</h3><p>Preserve where an idea came from, what it meant in context, and what remains uncertain.</p></article>
          <article><span>02</span><h3>Connect without collapsing</h3><p>Let science, philosophy, contemplative traditions and lived experience meet without pretending they carry the same evidential weight.</p></article>
          <article><span>03</span><h3>Correct without erasing</h3><p>Keep mistakes and revisions visible so the history of learning becomes part of the knowledge itself.</p></article>
          <article><span>04</span><h3>Serve rather than persuade</h3><p>Build tools that help people investigate questions for themselves instead of asking them to adopt a worldview.</p></article>
        </div>
      </section>

      <section className="principles">
        <div className="section-heading"><div><p className="section-label">If the mission is completed well</p><h2>What could it result in?</h2></div><p>Possible outcomes, not promises.</p></div>
        <div className="principle-grid">
          <article><span>01</span><h3>A durable public knowledge commons</h3><p>A navigable interdisciplinary library where sources, context, provenance and uncertainty remain visible.</p></article>
          <article><span>02</span><h3>Better research questions</h3><p>Patterns across science, philosophy, contemplative traditions and lived experience could reveal useful questions worth testing without being mistaken for proof.</p></article>
          <article><span>03</span><h3>Stronger evidence stewardship</h3><p>Claims could be separated more clearly into established evidence, interpretation, testimony, hypothesis and speculation.</p></article>
          <article><span>04</span><h3>Tools other people can use</h3><p>Open interfaces, provenance-aware search and reviewable knowledge graphs could help researchers, communities and curious readers explore complex topics more responsibly.</p></article>
          <article><span>05</span><h3>A self-correcting historical record</h3><p>Git history, explicit uncertainty and reversible decisions could preserve how ideas evolve rather than hiding mistakes or overclaiming certainty.</p></article>
          <article><span>06</span><h3>New interdisciplinary bridges</h3><p>Carefully typed relationships could make overlooked connections visible across neuroscience, consciousness studies, philosophy, spirituality, ecology, culture and other domains—while keeping correlation separate from causation.</p></article>
          <article><span>07</span><h3>A model for human–AI collaboration</h3><p>AkashicNET could demonstrate how AI can assist discovery, synthesis and navigation while provenance, rights, uncertainty and consequential judgement remain human-governed.</p></article>
          <article><span>08</span><h3>Service rather than certainty</h3><p>The larger aspiration is not to prove an “Akashic” worldview, but to build something useful enough that greater understanding, compassion, responsible collaboration and human flourishing become more possible.</p></article>
        </div>
      </section>

      <section className="statement">
        <div><p className="section-label">Varanasi · Sarnath</p><p className="side-note">A destination and a research question.</p></div>
        <div>
          <h2>Follow the thread, without deciding the answer in advance.</h2>
          <p>Varanasi and Sarnath represent both a personal direction of travel and a wider field of inquiry into consciousness, contemplative practice, memory, death, rebirth, meaning and the long history of human attempts to understand mind and existence.</p>
          <p>AkashicNET can preserve the route into those questions—including synchronicities and subjective experience—while keeping historical scholarship, scientific evidence, philosophical interpretation and spiritual belief visibly distinct.</p>
        </div>
      </section>

      <section className="boundary">
        <div className="boundary-title"><p className="section-label">Boundary</p><h2>Meaning is allowed.<br/>Overclaiming is not.</h2></div>
        <div className="boundary-list">
          <div><span className="status public">Public</span><p><strong>Vision:</strong> the mission, public-source links, reviewed outputs and high-level project status.</p></div>
          <div><span className="status governed">Governed</span><p><strong>Interpretation:</strong> spiritual, philosophical and experiential ideas can be represented, but their evidential status must remain explicit.</p></div>
          <div><span className="status private">Protected</span><p><strong>Personal and private material:</strong> unnecessary identifying details, raw working data and restricted source material remain outside the public website.</p></div>
        </div>
      </section>

      <aside className="page-quotation" aria-label="AkashicNET compass">
        <span>AkashicNET compass</span><blockquote>“Knowledge explains. Wisdom guides. Compassion decides how knowledge should serve.”</blockquote>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
