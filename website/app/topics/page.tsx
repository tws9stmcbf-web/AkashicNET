import type { Metadata } from "next";
import { topicSeed, topics } from "./data";
import styles from "./topics.module.css";

export const metadata: Metadata = {
  title: "Universal Topic Atlas | AkashicNET",
  description: "A public-safe discovery atlas for potentially any topic, with provenance, uncertainty, rights and connections kept visible.",
};

export default function TopicsPage() {
  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a href="/">AKASHICNET.ORG</a>
        <nav aria-label="Topic atlas navigation">
          <a href="#atlas">Atlas</a>
          <a href="/akashicomni">AkashicOMNI</a>
          <a href="/big-questions">Big Questions</a>
        </nav>
      </header>

      <section className={styles.hero}>
        <p className={styles.eyebrow}>Universal Topic Atlas · v{topicSeed.schema_version} · Exploratory</p>
        <h1>A page for every describable topic.</h1>
        <p>AkashicNET can grow toward a connected page for any subject while preserving what is documented, what is interpreted and what remains unknown.</p>
        <p className={styles.boundary}><strong>Discovery boundary:</strong> appearing in this atlas does not make a topic, claim or connection true. Review and reuse state appear on each record; presence in the atlas does not imply approval or publication.</p>
      </section>

      <section className={styles.content} id="atlas">
        <div className={styles.filters}>
          <div>
            <p className={styles.eyebrow}>Initial cross-domain seed</p>
            <h2>From neurons to galaxies</h2>
          </div>
          <p className={styles.count}>{topics.length} topic records · {topicSeed.registries.length} registries</p>
        </div>
        <div className={styles.grid}>
          {topics.map((topic) => (
            <a className={styles.card} href={`/topics/${topic.slug}`} key={topic.id}>
              <span>{topic.id} · {topic.domain}</span>
              <h3>{topic.label}</h3>
              <p>{topic.summary}</p>
              <strong>{topic.status} · {topic.rights.mode} →</strong>
            </a>
          ))}
        </div>
      </section>

      <footer className={styles.footer}>
        <a href="/">AKASHICNET.ORG</a>
        <p>Fund the question, not the answer.</p>
      </footer>
    </main>
  );
}
