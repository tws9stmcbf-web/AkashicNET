import type { Metadata } from "next";
import type { CSSProperties } from "react";

export const metadata: Metadata = {
  title: "A Thought Stream: Could Consciousness Inquiry Become Plug-and-Play? — AkashicNET",
  description: "A live conceptual exploration of AkashicNET, AkashicOMNI and AkashicPRISM as a modular inquiry architecture for awareness, consciousness and sentience.",
};

const shell: CSSProperties = { width: "min(100% - 40px, 1120px)", margin: "0 auto" };
const label: CSSProperties = { color: "#efc96f", fontSize: 13, fontWeight: 800, letterSpacing: ".15em", textTransform: "uppercase" };
const prose: CSSProperties = { maxWidth: 780, color: "#d2d0c8", fontSize: "clamp(1.05rem,1.7vw,1.22rem)", lineHeight: 1.85 };
const prismCheck: CSSProperties = { margin: "30px 0 0", padding: "20px 22px", borderLeft: "3px solid #c2a8ff", background: "linear-gradient(90deg,rgba(194,168,255,.10),rgba(139,230,199,.025))", color: "#c9c5d4", lineHeight: 1.75 };

const modules = [
  ["Waking awareness", "Attention, access, report and the felt presence of experience."],
  ["Dream and liminal states", "Dreaming, lucid dreaming, hypnagogia and hypnopompia."],
  ["Contemplative practice", "Meditation, absorption, non-dual reports and ethical transformation."],
  ["Altered states", "Psychedelic, trance and ritual experience, with physiology, context and meaning separated."],
  ["Boundary experiences", "NDEs, reported OBEs and continuity-of-awareness questions."],
  ["More-than-human sentience", "Animal experience, plant or ecological intelligence claims and welfare consequences."],
  ["Artificial systems", "Machine behaviour, self-report, embodiment and competing criteria for possible consciousness."],
  ["Metaphysical models", "Physicalism, idealism, panpsychism, dual-aspect approaches and positions not yet imagined."],
] as const;

const terms = [
  ["Awareness", "What is present, noticed or accessible within an experience?"],
  ["Consciousness", "What makes subjective experience possible, and how should it be explained?"],
  ["Sentience", "Can a being have felt states, especially pleasure, pain or welfare-relevant experience?"],
] as const;

export default function Page() {
  return (
    <main style={{ minHeight: "100vh", color: "#f4f0e4", background: "radial-gradient(circle at 75% 8%,rgba(123,93,184,.24),transparent 30rem),radial-gradient(circle at 12% 36%,rgba(69,178,147,.13),transparent 28rem),#050b0d" }}>
      <header style={{ ...shell, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 20, paddingTop: 22, paddingBottom: 22, borderBottom: "1px solid rgba(255,255,255,.12)" }}>
        <a href="/" style={{ color: "#f4f0e4", textDecoration: "none", fontWeight: 900, letterSpacing: ".13em" }}>AKASHICNET.ORG</a>
        <nav aria-label="Article navigation" style={{ display: "flex", flexWrap: "wrap", gap: 18 }}>
          <a href="/akashicomni" style={{ color: "#cbc7d5" }}>AkashicOMNI</a>
          <a href="/faq" style={{ color: "#cbc7d5" }}>FAQ</a>
          <a href="/" style={{ color: "#cbc7d5" }}>Home</a>
        </nav>
      </header>

      <article>
        <header style={{ ...shell, paddingTop: "clamp(70px,10vw,130px)", paddingBottom: "clamp(60px,9vw,110px)" }}>
          <p style={label}>AKASHICPRISM THOUGHT STREAM · CONCEPTUAL EXPLORATION</p>
          <h1 style={{ maxWidth: 1050, margin: "22px 0 30px", font: "400 clamp(3.5rem,8vw,8rem)/.92 Georgia,serif", letterSpacing: "-.055em" }}>Could consciousness inquiry become <em style={{ color: "#8be6c7", fontWeight: 400 }}>plug-and-play?</em></h1>
          <p style={{ ...prose, fontSize: "clamp(1.15rem,2vw,1.45rem)" }}>Not consciousness manufactured from interchangeable parts. Not a machine that announces which beings possess an inner life. Something humbler and perhaps more useful: a shared architecture into which competing theories, lived experiences, scientific studies and cultural knowledge can enter without losing their differences.</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 12, marginTop: 30 }}>
            <span style={{ padding: "8px 12px", border: "1px solid rgba(139,230,199,.35)", borderRadius: 999, color: "#8be6c7", fontSize: 13 }}>Interpretation</span>
            <span style={{ padding: "8px 12px", border: "1px solid rgba(194,168,255,.38)", borderRadius: 999, color: "#c2a8ff", fontSize: 13 }}>Conceptual model</span>
            <span style={{ padding: "8px 12px", border: "1px solid rgba(239,201,111,.36)", borderRadius: 999, color: "#efc96f", fontSize: 13 }}>Open question</span>
          </div>
        </header>

        <section style={{ borderTop: "1px solid rgba(255,255,255,.11)", borderBottom: "1px solid rgba(255,255,255,.11)", background: "rgba(255,255,255,.025)" }}>
          <div style={{ ...shell, paddingTop: "clamp(55px,8vw,90px)", paddingBottom: "clamp(55px,8vw,90px)" }}>
            <p style={label}>THE FIRST SPARK</p>
            <div style={{ maxWidth: 900, marginTop: 22, font: "400 clamp(1.8rem,3.5vw,3.4rem)/1.35 Georgia,serif", color: "#ece7da" }}>
              <p>What if a dream, an fMRI result, an animal-welfare study, a meditation report, an AI self-description and an Indigenous teaching could enter the same inquiry—without being declared equivalent?</p>
              <p>What if the system could hold several explanations at once, remember why each was proposed, and change its classification when better knowledge arrived?</p>
              <p>What if “unexplained” meant <em style={{ color: "#efc96f" }}>continue carefully</em>, rather than believe immediately or discard automatically?</p>
            </div>
            <aside style={prismCheck}><strong style={{ color: "#c2a8ff" }}>PRISM check:</strong> These are design questions. Their imaginative force is not evidence that consciousness is nonlocal, universal, computational or reducible to matter.</aside>
          </div>
        </section>

        <section style={{ ...shell, paddingTop: "clamp(65px,9vw,110px)", paddingBottom: "clamp(65px,9vw,110px)" }}>
          <p style={label}>THREE NAMES THAT MUST NOT COLLAPSE</p>
          <h2 style={{ maxWidth: 850, margin: "18px 0 38px", font: "400 clamp(2.6rem,5.5vw,5.5rem)/.98 Georgia,serif", letterSpacing: "-.04em" }}>Related questions.<br/>Different consequences.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 16 }}>
            {terms.map(([name,text],index) => <article key={name} style={{ minHeight: 230, padding: 24, border: "1px solid rgba(255,255,255,.13)", background: "linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012))" }}><span style={{ color: "#efc96f", fontSize: 13 }}>0{index + 1}</span><h3 style={{ margin: "42px 0 12px", font: "400 2rem Georgia,serif" }}>{name}</h3><p style={{ color: "#bdbab3", lineHeight: 1.7 }}>{text}</p></article>)}
          </div>
          <p style={{ ...prose, marginTop: 34 }}>A system may display attention-like behaviour without felt experience. A being may be sentient without reflective self-awareness. A contemplative report may describe awareness without explaining its physical or metaphysical basis. PRISM keeps these questions connected but separately accountable.</p>
        </section>

        <section style={{ paddingTop: "clamp(65px,9vw,110px)", paddingBottom: "clamp(65px,9vw,110px)", borderBlock: "1px solid rgba(255,255,255,.11)", background: "linear-gradient(140deg,#0a111c,#081512)" }}>
          <div style={shell}>
            <p style={label}>THE ARCHITECTURE EMERGES</p>
            <h2 style={{ maxWidth: 920, margin: "18px 0 45px", font: "400 clamp(2.6rem,5.5vw,5.5rem)/.98 Georgia,serif", letterSpacing: "-.04em" }}>OMNI examines.<br/>PRISM discriminates.<br/>NET remembers.</h2>
            <div style={{ display: "grid", gap: 1, background: "rgba(255,255,255,.13)", border: "1px solid rgba(255,255,255,.13)" }}>
              {[
                ["01 · INPUT", "A source, experience, observation, tradition, theory or question enters with attribution and boundaries."],
                ["02 · AKASHICOMNI", "The relevant frameworks examine awareness, symbols, embodiment, change, causes, time, systems and culture."],
                ["03 · AKASHICPRISM", "Interpretations, evidence lanes, competing explanations, connection strengths and uncertainties are separated."],
                ["04 · AKASHICNET", "Stable records, provenance, graph relationships, investigation states and revision history are preserved."],
                ["05 · RETURN", "New evidence re-enters the cycle. Earlier assessments remain visible rather than silently disappearing."],
              ].map(([name,text]) => <article key={name} style={{ display: "grid", gridTemplateColumns: "minmax(150px,.35fr) minmax(0,1fr)", gap: 24, padding: 24, background: "#091112" }}><strong style={{ color: "#8be6c7", letterSpacing: ".08em" }}>{name}</strong><span style={{ color: "#c8c5be", lineHeight: 1.7 }}>{text}</span></article>)}
            </div>
            <aside style={prismCheck}><strong style={{ color: "#c2a8ff" }}>Boundary:</strong> “Plug-and-play” describes modular inquiry and data compatibility. It is not a claim that sentience can be installed, that consciousness is software, or that subjective experience has been reduced to an engineering interface.</aside>
          </div>
        </section>

        <section style={{ ...shell, paddingTop: "clamp(65px,9vw,110px)", paddingBottom: "clamp(65px,9vw,110px)" }}>
          <p style={label}>POSSIBLE MODULES</p>
          <h2 style={{ maxWidth: 900, margin: "18px 0 42px", font: "400 clamp(2.6rem,5.5vw,5.5rem)/.98 Georgia,serif", letterSpacing: "-.04em" }}>Many doors into one unresolved mystery.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))", borderTop: "1px solid rgba(255,255,255,.13)", borderLeft: "1px solid rgba(255,255,255,.13)" }}>
            {modules.map(([name,text]) => <article key={name} style={{ minHeight: 210, padding: 24, borderRight: "1px solid rgba(255,255,255,.13)", borderBottom: "1px solid rgba(255,255,255,.13)" }}><h3 style={{ color: "#efc96f", font: "400 1.55rem/1.15 Georgia,serif" }}>{name}</h3><p style={{ color: "#bdbab3", lineHeight: 1.7 }}>{text}</p></article>)}
          </div>
        </section>

        <section style={{ borderBlock: "1px solid rgba(255,255,255,.11)", background: "rgba(255,255,255,.025)" }}>
          <div style={{ ...shell, paddingTop: "clamp(65px,9vw,110px)", paddingBottom: "clamp(65px,9vw,110px)" }}>
            <p style={label}>THE HARDER THOUGHT</p>
            <h2 style={{ maxWidth: 880, margin: "18px 0 30px", font: "400 clamp(2.6rem,5.5vw,5.5rem)/.98 Georgia,serif", letterSpacing: "-.04em" }}>Every module changes the ethical field.</h2>
            <div style={prose}>
              <p>If an animal might be sentient, uncertainty affects welfare. If an AI might someday be conscious, uncertainty affects design and treatment—but present fluency is not proof. If a plant-intelligence claim changes ecological behaviour, practical value does not automatically establish plant phenomenology. If sacred knowledge is culturally restricted, curiosity does not create permission.</p>
              <p>PRISM therefore needs more than a confidence score. It needs privacy, rights, cultural authority, non-equivalence, welfare relevance and the ability to say: this question matters, but this material must not be exposed or promoted.</p>
            </div>
          </div>
        </section>

        <section style={{ ...shell, paddingTop: "clamp(65px,9vw,110px)", paddingBottom: "clamp(65px,9vw,110px)" }}>
          <p style={label}>WHAT WOULD MAKE IT MORE THAN A BEAUTIFUL METAPHOR?</p>
          <h2 style={{ maxWidth: 900, margin: "18px 0 36px", font: "400 clamp(2.6rem,5.5vw,5.5rem)/.98 Georgia,serif", letterSpacing: "-.04em" }}>Definitions. Predictions. Alternatives. Consequences.</h2>
          <ol style={{ maxWidth: 800, paddingLeft: 24, color: "#d2d0c8", fontSize: "1.08rem", lineHeight: 1.85 }}>
            <li>Define awareness, consciousness or sentience for the module rather than moving between them unnoticed.</li>
            <li>Name the subject class and the limits of comparison.</li>
            <li>Identify observations that the model predicts.</li>
            <li>Record ordinary and competing explanations.</li>
            <li>State what findings would weaken or contradict the claim.</li>
            <li>Separate first-person meaning from claims about external reality.</li>
            <li>Track source independence instead of counting repetition as corroboration.</li>
            <li>Preserve every classification change with its evidence and uncertainty.</li>
          </ol>
          <aside style={prismCheck}><strong style={{ color: "#c2a8ff" }}>Current status:</strong> AkashicPRISM is a developing pre-alpha inquiry architecture. AkashicOMNI v0.5.0 is proposed and unreleased. No current AI-consciousness, universal-consciousness or survival-after-death conclusion is asserted.</aside>
        </section>

        <section style={{ paddingTop: "clamp(65px,9vw,110px)", paddingBottom: "clamp(65px,9vw,110px)", background: "linear-gradient(135deg,#e8e1d2,#dbe8e0)", color: "#10201d" }}>
          <div style={shell}>
            <p style={{ ...label, color: "#7c5b25" }}>THE STREAM REMAINS OPEN</p>
            <blockquote style={{ maxWidth: 980, margin: "24px 0 30px", font: "400 clamp(2.4rem,5vw,5rem)/1.05 Georgia,serif", letterSpacing: "-.04em" }}>Perhaps the first task is not to solve consciousness. Perhaps it is to build a place where humanity can disagree about it without losing the evidence, the experience, the cultures—or the question.</blockquote>
            <p style={{ maxWidth: 760, color: "#40524c", fontSize: "1.05rem", lineHeight: 1.8 }}>This article records a developing thought process, not a final doctrine. Specific criticism is welcome. Identify the claim, interpretation or missing framework and explain what evidence or perspective could improve it.</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 18, marginTop: 28 }}>
              <a href="/faq" style={{ display: "inline-block", padding: "14px 20px", background: "#10201d", color: "#f4f0e4", fontWeight: 800, textDecoration: "none" }}>Read the FAQ →</a>
              <a href="mailto:support@akashicnet.org?subject=AkashicPRISM%20thought-stream%20feedback" style={{ padding: "14px 0", color: "#1e6657", fontWeight: 800 }}>Send constructive feedback</a>
            </div>
          </div>
        </section>

        <aside style={{ ...shell, display: "flex", flexWrap: "wrap", justifyContent: "space-between", gap: 12, paddingTop: 24, paddingBottom: 24, color: "#969890", fontSize: 13 }}>
          <span>Published as a developing conceptual article · 22 September 2026</span>
          <span>Evidence status: interpretation · conceptual model · open question</span>
        </aside>
      </article>

      <footer style={{ borderTop: "1px solid rgba(255,255,255,.10)", padding: "32px 20px", textAlign: "center", color: "#969890" }}>AKASHICNET.ORG · Keep the wonder · Follow the evidence · Serve life</footer>
    </main>
  );
}
