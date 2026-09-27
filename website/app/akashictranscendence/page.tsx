import type { Metadata } from "next";
import type { CSSProperties } from "react";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "AkashicTRANSCENDENCE | Sacred Toroidal Love",
  description: "An AkashicNET arts portal inspired by #HOMESENSE800: BuddhaFly Nature, sacred toroidal love and a birthday-moon dance at Ozora 2026.",
};

const journeys = [
  ["Buddha nature", "Buddha%20nature"],
  ["Love and consciousness", "love%20consciousness"],
  ["NDEs and OBEs", "NDE%20OR%20OBE"],
  ["Past lives and reincarnation", "past%20lives%20OR%20reincarnation"],
  ["Akashic and timeless experiences", "Akashic%20OR%20timeless"],
  ["Toroidal fields", "toroidal%20OR%20torus"],
];

const scaleJourney = [
  ["01", "Quantum possibility", "The smallest speculative threshold"],
  ["02", "Cell · microbiome · blood", "Living exchange within the body"],
  ["03", "Heart", "Rhythm, circulation and felt connection"],
  ["04", "Tree", "Roots below, canopy above"],
  ["05", "Forest", "Many lives forming an ecosystem"],
  ["06", "Pachamama", "The living Earth as our shared home"],
  ["07", "Moon · Sun", "Cycles, light and relationship"],
  ["08", "Solar system", "Our local celestial neighbourhood"],
  ["09", "Galaxies", "Vast islands of stars"],
  ["10", "CosmOS", "The widest horizon of the visual journey"],
];

const dimensions = [
  ["01", "AWAKEN", "Awareness and awakening"],
  ["02", "HIERATIC", "Sacred symbols and archetypes"],
  ["03", "HOMESENSE · Phase 8", "TRANSCENDENCE active · embodied life and synchronicity"],
  ["04", "ADAPT", "Learning through change"],
  ["05", "REGENERATE", "Repair, renewal and flourishing"],
  ["06", "TRANSCEND", "Transformation beyond present boundaries"],
  ["07", "#METAD v2.1", "Metadimensional analysis"],
  ["08", "ACTC v2.0", "Agency, context, temporal order and candidate causal pathways"],
  ["09", "MultidimensionalCUT v4.0.0 · PAST", "Compare prior patterns and inherited context"],
  ["10", "MultidimensionalCUT v4.0.0 · PRESENT", "Describe the current experience and conditions precisely"],
  ["11", "MultidimensionalCUT v4.0.0 · FUTURE", "Explore what to observe, test or cultivate next"],
  ["12", "UMASC v7.2", "Relate matter, awareness, systems and culture without collapsing their differences"],
  ["13", "AkashicNET", "The integrating living knowledge field"],
];

export default function AkashicTranscendencePage() {
  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a href="/" className={styles.wordmark}>AKASHICNET.ORG</a>
        <nav aria-label="AkashicTRANSCENDENCE navigation">
          <a href="#love-cubed">Love Cubed</a>
          <a href="#poem">Poem</a>
          <a href="#journeys">N2N journeys</a>
          <a href="/akashicvision">AkashicVISION</a>
        </nav>
      </header>

      <section className={styles.hero} aria-labelledby="transcendence-title">
        <img src="/images/akashictranscendence-homesense800.webp" alt="BuddhaFly Effect artwork overlooking the illuminated Ozora festival beneath a dramatic sunset sky." />
        <div className={styles.overlay} />
        <div className={styles.heroCopy}>
          <p>#HOMESENSE800 · ARTS</p>
          <h1 id="transcendence-title">Akashic<span>TRANSCENDENCE</span></h1>
          <strong>Sacred Toroidal Love ♾️❤️</strong>
          <small>BuddhaFly Nature beneath the birthday moon · Ozora 2026</small>
        </div>
      </section>

      <section className={styles.loveCubed} id="love-cubed" aria-labelledby="love-cubed-title">
        <div className={styles.scaleSky} aria-hidden="true">
          <div className={styles.tesseract}>
            <span className={styles.tesseractInner} />
          </div>
          <div className={styles.torus}>
            <span className={styles.torusLeft} />
            <span className={styles.torusRight} />
            <span className={styles.livingHeart}>❤️</span>
          </div>
          <div className={styles.scaleParticles}>
            {scaleJourney.map(([number, name], index) => (
              <span key={number} style={{ "--orbit": index } as CSSProperties}>{name}</span>
            ))}
          </div>
        </div>
        <div className={styles.scaleCopy}>
          <p>#HOMESENSE³ ♾️❤️³</p>
          <h2 id="love-cubed-title">LOVE CUBED</h2>
          <blockquote>As above, so below.<br />As within, so without.</blockquote>
          <p>One poetic scale journey: from quantum possibility, through the living body and biosphere, toward galaxies and CosmOS.</p>
          <blockquote className={styles.loveInvocation}>May we carry the courage of the lion, the strength of the bull, and sacred love flowing infinitely through all beings and the cosmos itself.<small>Remain awake to deception, while honouring the wild wisdom of the wolf.</small></blockquote>
          <ol>
            {scaleJourney.map(([number, name, meaning]) => (
              <li key={number}><span>{number}</span><div><strong>{name}</strong><small>{meaning}</small></div></li>
            ))}
          </ol>
          <small className={styles.scaleBoundary}>Artistic and interpretive symbolism. Toroidal organisation is not presented as an established structure at every scale.</small>
        </div>
      </section>

      <section className={styles.origin}>
        <p>The original <strong>#HOMESENSE800</strong> holds one of the most peaceful and deeply chilled moments I have ever felt.</p>
        <span>Personal reflection · Creative expression</span>
      </section>

      <article className={styles.poem} id="poem">
        <p>Finite in form,<br />infinite in flight,<br />a BuddhaFly dances<br />between darkness and light.</p>
        <p>No destination.<br />No performance.<br />Nothing to prove.</p>
        <p>Only the moon above,<br />the music within,<br />the Earth beneath<br />and the quiet recognition<br />that I belong to it all.</p>
        <p>Angel and devil,<br />Shiva and Shakti,<br />masculine and feminine,<br />yin becoming yang,<br />the cosmos meeting itself<br />within every living being.</p>
        <p>For the seen and unseen,<br />the heard and unheard,<br />the hugged and unhugged,<br />the humorous and unhumoured,<br />the centred and beautifully unhinged.</p>
        <p>May sacred love flow<br />like a torus through the heart,<br />returning without ending,<br />moving through the infinite eight,<br />holding birth, death and becoming<br />within one boundless embrace.</p>
        <p>Perhaps Buddha-nature<br />is not somewhere beyond us.</p>
        <p>Perhaps it awakens<br />in moments such as this,<br />when the mind becomes still,<br />the heart remains open<br />and the whole cosmos<br />is invited to dance.</p>
        <blockquote>One Earth.<br />One Heart.<br />One Dance.<br />One Love.</blockquote>
        <footer>For all beings in the cosmos,<br />including the cosmos. ♾️❤️🌕</footer>
      </article>

      <section className={styles.framework} aria-labelledby="framework-title">
        <p>THE AKASHICNET 13D STRUCTURE</p>
        <h2 id="framework-title">Thirteen ways of seeing.<br />One living inquiry.</h2>
        <p className={styles.frameworkIntro}>These are interpretive dimensions: distinct viewpoints used to examine an idea more completely. They are not proposed as thirteen established physical dimensions.</p>
        <ol>
          {dimensions.map(([number, name, purpose]) => (
            <li key={number}><span>{number}</span><div><strong>{name}</strong><small>{purpose}</small></div></li>
          ))}
        </ol>
        <p className={styles.frameworkNote}><strong>Current creative phase:</strong> HOMESENSE Phase 8 · TRANSCENDENCE. <strong>AkashicTRANSCENDENCE</strong> is its Arts portal through the sixth lens: TRANSCEND.</p>
      </section>

      <section className={styles.journeys} id="journeys" aria-labelledby="journeys-title">
        <p>THE LIVING KNOWLEDGE SPINE</p>
        <h2 id="journeys-title">Continue through Neurons to Nirvana</h2>
        <div>
          {journeys.map(([label, query]) => (
            <a key={label} href={`https://www.reddit.com/r/NeuronsToNirvana/search/?q=${query}&restrict_sr=1`}>{label}<span>↗</span></a>
          ))}
        </div>
      </section>

      <section className={styles.bridge}>
        <p>AkashicTRANSCENDENCE is the creative, embodied expression of the longer horizon.</p>
        <a href="/akashicvision">Enter AkashicVISION →</a>
      </section>

      <footer className={styles.siteFooter}>
        <a href="/">AKASHICNET.ORG</a>
        <p>Boundless Awareness Is Infinite Love</p>
      </footer>
    </main>
  );
}
