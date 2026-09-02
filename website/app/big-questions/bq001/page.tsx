import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BQ001 — Does consciousness continue beyond the individual? — AKASHICNET.ORG",
  description:
    "An evidence-mapped AkashicNET investigation of consciousness, cardiac arrest, memory, reincarnation-type cases, contemplative traditions and philosophy of mind.",
};

type EvidenceCard = {
  title: string;
  label: "Established Evidence" | "Interpretation";
  text: string;
  boundary: string;
  sources: { label: string; href: string }[];
};

const evidence: EvidenceCard[] = [
  {
    title: "Brain states and conscious states are strongly related under studied conditions",
    label: "Established Evidence",
    text: "Experimental and clinical work links measurable brain states, autobiographical memory and reported conscious experience under the conditions studied.",
    boundary:
      "This does not by itself prove that post-mortem continuation is impossible.",
    sources: [
      { label: "Maschke et al. 2024", href: "https://www.nature.com/articles/s42003-024-06613-8" },
      { label: "El Haj et al. 2019", href: "https://pubmed.ncbi.nlm.nih.gov/31322576/" },
    ],
  },
  {
    title: "Some resuscitated patients report experiences associated with cardiac arrest",
    label: "Established Evidence",
    text: "Prospective AWARE studies document survivor reports and attempted objective verification during cardiac-arrest research.",
    boundary:
      "Cardiac arrest during attempted resuscitation is not equivalent to irreversible biological death, and retrospective recall does not uniquely establish the timing of an experience.",
    sources: [
      { label: "AWARE 2014", href: "https://pubmed.ncbi.nlm.nih.gov/25301715/" },
      { label: "AWARE II 2023", href: "https://pubmed.ncbi.nlm.nih.gov/37423492/" },
    ],
  },
  {
    title: "Near-death inference is constrained by terminology, timing and mechanism uncertainty",
    label: "Interpretation",
    text: "Neuroscientific reviews argue that careful definitions and plausible physiological mechanisms are necessary before stronger claims can be made.",
    boundary:
      "A plausible neuroscientific model is not complete proof that every NDE is fully explained, and methodological critique is not proof of non-survival.",
    sources: [
      { label: "Martial et al. 2022", href: "https://pubmed.ncbi.nlm.nih.gov/36017883/" },
      { label: "Martial et al. 2025", href: "https://pubmed.ncbi.nlm.nih.gov/40159547/" },
    ],
  },
  {
    title: "Autobiographical memory contributes to experienced self-continuity",
    label: "Interpretation",
    text: "Psychology treats self-continuity as a relation among past, present and future selves, with memory playing an important role.",
    boundary:
      "Psychological self-continuity is not identical to metaphysical personal identity or post-mortem persistence.",
    sources: [
      { label: "Sow et al. 2022", href: "https://pubmed.ncbi.nlm.nih.gov/36165349/" },
      { label: "Sedikides et al. 2023", href: "https://pubmed.ncbi.nlm.nih.gov/35961040/" },
    ],
  },
  {
    title: "A peer-reviewed literature exists on children reporting previous-life memories",
    label: "Established Evidence",
    text: "Published observational research includes case reports, interviews, documentary analysis and small comparative studies, including reports of biographical correspondences.",
    boundary:
      "A reported match or unexplained case is not proof of reincarnation. Information leakage, retrospective reconstruction, selection effects and alternative explanations remain live concerns.",
    sources: [
      { label: "Scoping review 2021", href: "https://pubmed.ncbi.nlm.nih.gov/34147343/" },
      { label: "Haraldsson 2003", href: "https://pubmed.ncbi.nlm.nih.gov/12689435/" },
      { label: "Moraes et al. 2024", href: "https://pubmed.ncbi.nlm.nih.gov/39341119/" },
    ],
  },
  {
    title: "Stronger reincarnation-type inference requires stronger prospective controls",
    label: "Interpretation",
    text: "Early documentation, independent witnesses, explicit accounting of information pathways, blinded or prospective verification where feasible, and transparent reporting of misses as well as matches would strengthen future research.",
    boundary:
      "Failure of one psychological explanation does not establish reincarnation; psychological correlates do not establish that reincarnation is impossible.",
    sources: [
      { label: "Tucker 2025", href: "https://pubmed.ncbi.nlm.nih.gov/40627512/" },
      { label: "Thomas et al. 2025 (2026 issue)", href: "https://pubmed.ncbi.nlm.nih.gov/41265055/" },
    ],
  },
  {
    title: "Contemplative traditions offer non-ordinary models of selfhood",
    label: "Interpretation",
    text: "Buddhist non-self analysis and meditation frameworks examine how the sense of self can be constructed, deconstructed and transformed.",
    boundary:
      "Contemplative phenomenology, tradition and meditation-related changes in self-processing do not establish external ontology or survival after death.",
    sources: [
      { label: "Siderits 2011", href: "https://academic.oup.com/edited-volume/38581/chapter-abstract/334605685" },
      { label: "Dahl et al. 2015", href: "https://pubmed.ncbi.nlm.nih.gov/26231761/" },
      { label: "Vago & Silbersweig 2012", href: "https://pubmed.ncbi.nlm.nih.gov/23112770/" },
    ],
  },
  {
    title: "Physicalism, dualism and panpsychism remain competing philosophical frameworks",
    label: "Interpretation",
    text: "These positions offer different accounts of how mind relates to the physical world, but none functions as an empirical verdict on BQ001.",
    boundary:
      "Philosophical coherence or possibility is not empirical evidence that personal consciousness survives death; physicalism as philosophy is not itself proof of non-survival.",
    sources: [
      { label: "SEP: Physicalism", href: "https://plato.stanford.edu/entries/physicalism/" },
      { label: "SEP: Dualism", href: "https://plato.stanford.edu/entries/dualism/" },
      { label: "SEP: Panpsychism", href: "https://plato.stanford.edu/entries/panpsychism/" },
    ],
  },
];

const counterInferences = [
  "Brain dependence under studied conditions does not prove non-survival.",
  "Cardiac-arrest reports do not prove consciousness existed during irreversible brain failure.",
  "A matching past-life case does not prove reincarnation.",
  "Failure to explain a case with one psychological hypothesis does not prove reincarnation.",
  "Contemplative experience does not prove a metaphysical ontology.",
  "Philosophical possibility does not establish empirical actuality.",
  "Model-support relationships are not votes and do not upgrade evidence class.",
];

const openQuestions = [
  "Which observations could discriminate biological-dependence models from continuity models?",
  "Can prospective cardiac-arrest studies establish tighter temporal links between reported experience and measurable brain state?",
  "Can reincarnation-type research produce prospectively documented, independently verified cases with information pathways tightly controlled?",
  "What would count as continuity of an individual rather than continuity of information, resemblance or influence?",
  "Which philosophy-of-mind claims can be translated into empirically discriminating predictions?",
];

const shell: React.CSSProperties = {
  maxWidth: 1120,
  margin: "0 auto",
  padding: "0 22px",
};

const panel: React.CSSProperties = {
  border: "1px solid rgba(227,190,87,.24)",
  background: "linear-gradient(145deg, rgba(16,18,31,.88), rgba(8,10,20,.96))",
  borderRadius: 24,
  padding: 24,
  boxShadow: "0 22px 70px rgba(0,0,0,.28)",
};

export default function BQ001Page() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f2e8", background: "radial-gradient(circle at 50% 0%, rgba(75,48,145,.20), transparent 34%), #05060b" }}>
      <header style={{ ...shell, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, paddingTop: 20, paddingBottom: 20 }}>
        <a href="/" style={{ color: "#f5f2e8", textDecoration: "none", fontWeight: 800, letterSpacing: ".12em" }}>AKASHICNET.ORG</a>
        <nav aria-label="Big Question navigation" style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
          <a href="/" style={{ color: "#d9d4c7" }}>Home</a>
          <a href="/about" style={{ color: "#d9d4c7" }}>About</a>
          <a href="#sources" style={{ color: "#d9d4c7" }}>Sources</a>
        </nav>
      </header>

      <section style={{ ...shell, paddingTop: 72, paddingBottom: 54, textAlign: "center" }}>
        <p style={{ color: "#d8b95c", letterSpacing: ".18em", fontWeight: 800, fontSize: 13 }}>BIG QUESTION 001 · PUBLIC INVESTIGATION</p>
        <h1 style={{ margin: "16px auto", maxWidth: 900, fontSize: "clamp(2.7rem, 8vw, 6.6rem)", lineHeight: .96, letterSpacing: "-.045em" }}>Does consciousness continue beyond the individual?</h1>
        <p style={{ maxWidth: 760, margin: "26px auto", color: "#c8c4bb", fontSize: "clamp(1.05rem, 2vw, 1.3rem)", lineHeight: 1.7 }}>AkashicNET maps the evidence without purchasing a conclusion. Neuroscience, cardiac-arrest research, memory and identity, reincarnation-type cases, contemplative traditions and philosophy of mind are kept visible together without flattening their evidential differences.</p>
        <div role="status" aria-label="Current conclusion" style={{ display: "inline-flex", alignItems: "center", gap: 10, border: "1px solid rgba(227,190,87,.52)", borderRadius: 999, padding: "10px 18px", background: "rgba(227,190,87,.08)", color: "#f1d47b", fontWeight: 900, letterSpacing: ".12em" }}>CURRENT STATUS · UNRESOLVED</div>
      </section>

      <section style={{ ...shell, paddingBottom: 44 }} aria-labelledby="legend-title">
        <div style={panel}>
          <h2 id="legend-title" style={{ marginTop: 0 }}>How to read the evidence</h2>
          <p style={{ color: "#c8c4bb", lineHeight: 1.7 }}>AkashicNET does not collapse different kinds of knowledge into a single score. The full taxonomy is preserved even where this first synthesis currently uses only two classes.</p>
          <p style={{ marginBottom: 0, fontWeight: 800, lineHeight: 1.8 }}>Established Evidence · Interpretation · Lived Experience/Testimony · Hypothesis · Speculation</p>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 28, paddingBottom: 22 }}>
        <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>COMPETING MODELS</p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(280px,1fr))", gap: 18 }}>
          <article style={panel}><h2>Biological dependence</h2><p style={{ color: "#c8c4bb", lineHeight: 1.7 }}>Individual conscious experience appears strongly dependent on biological brain function under observed conditions.</p><strong>UNRESOLVED</strong></article>
          <article style={panel}><h2>Continuity</h2><p style={{ color: "#c8c4bb", lineHeight: 1.7 }}>Some anomalous reports and non-reductive philosophical positions leave open the possibility that some aspect of consciousness could continue beyond individual biological functioning.</p><strong>UNRESOLVED</strong></article>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 50, paddingBottom: 30 }}>
        <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>EVIDENCE BY DOMAIN</p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))", gap: 18 }}>
          {evidence.map((item) => (
            <article key={item.title} style={panel}>
              <span style={{ display: "inline-block", color: item.label === "Established Evidence" ? "#a9e4c5" : "#cbb7ff", fontSize: 12, fontWeight: 900, letterSpacing: ".12em", textTransform: "uppercase" }}>{item.label}</span>
              <h2 style={{ fontSize: "1.35rem", lineHeight: 1.25 }}>{item.title}</h2>
              <p style={{ color: "#d1cdc4", lineHeight: 1.7 }}>{item.text}</p>
              <p style={{ color: "#f0d681", lineHeight: 1.6 }}><strong>Boundary:</strong> {item.boundary}</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
                {item.sources.map((source) => <a key={source.href} href={source.href} target="_blank" rel="noreferrer" style={{ color: "#9fd8ff" }}>{source.label}</a>)}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 38, paddingBottom: 28 }}>
        <div style={{ ...panel, borderColor: "rgba(227,190,87,.42)" }}>
          <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>WHAT THIS DOES NOT SHOW</p>
          <h2>Counter-inferences are part of the evidence map.</h2>
          <ul style={{ lineHeight: 1.8, color: "#d1cdc4", paddingLeft: 22 }}>
            {counterInferences.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section style={{ ...shell, paddingTop: 30, paddingBottom: 44 }}>
        <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>OPEN QUESTIONS</p>
        <ol style={{ lineHeight: 1.85, color: "#d1cdc4", paddingLeft: 24 }}>
          {openQuestions.map((item) => <li key={item}>{item}</li>)}
        </ol>
      </section>

      <section style={{ ...shell, paddingTop: 30, paddingBottom: 64 }}>
        <div style={{ ...panel, textAlign: "center", padding: "clamp(28px,6vw,58px)" }}>
          <p style={{ color: "#d8b95c", fontWeight: 900, letterSpacing: ".15em", fontSize: 13 }}>CURRENT CONCLUSION · UNRESOLVED</p>
          <h2 style={{ fontSize: "clamp(1.8rem,4vw,3.3rem)", lineHeight: 1.15 }}>The evidence constrains the possibilities. It does not yet settle them.</h2>
          <p style={{ maxWidth: 820, margin: "20px auto 0", color: "#d1cdc4", lineHeight: 1.8 }}>Current evidence supports strong relationships between biological brain states, memory and conscious experience, while also documenting anomalous reports and contested case literatures that are not fully settled by the present evidence base. None of the validated BQ001 batches establishes either personal consciousness surviving irreversible death or the impossibility of such survival.</p>
          <p style={{ marginTop: 28, fontWeight: 900 }}>Fund the question — not the answer.</p>
        </div>
      </section>

      <section id="sources" style={{ ...shell, paddingBottom: 72 }}>
        <p style={{ color: "#d8b95c", fontWeight: 800, letterSpacing: ".14em", fontSize: 13 }}>PROVENANCE</p>
        <p style={{ color: "#c8c4bb", lineHeight: 1.7 }}>This page is a public adaptation of the validated BQ001 synthesis in the AkashicNET repository. Every evidence card above is constrained by the underlying claim/source records; uncertainty and evidence class are preserved rather than converted into a confidence score.</p>
        <p style={{ color: "#c8c4bb" }}>BQ001 · Public synthesis v0.1.1 · AkashicNET PRE-ALPHA v0.10.x engine</p>
      </section>

      <footer style={{ borderTop: "1px solid rgba(255,255,255,.08)", padding: "30px 22px", textAlign: "center", color: "#9f9c95" }}>AKASHICNET.ORG · Open Heart · Open Mind · Open Knowledge · Awaken within · Serve without ♾️</footer>
    </main>
  );
}