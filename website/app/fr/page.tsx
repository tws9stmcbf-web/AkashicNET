import type { Metadata } from "next";
import styles from "../localizedHome.module.css";

export const metadata: Metadata = {
  title: "AkashicNET en français — Un réseau vivant de connaissances",
  description: "Une introduction à AkashicNET : recherche sur la conscience, expérience vécue, sagesse contemplative et savoir planétaire, sans confondre possibilité et preuve.",
  alternates: {
    canonical: "https://akashicnet.org/fr",
    languages: { en: "https://akashicnet.org/", de: "https://akashicnet.org/de", es: "https://akashicnet.org/es", "pt-BR": "https://akashicnet.org/pt", fr: "https://akashicnet.org/fr", "x-default": "https://akashicnet.org/" },
  },
};

const principles = [
  [
    "Les preuves avant la certitude",
    "Les affirmations restent reliées aux sources, au contexte et à l’incertitude. La ressemblance des mots ne constitue jamais une preuve."
  ],
  [
    "La compassion avant l’échelle",
    "Le soin inspiré par l’idéal du bodhisattva, la réduction des risques et la dignité humaine orientent la manière dont les connaissances sont reliées et partagées."
  ],
  [
    "Le pluralisme sans confusion",
    "Les perspectives scientifiques, philosophiques, contemplatives et vécues peuvent se rencontrer sans être fondues dans une explication unique."
  ],
  [
    "La vie privée comme architecture",
    "L’apprentissage public et les données de travail protégées restent séparés par conception."
  ],
  [
    "La responsabilité demeure humaine",
    "L’automatisation peut aider à la découverte. Le jugement, les valeurs et la responsabilité demeurent humains."
  ],
  [
    "Réviser est une force",
    "Toute carte est provisoire. De meilleures preuves peuvent corriger, approfondir ou dissoudre une connexion antérieure."
  ]
];

export default function LocalizedHome() {
  return <main lang="fr" className={styles.page}>
    <header className={styles.nav}>
      <a className={styles.brand} href="/fr"><img src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span>AKASHICNET.ORG</span></a>
      <nav aria-label="Navigation principale"><a href="#start">Accueil</a><a href="#principles">Principes</a><a href="/big-questions">Grandes questions</a><a href="/support-impact">Soutenir</a><a className={styles.languages} href="/">EN</a><a className={styles.languages} href="/de">DE</a><a className={styles.languages} href="/es">ES</a><a className={styles.languages} href="/pt">PT</a><a className={styles.languages} href="/fr">FR</a></nav>
    </header>
    <section className={styles.hero} id="start">
      <p className={styles.kicker}>Un réseau vivant de connaissances · Introduction française · v0.1</p>
      <h1>S’éveiller intérieurement.<br/><em>Servir au-dehors.</em></h1>
      <p className={styles.lede}>AkashicNET explore comment la recherche sur la conscience, l’expérience vécue, la sagesse contemplative, la créativité et le savoir planétaire pourraient se relier, sans confondre possibilité et preuve.</p>
      <div className={styles.actions}><a href="#principles">Explorer AkashicNET</a><a href="/akashicomni">AkashicOMNI</a><a href="/big-questions/bq001">BQ001 · La conscience continue-t-elle au-delà de l’individu ?</a></div>
      <p className={styles.notice}><strong>Statut de traduction:</strong> introduction éditoriale française v0.1. La version anglaise reste la référence pour les registres techniques, les niveaux de preuve et les versions.</p>
    </section>
    <section className={styles.section} id="principles">
      <p className={styles.kicker}>Comment AkashicNET traite les connaissances</p><h2>Ouvert à l’inconnu. Lié à la responsabilité.</h2>
      <div className={styles.grid}>{principles.map(([title,text],i)=><article className={styles.card} key={title}><h3>{String(i+1).padStart(2,"0")} · {title}</h3><p>{text}</p></article>)}</div>
    </section>
    <section className={styles.section}><div className={styles.boundary}><strong>Limite des preuves:</strong> La signification spirituelle, l’expérience personnelle et les preuves scientifiques ne sont pas considérées comme équivalentes. AkashicNET finance la question, pas la réponse. BQ001 reste NON RÉSOLUE.</div></section>
    <footer className={styles.footer}><a href="/">English</a><a href="/de">Deutsch</a><a href="/es">Español</a><a href="/pt">Português</a><a href="/fr">Français</a><p>La conscience sans limites est un amour infini.</p></footer>
  </main>;
}
