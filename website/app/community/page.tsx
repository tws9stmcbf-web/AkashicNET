import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Community Highlights — AkashicNET",
  description: "A curated doorway from AkashicNET into selected public posts from r/NeuronsToNirvana.",
};

const highlights = [
  {
    kind: "Featured launch",
    mark: "🕸️",
    title: "AkashicNET.org is alive",
    text: "The public launch announcement: a living, multidimensional library of consciousness grounded in provenance, uncertainty and human judgement.",
    note: "Citizen science · 30 August 2026",
    href: "https://www.reddit.com/r/NeuronsToNirvana/comments/1w2awju/akashicnetorg_is_alive_a_living_multidimensional/",
  },
  {
    kind: "Community compass",
    mark: "🧭",
    title: "Disclaimer & Shamanic Humble Reflections",
    text: "The community’s public boundary between education, lived and spiritual interpretation, professional advice and established scientific fact.",
    note: "Discernment · Harm reduction · Transparency",
    href: "https://www.reddit.com/r/NeuronsToNirvana/comments/1u49cm7/rneuronstonirvana_disclaimer_shamanic_humble/",
  },
  {
    kind: "Inspiring practice",
    mark: "🪷🦋",
    title: "#HOMESENSE800 — The Buddhafly Effect",
    text: "An Ozora-born reflection on awakening, transformation, curiosity and perspective—holding personal synchronicity as meaningful experience without presenting it as objective proof.",
    note: "Phase 8 · Transcendence · Living practice",
    href: "https://www.reddit.com/r/NeuronsToNirvana/comments/1vr7i7x/homesense800_the_buddhafly_effect_phase_8/",
  },
];

export default function CommunityPage() {
  return (
    <main className="community-page">
      <header className="nav-shell community-nav">
        <a className="wordmark" href="/" aria-label="Return to AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="Community navigation"><a href="/">Home</a><a href="/about">About</a><a href="https://www.reddit.com/r/NeuronsToNirvana/" target="_blank" rel="noreferrer">All Reddit posts ↗</a></nav>
      </header>

      <section className="community-hero">
        <div className="community-identity">
          <span className="n2n-logo" aria-hidden="true"><b>🧠</b><i>→</i><b>🪷</b></span>
          <div><span>Neurons</span><small>to</small><span>Nirvana</span></div>
        </div>
        <p className="section-label">From the living community</p>
        <h1>Ideas become alive<br/><em>when they are shared.</em></h1>
        <p>Selected public pathways into r/NeuronsToNirvana—the community soil from which AkashicNET emerged. These links open on Reddit; no private corpus data is exposed here.</p>
      </section>

      <section className="highlight-grid" aria-label="Curated community posts">
        {highlights.map((item, index) => (
          <article className={`${index === 0 ? "featured-highlight " : ""}highlight-theme-${index + 1}`} key={item.href}>
            <div className="highlight-top"><span aria-hidden="true">{item.mark}</span><p>{item.kind}</p><b>{String(index + 1).padStart(2, "0")}</b></div>
            <h2>{item.title}</h2>
            <p>{item.text}</p>
            <small>{item.note}</small>
            <a href={item.href} target="_blank" rel="noreferrer">Read on Reddit <span>↗</span></a>
          </article>
        ))}
      </section>

      <figure className="matrix-art">
        <img src="/images/matrix-enlightenment-library.png" alt="A luminous living tree forms a portal into an infinite library, surrounded by neural, mycelial and constellation-like networks, lotus flowers and butterflies." />
        <figcaption><span>Visual metaphor · Iteration 01</span><p>Matrix · Enlightenment · Library — knowledge as a living relationship between roots, memory, transformation and the unknown.</p></figcaption>
      </figure>

      <section className="matrix-oath" aria-labelledby="matrix-oath-title">
        <div className="oath-intro">
          <p className="section-label">Matrix · Enlightenment · Library</p>
          <h2 id="matrix-oath-title">A Synchronicity Oath<br/><em>for the living library.</em></h2>
          <p>A poetic community charter—not a scientific claim—joining inner awareness to responsible public knowledge.</p>
        </div>
        <div className="oath-lines">
          <p><span>01</span>I enter with curiosity, not certainty.</p>
          <p><span>02</span>I honour evidence, experience and the space between them.</p>
          <p><span>03</span>I protect privacy, dignity and the right to remain unknown.</p>
          <p><span>04</span>I connect perspectives without forcing them into sameness.</p>
          <p><span>05</span>I awaken within—and place what I learn in service of life.</p>
        </div>
        <div className="oath-seal" aria-label="Closing words"><span>∞</span><p>Open mind · Kind heart · Discernment · Service</p></div>
      </section>

      <section className="community-end">
        <p className="section-label">Continue exploring</p>
        <h2>Thousands of signals.<br/><em>One evolving conversation.</em></h2>
        <div><a className="primary-link" href="https://www.reddit.com/r/NeuronsToNirvana/" target="_blank" rel="noreferrer">Enter r/NeuronsToNirvana <span>↗</span></a><a className="text-link" href="/">Return to AkashicNET</a></div>
        <p className="community-blessing"><span>Community mantra</span> Sacred love is the highest frequency in the cosmos.<br/><em>Open minds. Kind hearts. Shared discovery. Responsible stewardship.</em></p>
      </section>

      <aside className="page-quotation community-quotation" aria-label="Community compass">
        <span>Community compass</span><blockquote>“Curiosity over certainty. Dialogue over polarisation. Stewardship over extraction.”</blockquote>
      </aside>
      <aside className="page-provenance" aria-label="Page iteration and update date">
        <span>Community page · Iteration 04</span><span>Updated 30 August 2026</span>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
