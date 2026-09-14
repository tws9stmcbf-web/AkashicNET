import type { Metadata } from "next";
import styles from "../localizedHome.module.css";

export const metadata: Metadata = {
  title: "AkashicNET en español — Una red viva de conocimiento",
  description: "Una introducción a AkashicNET: investigación de la consciencia, experiencia vivida, sabiduría contemplativa y conocimiento planetario, sin confundir posibilidad con prueba.",
  alternates: {
    canonical: "https://akashicnet.org/es",
    languages: { en: "https://akashicnet.org/", de: "https://akashicnet.org/de", es: "https://akashicnet.org/es", "pt-BR": "https://akashicnet.org/pt", fr: "https://akashicnet.org/fr", "x-default": "https://akashicnet.org/" },
  },
};

const principles = [
  [
    "Evidencia antes que certeza",
    "Las afirmaciones permanecen vinculadas a sus fuentes, contexto e incertidumbre. La similitud de palabras nunca constituye una prueba."
  ],
  [
    "Compasión antes que escala",
    "El cuidado inspirado en el ideal del bodhisattva, la reducción de daños y la dignidad humana orientan cómo se conecta y comparte el conocimiento."
  ],
  [
    "Pluralismo sin confusión",
    "Las perspectivas científicas, filosóficas, contemplativas y vividas pueden encontrarse sin ser forzadas a una sola explicación."
  ],
  [
    "La privacidad como arquitectura",
    "El aprendizaje público y los datos de trabajo protegidos se mantienen separados por diseño."
  ],
  [
    "La responsabilidad sigue siendo humana",
    "La automatización puede ayudar a descubrir. El juicio, los valores y la responsabilidad siguen siendo humanos."
  ],
  [
    "Revisar es una fortaleza",
    "Todo mapa es provisional. Una evidencia mejor puede corregir, profundizar o disolver una conexión anterior."
  ]
];

export default function LocalizedHome() {
  return <main lang="es" className={styles.page}>
    <header className={styles.nav}>
      <a className={styles.brand} href="/es"><img src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span>AKASHICNET.ORG</span></a>
      <nav aria-label="Navegación principal"><a href="#start">Inicio</a><a href="#principles">Principios</a><a href="/big-questions">Grandes preguntas</a><a href="/support-impact">Apoyar</a><a className={styles.languages} href="/">EN</a><a className={styles.languages} href="/de">DE</a><a className={styles.languages} href="/es">ES</a><a className={styles.languages} href="/pt">PT</a><a className={styles.languages} href="/fr">FR</a></nav>
    </header>
    <section className={styles.hero} id="start">
      <p className={styles.kicker}>Una red viva de conocimiento · Introducción en español · v0.1</p>
      <h1>Despertar por dentro.<br/><em>Servir hacia fuera.</em></h1>
      <p className={styles.lede}>AkashicNET explora cómo podrían relacionarse la investigación de la consciencia, la experiencia vivida, la sabiduría contemplativa, la creatividad y el conocimiento planetario, sin confundir posibilidad con prueba.</p>
      <div className={styles.actions}><a href="#principles">Explorar AkashicNET</a><a href="/akashicomni">AkashicOMNI</a><a href="/big-questions/bq001">BQ001 · ¿Continúa la consciencia más allá del individuo?</a></div>
      <p className={styles.notice}><strong>Estado de traducción:</strong> introducción editorial en español v0.1. La versión inglesa sigue siendo la referencia para los registros técnicos, estados de evidencia y versiones.</p>
    </section>
    <section className={styles.section} id="principles">
      <p className={styles.kicker}>Cómo trata AkashicNET el conocimiento</p><h2>Abierto a lo desconocido. Vinculado a la responsabilidad.</h2>
      <div className={styles.grid}>{principles.map(([title,text],i)=><article className={styles.card} key={title}><h3>{String(i+1).padStart(2,"0")} · {title}</h3><p>{text}</p></article>)}</div>
    </section>
    <section className={styles.section}><div className={styles.boundary}><strong>Límite de evidencia:</strong> El significado espiritual, la experiencia personal y la evidencia científica no se tratan como equivalentes. AkashicNET financia la pregunta, no la respuesta. BQ001 permanece SIN RESOLVER.</div></section>
    <footer className={styles.footer}><a href="/">English</a><a href="/de">Deutsch</a><a href="/es">Español</a><a href="/pt">Português</a><a href="/fr">Français</a><p>La consciencia ilimitada es amor infinito.</p></footer>
  </main>;
}
