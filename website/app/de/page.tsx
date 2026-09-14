import type { Metadata } from "next";
import styles from "../localizedHome.module.css";

export const metadata: Metadata = {
  title: "AkashicNET auf Deutsch — Ein lebendiges Wissensnetz",
  description: "AkashicNET verbindet Bewusstseinsforschung, gelebte Erfahrung, kontemplative Weisheit, Kreativität und planetarisches Wissen – ohne Möglichkeit mit Beweis zu verwechseln.",
  alternates: {
    canonical: "https://akashicnet.org/de",
    languages: { en: "https://akashicnet.org/", de: "https://akashicnet.org/de", es: "https://akashicnet.org/es", "pt-BR": "https://akashicnet.org/pt", fr: "https://akashicnet.org/fr", "x-default": "https://akashicnet.org/" },
  },
};

const principles = [
  ["Evidenz vor Gewissheit", "Aussagen bleiben mit Quellen, Kontext und Unsicherheit verbunden. Ähnliche Begriffe allein sind kein Beweis."],
  ["Mitgefühl vor Reichweite", "Bodhisattva-inspirierte Fürsorge, Schadensminderung und Menschenwürde bestimmen, wie Wissen geteilt wird."],
  ["Pluralismus ohne Vermischung", "Wissenschaftliche, philosophische, kontemplative und gelebte Perspektiven dürfen einander begegnen, ohne zu einer Erklärung verschmolzen zu werden."],
  ["Privatsphäre als Architektur", "Öffentliches Lernen und geschützte Arbeitsdaten bleiben grundsätzlich getrennt."],
  ["Menschen bleiben verantwortlich", "Automatisierung unterstützt die Entdeckung. Urteil, Werte und Verantwortung bleiben menschlich."],
  ["Revision ist eine Stärke", "Jede Karte ist vorläufig. Bessere Evidenz darf frühere Verbindungen korrigieren oder auflösen."],
];

export default function GermanHome() {
  return <main lang="de" className={styles.page}>
    <header className={styles.nav}>
      <a className={styles.brand} href="/de"><img src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span>AKASHICNET.ORG</span></a>
      <nav aria-label="Hauptnavigation"><a href="#beginn">Start</a><a href="#prinzipien">Prinzipien</a><a href="/big-questions">Große Fragen</a><a href="/support-impact">Unterstützen</a><a className={styles.languages} href="/">EN</a><a className={styles.languages} href="/de" aria-current="page">DE</a><a className={styles.languages} href="/es">ES</a><a className={styles.languages} href="/pt">PT</a><a className={styles.languages} href="/fr">FR</a></nav>
    </header>
    <section className={styles.hero} id="beginn">
      <p className={styles.kicker}>Ein lebendiges Wissensnetz · Deutsche Einführung · v0.1</p>
      <h1>Im Inneren erwachen.<br/><em>Nach außen dienen.</em></h1>
      <p className={styles.lede}>AkashicNET untersucht, wie Bewusstseinsforschung, gelebte Erfahrung, kontemplative Weisheit, Kreativität und planetarisches Wissen zusammenhängen könnten, ohne Möglichkeit mit Beweis zu verwechseln.</p>
      <div className={styles.actions}><a href="#prinzipien">AkashicNET entdecken</a><a href="/akashicomni">AkashicOMNI</a><a href="/big-questions/bq001">BQ001 · Bewusstsein nach dem Individuum?</a></div>
      <p className={styles.notice}><strong>Übersetzungsstatus:</strong> redaktionell erstellte deutsche Einführung v0.1. Die englische Fassung bleibt für technische Register, Evidenzstände und Versionsangaben maßgeblich.</p>
    </section>
    <section className={styles.section} id="prinzipien">
      <p className={styles.kicker}>Wie AkashicNET Wissen behandelt</p><h2>Offen für das Unbekannte. Gebunden an Verantwortung.</h2>
      <div className={styles.grid}>{principles.map(([title,text],i)=><article className={styles.card} key={title}><h3>{String(i+1).padStart(2,"0")} · {title}</h3><p>{text}</p></article>)}</div>
    </section>
    <section className={styles.section}><div className={styles.boundary}><strong>Evidenzgrenze:</strong> Spirituelle Bedeutung, persönliche Erfahrung und wissenschaftliche Evidenz werden nicht gleichgesetzt. AkashicNET finanziert die Frage, nicht die Antwort. BQ001 bleibt UNGEKLÄRT.</div></section>
    <footer className={styles.footer}><a href="/">English</a><a href="/de">Deutsch</a><a href="/es">Español</a><a href="/pt">Português</a><a href="/fr">Français</a><p>Grenzenloses Bewusstsein ist unendliche Liebe.</p></footer>
  </main>;
}
