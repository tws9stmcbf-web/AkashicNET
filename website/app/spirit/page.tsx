const journeys = [
  {
    mark: "🧘",
    title: "Practice and presence",
    text: "Vipassana, mettā, contemplative practice and Bodhisattva-inspired service form the ethical centre of the journey.",
    note: "Practice · Compassion · Meaning",
  },
  {
    mark: "☸",
    title: "Pilgrimage and place",
    text: "Sarnath, the Golden Temple, a special tree and the Dalai Lama Temple Complex are preserved as places of memory, encounter and reflection.",
    note: "Place · Memory · Cultural humility",
  },
  {
    mark: "🌀",
    title: "Festival fieldwork",
    text: "BOOM, Being Gathering, O.Z.O.R.A.'s Fairy Garden, Tribal Gathering, ICPR, Tryp Expo and Trikaya Dream Escape become waypoints rather than proof claims.",
    note: "Community · Psytrance · Inquiry",
  },
  {
    mark: "29",
    title: "Synchronicity and play",
    text: "The recurring 29 thread, full moons, a cow's hello and a baby's laughter after eye contact are held as meaningful lived experience without asserting an external hidden mechanism.",
    note: "Testimony · Pattern · Playful universe",
  },
];

const related = [
  ["Mind", "Consciousness, neurodiversity and metacognition", "/#architecture"],
  ["Heart", "Compassion, relationship and mettā intelligence", "/#ethics"],
  ["Community", "The public conversations from which the map grew", "/community"],
  ["Big Questions", "Open inquiry without premature certainty", "/big-questions"],
];

export const metadata = {
  title: "Spirit | The Infinity Key | AkashicNET",
  description: "A lived-experience and artistic-metaphor journey from neurons, through nature, to nirvana.",
};

export default function SpiritPage() {
  return (
    <main style={{ minHeight: "100vh", background: "#070b1a", color: "#f5f0df" }}>
      <header className="nav-shell">
        <a className="wordmark" href="/" aria-label="AkashicNET.org home">
          <img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" />
          <span className="brand-name">AKASHICNET.ORG</span>
        </a>
        <nav aria-label="Spirit navigation">
          <a href="/">Home</a>
          <a href="#journey">Journey</a>
          <a href="#boundary">Evidence boundary</a>
          <a href="/community">Community</a>
        </nav>
      </header>

      <section style={{ width: "min(1180px,calc(100% - 32px))", margin: "0 auto", padding: "clamp(7rem,8vw,8rem) 0 70px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,380px),1fr))", border: "1px solid rgba(231,205,126,.35)", borderRadius: 30, overflow: "hidden", background: "radial-gradient(circle at 20% 10%,rgba(77,63,171,.28),rgba(7,11,26,.98) 62%)", boxShadow: "0 32px 110px rgba(0,0,0,.44)" }}>
          <div style={{ padding: "clamp(30px,6vw,72px)", alignSelf: "center" }}>
            <p className="section-label">SPIRIT · LIVED EXPERIENCE · ARTISTIC METAPHOR</p>
            <h1 style={{ margin: "18px 0", fontFamily: "var(--font-display,serif)", fontSize: "clamp(3rem,7vw,6.5rem)", lineHeight: .88 }}>The Infinity<br /><em>Key.</em></h1>
            <p style={{ color: "#e7cd7e", fontSize: "clamp(1rem,2vw,1.28rem)", letterSpacing: ".05em", lineHeight: 1.55 }}>FROM NEURONS · THROUGH NATURE · TO NIRVANA</p>
            <p style={{ color: "#cbd0dd", fontSize: "1.08rem", lineHeight: 1.8 }}>A playful autobiographical map of contemplative practice, sacred places, festival fieldwork, family memories and synchronicities carried toward the AkashicNET Stargate.</p>
            <p style={{ color: "#f0d681", fontWeight: 800 }}>Cultivating love and wisdom. Boundless awareness is infinite love.</p>
          </div>
        </div>
      </section>

      <section id="journey" style={{ width: "min(1100px,calc(100% - 32px))", margin: "0 auto", padding: "30px 0 90px" }}>
        <div className="section-heading">
          <div><p className="section-label">THE JOURNEY</p><h2>One path, many kinds of meaning.</h2></div>
          <p>The story is presented in readable, accessible layers rather than relying on tiny lettering embedded inside a single poster.</p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,240px),1fr))", gap: 18 }}>
          {journeys.map((item) => (
            <article key={item.title} style={{ padding: 28, border: "1px solid rgba(231,205,126,.24)", borderRadius: 22, background: "linear-gradient(145deg,rgba(18,28,57,.94),rgba(7,11,26,.98))" }}>
              <span aria-hidden="true" style={{ color: "#e7cd7e", fontSize: 30, fontWeight: 900 }}>{item.mark}</span>
              <h3 style={{ fontSize: "1.35rem", margin: "18px 0 12px" }}>{item.title}</h3>
              <p style={{ color: "#cbd0dd", lineHeight: 1.7 }}>{item.text}</p>
              <small style={{ color: "#e7cd7e", letterSpacing: ".06em" }}>{item.note}</small>
            </article>
          ))}
        </div>
      </section>

      <section id="boundary" style={{ width: "min(1000px,calc(100% - 32px))", margin: "0 auto 90px", padding: "clamp(28px,5vw,56px)", borderLeft: "4px solid #e7cd7e", background: "rgba(18,28,57,.72)", borderRadius: "0 24px 24px 0" }}>
        <p className="section-label">HOW AKASHICNET KNOWS</p>
        <h2 style={{ fontSize: "clamp(2rem,5vw,4rem)", margin: "12px 0" }}>Meaning is preserved without becoming proof.</h2>
        <p style={{ color: "#cbd0dd", lineHeight: 1.8, fontSize: "1.08rem" }}>This page records first-person memory, spiritual interpretation and artistic metaphor. It does not establish supernatural causation, validate an external Akashic archive, or convert synchronicity into scientific evidence. Dates and public event names are provenance; their arrangement is interpretation.</p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginTop: 22 }}>
          {["Lived Experience / Testimony", "Interpretation", "Artistic Metaphor", "Not Scientific Evidence"].map((label) => <span key={label} style={{ padding: "9px 13px", border: "1px solid rgba(231,205,126,.38)", borderRadius: 999, color: "#f0d681", fontSize: 13, fontWeight: 800 }}>{label}</span>)}
        </div>
      </section>

      <section style={{ width: "min(1100px,calc(100% - 32px))", margin: "0 auto", padding: "0 0 100px" }}>
        <p className="section-label">RELATED PORTALS</p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,220px),1fr))", gap: 16 }}>
          {related.map(([title, text, href]) => (
            <a key={title} href={href} style={{ display: "block", padding: 24, border: "1px solid rgba(159,216,255,.2)", borderRadius: 18, color: "inherit", textDecoration: "none", background: "rgba(10,16,34,.88)" }}>
              <strong style={{ display: "block", color: "#e7cd7e", fontSize: "1.2rem" }}>{title} →</strong>
              <span style={{ display: "block", marginTop: 10, color: "#aeb8c9", lineHeight: 1.55 }}>{text}</span>
            </a>
          ))}
        </div>
      </section>

      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt=""/><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
