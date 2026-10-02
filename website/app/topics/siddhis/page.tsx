import type { Metadata } from "next";
import styles from "./siddhis.module.css";

export const metadata: Metadata = {
  title: "Siddhis — Spiritual Attainments, Extraordinary Claims & Open Questions | AkashicNET",
  description: "A draft question map for source review of siddhis, contemplative experience and extraordinary claims. Status UNRESOLVED; no evidence assessment or community connections approved.",
};

const traditions = [
  { term: "Siddhi", home: "Terminology question", note: "Which meanings and uses should be distinguished in specific texts, translations and lineages? Source review pending." },
  { term: "Iddhi / Ṛddhi", home: "Terminology question", note: "Which texts and traditions use these terms, and how do their interpretations differ? Source review pending." },
  { term: "Abhiññā", home: "Terminology question", note: "How should this term be translated and contextualised without equating religious categories with laboratory findings? Source review pending." },
];

const lanes = [
  ["Historical questions · source review pending", "Which passages describe particular attainments, in which editions and translations, and with what interpretive limitations? No historical evidence classification is assigned here."],
  ["Meditation questions · source review pending", "What do specific studies measure, with which controls and limitations? Which claims, if any, would those measurements address? No scientific evidence classification is assigned here."],
  ["Testimony questions · intake review pending", "How could accounts of unusual experience be documented with consent, context and alternative explanations? No testimony is registered or assessed here."],
  ["Empirical questions · source review pending", "Which claim-specific experiments, replications and contrary findings would need assessment before an evidence label could be justified?"],
  ["Explanatory questions · no model support", "What testable predictions would distinguish proposed mechanisms from metaphors or competing explanations? No mechanism is endorsed here."],
];

export default function SiddhisPage() {
  return <main className={styles.page}>
    <header className={styles.nav}>
      <a href="/" className={styles.brand}><img src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span>AKASHICNET.ORG</span></a>
      <nav aria-label="Siddhis page navigation"><a href="#meaning">Meaning</a><a href="#evidence">Evidence</a><a href="#questions">Open questions</a><a href="#sources">Sources</a></nav>
    </header>

    <section className={styles.hero}>
      <p className={styles.kicker}>CONTEMPLATIVE TRADITIONS · ANOMALOUS EXPERIENCE · OPEN INQUIRY</p>
      <h1>Siddhis</h1>
      <p className={styles.subtitle}>Spiritual attainments, extraordinary claims and the discipline of not confusing wonder with proof.</p>
      <div className={styles.status}><strong>CURRENT STATUS · UNRESOLVED</strong><span>Draft question map only. Historical and scientific source review is pending; no evidence labels or topic connections are approved.</span></div>
    </section>

    <section className={styles.section} id="meaning">
      <p className={styles.kicker}>01 · What the term can mean</p>
      <h2>One word, several traditions, many interpretations.</h2>
      <p className={styles.intro}>Which meanings, texts and lineages belong in this inquiry? Terminology and cultural context require source-specific review before this page can present a historical account.</p>
      <div className={styles.cards}>{traditions.map(x=><article key={x.term}><span>{x.home}</span><h3>{x.term}</h3><p>{x.note}</p></article>)}</div>
      <aside className={styles.warning}><strong>Textual question for review</strong><p>What do particular passages and commentaries say about attainment, attachment and liberation? Attribution and interpretation remain pending a governed source record.</p></aside>
    </section>

    <section className={styles.section} id="evidence">
      <p className={styles.kicker}>02 · Questions for evidence review</p>
      <h2>Separate the questions before assessing evidence.</h2>
      <div className={styles.lanes}>{lanes.map(([title,text],i)=><article key={title}><b>{String(i+1).padStart(2,"0")}</b><div><h3>{title}</h3><p>{text}</p></div></article>)}</div>
      <blockquote>Explaining an experience neurologically does not automatically explain it away. Finding an experience meaningful does not automatically establish its proposed cause.</blockquote>
    </section>

    <section className={styles.section} id="questions">
      <p className={styles.kicker}>03 · Major open questions</p>
      <h2>Questions worth preserving.</h2>
      <ol className={styles.questions}>
        <li><strong>Definition:</strong> Which siddhis describe trainable cognitive skills, metaphorical insight, religious accomplishment, folklore or literal paranormal claims?</li>
        <li><strong>Measurement:</strong> Can a claimed ability be defined before testing, measured under blinded conditions and replicated independently?</li>
        <li><strong>Mechanism:</strong> Do unusual experiences arise through attention, interoception, memory, inference, social transmission, fraud, unknown processes or several pathways?</li>
        <li><strong>Culture:</strong> How do expectation, lineage, language and ritual shape both experience and interpretation?</li>
        <li><strong>Ethics:</strong> When do authority, charisma, money or promises of special power create risks of exploitation?</li>
        <li><strong>Practice:</strong> Can contemplative development be studied without reducing traditions to performance claims or encouraging attachment to powers?</li>
      </ol>
    </section>

    <section className={styles.section}>
      <p className={styles.kicker}>04 · NeuronsToNirvana connections</p>
      <h2>Connections withheld pending review.</h2>
      <p className={styles.intro}>No community records are approved as Siddhis topic connections. Unassessed URL inventory entries do not establish semantic relevance. Mutable search results are excluded. Any future connection requires a frozen local record, explicit candidate provenance and completed review; Reddit live access remains HOLD.</p>
    </section>

    <section className={styles.section} id="sources">
      <p className={styles.kicker}>05 · Source registration pending</p>
      <h2>No supporting references approved.</h2>
      <p>Historical and scientific starting links have been withheld. Before any evidence-asserting claim is added, governed references must record authorship, publication details, evidence status, limitations and explicit claim-to-source mappings. A link alone is not a reviewed reference.</p>
    </section>

    <section className={styles.boundary}>
      <h2>Safety and integrity boundary</h2>
      <p>Draft only: evidence, rights, privacy, publication and promotion gates remain CLOSED. Private material is prohibited. Accepted canonical edges remain 0; supports_models remains empty. This page authorizes no publication or deployment.</p>
      <p>This page does not promise powers, certify teachers, prescribe intensive practices or recommend substances. Distressing perceptions, insomnia, paranoia, loss of functioning or a sense of being commanded deserve grounded support and, when needed, qualified medical care. Spiritual interpretation and clinical assessment can coexist without either being used to dismiss the other.</p>
      <p><strong>AkashicNET funds the question, not the answer.</strong></p>
    </section>

    <footer className={styles.footer}><a href="/">← AkashicNET home</a><span>Boundless awareness is infinite love.</span><span>Evidence boundary · v0.1</span></footer>
  </main>;
}
