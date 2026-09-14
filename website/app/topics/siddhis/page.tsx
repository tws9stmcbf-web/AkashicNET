import type { Metadata } from "next";
import styles from "./siddhis.module.css";

export const metadata: Metadata = {
  title: "Siddhis — Spiritual Attainments, Extraordinary Claims & Open Questions | AkashicNET",
  description: "An evidence-bounded map of siddhis in Yoga and Buddhist traditions, contemplative experience, scientific research and unresolved extraordinary claims.",
};

const traditions = [
  { term: "Siddhi", home: "Yoga and wider Indian traditions", note: "A broad term for accomplishment, attainment or extraordinary capacity. Patañjali’s Yoga Sūtras discuss such claims in Vibhūti Pāda." },
  { term: "Iddhi / Ṛddhi", home: "Buddhist traditions", note: "Terms associated with extraordinary capacities in Buddhist literature; interpretation and emphasis vary by school and text." },
  { term: "Abhiññā", home: "Early Buddhist frameworks", note: "Higher knowledges described in canonical and commentarial traditions. Their religious role is not equivalent to modern laboratory evidence." },
];

const lanes = [
  ["Established historical fact", "South Asian religious and philosophical texts describe siddhis or related attainments. This establishes a history of ideas and practice, not the literal reality of every attributed power."],
  ["Established meditation research", "Meditation can affect attention, emotion, perception and measurable brain activity. These findings do not establish telepathy, clairvoyance, levitation or survival of consciousness."],
  ["Lived experience / testimony", "Practitioners report unusual perceptions, intuitions, bodily energies, synchronicities and transformative states. Testimony matters phenomenologically but cannot validate universal causal claims by itself."],
  ["Contested empirical research", "Some parapsychology programmes report statistical anomalies; methods, effect sizes, replication, publication bias and interpretation remain actively disputed."],
  ["Speculation", "Quantum, field, Akashic or multidimensional explanations are hypotheses or metaphors unless a specific mechanism produces independently replicable predictions."],
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
      <div className={styles.status}><strong>CURRENT STATUS · UNRESOLVED</strong><span>Traditional significance is established. Particular extraordinary abilities require claim-specific evidence.</span></div>
    </section>

    <section className={styles.section} id="meaning">
      <p className={styles.kicker}>01 · What the term can mean</p>
      <h2>One word, several traditions, many interpretations.</h2>
      <p className={styles.intro}>“Siddhi” can mean accomplishment or attainment, not only “superpower.” Lists differ across Hindu, Yoga, Buddhist, Jain and tantric lineages. AkashicNET therefore preserves each tradition’s own context rather than treating every list as one universal catalogue.</p>
      <div className={styles.cards}>{traditions.map(x=><article key={x.term}><span>{x.home}</span><h3>{x.term}</h3><p>{x.note}</p></article>)}</div>
      <aside className={styles.warning}><strong>The contemplative warning</strong><p>Patañjali’s third book describes extraordinary attainments while also warning that they may obstruct liberation when pursued as objects of attachment. Discernment, humility and freedom remain more important than display.</p></aside>
    </section>

    <section className={styles.section} id="evidence">
      <p className={styles.kicker}>02 · Evidence map</p>
      <h2>Do not collapse the lanes.</h2>
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
      <h2>A constellation, not confirmation.</h2>
      <p className={styles.intro}>The community archive already contains adjacent material on telepathy, precognition, reincarnation, altered states, meditation and the reliability of perception. These are candidate connections for review; proximity does not promote them into proof of siddhis.</p>
      <div className={styles.links}>
        <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/1hcvvjs/telepathic_connections_with_gail_hayssen_and/">Telepathic connections · IONS discussion ↗</a>
        <a href="https://www.reddit.com/r/NeuronsToNirvana/comments/17zzx4k/can_you_trust_your_own_brain_a_neuroscientist/">Can you trust your own brain? · Perception and inference ↗</a>
        <a href="https://www.reddit.com/r/NeuronsToNirvana/search/?q=precognition&restrict_sr=1">Search N2N · Precognition ↗</a>
        <a href="https://www.reddit.com/r/NeuronsToNirvana/search/?q=meditation&restrict_sr=1">Search N2N · Meditation ↗</a>
      </div>
    </section>

    <section className={styles.section} id="sources">
      <p className={styles.kicker}>05 · Starting sources</p>
      <h2>Read tradition and experiment on their own terms.</h2>
      <ul className={styles.sources}>
        <li><a href="https://www.vignanam.org/meaning/english/patanjali-yoga-sutras-3-vibhuti-pada.html">Patañjali Yoga Sūtras · Vibhūti Pāda translation ↗</a><span>Primary-text doorway; translations and commentaries vary.</span></li>
        <li><a href="https://suttacentral.net/">SuttaCentral ↗</a><span>Searchable early Buddhist texts and translations for iddhi and abhiññā.</span></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC1697747/">Studies of advanced Tibetan Buddhist meditation ↗</a><span>Scientific discussion of measurable contemplative physiology, not validation of supernatural claims.</span></li>
        <li><a href="https://doi.org/10.1016/j.neubiorev.2016.03.021">Functional neuroanatomy of meditation · review and meta-analysis ↗</a><span>Evidence for heterogeneous neural correlates across meditation styles.</span></li>
      </ul>
    </section>

    <section className={styles.boundary}>
      <h2>Safety and integrity boundary</h2>
      <p>This page does not promise powers, certify teachers, prescribe intensive practices or recommend substances. Distressing perceptions, insomnia, paranoia, loss of functioning or a sense of being commanded deserve grounded support and, when needed, qualified medical care. Spiritual interpretation and clinical assessment can coexist without either being used to dismiss the other.</p>
      <p><strong>AkashicNET funds the question, not the answer.</strong></p>
    </section>

    <footer className={styles.footer}><a href="/">← AkashicNET home</a><span>Boundless awareness is infinite love.</span><span>Evidence boundary · v0.1</span></footer>
  </main>;
}
