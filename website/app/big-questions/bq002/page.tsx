import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BQ002 · Where do thoughts come from? · AKASHICNET.ORG",
  description:
    "An evidence-labelled AkashicNET inquiry into spontaneous thought, creative inspiration, neural processes, contemplative perspectives and transpersonal hypotheses.",
};

const shell: React.CSSProperties = { maxWidth: 1120, margin: "0 auto", padding: "0 22px" };
const panel: React.CSSProperties = {
  border: "1px solid rgba(227,190,87,.24)",
  background: "linear-gradient(145deg, rgba(16,18,31,.90), rgba(8,10,20,.97))",
  borderRadius: 24,
  padding: 24,
  boxShadow: "0 22px 70px rgba(0,0,0,.28)",
};

const lenses = [
  {
    label: "Established Evidence",
    title: "Distributed neural activity",
    text: "Thought is associated with activity distributed across brain systems involved in perception, memory, emotion, prediction and cognitive control.",
    boundary: "Describing neural correlates and mechanisms does not by itself explain why thought is accompanied by subjective experience.",
  },
  {
    label: "Interpretation",
    title: "Unconscious construction",
    text: "A thought may become consciously available only after memory, affect and association have already shaped it.",
    boundary: "The feeling that a thought arrived fully formed does not uniquely identify where it originated.",
  },
  {
    label: "Interpretation",
    title: "Embodied and social cognition",
    text: "Bodies, relationships, language and culture help shape which thoughts become available and meaningful.",
    boundary: "Influence from context is not evidence that thoughts are stored outside individual beings.",
  },
  {
    label: "Contemplative Perspective",
    title: "Mind as a sense",
    text: "Buddhist traditions can treat thoughts as mental objects known by mental consciousness, sometimes described as a sixth sense.",
    boundary: "This does not automatically imply an eternal cosmic archive, and Buddhist traditions should not be collapsed into one metaphysical claim.",
  },
  {
    label: "Hypothesis",
    title: "Transpersonal information",
    text: "Akashic, morphic-resonance, ether and quantum-mind proposals ask whether information or mind extends beyond individual brains.",
    boundary: "These are distinct proposals. None currently establishes a universal memory containing every thought and action.",
  },
];

const pathway = [
  "Thought",
  "Language · image · music · gesture",
  "Another mind",
  "Attention · emotion · memory",
  "Meaning · choice",
  "Action · collective ripples",
];

export default function BQ002Page() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f2e8", background: "radial-gradient(circle at 50% 0%, rgba(91,52,171,.24), transparent 34%), #05060b" }}>
      <header style={{ ...shell, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, paddingTop: 20, paddingBottom: 20 }}>
        <a href="/" style={{ color: "#f5f2e8", textDecoration: "none", fontWeight: 800, letterSpacing: ".12em" }}>AKASHICNET.ORG</a>
        <nav aria-label="Big Question navigation" style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
          <a href="/" style={{ color: "#d9d4c7" }}>Home</a>
          <a href="/big-questions" style={{ color: "#d9d4c7" }}>All Big Questions</a>
          <a href="/big-questions/bq001" style={{ color: "#d9d4c7" }}>BQ001</a>
          <a href="#sources" style={{ color: "#d9d4c7" }}>Sources</a>
        </nav>
      </header>

      <section style={{ ...shell, paddingTop: 72, paddingBottom: 54, textAlign: "center" }}>
        <p style={{ color: "#d8b95c", letterSpacing: ".18em", fontWeight: 800, fontSize: 13 }}>BIG QUESTION 002 · PUBLIC EXPLORATORY INQUIRY</p>
        <h1 style={{ margin: "16px auto", maxWidth: 900, fontSize: "clamp(2.8rem, 8vw, 6.8rem)", lineHeight: .96, letterSpacing: "-.045em" }}>Where do thoughts come from?</h1>
        <p style={{ maxWidth: 780, margin: "26px auto", color: "#c8c4bb", fontSize: "clamp(1.05rem, 2vw, 1.3rem)", lineHeight: 1.7 }}>
          We often notice a thought only after it has appeared. AkashicNET compares neural, psychological, embodied, contemplative and transpersonal accounts without treating mystery as proof.
        </p>
        <div role="status" aria-label="Current conclusion" style={{ display: "inline-flex", alignItems: "center", gap: 10, border: "1px solid rgba(227,190,87,.52)", borderRadius: 999, padding: "10px 18px", background: "rgba(227,190,87,.08)", color: "#f1d47b", fontWeight: 900, letterSpacing: ".12em" }}>CURRENT STATUS · UNRESOLVED · DEEPENING · LEVEL 4/10</div>
      </section>

      <section style={{ ...shell, paddingBottom: 44 }}>
        <div style={panel}>
          <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>THE LIFE OF A COMMUNICATED THOUGHT</p>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center", lineHeight: 1.5 }}>
            {pathway.map((step, index) => (
              <span key={step} style={{ display: "contents" }}>
                <strong style={{ padding: "10px 14px", borderRadius: 999, background: "rgba(116,84,202,.16)", border: "1px solid rgba(159,216,255,.2)" }}>{step}</strong>
                {index < pathway.length - 1 && <span aria-hidden="true" style={{ color: "#d8b95c" }}>→</span>}
              </span>
            ))}
          </div>
          <p style={{ color: "#c8c4bb", lineHeight: 1.7, marginBottom: 0 }}>Once expressed, a private thought becomes a shared signal. Its consequences are co-created by the sender, receiver and context.</p>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 28, paddingBottom: 30 }}>
        <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>FIVE DISTINCT LENSES</p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(290px,1fr))", gap: 18 }}>
          {lenses.map((item) => (
            <article key={item.title} style={panel}>
              <span style={{ color: item.label === "Established Evidence" ? "#a9e4c5" : item.label === "Hypothesis" ? "#f0a6df" : "#cbb7ff", fontSize: 12, fontWeight: 900, letterSpacing: ".1em", textTransform: "uppercase" }}>{item.label}</span>
              <h2 style={{ fontSize: "1.4rem", lineHeight: 1.25 }}>{item.title}</h2>
              <p style={{ color: "#d1cdc4", lineHeight: 1.7 }}>{item.text}</p>
              <p style={{ color: "#f0d681", lineHeight: 1.6 }}><strong>Boundary:</strong> {item.boundary}</p>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 34, paddingBottom: 34 }} aria-labelledby="profile-title">
        <div style={{ ...panel, borderColor: "rgba(159,216,255,.38)" }}>
          <p style={{ color: "#9fd8ff", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>PROVISIONAL EVIDENCE PROFILE</p>
          <h2 id="profile-title" style={{ fontSize: "clamp(1.8rem,4vw,3rem)", lineHeight: 1.15 }}>Unresolved · Deepening · Level 4/10</h2>
          <p style={{ color: "#d1cdc4", lineHeight: 1.75 }}>Level 4 means the inquiry has framed the question, mapped initial sources and separated major explanatory models. It measures completed research work, not truth probability or confidence in transpersonal claims. The neural and psychological construction of thought has substantial empirical support, while the complete origin of thought remains unresolved.</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(230px,1fr))", gap: 12, marginTop: 22 }}>
            {[
              ["⚪", "Overall", "UNRESOLVED", "No complete origin theory is established."],
              ["🩵", "Momentum", "DEEPENING · LEVEL 4/10", "Advances toward Level 5 through a claim-by-claim evidence map with counter-sources and explicit gaps."],
              ["🟢", "Neural mechanisms", "SUBSTANTIAL", "Could deepen within the next quarter to 3 years through time-resolved studies."],
              ["🟠", "Transpersonal models", "SPECULATIVE", "Could move over years or decades only through distinctive, replicated predictions."],
            ].map(([icon, label, value, note]) => (
              <article key={label} style={{ padding: 18, border: "1px solid rgba(255,255,255,.10)", borderRadius: 15, background: "rgba(255,255,255,.025)" }}>
                <span aria-hidden="true" style={{ fontSize: 22 }}>{icon}</span>
                <span style={{ display: "block", marginTop: 8, color: "#a9a59c", fontSize: 11, fontWeight: 900, letterSpacing: ".1em" }}>{label}</span>
                <strong style={{ display: "block", marginTop: 8 }}>{value}</strong>
                <small style={{ display: "block", marginTop: 10, color: "#c8c4bb", lineHeight: 1.6 }}>{note}</small>
              </article>
            ))}
          </div>
          <p style={{ marginBottom: 0, marginTop: 22, color: "#c8c4bb", lineHeight: 1.7 }}><strong>Time horizons:</strong> next quarter—improve definitions and measurement; 1–3 years—compare preregistered models; decade—evaluate whether converging results require a revised theory of mind.</p>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 34, paddingBottom: 34 }}>
        <div style={{ ...panel, borderColor: "rgba(159,216,255,.35)" }}>
          <p style={{ color: "#9fd8ff", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>CREATIVE TESTIMONY · BOB DYLAN</p>
          <h2 style={{ fontSize: "clamp(1.8rem,4vw,3rem)", marginBottom: 18 }}>“All those early songs were almost magically written.”</h2>
          <blockquote style={{ margin: "0 0 18px", color: "#f0d681", fontSize: "1.25rem", lineHeight: 1.6 }}>“I don’t know how I got to write those songs.”</blockquote>
          <p style={{ color: "#d1cdc4", lineHeight: 1.8 }}>Dylan’s account preserves the experience of creativity arriving without a complete conscious explanation. It is artist testimony about phenomenology, not causal proof of a neural, spiritual or Akashic source.</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 14 }}>
            <a href="https://www.cbsnews.com/video/bob-dylan-songs-were-magically-written/" target="_blank" rel="noreferrer" style={{ color: "#9fd8ff" }}>CBS News interview excerpt</a>
            <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1fodkgy/moment_from_bob_dylans_60_minutes_interview_1m16s/" target="_blank" rel="noreferrer" style={{ color: "#9fd8ff" }}>r/NeuronsToNirvana archive</a>
          </div>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 34, paddingBottom: 34 }}>
        <div style={panel}>
          <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>PERSONAL CONCEPTUAL LINEAGE</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(230px,1fr))", gap: 18 }}>
            <article><strong style={{ color: "#f0d681" }}>2022 · MEL idea</strong><p style={{ color: "#d1cdc4", lineHeight: 1.7 }}>An early Matrix Enlightenment Library concept linking knowledge, awareness and collective memory.</p></article>
            <article><strong style={{ color: "#f0d681" }}>Easter 2024 · NDE-like vision</strong><p style={{ color: "#d1cdc4", lineHeight: 1.7 }}>A personal visionary experience during emergency surgery, later interpreted through Akashic imagery.</p></article>
            <article><strong style={{ color: "#f0d681" }}>2026 · AkashicNET inquiry</strong><p style={{ color: "#d1cdc4", lineHeight: 1.7 }}>The lineage becomes an evidence-labelled question about thought, memory and consciousness.</p></article>
          </div>
          <p style={{ marginBottom: 0, color: "#c8c4bb", lineHeight: 1.7 }}><strong>Provenance boundary:</strong> Personal conceptual development and lived experience do not scientifically confirm an Akashic Library.</p>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 34, paddingBottom: 34 }}>
        <div style={{ ...panel, borderColor: "rgba(227,190,87,.42)" }}>
          <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>METHOD</p>
          <ol style={{ color: "#d1cdc4", lineHeight: 1.9, paddingLeft: 24 }}>
            <li>Identify the thought and record its context and felt state.</li>
            <li>Trace plausible memories, associations, emotions and environmental cues.</li>
            <li>Compare neural, psychological and contemplative accounts without collapsing them.</li>
            <li>Classify each claim as evidence, interpretation, testimony, hypothesis or speculation.</li>
            <li>Observe immediate and delayed effects after the thought is communicated.</li>
            <li>Separate correlation, plausible influence and demonstrated causation.</li>
          </ol>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 30, paddingBottom: 64 }}>
        <div style={{ ...panel, textAlign: "center", padding: "clamp(28px,6vw,58px)" }}>
          <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".15em", fontSize: 13 }}>CURRENT CONCLUSION · UNRESOLVED</p>
          <h2 style={{ fontSize: "clamp(1.8rem,4vw,3.3rem)", lineHeight: 1.15 }}>The experience of a thought arriving is real. Its complete origin remains open.</h2>
          <p style={{ maxWidth: 820, margin: "20px auto 0", color: "#d1cdc4", lineHeight: 1.8 }}>Neural and psychological models offer evidence-based mechanisms. Contemplative traditions offer disciplined phenomenological perspectives. Transpersonal proposals remain hypotheses or speculation unless independently supported.</p>
          <p style={{ marginTop: 28, fontWeight: 900 }}>Fund the question, not the answer.</p>
        </div>
      </section>

      <section id="sources" style={{ ...shell, paddingBottom: 72 }}>
        <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>PRIMARY COMMUNITY PROVENANCE</p>
        <p><a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1wanq3d/a_thought_just_popped_in_and_out_of_my_head_how/" target="_blank" rel="noreferrer" style={{ color: "#9fd8ff" }}>A Thought Just Popped In and Out of My Head</a></p>
        <p><a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1qq3m4b/an_observation_about_a_thought_i_keep_coming_back/" target="_blank" rel="noreferrer" style={{ color: "#9fd8ff" }}>An Observation About a Thought I Keep Coming Back To</a></p>
        <p style={{ color: "#c8c4bb" }}>BQ002 · Public exploratory inquiry v0.2 · No truth promotion authorised</p>
      </section>

      <footer style={{ borderTop: "1px solid rgba(255,255,255,.08)", padding: "30px 22px", textAlign: "center", color: "#9f9c95" }}>AKASHICNET.ORG · Open Heart · Open Mind · Open Knowledge · Awaken within · Serve without ♾️</footer>
    </main>
  );
}
