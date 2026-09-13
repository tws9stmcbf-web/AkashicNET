import type { Metadata } from "next";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "AkashicVISION | From the Primordial OM to the Omega Point",
  description: "A lived-experience-led, evidence-bounded vision of AkashicNET from an Easter Monday 3 a.m. near-death experience toward a 2042–2047 planetary knowledge network.",
};

const layers = [
  {
    label: "Lived Experience/Testimony",
    title: "The threshold",
    text: "On Easter Monday 2024, at approximately 3 a.m., during an emergency appendectomy, the founder reports a near-death experience perceived as contact with an immeasurable field of memory, relationship and meaning: Akasha.",
  },
  {
    label: "Interpretation",
    title: "The revelation",
    text: "The experience is interpreted as an encounter with what spiritual traditions have called the Akashic records. That interpretation gives the experience meaning; it does not establish an external archive as scientific fact.",
  },
  {
    label: "Unresolved",
    title: "The question",
    text: "Was this a neurophysiological event, a psychologically meaningful visionary state, contact with something beyond the individual, or a combination not yet understood? AkashicNET leaves the question open.",
  },
];

const translation = [
  ["Perception", "A field in which apparently separate moments felt connected."],
  ["Principle", "Preserve relationships without erasing uncertainty or difference."],
  ["Practice", "Build a provenance-linked Evidence Commons with transparent human stewardship."],
  ["Purpose", "Develop meta-intelligence for wiser decisions and the benefit of all beings."],
];

export default function AkashicVisionPage() {
  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a href="/" className={styles.wordmark}>AKASHICNET.ORG</a>
        <nav aria-label="AkashicVISION navigation">
          <a href="#experience">Experience</a>
          <a href="#translation">Translation</a>
          <a href="#vision">2042–2047</a>
          <a href="/big-questions/bq001">BQ001</a>
        </nav>
      </header>

      <section className={styles.hero} aria-labelledby="vision-title">
        <img
          className={styles.heroImage}
          src="/images/akashicvision-nde-merkaba-flower-of-life.png"
          alt="Artistic vision of a luminous toroidal heart within a Merkaba, surrounded by a faint Flower of Life and a cosmic library."
        />
        <div className={styles.vignette} />
        <div className={styles.heroCopy}>
          <p className={styles.eyebrow}>AkashicVISION · Lived Experience/Testimony</p>
          <h1 id="vision-title">From the threshold<br />to a living library.</h1>
          <p>Easter Monday · 3 a.m. · 2024</p>
        </div>
        <div className={styles.crawlWindow} aria-hidden="true">
          <div className={styles.crawl}>
            <strong>AKASHICVISION</strong>
            <span>A perception at the edge of life.</span>
            <span>A revelation named Akasha.</span>
            <span>Not proof. Not doctrine.</span>
            <span>A question carried back.</span>
            <span>How might knowledge remember</span>
            <span>its sources, uncertainty and responsibility?</span>
            <span>How might intelligence serve all beings?</span>
          </div>
        </div>
        <a className={styles.scrollCue} href="#experience">Enter the account ↓</a>
      </section>

      <section className={styles.boundary}>
        <span>Evidence boundary</span>
        <p>The artwork and language on this page interpret a reported near-death experience. They do not establish survival after death, an external Akashic archive, the scientific action of sacred geometry or any completed AI capability.</p>
      </section>

      <section className={styles.story} id="experience">
        <div className={styles.sectionIntro}>
          <p className={styles.kicker}>The Easter Monday perception</p>
          <h2>A testimony held without being universalised.</h2>
          <p>AkashicNET can honour the depth of an experience while remaining honest about what the experience can and cannot demonstrate.</p>
        </div>
        <div className={styles.layerGrid}>
          {layers.map((layer, index) => (
            <article key={layer.title} className={styles.layerCard}>
              <span>0{index + 1} · {layer.label}</span>
              <h3>{layer.title}</h3>
              <p>{layer.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.symbols} aria-labelledby="symbols-title">
        <div>
          <p className={styles.kicker}>Symbolic field</p>
          <h2 id="symbols-title">A toroidal heart inside a Merkaba.</h2>
          <p>The toroidal heart represents love circulating through relationship rather than terminating in the self. The Merkaba represents multiple directions held within one dynamic structure. The Flower of Life suggests recurring relationship and emergence.</p>
        </div>
        <aside>
          <strong>Interpretation · Artistic metaphor</strong>
          <p>These forms organise the page’s meaning. Their presence is not evidence that the NDE had a geometric mechanism or that sacred geometry has been scientifically validated as a carrier of consciousness.</p>
        </aside>
      </section>

      <section className={styles.translation} id="translation">
        <div className={styles.sectionIntro}>
          <p className={styles.kicker}>From revelation to responsibility</p>
          <h2>The experience became a design question.</h2>
          <p>Rather than turning one extraordinary perception into an unquestionable answer, AkashicNET translates it into a disciplined way of holding knowledge.</p>
        </div>
        <div className={styles.translationFlow}>
          {translation.map(([title, text], index) => (
            <article key={title}>
              <span>0{index + 1}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
        <blockquote>Compassion guides purpose. Evidence governs factual claims. Wisdom serves all beings.</blockquote>
      </section>

      <section className={styles.vision} id="vision">
        <img
          src="/images/akashicvision-sigil-2042-2047.png"
          alt="AkashicVISION sigil mapping seven stages from ethical roots through evidence and awareness to planetary service."
        />
        <div>
          <p className={styles.kicker}>AkashicVISION · 2042–2047</p>
          <h2>From the Primordial OM to the Omega Point.</h2>
          <p><strong>Now:</strong> a human-curated living Evidence Commons.</p>
          <p><strong>Developing:</strong> a provenance-led, values-aligned meta-intelligence architecture.</p>
          <p><strong>Vision:</strong> a living planetary knowledge network developed for the benefit of all beings.</p>
          <p className={styles.status}>Vision · Interpretation · Speculation</p>
        </div>
      </section>

      <section className={styles.constellation} aria-labelledby="constellation-title">
        <div className={styles.sectionIntro}>
          <div>
            <p className={styles.kicker}>One compass · many horizons</p>
            <h2 id="constellation-title">Vision chooses a direction. Futures remain plural.</h2>
          </div>
          <p>AkashicVISION is the ethical north star, not a fixed prediction. Its emerging offshoots examine different dimensions of possibility while remaining answerable to evidence, uncertainty and the benefit of all beings.</p>
        </div>
        <div className={styles.constellationGrid}>
          <article>
            <span>Emerging offshoot</span>
            <h3>Akashic Futures Lab</h3>
            <p>Possible, probable, preferable and preventable futures. One guiding vision can inform infinitely many scenarios without pretending to determine them.</p>
          </article>
          <article>
            <span>Mathematics · Physics · Cosmology</span>
            <h3>AkashicINFINITE</h3>
            <p>Mathematics at the edge of imagination: infinities, limits, paradoxes, transfinite numbers, fractals, black holes, recurrence, deep time and possible universes.</p>
            <p className={styles.sourceNote}><em>A Trip to Infinity</em> is one cultural starting portal, not an evidential authority or the boundary of the subject.</p>
          </article>
          <article>
            <span>Continuity · Memory · Identity</span>
            <h3>AkashicTIMELESS</h3>
            <p>NDEs, ancestry, memory, reincarnation and continuity across time. “Reincarnation Reimagined” belongs here as an open inquiry.</p>
          </article>
          <article>
            <span>Contemplative lens</span>
            <h3>AkashicETERNAL</h3>
            <p>What traditions call the enduring, deathless or sacred, preserved as interpretation and speculation rather than established external ontology.</p>
          </article>
        </div>
        <p className={styles.constellationBoundary}><strong>Evidence boundary:</strong> shared themes generate questions. They do not establish equivalence between mathematical infinity, cosmological models, personal experience and spiritual teachings.</p>
      </section>

      <section className={styles.vows}>
        <p className={styles.kicker}>Root requirement</p>
        <h2>Compassion is not a later safety layer.</h2>
        <div>
          <span>Serve all beings</span>
          <span>Transform suffering</span>
          <span>Learn boundless wisdom</span>
          <span>Embody awakening</span>
        </div>
        <p>The Bodhisattva’s boundless vows provide ethical direction, not religious authority. Participation requires neither a spiritual belief nor acceptance of the NDE interpretation.</p>
      </section>

      <section className={styles.questions}>
        <p className={styles.kicker}>The inquiry remains open</p>
        <h2>What happened at the threshold?</h2>
        <p>BQ001 remains UNRESOLVED. AkashicNET records competing models, counter-inferences and future evidence without promoting a preferred metaphysical conclusion.</p>
        <div className={styles.actions}>
          <a href="/big-questions/bq001">Explore BQ001 →</a>
          <a href="mailto:support@akashicnet.org">Request the detailed roadmap →</a>
        </div>
      </section>

      <footer className={styles.footer}>
        <a href="/">AKASHICNET.ORG</a>
        <p>Boundless Awareness Is Infinite Love</p>
        <p>AkashicVISION · 2042–2047</p>
      </footer>
    </main>
  );
}
