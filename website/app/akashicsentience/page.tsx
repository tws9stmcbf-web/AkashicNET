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

const sources = [
  {
    name: "María Sabina and the Mazatec velada",
    mode: "Indigenous ceremonial transmission",
    status: "Cultural record · Testimony · Interpretation",
    note: "Smithsonian Folkways preserves a recorded mushroom velada. AkashicSENTIENCE treats it as sacred ceremonial knowledge in Mazatec context, not generic Western channeling.",
    href: "https://folkways.si.edu/maria-sabina/mushroom-ceremony-of-the-mazatec-indians-of-mexico/world/music/album/smithsonian",
  },
  {
    name: "Edgar Cayce readings",
    mode: "Trance discourse",
    status: "Historical record · Testimony · Interpretation",
    note: "A.R.E. public pages document Cayce's attributed sources and selected reading identifiers. Protected readings remain link-and-metadata only.",
    href: "https://edgarcayce.org/edgar-cayce/readings/akashic-records/",
  },
  {
    name: "Jane Roberts papers",
    mode: "Trance dictation · Seth material",
    status: "Institutional archive · Testimony",
    note: "Yale preserves correspondence, journals, manuscripts and audiovisual material documenting Roberts's life and work.",
    href: "https://archives.yale.edu/repositories/12/resources/4482",
  },
  {
    name: "Patience Worth collection",
    mode: "Automatic communication · Literary production",
    status: "Institutional archive · Testimony",
    note: "Washington University preserves correspondence, typescripts and extensive dialogue volumes associated with Pearl Curran and Patience Worth.",
    href: "https://aspace.wustl.edu/repositories/6/resources/789",
  },
  {
    name: "Eileen J. Garrett collection",
    mode: "Trance mediumship · Parapsychology",
    status: "Institutional archive · Research history",
    note: "UMBC holds the Parapsychology Foundation collection, providing context for mediumship research and its competing interpretations.",
    href: "https://library.umbc.edu/garrett/",
  },
  {
    name: "Chico Xavier case literature",
    mode: "Psychography · After-death communication",
    status: "Testimony · Case research · Contested",
    note: "A PubMed-indexed case study examines one attributed letter. A single case cannot establish the source of Xavier's wider corpus.",
    href: "https://pubmed.ncbi.nlm.nih.gov/31158111/",
  },
  {
    name: "STAR GATE collection",
    mode: "Remote viewing · Anomalous cognition",
    status: "Declassified history · Contested evidence",
    note: "CIA records establish programme history. Declassification authenticates documents, not paranormal claims or an Akashic mechanism.",
    href: "https://www.cia.gov/readingroom/collection/stargate",
  },
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
        <p className={styles.kicker}>Public-safe source constellation · Batch 01</p>
        <h2>Records for discovery, not a hierarchy of truth.</h2>
        <div className={styles.sources}>
          {sources.map((source) => (
            <article key={source.name}>
              <span>{source.status}</span>
              <h3>{source.name}</h3>
              <p><strong>{source.mode}</strong></p>
              <p>{source.note}</p>
              <a href={source.href}>Open source record ↗</a>
            </article>
          ))}
        </div>
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
          <li>Respect cultural sovereignty, permissions and rights. Import metadata only unless reuse is clearly permitted.</li>
        </ol>
        <blockquote>HOMESENSE embodies the encounter. AkashicSENTIENCE examines who or what seemed to be encountered. Human 2.0 asks what we become afterward.</blockquote>
      </section>

      <section className={styles.unresolved}>
        <span>CURRENT STATUS</span>
        <strong>UNRESOLVED</strong>
        <p>AkashicSENTIENCE neither dismisses an encounter nor certifies its explanation.</p>
        <a href="/big-questions/bq001">Continue to BQ001 →</a>
      </section>

      <footer className={styles.footer}>
        <a href="/">AKASHICNET.ORG</a>
        <p>Boundless Awareness Is Infinite Love</p>
      </footer>
    </main>
  );
}
