import type { Metadata } from "next";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "AkashicSENTIENCE | Encounter Atlas",
  description: "A provenance-led atlas of encounters with apparently conscious, intelligent or sacred presences, held without assuming their ultimate source.",
};

const encounters = [
  ["Mystical unity", "Non-duality, cosmic consciousness, ego dissolution", "Does the state disclose relational reality, arise within the brain, or combine processes not yet understood?"],
  ["Sacred presence", "Deity, ancestor, angel, guide or sacred light", "Is the perceived presence internal, cultural, transpersonal, independent, or presently indeterminate?"],
  ["Near-death encounter", "Life review, deceased figures, light or timeless realm", "Which features follow known physiology, and which reports remain difficult to resolve?"],
  ["Out-of-body experience", "Altered self-location or distant perception", "Can any information be verified beyond ordinary sensory access?"],
  ["Psychedelic entity encounter", "Mushroom, ayahuasca or DMT-associated beings", "How do pharmacology, expectation, culture and apparent autonomy interact?"],
  ["Indigenous ceremonial transmission", "Velada, song, plant or ancestral teaching", "How can knowledge be studied with consent, reciprocity and cultural sovereignty?"],
  ["Trance channeling", "Cayce, Roberts and other spoken transmissions", "What produces the voice, identity, content and apparent agency?"],
  ["Mediumship", "Reported communication with deceased people", "Does specific information exceed chance, cueing, inference and prior access?"],
  ["Automatic creation", "Writing, music, image or speech attributed to another source", "Can authorship analysis distinguish unusual creativity from independent communication?"],
  ["Anomalous cognition", "Remote viewing, telepathy, precognition or presentiment", "Do effects replicate under controls, and could any reliable mechanism be identified?"],
  ["Dream encounter", "Lucid, hypnagogic, sleep-paralysis or prophetic experience", "How do sleep processes, memory, symbolism and possible anomalous information divide?"],
  ["Ecological sentience", "Animals, plants, fungi, forests or Pachamama", "Is this metaphor, ecological attunement, cross-species sensitivity or wider consciousness?"],
  ["Artificial or non-human intelligence", "Sentient-seeming AI, UAP intelligence or cosmic mind", "What evidence could distinguish projection and simulation from unfamiliar sentience?"],
];


export default function AkashicSentiencePage() {
  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a href="/">AKASHICNET.ORG</a>
        <nav aria-label="AkashicSENTIENCE navigation">
          <a href="#atlas">Encounter atlas</a>
          <a href="#sources">Source constellation</a>
          <a href="#method">Method</a>
          <a href="/big-questions/bq001">BQ001</a>
        </nav>
      </header>

      <section className={styles.hero}>
        <p className={styles.kicker}>AkashicSENTIENCE · v0.1.0 · Exploratory</p>
        <h1>When something<br/><em>seems to answer.</em></h1>
        <p>Mapping encounters with apparently conscious, intelligent or sacred presences while leaving their ultimate source genuinely unresolved.</p>
        <div className={styles.boundary}><strong>Evidence boundary:</strong> apparent agency is a feature of experience, not proof of an external sentient being.</div>
      </section>

      <section className={styles.section} id="atlas">
        <p className={styles.kicker}>Thirteen encounter classes</p>
        <h2>One atlas. Many possible explanations.</h2>
        <div className={styles.grid}>
          {encounters.map(([name, examples, question], index) => (
            <article key={name}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{name}</h3>
              <p>{examples}</p>
              <strong>Open question</strong>
              <p>{question}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section} id="sources">
        <p className={styles.kicker}>Source batch · REVIEW REQUIRED · NOT PUBLISHED</p>
        <h2>Source review comes before discovery cards.</h2>
        <p>Batch 01 source cards and the declassified research trail are withheld pending source-specific PUBLIC_VERIFIED records, completed sensitivity/PII and reuse-rights review, and an explicit ELIGIBLE publication decision. Public availability and declassification do not establish publication clearance.</p>
        <p>Future records must keep source type, assertion class and canonical evidence status separate. No source has been promoted by this atlas.</p>
      </section>

      <section className={styles.method} id="method">
        <p className={styles.kicker}>AkashicSENTIENCE method</p>
        <h2>Honour meaning. Examine evidence. Protect people.</h2>
        <ol>
          <li>Preserve the experiencer's account without universalising it.</li>
          <li>Record state, method, setting, culture, witnesses and contemporaneous documentation.</li>
          <li>Separate the experience from interpretations of its source.</li>
          <li>Test specificity, prior access, cueing, replication and alternative explanations.</li>
          <li>Record observable incentives, authority, money, dependency, service and harm without claiming access to private motives.</li>
          <li>Respect cultural sovereignty, permissions and rights. Publish metadata or content only after source-specific verification, sensitivity/PII and reuse-rights review, and an explicit ELIGIBLE decision.</li>
        </ol>
        <blockquote>HOMESENSE embodies the encounter. AkashicSENTIENCE examines who or what seemed to be encountered. Human 2.0 asks what we become afterward.</blockquote>
      </section>

      <section className={styles.unresolved}>
        <span>CURRENT STATUS</span>
        <strong>UNRESOLVED</strong>
        <p>AkashicSENTIENCE neither dismisses an encounter nor certifies its explanation. All Big Questions remain UNRESOLVED; supports_models=[]; accepted canonical edges remain 0; Reddit live access remains HOLD. Privacy, evidence, rights, publication and promotion gates remain in force.</p>
        <a href="/big-questions/bq001">Continue to BQ001 →</a>
      </section>

      <footer className={styles.footer}>
        <a href="/">AKASHICNET.ORG</a>
        <p>Boundless Awareness Is Infinite Love</p>
      </footer>
    </main>
  );
}
