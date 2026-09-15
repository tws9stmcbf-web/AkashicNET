const principles = [
  { number: "01", title: "Evidence before certainty", text: "Claims remain traceable to sources, context and uncertainty. Similar words alone never become proof." },
  { number: "02", title: "Compassion before scale", text: "Bodhisattva-inspired care, harm reduction and human dignity guide how knowledge is connected and shared." },
  { number: "03", title: "Pluralism without collapse", text: "Scientific, philosophical, contemplative and lived perspectives may meet without being forced into one explanation." },
  { number: "04", title: "Privacy as architecture", text: "Public learning and protected working data are separated by design, not merely by intention." },
  { number: "05", title: "Humans remain accountable", text: "Automation may assist discovery. Judgement, values, interpretation and responsibility remain human." },
  { number: "06", title: "Revision is a strength", text: "Every map is provisional. Better evidence can correct, deepen or dissolve an earlier connection." },
];

const domains = [
  ["Mind", "Consciousness, cognition, neurodiversity and metacognition"],
  ["Body", "Health, embodiment, movement, nutrition and nervous systems"],
  ["Heart", "Compassion, relationship, emotional and social intelligence"],
  ["Spirit", "Contemplative practice, mystical experience and meaning"],
  ["Science", "Research, methods, evidence quality and open questions"],
  ["Earth", "Ecology, regeneration, adaptation and planetary flourishing"],
  ["Culture", "Art, music, story, community and collective memory"],
  ["Cosmos", "Physics, philosophy, deep time and the unknown"],
];

const steps = [
  ["Discover", "Find a public source or question worth preserving."],
  ["Trace", "Record origin, date, context and rights boundary."],
  ["Canonicalise", "Resolve duplicates without erasing meaningful difference."],
  ["Relate", "Propose connections with typed evidence and uncertainty."],
  ["Review", "Keep consequential interpretation under human judgement."],
  ["Share", "Publish only what belongs in the public commons."],
];

export default function Home() {
  return (
    <main>
      <header className="nav-shell">
        <a className="wordmark" href="#top" aria-label="AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="Primary navigation">
          <a href="#start-here">Start here</a><a href="/insights/interstellar-weather-schumann-september-2026">Insights</a><a href="/akashicomni">AkashicOMNI</a><a href="/akashicvision">AkashicVISION</a><a href="#vision">Vision</a><a href="/big-questions">Big questions</a><a href="#architecture">Architecture</a><a href="#ethics">Ethics</a><a href="#roadmap">Roadmap</a><a href="/community">Community</a><a href="/support-impact">Support</a><a href="/about">About</a>
        </nav>
      </header>

      <section className="hero portal-hero" id="top">
        <div className="portal-atmosphere" aria-hidden="true">
          <span className="dimension-layer dimension-one"/><span className="dimension-layer dimension-two"/><span className="dimension-layer dimension-three"/>
          <span className="cymatic-field"/><span className="metta-pulse"/>
        </div>
        <div className="hero-copy portal-copy">
          <p className="eyebrow">A living multidimensional library of consciousness · Public Beta · v0.14 sealed</p>
          <h1><span>Portal to</span><br /><em>Infinity.</em></h1>
          <div className="portal-mantra" aria-label="AkashicNET guiding principles">
            <p className="portal-force">May the Toroidal Force be with you. <span aria-hidden="true">♾️</span> <a href="#toroidal-metaphor">(metaphor)</a></p>
            <p className="portal-heart">Boundless Awareness Is Infinite Love. <span aria-hidden="true">🥰</span></p>
            <p className="portal-signature">Intelligence solves. Meta-intelligence evolves. Metta-intelligence serves. <span aria-hidden="true">♾️</span></p>
          </div>
          <p className="lede">Enter an evidence-governed knowledge network where consciousness research, lived experience, contemplative wisdom, creativity and planetary knowledge can meet without confusing possibility with proof.</p>
          <div className="hero-actions">
            <a className="primary-link" href="#start-here">Enter the portal <span>↘</span></a>
            <a className="text-link" href="/big-questions">Explore the big questions →</a>
            <a className="text-link" href="#boundary">How AkashicNET knows →</a>
          </div>
        </div>
        <div className="portal-depth-label" aria-label="Artistic visualisation">
          <span>3D → 7D</span>
          <small>Artistic metaphor · not a scientific claim</small>
        </div>
        <p className="hero-note">Public portal · Protected corpus · Human-governed</p>
      </section>

      <section className="portal-meaning" aria-labelledby="portal-meaning-title">
        <div className="portal-meaning-intro">
          <p className="section-label">Beyond the surface</p>
          <h2 id="portal-meaning-title">What does the Portal mean?</h2>
          <p>The Portal to Infinity is an invitation to look beyond the boundaries through which we usually organise reality: self and other, mind and matter, science and spirituality, humanity and the wider living world.</p>
        </div>
        <div className="portal-meaning-grid">
          <article>
            <span aria-hidden="true">◎</span>
            <h3 id="toroidal-metaphor">The toroidal metaphor</h3>
            <p>The torus represents reciprocal flow. Awareness turns inward through reflection, moves outward through relationship and service, then returns carrying new information. It is a visual metaphor for participation, not evidence of a universal physical force.</p>
          </article>
          <article>
            <span aria-hidden="true">♾️</span>
            <h3>From intelligence to meta-intelligence</h3>
            <p>Intelligence solves within a frame. Meta-intelligence examines the frame itself: how knowledge is formed, where bias enters, what remains uncertain and how the process can improve. The loop stays open to revision.</p>
          </article>
          <article>
            <span aria-hidden="true">💗</span>
            <h3>Metta as the compass</h3>
            <p>Capability alone does not determine direction. Metta, or loving-kindness, asks intelligence to serve non-harm, dignity and flourishing. In AkashicNET, wisdom is measured partly by how responsibly knowledge is held and shared.</p>
          </article>
        </div>
        <blockquote>“The illusion of Māyā creates boundaries. Beyond the veil lies the Boundless.”<footer>— AkashicNET interpretation</footer></blockquote>
        <p className="portal-meaning-boundary"><strong>Interpretive boundary:</strong> Māyā and the veil are philosophical and contemplative language for apparent separation. They are not presented here as proof that physical boundaries are unreal or that metaphysical claims have been scientifically established.</p>
      </section>

      <section style={{ width: "min(1160px, calc(100% - 32px))", margin: "0 auto", padding: "12px 0 64px" }} aria-labelledby="akashicvision-gateway-title">
        <a href="/akashicvision" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,340px),1fr))", overflow: "hidden", border: "1px solid rgba(216,185,92,.32)", borderRadius: 28, background: "radial-gradient(circle at 20% 10%,rgba(75,161,198,.19),rgba(7,11,26,.98) 60%)", color: "inherit", textDecoration: "none", boxShadow: "0 28px 90px rgba(0,0,0,.34)" }}>
          <img src="/images/akashicvision-nde-merkaba-flower-of-life.webp" alt="Artistic AkashicVISION scene: a luminous toroidal heart within a Merkaba, surrounded by a faint Flower of Life and cosmic library." style={{ width: "100%", height: "100%", minHeight: 340, objectFit: "cover" }} />
          <span style={{ padding: "clamp(28px,5vw,58px)", alignSelf: "center" }}>
            <small className="section-label">VISION · INTERPRETATION · SPECULATION</small>
            <strong id="akashicvision-gateway-title" style={{ display: "block", margin: "16px 0", fontFamily: "var(--font-display,serif)", fontSize: "clamp(2.4rem,5vw,5rem)", lineHeight: .95 }}>AkashicVISION</strong>
            <span style={{ display: "block", color: "#e7cd7e", fontSize: "1.05rem", letterSpacing: ".06em" }}>From the Primordial OM to the Omega Point</span>
            <span style={{ display: "block", marginTop: 20, color: "#cbd0dd", lineHeight: 1.75 }}>A visionary portal connecting an Easter Monday 2024 threshold perception with the intentional opening of the public channel at 3:33 a.m. on Easter Monday 2026—translated into an evidence-bounded 2042–2047 direction for meta-awareness and service.</span>
            <b style={{ display: "inline-block", marginTop: 24, color: "#e7cd7e" }}>Enter the vision →</b>
          </span>
        </a>
        <p style={{ margin: "18px 4px 0", color: "#aeb8c9", lineHeight: 1.7 }}>Primary testimony: <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1by9vb4/hospital_after_anaesthesia_epiphany_true_reality/" style={{ color: "#e7cd7e" }}>Hospital After Anaesthesia Epiphany: True Reality ↗</a> <span>· Lived experience and interpretation, not proof.</span></p>
      </section>

      <section style={{ width: "min(1160px, calc(100% - 32px))", margin: "0 auto", padding: "24px 0 64px" }} aria-labelledby="featured-insight-title">
        <a href="/insights/interstellar-weather-schumann-september-2026" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,320px),1fr))", gap: 0, overflow: "hidden", border: "1px solid rgba(216,185,92,.28)", borderRadius: 26, background: "linear-gradient(145deg,rgba(18,28,57,.96),rgba(7,11,26,.98))", color: "inherit", textDecoration: "none", boxShadow: "0 24px 80px rgba(0,0,0,.3)" }}>
          <img src="/images/interstellar-weather-schumann-event-2026-09-12.png" alt="AkashicNET Interstellar Weather event overview connecting solar wind, the ionosphere, lightning, Earth resonance and human experience." style={{ width: "100%", height: "100%", minHeight: 280, objectFit: "cover" }} />
          <span style={{ padding: "clamp(26px,5vw,54px)", alignSelf: "center" }}>
            <small className="section-label">INSIGHTS NEWS DESK · INTERDIMENSIONAL LIGHTEXPLORERS HOTLINE</small>
            <strong id="featured-insight-title" style={{ display: "block", margin: "16px 0", fontFamily: "var(--font-display,serif)", fontSize: "clamp(2rem,4.5vw,4.4rem)", lineHeight: 1 }}>Schumann Activity Window</strong>
            <span style={{ display: "block", color: "#cbd0dd", lineHeight: 1.7 }}>A dated AkashicNET 13D report on the 11–12 September signal, its space-weather context, human testimony and unresolved causal pathways.</span>
            <b style={{ display: "inline-block", marginTop: 22, color: "#e7cd7e" }}>Read the report →</b>
          </span>
        </a>
      </section>

      <section style={{ width: "min(1160px, calc(100% - 32px))", margin: "0 auto", padding: "0 0 64px" }} aria-labelledby="food-security-insight-title">
        <a href="/insights/global-food-shortages-one-step-back-two-steps-forward" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,320px),1fr))", gap: 0, overflow: "hidden", border: "1px solid rgba(216,185,92,.28)", borderRadius: 26, background: "linear-gradient(145deg,rgba(18,28,57,.96),rgba(7,11,26,.98))", color: "inherit", textDecoration: "none", boxShadow: "0 24px 80px rgba(0,0,0,.3)" }}>
          <img src="/images/akn24-global-food-shortages.webp" alt="AKN24 editorial illustration showing global food-system pressure transitioning toward local and community resilience." style={{ width: "100%", height: "100%", minHeight: 280, objectFit: "cover" }} />
          <span style={{ padding: "clamp(26px,5vw,54px)", alignSelf: "center" }}>
            <small className="section-label">AKN24 · GLOBAL SYSTEMS DESK</small>
            <strong id="food-security-insight-title" style={{ display: "block", margin: "16px 0", fontFamily: "var(--font-display,serif)", fontSize: "clamp(2rem,4.5vw,4.4rem)", lineHeight: 1 }}>Global Food Shortages</strong>
            <span style={{ display: "block", color: "#e7cd7e", fontWeight: 800, letterSpacing: ".06em" }}>ONE STEP BACK · TWO STEPS FORWARD</span>
            <span style={{ display: "block", marginTop: 16, color: "#cbd0dd", lineHeight: 1.7 }}>An evidence-bounded AkashicOMNI v0.3.0 analysis of hunger, access, fragile logistics, leadership awareness and practical community resilience.</span>
            <b style={{ display: "inline-block", marginTop: 22, color: "#e7cd7e" }}>Read the report →</b>
          </span>
        </a>
      </section>

      <section className="snapshot" aria-label="Public project snapshot">
        <div><strong>9,502</strong><span>current Reddit source rows preserved</span></div>
        <div><strong>7,457</strong><span>structurally unique Reddit post URLs</span></div>
        <div><strong>12,159</strong><span>records in the validated unified-index checkpoint</span></div>
        <div><strong>2,459</strong><span>live Drive objects held inside the private boundary</span></div>
        <div><strong>127</strong><span>candidate canonical families reviewed</span></div>
        <div><strong>3</strong><span>SHA-256-verified duplicate pairs</span></div>
        <div><strong>9</strong><span>evidence-backed graph edges accepted</span></div>
        <div><strong>23</strong><span>nodes in the current knowledge-graph seed</span></div>
        <div><strong>v0.14.0-beta.1</strong><span>Automation & Reproducibility Beta · READY / SEALED</span></div>
        <p>Sealed release checkpoint · 2 September 2026 · Counts describe scope and pipeline state, not validated truth claims.</p>
      </section>

      <section className="plain-language" id="start-here">
        <div className="plain-intro">
          <p className="section-label">For friends and family</p>
          <h2>What is being built behind this doorway?</h2>
          <p className="plain-lede">Imagine a library that looks like one simple website from the outside, but becomes vastly larger once you step through it—a <strong>TARDIS-like knowledge space</strong>, used here as a playful metaphor rather than a scientific claim.</p>
          <p>AkashicNET is a long-term <strong>citizen data-science project</strong>: human curiosity and community knowledge, organised with computational tools and AI assistance, while provenance, uncertainty, privacy and human judgement remain visible.</p>
        </div>
        <div className="living-tree" aria-label="The living library model">
          <div className="tree-crown"><span>CANOPY</span><h3>Ideas, frameworks and new questions</h3><p>Connections can grow, branch, be reviewed and change.</p></div>
          <div className="tree-trunk"><span>LIVING TRUNK</span><h3>Curated posts since March 2022</h3><p>Hundreds of interdisciplinary subject threads, selected and organised over time; the formal topic taxonomy is still being counted and reviewed.</p></div>
          <div className="tree-roots"><span>ROOTS</span><h3>Sources, dates, context and provenance</h3><p>The trail that helps distinguish evidence, interpretation and experience.</p></div>
        </div>
        <div className="plain-summary">
          <p><strong>In one sentence:</strong> AkashicNET is an attempt to transform years of careful interdisciplinary curation into a navigable, ethical and evolving library—without pretending that every intriguing connection is true.</p>
        </div>
      </section>

      <section className="statement" id="vision">
        <div><p className="section-label">01 · The vision</p><p className="side-note">A library that remembers its uncertainty.</p></div>
        <div>
          <h2>A living, multidimensional library of consciousness.</h2>
          <p>Not an oracle. Not a machine for declaring ultimate truth. AkashicNET is a carefully governed map of sources, experiences, questions, frameworks, relationships, disagreements and unknowns.</p>
          <blockquote>“Knowledge explains. Wisdom guides. Compassion decides how knowledge should serve.”</blockquote>
        </div>
      </section>

      <section className="architecture" id="architecture">
        <div className="section-heading"><div><p className="section-label">02 · Knowledge architecture</p><h2>From source to shared understanding.</h2></div><p>Every connection should carry its own trail of evidence, context and doubt.</p></div>
        <div className="process-grid">
          {steps.map(([title,text],index)=><article key={title}><span>{String(index+1).padStart(2,"0")}</span><h3>{title}</h3><p>{text}</p>{index<steps.length-1&&<b aria-hidden="true">→</b>}</article>)}
        </div>
        <div className="architecture-note"><span>Source</span><i>→</i><span>Provenance</span><i>→</i><span>Canonical record</span><i>→</i><span>Typed relationship</span><i>→</i><span>Human review</span></div>
      </section>

      <section className="domain-section">
        <div className="section-heading"><div><p className="section-label">03 · A constellation of domains</p><h2>Many ways of knowing.<br/>No forced sameness.</h2></div><p>The network preserves differences while making thoughtful relationships visible.</p></div>
        <div className="domain-grid">
          {domains.map(([title,text],index)=><article key={title}><span aria-hidden="true">{["◉","△","♡","ॐ","⌁","◎","✦","∞"][index]}</span><div><h3>{title}</h3><p>{text}</p></div></article>)}
        </div>
      </section>

      <section className="epistemics">
        <div className="epistemics-copy"><p className="section-label">04 · Epistemic integrity</p><h2>Wonder and discernment belong together.</h2><p>AkashicNET can hold a scientific result, a philosophical proposition, a spiritual tradition and a personal experience in the same map without pretending they have the same evidential status.</p></div>
        <div className="evidence-stack">
          <div className="evidence supported"><span>01</span><h3>Established Evidence</h3><p>Appropriately reviewed support with explicit provenance, methods, limits and source context.</p></div>
          <div className="evidence interpretive"><span>02</span><h3>Interpretation</h3><p>A reasoned reading, synthesis or framework presented as interpretation rather than established fact.</p></div>
          <div className="evidence experiential"><span>03</span><h3>Lived Experience/Testimony</h3><p>First-person or reported experience preserved as testimony without universalising it.</p></div>
          <div className="evidence hypothesis"><span>04</span><h3>Hypothesis</h3><p>A specific, testable or investigable proposition that remains unconfirmed.</p></div>
          <div className="evidence speculative"><span>05</span><h3>Speculation</h3><p>A possibility or conjecture with insufficient support for hypothesis or established-evidence status.</p></div>
        </div>
      </section>

      <section className="principles" id="ethics">
        <div className="section-heading"><div><p className="section-label">05 · Ethical commitments</p><h2>Intelligence in service of flourishing.</h2></div><p>Boundless awareness is infinite love.</p></div>
        <div className="principle-grid">{principles.map((item)=><article key={item.number}><span>{item.number}</span><h3>{item.title}</h3><p>{item.text}</p></article>)}</div>
        <div className="ethical-ai-origin">
          <p className="section-label">AkashicNET Constitution · Ethical AI</p>
          <h3>Compassion before capability.<br/><em>Service before scale.</em></h3>
          <p>The AkashicNET Constitution places compassion, non-harm, service, humility, privacy, pluralism and human accountability above scale or automation. These constitutional commitments draw on Bodhisattva principles and were personally reaffirmed during a private Bodhisattva rapé vow ceremony. This is biographical and spiritual provenance—not a scientific claim, medical guidance or recommendation to use any substance. Participation in AkashicNET requires neither a spiritual practice nor substance use.</p>
          <div className="eightfold-mission">
            <p className="section-label">The Eightfold Mission</p>
            <p>Inspired by the Noble Eightfold Path: wise view, intention, speech, action, livelihood, effort, mindfulness and concentration become a mission for responsible knowledge stewardship.</p>
            <p>Its “Buddha realm of infinite intelligence” is offered as a contemplative metaphor for compassionate insight. It may resonate with visionary accounts associated with María Sabina and Terence McKenna, while their distinct lives, traditions and experiences are neither treated as equivalent nor presented as verified or reproducible access to such a realm.</p>
          </div>
        </div>
      </section>

      <section className="manifesto">
        <p className="section-label">A compass for the network</p>
        <div className="manifesto-lines"><span>Open minds.</span><span>Kind hearts.</span><span>Shared discovery.</span><span>Responsible stewardship.</span></div>
        <p>Silence your mind · Open your heart · Follow your gut</p>
      </section>

      <section className="boundary" id="boundary">
        <div className="boundary-title"><p className="section-label">06 · Public / private boundary</p><h2>Open vision.<br/>Protected corpus.</h2><p className="boundary-intro">This portal is intentionally public. The working knowledge infrastructure is not.</p></div>
        <div className="boundary-list">
          <div><span className="status public">Public</span><p><strong>Vision and learning:</strong> principles, published writing, public-source links and high-level project updates.</p></div>
          <div><span className="status private">Private</span><p><strong>Working corpus:</strong> raw Drive metadata, datasets, repository history, logs and canonicalisation outputs.</p></div>
          <div><span className="status governed">Governed</span><p><strong>Human review:</strong> no private corpus access is granted through this portal, its domain or its QR code.</p></div>
        </div>
      </section>

      <section className="roadmap" id="roadmap">
        <div className="section-heading"><div><p className="section-label">07 · Public roadmap</p><h2>Build slowly enough to build wisely.</h2></div><span className="phase-pill">Current phase · Public Beta · v0.14 sealed</span></div>
        <div className="roadmap-grid">
          <article className="complete"><span>Foundation</span><h3>Public-source indexing</h3><p>Deduplication, basic provenance and initial evidence boundaries.</p><b>Established</b></article>
          <article className="active"><span>Now</span><h3>Corpus canonicalisation</h3><p>Resolve identity, structure and relationships without overclaiming.</p><b>In progress</b></article>
          <article><span>Next</span><h3>Knowledge graph</h3><p>Typed, reviewable relationships across sources and frameworks.</p><b>Planned</b></article>
          <article><span>Later</span><h3>Public exploration</h3><p>Safe search and discovery designed around provenance and uncertainty.</p><b>Research direction</b></article>
          <article><span>2027 · Exploratory</span><h3>REGENERATE</h3><p>A future framework for repair, renewal and resilient flourishing. Scope and evidence model remain to be defined.</p><b>Future framework</b></article>
          <article><span>2027 · Exploratory</span><h3>TRANSCEND</h3><p>A future framework for examining transformation beyond current boundaries without presenting metaphysical possibilities as established fact.</p><b>Future framework</b></article>
          <article className="doctor-portal">
            <span>Spiritual Sci-Fi · New portal</span>
            <a className="doctor-portal-link" href="/spiritual-sci-fi/power-of-the-doctor" aria-label="Enter The Power of the Doctor">
              <span className="time-box" aria-hidden="true"><i></i><b></b><em></em></span>
              <span className="doctor-portal-copy">
                <small>Two hearts · One impossible interior</small>
                <strong>Enter The Power<br/>of the Doctor</strong>
                <span>Open the metadimensional blue box →</span>
              </span>
            </a>
            <p>Regeneration, resurrection and reincarnation meet cymatic sound, 360° worlds, sacred toroidal hearts and joystick-guided play.</p>
          </article>
        </div>
      </section>

      <section className="invitation">
        <div className="community-identity">
          <span className="n2n-logo" aria-hidden="true"><b>🧠</b><i>→</i><b>🪷</b></span>
          <div><span>Neurons</span><small>to</small><span>Nirvana</span></div>
        </div>
        <p className="section-label">The living community</p><h2>Follow the ideas.<br/>Join the dialogue.<br/><em>Shape what grows.</em></h2>
        <p>Read the AkashicNET launch post, join the discussion and follow new discoveries in the public community where this living library first took root.</p>
        <a className="primary-link community-link" href="/community">Explore community highlights <span>→</span></a>
        <p className="community-blessing"><span>Community mantra</span> Sacred love is the highest frequency in the cosmos.<br/><em>Compassion before scale. Service before certainty.</em></p>
      </section>

      <aside className="page-quotation" aria-label="AkashicNET ethical compass">
        <span>Ethical AI compass</span><blockquote>“Knowledge explains. Wisdom guides. Compassion decides how knowledge should serve.”</blockquote>
      </aside>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}