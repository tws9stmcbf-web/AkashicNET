import type { Metadata } from "next";
import styles from "../localizedHome.module.css";

export const metadata: Metadata = {
  title: "AkashicNET em português — Uma rede viva de conhecimento",
  description: "Uma introdução à AkashicNET: pesquisa da consciência, experiência vivida, sabedoria contemplativa e conhecimento planetário, sem confundir possibilidade com prova.",
  alternates: {
    canonical: "https://akashicnet.org/pt",
    languages: { en: "https://akashicnet.org/", de: "https://akashicnet.org/de", es: "https://akashicnet.org/es", "pt-BR": "https://akashicnet.org/pt", fr: "https://akashicnet.org/fr", "x-default": "https://akashicnet.org/" },
  },
};

const principles = [
  [
    "Evidência antes da certeza",
    "As afirmações permanecem ligadas às fontes, ao contexto e à incerteza. Palavras semelhantes, por si só, nunca se tornam prova."
  ],
  [
    "Compaixão antes da escala",
    "O cuidado inspirado no ideal do bodhisattva, a redução de danos e a dignidade humana orientam como o conhecimento é conectado e compartilhado."
  ],
  [
    "Pluralismo sem confusão",
    "Perspectivas científicas, filosóficas, contemplativas e vividas podem se encontrar sem serem forçadas a uma única explicação."
  ],
  [
    "Privacidade como arquitetura",
    "O aprendizado público e os dados de trabalho protegidos permanecem separados por projeto."
  ],
  [
    "A responsabilidade permanece humana",
    "A automação pode ajudar na descoberta. O julgamento, os valores e a responsabilidade permanecem humanos."
  ],
  [
    "Revisar é uma força",
    "Todo mapa é provisório. Evidências melhores podem corrigir, aprofundar ou desfazer uma conexão anterior."
  ]
];

export default function LocalizedHome() {
  return <main lang="pt-BR" className={styles.page}>
    <header className={styles.nav}>
      <a className={styles.brand} href="/pt"><img src="/images/akashicnet-toroidal-love-logo.png" alt=""/><span>AKASHICNET.ORG</span></a>
      <nav aria-label="Navegação principal"><a href="#start">Início</a><a href="#principles">Princípios</a><a href="/big-questions">Grandes perguntas</a><a href="/support-impact">Apoiar</a><a className={styles.languages} href="/">EN</a><a className={styles.languages} href="/de">DE</a><a className={styles.languages} href="/es">ES</a><a className={styles.languages} href="/pt" aria-current="page">PT</a><a className={styles.languages} href="/fr">FR</a></nav>
    </header>
    <section className={styles.hero} id="start">
      <p className={styles.kicker}>Uma rede viva de conhecimento · Introdução em português do Brasil · v0.1</p>
      <h1>Despertar por dentro.<br/><em>Servir para fora.</em></h1>
      <p className={styles.lede}>AkashicNET explora como a pesquisa da consciência, a experiência vivida, a sabedoria contemplativa, a criatividade e o conhecimento planetário podem se relacionar, sem confundir possibilidade com prova.</p>
      <div className={styles.actions}><a href="#principles">Explorar AkashicNET</a><a href="/akashicomni">AkashicOMNI</a><a href="/big-questions/bq001">BQ001 · A consciência continua além do indivíduo?</a></div>
      <p className={styles.notice}><strong>Status da tradução:</strong> introdução editorial em português do Brasil v0.1. A versão em inglês continua sendo a referência para registros técnicos, estados das evidências e versões.</p>
    </section>
    <section className={styles.section} id="principles">
      <p className={styles.kicker}>Como AkashicNET trata o conhecimento</p><h2>Aberto ao desconhecido. Vinculado à responsabilidade.</h2>
      <div className={styles.grid}>{principles.map(([title,text],i)=><article className={styles.card} key={title}><h3>{String(i+1).padStart(2,"0")} · {title}</h3><p>{text}</p></article>)}</div>
    </section>
    <section className={styles.section}><div className={styles.boundary}><strong>Limite das evidências:</strong> O significado espiritual, a experiência pessoal e a evidência científica não são tratados como equivalentes. AkashicNET financia a pergunta, não a resposta. A BQ001 permanece NÃO RESOLVIDA.</div></section>
    <footer className={styles.footer}><a href="/">English</a><a href="/de">Deutsch</a><a href="/es">Español</a><a href="/pt">Português</a><a href="/fr">Français</a><p>Consciência sem limites é amor infinito.</p></footer>
  </main>;
}
