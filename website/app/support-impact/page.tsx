import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Support & Impact · AKASHICNET.ORG",
  description: "See what AkashicNET has built, how it is governed, what comes next and how independent support can help.",
};

const shell: React.CSSProperties = { maxWidth: 1120, margin: "0 auto", padding: "0 22px" };
const panel: React.CSSProperties = {
  border: "1px solid rgba(227,190,87,.25)",
  borderRadius: 22,
  background: "linear-gradient(145deg,rgba(17,20,35,.92),rgba(7,9,18,.98))",
  padding: 24,
};

const journey = [
  ["01", "Why it matters", "Knowledge systems should preserve evidence, uncertainty, dignity and many ways of knowing."],
  ["02", "What exists now", "A public portal, living Evidence Commons, Big Questions, AkashicOMNI and provenance-led development infrastructure."],
  ["03", "How it is governed", "Privacy boundaries, evidence labels, human accountability and explicit no-promotion safeguards."],
  ["04", "What comes next", "A clearer public library, richer evidence maps, safer exploration tools and research partnerships."],
  ["05", "What support enables", "Protected development time, infrastructure, research review, accessible publication and collaboration."],
  ["06", "Choose a pathway", "One-time support, recurring support, research partnership or contributed expertise."],
];

const supportUses = [
  ["Sustain the builder", "Basic living stability and protected time for independent development."],
  ["Strengthen infrastructure", "Hosting, storage, software, testing, accessibility and suitable equipment."],
  ["Advance research", "Source review, evidence mapping, methodological design and Big Question updates."],
  ["Expand public access", "Readable reports, educational pages, visualisations and provenance-linked discovery."],
];

export default function SupportImpactPage() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f2e8", background: "radial-gradient(circle at 50% 0%,rgba(73,53,145,.28),transparent 34%),#05060b" }}>
      <header style={{ ...shell, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 18, paddingTop: 20, paddingBottom: 20 }}>
        <a href="/" style={{ color: "#f5f2e8", textDecoration: "none", fontWeight: 900, letterSpacing: ".12em" }}>AKASHICNET.ORG</a>
        <nav aria-label="Support navigation" style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
          <a href="/" style={{ color: "#d9d4c7" }}>Home</a>
          <a href="/big-questions" style={{ color: "#d9d4c7" }}>Big Questions</a>
          <a href="/akashicomni" style={{ color: "#d9d4c7" }}>AkashicOMNI</a>
        </nav>
      </header>

      <section style={{ ...shell, paddingTop: 76, paddingBottom: 58, textAlign: "center" }}>
        <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".17em", fontSize: 13 }}>SUPPORT & IMPACT · INDEPENDENT PUBLIC-INTEREST DEVELOPMENT</p>
        <h1 style={{ margin: "18px auto", maxWidth: 980, fontSize: "clamp(3rem,8vw,7rem)", lineHeight: .94, letterSpacing: "-.045em" }}>Fund the questions.<br/><em style={{ color: "#d8b95c" }}>Not predetermined answers.</em></h1>
        <p style={{ maxWidth: 790, margin: "28px auto", color: "#cbc7bd", fontSize: "clamp(1.05rem,2vw,1.3rem)", lineHeight: 1.75 }}>Help build an independent, compassion-led knowledge commons where evidence remains traceable, uncertainty remains visible and intelligence develops for the benefit of all beings.</p>
        <a href="#pathways" style={{ display: "inline-block", padding: "15px 24px", borderRadius: 999, background: "#d8b95c", color: "#080a12", fontWeight: 900, textDecoration: "none" }}>See how support helps ↓</a>
      </section>

      <section style={{ ...shell, paddingBottom: 56 }} aria-labelledby="journey-title">
        <p style={{ color: "#9fd8ff", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>DONOR NAVIGATION MAP</p>
        <h2 id="journey-title" style={{ fontSize: "clamp(2rem,5vw,4rem)", marginTop: 10 }}>From discovery to meaningful support.</h2>
        <ol style={{ listStyle: "none", padding: 0, display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(270px,1fr))", gap: 16 }}>
          {journey.map(([number,title,text],index) => (
            <li key={number} style={{ ...panel, position: "relative" }}>
              <span style={{ color: "#9fd8ff", fontWeight: 900, letterSpacing: ".12em" }}>{number}</span>
              <h3 style={{ fontSize: "1.45rem", marginBottom: 10 }}>{title}</h3>
              <p style={{ color: "#c8c4bb", lineHeight: 1.7, marginBottom: 0 }}>{text}</p>
              {index < journey.length - 1 && <span aria-hidden="true" style={{ position: "absolute", right: 14, top: 14, color: "#d8b95c" }}>→</span>}
            </li>
          ))}
        </ol>
      </section>

      <section style={{ ...shell, paddingTop: 28, paddingBottom: 52 }} aria-labelledby="trust-title">
        <div style={{ ...panel, borderColor: "rgba(159,216,255,.32)" }}>
          <p style={{ color: "#9fd8ff", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>THE TRUST LAYER</p>
          <h2 id="trust-title" style={{ fontSize: "clamp(2rem,4vw,3.4rem)" }}>Wonder with safeguards.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(210px,1fr))", gap: 14 }}>
            {[
              ["Evidence", "Claims retain sources, context, limitations and evidence class."],
              ["Privacy", "The public portal remains separated from protected working data."],
              ["Accountability", "Automation assists; consequential judgement remains human."],
              ["Revision", "Better evidence may strengthen, redirect or dissolve an earlier interpretation."],
            ].map(([title,text]) => <article key={title} style={{ padding: 18, border: "1px solid rgba(255,255,255,.09)", borderRadius: 16 }}><strong style={{ color: "#f1d47b" }}>{title}</strong><p style={{ color: "#c8c4bb", lineHeight: 1.65, marginBottom: 0 }}>{text}</p></article>)}
          </div>
        </div>
      </section>

      <section id="pathways" style={{ ...shell, paddingTop: 28, paddingBottom: 50 }} aria-labelledby="impact-title">
        <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>WHAT SUPPORT ENABLES</p>
        <h2 id="impact-title" style={{ fontSize: "clamp(2rem,5vw,4rem)" }}>Make the next stage possible.</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 16 }}>
          {supportUses.map(([title,text]) => <article key={title} style={panel}><h3 style={{ color: "#f1d47b", fontSize: "1.4rem" }}>{title}</h3><p style={{ color: "#c8c4bb", lineHeight: 1.7 }}>{text}</p></article>)}
        </div>
        <p style={{ color: "#aaa69d", lineHeight: 1.7 }}>Support enables development capacity; it does not purchase conclusions, evidence ratings, editorial control or privileged access to protected data.</p>
      </section>

      <section style={{ ...shell, paddingTop: 28, paddingBottom: 52 }} aria-labelledby="finance-title">
        <div style={{ ...panel, borderColor: "rgba(216,185,92,.38)" }}>
          <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>SEPTEMBER 2026 · FINANCIAL MODEL IN DEVELOPMENT</p>
          <h2 id="finance-title" style={{ fontSize: "clamp(2rem,4.5vw,3.6rem)" }}>From survival funding to sustainable stewardship.</h2>
          <p style={{ color: "#d1cdc4", lineHeight: 1.75 }}>This month AkashicNET will develop a transparent financial model before publishing numerical targets. The model will distinguish the creator’s basic living stability from project infrastructure, research and public-access costs.</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(230px,1fr))", gap: 14, marginTop: 22 }}>
            {[
              ["Baseline", "Define essential monthly living and independent-development capacity."],
              ["Infrastructure", "Document hosting, storage, software, equipment and accessibility costs."],
              ["Runway", "Model one-time and recurring support scenarios without promising outcomes."],
              ["Transparency", "Design a quarterly income, expenditure, progress and next-needs report."],
            ].map(([title,text]) => <article key={title} style={{ padding: 18, border: "1px solid rgba(255,255,255,.10)", borderRadius: 16, background: "rgba(255,255,255,.025)" }}><strong style={{ color: "#f1d47b" }}>{title}</strong><p style={{ color: "#c8c4bb", lineHeight: 1.65, marginBottom: 0 }}>{text}</p></article>)}
          </div>
          <p style={{ marginBottom: 0, marginTop: 22, color: "#c8c4bb", lineHeight: 1.7 }}><strong>Publication rule:</strong> all figures will be labelled as verified actuals, estimates or scenarios. Donations will never determine evidence conclusions or buy access to protected corpus data.</p>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 28, paddingBottom: 52 }} aria-labelledby="ask-title">
        <div style={{ ...panel, borderColor: "rgba(117,219,199,.38)", background: "radial-gradient(circle at 50% 0%,rgba(117,219,199,.10),transparent 56%),linear-gradient(145deg,rgba(17,20,35,.94),rgba(7,9,18,.99))" }}>
          <p style={{ color: "#75dbc7", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>ASK AKASHICNET · A REPORT FOR A COFFEE</p>
          <h2 id="ask-title" style={{ fontSize: "clamp(2rem,4.5vw,3.6rem)" }}>Bring a detailed question.</h2>
          <p style={{ color: "#d1cdc4", fontSize: "1.08rem", lineHeight: 1.8 }}>If a question needs more than a short answer, request a focused AkashicNET briefing. Where capacity and suitable public sources allow, the response can map evidence, interpretations, competing perspectives, uncertainty and practical next steps.</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 14, marginTop: 22 }}>
            <article style={{ padding: 18, border: "1px solid rgba(255,255,255,.10)", borderRadius: 16 }}><strong style={{ color: "#f1d47b" }}>1 · Ask</strong><p style={{ color: "#c8c4bb", lineHeight: 1.65, marginBottom: 0 }}>Send the question, intended audience, desired depth and any sources already found.</p></article>
            <article style={{ padding: 18, border: "1px solid rgba(255,255,255,.10)", borderRadius: 16 }}><strong style={{ color: "#f1d47b" }}>2 · Scope</strong><p style={{ color: "#c8c4bb", lineHeight: 1.65, marginBottom: 0 }}>AkashicNET confirms whether a short reply, evidence brief or larger commissioned report is feasible.</p></article>
            <article style={{ padding: 18, border: "1px solid rgba(255,255,255,.10)", borderRadius: 16 }}><strong style={{ color: "#f1d47b" }}>3 · Support</strong><p style={{ color: "#c8c4bb", lineHeight: 1.65, marginBottom: 0 }}>For a bounded brief, contribute a coffee if able. Larger work is agreed transparently before research begins.</p></article>
          </div>
          <p style={{ color: "#c8c4bb", lineHeight: 1.75, marginTop: 22 }}><strong>Why this exists:</strong> AkashicNET is being developed independently, without institutional funding and with limited personal resources. Recent basic stability has depended partly on emergency family support following a prolonged financial dispute and administrative difficulties, compounded by ADHD-related executive-function challenges. This context is shared for transparency, not blame. Support helps provide stability, research time and infrastructure so careful public-interest work can continue. The question remains welcome even when someone cannot contribute.</p>
          <p style={{ color: "#aaa69d", lineHeight: 1.7 }}><strong>Boundary:</strong> availability depends on capacity and source access. A contribution does not guarantee a particular conclusion, and this pathway does not replace medical, legal, mental-health or financial professionals.</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 14, marginTop: 24 }}>
            <a href="mailto:support@akashicnet.org?subject=Detailed%20AkashicNET%20question&body=My%20question%3A%0A%0AIntended%20audience%3A%0A%0ADesired%20depth%3A%0A%0ASources%20already%20found%3A" style={{ padding: "14px 21px", borderRadius: 999, background: "#75dbc7", color: "#071016", fontWeight: 900, textDecoration: "none" }}>Request assistance →</a>
            <a href="https://buymeacoffee.com/akashicnet" target="_blank" rel="noreferrer" style={{ padding: "14px 21px", borderRadius: 999, border: "1px solid rgba(216,185,92,.5)", color: "#f1d47b", fontWeight: 900, textDecoration: "none" }}>☕ Support a report</a>
          </div>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 26, paddingBottom: 68 }} aria-labelledby="choose-title">
        <div style={{ ...panel, textAlign: "center", padding: "clamp(28px,6vw,56px)" }}>
          <p style={{ color: "#75dbc7", fontWeight: 900, letterSpacing: ".14em", fontSize: 13 }}>CHOOSE HOW TO HELP</p>
          <h2 id="choose-title" style={{ fontSize: "clamp(2rem,5vw,4rem)" }}>Support, collaborate or open a conversation.</h2>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 14, marginTop: 28 }}>
            <a href="https://buymeacoffee.com/akashicnet" target="_blank" rel="noreferrer" style={{ padding: "15px 22px", borderRadius: 999, background: "#d8b95c", color: "#080a12", fontWeight: 900, textDecoration: "none" }}>☕ Support AkashicNET</a>
            <a href="mailto:support@akashicnet.org?subject=AkashicNET%20research%20or%20development%20partnership" style={{ padding: "15px 22px", borderRadius: 999, border: "1px solid rgba(159,216,255,.45)", color: "#9fd8ff", fontWeight: 900, textDecoration: "none" }}>Research partnership</a>
            <a href="mailto:support@akashicnet.org?subject=Contributing%20skills%20to%20AkashicNET" style={{ padding: "15px 22px", borderRadius: 999, border: "1px solid rgba(117,219,199,.45)", color: "#75dbc7", fontWeight: 900, textDecoration: "none" }}>Contribute skills</a>
          </div>
          <p style={{ color: "#c8c4bb", lineHeight: 1.7, marginTop: 26 }}>Detailed development roadmaps are available on request from <a href="mailto:support@akashicnet.org" style={{ color: "#f1d47b" }}>support@akashicnet.org</a>.</p>
        </div>
      </section>

      <footer style={{ borderTop: "1px solid rgba(255,255,255,.08)", padding: "30px 22px", textAlign: "center", color: "#9f9c95" }}>AKASHICNET.ORG · Independent inquiry · Transparent uncertainty · Compassionate purpose</footer>
    </main>
  );
}
