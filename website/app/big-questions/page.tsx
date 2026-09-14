import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Big Questions · Evidence Profiles · AKASHICNET.ORG",
  description: "A colour-coded index of AkashicNET Big Questions, their provisional evidence profiles and potential review horizons.",
};

const questions = [
  {
    id: "BQ001",
    title: "Does consciousness continue beyond the individual?",
    href: "/big-questions/bq001",
    status: "UNRESOLVED · DEEPENING ↗",
    colour: "🩵",
    evidence: "🟠 LIMITED · MIXED",
    direction: "⚪ NOT YET DETERMINED",
    quarter: "Launch reporting-suppression study; preregister prospective protocols; expand source audit.",
    year: "Begin blinded case matching, cultural-comparison and mettā-integration studies.",
    decade: "Assess multicentre replication and whether evidence converges on, revises or weakens a defined continuity model.",
    maturity: "Canonical synthesis · v0.1.1 · page expanded Sep 2026",
  },
  {
    id: "BQ002",
    title: "Where do thoughts come from?",
    href: "/big-questions/bq002",
    status: "UNRESOLVED · DEEPENING ↗",
    colour: "🩵",
    evidence: "🟢 SUBSTANTIAL FOR NEURAL MECHANISMS",
    direction: "🟠 TRANSPERSONAL CLAIMS SPECULATIVE",
    quarter: "Clarify definitions and identify measurable predictions that distinguish competing accounts.",
    year: "Compare preregistered neural, psychological, embodied and phenomenological models.",
    decade: "Evaluate whether converging results can explain thought generation or require a revised theory of mind.",
    maturity: "Public exploratory inquiry · v0.2",
  },
];

const shell: React.CSSProperties = { maxWidth: 1180, margin: "0 auto", padding: "0 22px" };
const panel: React.CSSProperties = {
  border: "1px solid rgba(159,216,255,.26)",
  background: "linear-gradient(145deg, rgba(16,18,31,.92), rgba(8,10,20,.98))",
  borderRadius: 24,
  padding: 24,
  boxShadow: "0 22px 70px rgba(0,0,0,.28)",
};

export default function BigQuestionsPage() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f2e8", background: "radial-gradient(circle at 50% 0%, rgba(75,48,145,.25), transparent 35%), #05060b" }}>
      <header style={{ ...shell, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, paddingTop: 20, paddingBottom: 20 }}>
        <a href="/" style={{ color: "#f5f2e8", textDecoration: "none", fontWeight: 800, letterSpacing: ".12em" }}>AKASHICNET.ORG</a>
        <nav aria-label="Big Questions navigation" style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
          <a href="/" style={{ color: "#d9d4c7" }}>Home</a>
          <a href="/akashicomni" style={{ color: "#d9d4c7" }}>AkashicOMNI</a>
        </nav>
      </header>

      <section style={{ ...shell, paddingTop: 72, paddingBottom: 48, textAlign: "center" }}>
        <p style={{ color: "#d8b95c", letterSpacing: ".18em", fontWeight: 900, fontSize: 13 }}>THE BIG QUESTIONS · PROVISIONAL EVIDENCE MAP</p>
        <h1 style={{ margin: "16px auto", maxWidth: 980, fontSize: "clamp(3rem,8vw,7rem)", lineHeight: .94, letterSpacing: "-.045em" }}>Questions large enough to remain open.</h1>
        <p style={{ maxWidth: 820, margin: "26px auto", color: "#c8c4bb", fontSize: "clamp(1.05rem,2vw,1.3rem)", lineHeight: 1.75 }}>Every question receives a colour-coded profile, a stated boundary and a review horizon. Ratings describe the present evidence—not belief, importance or final truth.</p>
      </section>

      <section style={{ ...shell, paddingBottom: 36 }} aria-labelledby="key-title">
        <div style={panel}>
          <h2 id="key-title" style={{ marginTop: 0 }}>One shared colour language</h2>
          <p style={{ color: "#c8c4bb", lineHeight: 1.9, marginBottom: 0 }}><strong>🔴 Caution or weak support</strong> · <strong>🟠 Limited, emerging or speculative</strong> · <strong>⚪ Unresolved or undetermined</strong> · <strong>🩵 Deepening inquiry</strong> · <strong>🟢 Substantial within the named axis</strong> · <strong>💜 Philosophical or interpretive potential</strong></p>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 26, paddingBottom: 42 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,430px),1fr))", gap: 20 }}>
          {questions.map((question) => (
            <article key={question.id} style={panel}>
              <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>{question.id} · {question.maturity}</p>
              <h2 style={{ fontSize: "clamp(1.8rem,3.5vw,3rem)", lineHeight: 1.12 }}>{question.title}</h2>
              <div role="status" style={{ display: "inline-flex", gap: 8, padding: "9px 14px", borderRadius: 999, background: "rgba(159,216,255,.08)", border: "1px solid rgba(159,216,255,.28)", fontWeight: 900 }}>{question.colour} {question.status}</div>
              <p style={{ color: "#d1cdc4", lineHeight: 1.7 }}><strong>Evidence:</strong> {question.evidence}<br/><strong>Direction:</strong> {question.direction}</p>
              <div style={{ marginTop: 22, display: "grid", gap: 10 }}>
                <div style={{ padding: 15, borderRadius: 14, background: "rgba(255,255,255,.03)" }}><strong style={{ color: "#9fd8ff" }}>NEXT QUARTER</strong><p style={{ color: "#c8c4bb", lineHeight: 1.6, marginBottom: 0 }}>{question.quarter}</p></div>
                <div style={{ padding: 15, borderRadius: 14, background: "rgba(255,255,255,.03)" }}><strong style={{ color: "#a9e4c5" }}>NEXT 1–3 YEARS</strong><p style={{ color: "#c8c4bb", lineHeight: 1.6, marginBottom: 0 }}>{question.year}</p></div>
                <div style={{ padding: 15, borderRadius: 14, background: "rgba(255,255,255,.03)" }}><strong style={{ color: "#cbb7ff" }}>NEXT DECADE</strong><p style={{ color: "#c8c4bb", lineHeight: 1.6, marginBottom: 0 }}>{question.decade}</p></div>
              </div>
              <a href={question.href} style={{ display: "inline-block", marginTop: 24, color: "#f1d47b", fontWeight: 900 }}>Open the full evidence profile →</a>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...shell, paddingBottom: 66 }}>
        <div style={{ ...panel, borderColor: "rgba(216,185,92,.38)", textAlign: "center" }}>
          <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>HOW RATINGS CHANGE</p>
          <h2 style={{ fontSize: "clamp(1.8rem,4vw,3.2rem)" }}>Scheduled review—not scheduled belief.</h2>
          <p style={{ maxWidth: 850, margin: "0 auto", color: "#d1cdc4", lineHeight: 1.8 }}>A rating changes only when new evidence, stronger methods, independent replication or meaningful counter-evidence changes a named axis. Time alone never upgrades a claim. Some questions may deepen for decades while remaining unresolved.</p>
          <p style={{ color: "#c8c4bb", lineHeight: 1.8 }}><strong>Typical pathway:</strong> ⚪ Unresolved → 🩵 Deepening → 🟠 Signal detected → 🟢 Converging evidence → 💜 Provisional support for a clearly defined model</p>
        </div>
      </section>

      <footer style={{ borderTop: "1px solid rgba(255,255,255,.08)", padding: "30px 22px", textAlign: "center", color: "#9f9c95" }}>AKASHICNET.ORG · Fund the question—not the answer.</footer>
    </main>
  );
}
