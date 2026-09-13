import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "The Power of the Doctor · HOMESENSE VR — AKASHICNET.ORG",
  description:
    "A Spiritual Sci-Fi exploration of regeneration, resurrection, reincarnation and continuity through the speculative HOMESENSE VR concept.",
};

const shell = { width: "min(1160px, calc(100% - 32px))", margin: "0 auto" };
const panel = {
  border: "1px solid rgba(216,185,92,.24)",
  borderRadius: 24,
  background: "linear-gradient(145deg, rgba(19,25,47,.94), rgba(8,12,28,.96))",
  boxShadow: "0 24px 80px rgba(0,0,0,.28)",
};

const models = [
  {
    title: "Regeneration",
    source: "Doctor Who",
    continuity: "One continuing being changes body and personality while retaining an accumulated history.",
    question: "How much can change before identity becomes someone new?",
  },
  {
    title: "Resurrection",
    source: "Battlestar Galactica",
    continuity: "A Cylon identity-pattern is transferred into another prepared biological body.",
    question: "Is the awakened being the original consciousness, a continuation or a copy?",
  },
  {
    title: "Reincarnation",
    source: "Religious and philosophical traditions",
    continuity: "Different traditions propose karmic, mental or spiritual continuity across lives, often without ordinary autobiographical recall.",
    question: "What, if anything, must persist for rebirth to count as continuity?",
  },
];

const chambers = [
  ["01 · The Edge", "Encounter former versions of the self as guides. Integrate what they remember without treating them as separate, proven souls."],
  ["02 · The Resurrection Tank", "Reconstruct an identity from fragmented memories. A perfect reconstruction still leaves the player asking whether copying equals survival."],
  ["03 · The Reincarnation Field", "Follow recurring symbols and dispositions across imagined lives. The game never declares whether they are memory, karma, archetype or coincidence."],
];

export default function PowerOfTheDoctorPage() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f0e7", background: "radial-gradient(circle at 50% 15%, #182c59 0, #0a1026 34%, #050711 76%)" }}>
      <header className="nav-shell">
        <a className="wordmark" href="/" aria-label="AkashicNET.org home">
          <img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" />
          <span className="brand-name">AKASHICNET.ORG</span>
        </a>
        <nav aria-label="Page navigation">
          <a href="/spiritual-sci-fi">Spiritual Sci-Fi</a>
          <a href="#continuity">Three models</a>
          <a href="#experience">VR concept</a>
          <a href="/big-questions/bq001">BQ001</a>
        </nav>
      </header>

      <section style={{ ...shell, padding: "clamp(72px,10vw,130px) 0 54px", textAlign: "center" }}>
        <p className="section-label">SPIRITUAL SCI-FI · CULTURAL INTERPRETATION · FUTURE / EXPLORATORY</p>
        <h1 style={{ margin: "20px auto", maxWidth: 980, fontSize: "clamp(3rem,8vw,7.4rem)", lineHeight: .92 }}>
          The Power<br /><em style={{ color: "#d8b95c" }}>of the Doctor</em>
        </h1>
        <p style={{ maxWidth: 800, margin: "28px auto 0", fontSize: "clamp(1.1rem,2.2vw,1.45rem)", lineHeight: 1.75, color: "#d7d9e4" }}>
          What science fiction can teach us about continuity when a body, personality or world changes.
          A bridge from regeneration and resurrection to reincarnation, meta-awareness and mettā-awareness.
        </p>
        <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap", gap: 12, marginTop: 30 }}>
          {["MICRO", "META", "METTĀ", "MACRO"].map((word) => (
            <span key={word} style={{ border: "1px solid rgba(216,185,92,.38)", borderRadius: 99, padding: "9px 16px", color: "#e6ce85", letterSpacing: ".12em", fontWeight: 800 }}>{word}</span>
          ))}
        </div>
      </section>

      <section style={{ ...shell, ...panel, overflow: "hidden", padding: 0 }}>
        <img
          src="/images/homesense-vr-power-of-the-doctor-storyboard.png"
          alt="Six-panel HOMESENSE VR concept storyboard: a traveller enters a small blue portal, puts on a headset inside a spherical chamber, sees sound create cymatic forms, explores a 360-degree neural and cosmic environment, aligns symbols, and returns through a warm doorway marked Home."
          style={{ display: "block", width: "100%", height: "auto" }}
        />
        <p style={{ margin: 0, padding: "18px 22px", color: "#b9bfd0", lineHeight: 1.65 }}>
          <strong style={{ color: "#f3dc96" }}>AkashicNET concept artwork.</strong> A speculative storyboard, not a functioning VR product and not scientific evidence that quantum phenomena, dark matter or post-mortem consciousness can be perceived directly.
        </p>
      </section>

      <section style={{ ...shell, padding: "84px 0 24px" }}>
        <p className="section-label">THE SCENE YOU REMEMBER</p>
        <div style={{ ...panel, padding: "clamp(24px,5vw,52px)", marginTop: 18 }}>
          <h2 style={{ fontSize: "clamp(2rem,5vw,4rem)", marginTop: 0 }}>The Guardians of the Edge</h2>
          <p style={{ color: "#d7d9e4", lineHeight: 1.85, fontSize: "1.08rem" }}>
            In Jodie Whittaker&apos;s final special, <em>The Power of the Doctor</em> (2022), the Master forces the Thirteenth Doctor into regeneration. Within a liminal mental landscape called the Edge, manifestations of earlier Doctors appear as Guardians of the Edge. They represent previous incarnations remaining present within a continuing identity. The Doctor&apos;s actual final regeneration occurs later in the story.
          </p>
          <p style={{ color: "#d7d9e4", lineHeight: 1.85 }}>
            This resembles reincarnation symbolically, but it is not the same claim. <em>Doctor Who</em> presents fictional biological regeneration with unusually strong continuity of memory. The Edge becomes useful here as a cultural thought experiment: <strong>can former selves remain accessible without being separate selves?</strong>
          </p>
          <p style={{ marginBottom: 0 }}>
            <a href="https://www.youtube.com/watch?v=0SuDVcTv25g">Watch the official “Guardians of the Edge” clip ↗</a>
          </p>
        </div>
      </section>

      <section id="continuity" style={{ ...shell, padding: "70px 0 30px" }}>
        <p className="section-label">THREE FICTIONAL AND PHILOSOPHICAL LENSES</p>
        <h2 style={{ maxWidth: 840, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.05 }}>Three ways to ask what continues.</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 18, marginTop: 34 }}>
          {models.map((model) => (
            <article key={model.title} style={{ ...panel, padding: 26 }}>
              <span style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".1em" }}>{model.source}</span>
              <h3 style={{ fontSize: "1.7rem", marginBottom: 12 }}>{model.title}</h3>
              <p style={{ color: "#cbd0dd", lineHeight: 1.7 }}>{model.continuity}</p>
              <p style={{ borderTop: "1px solid rgba(216,185,92,.2)", paddingTop: 16, lineHeight: 1.65 }}><strong>Identity puzzle:</strong> {model.question}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="experience" style={{ ...shell, padding: "86px 0 30px" }}>
        <p className="section-label">HOMESENSE VR · PLACEHOLDER CONCEPT</p>
        <h2 style={{ maxWidth: 900, fontSize: "clamp(2.2rem,5vw,4.6rem)", lineHeight: 1.04 }}>
          A confined chamber.<br />An infinite perceptual interior.
        </h2>
        <p style={{ maxWidth: 820, color: "#d7d9e4", fontSize: "1.08rem", lineHeight: 1.85 }}>
          The player enters a TARDIS-like spherical room filled with 360° imagery and spatial sound. Resonant tones produce visible cymatic patterns. Solving puzzles changes scale from quantum possibility to embodied experience to the largely unobserved cosmos. The altered states are simulated through audiovisual design; no substance use is required or depicted.
        </p>
        <div style={{ display: "grid", gap: 16, marginTop: 34 }}>
          {chambers.map(([title, text]) => (
            <article key={title} style={{ ...panel, padding: "24px clamp(22px,4vw,42px)", display: "grid", gridTemplateColumns: "minmax(180px, .5fr) 1.5fr", gap: 24, alignItems: "start" }}>
              <h3 style={{ margin: 0, color: "#e7cd7e" }}>{title}</h3>
              <p style={{ margin: 0, color: "#cbd0dd", lineHeight: 1.75 }}>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...shell, padding: "86px 0" }}>
        <div style={{ ...panel, padding: "clamp(28px,6vw,64px)", textAlign: "center", background: "radial-gradient(circle at 50% 0, rgba(116,75,185,.3), rgba(10,14,32,.96) 58%)" }}>
          <p className="section-label">THE BIGGER AND SMALLER PICTURE</p>
          <h2 style={{ fontSize: "clamp(2rem,5vw,4rem)" }}>What can we observe, infer, imagine and HOMESENSE?</h2>
          <p style={{ maxWidth: 850, margin: "0 auto", color: "#d7d9e4", lineHeight: 1.85 }}>
            Human senses and instruments reveal only limited ranges and scales. Science extends observation through measurement; philosophy tests concepts; contemplative practice examines experience; art and science fiction let us rehearse possibilities. None should silently replace the others.
          </p>
          <blockquote style={{ margin: "34px auto 0", maxWidth: 790, color: "#f2d98e", fontSize: "clamp(1.35rem,3vw,2.2rem)", lineHeight: 1.45 }}>
            “Meta-awareness recognises the lens. Mettā-awareness cares for every being seen through it.”
          </blockquote>
        </div>
      </section>

      <section style={{ ...shell, paddingBottom: 86 }}>
        <div style={{ borderLeft: "4px solid #d8b95c", padding: "8px 0 8px 24px", maxWidth: 920 }}>
          <p className="section-label">EVIDENCE BOUNDARY</p>
          <p style={{ color: "#cbd0dd", lineHeight: 1.8 }}>
            <strong>Interpretation:</strong> the comparison among regeneration, resurrection and reincarnation is a cultural and philosophical analysis. <strong>Speculation:</strong> HOMESENSE VR is a future creative concept. It does not establish survival after death, direct perception of dark matter, quantum consciousness or any franchise&apos;s fictional mechanism as physically possible.
          </p>
          <p style={{ color: "#f0d98f", fontWeight: 800 }}>BQ001 remains UNRESOLVED. Fund the question, not the answer.</p>
          <a href="/big-questions/bq001">Explore BQ001: Does consciousness continue beyond the individual? →</a>
        </div>
      </section>

      <footer>
        <div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" /><p className="brand-name">AKASHICNET.ORG</p></div>
        <p>Spiritual Sci-Fi · Wonder with discernment</p>
        <p>Awaken within · Serve without · 2026</p>
      </footer>
    </main>
  );
}
