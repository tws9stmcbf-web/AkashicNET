import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { findTopic, labelForSlug, topics } from "../data";
import styles from "../topics.module.css";

export function generateStaticParams() {
  return topics.map((topic) => ({ slug: topic.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const topic = findTopic(slug);
  if (!topic) return { title: "Topic not found | AkashicNET" };
  return {
    title: `${topic.label} | AkashicNET Topic Atlas`,
    description: topic.summary,
  };
}

export default async function TopicPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const topic = findTopic(slug);
  if (!topic) notFound();

  return (
    <main className={styles.page}>
      <header className={styles.nav}>
        <a href="/">AKASHICNET.ORG</a>
        <nav aria-label="Topic navigation">
          <a href="/topics">All topics</a>
          <a href="/akashicomni">AkashicOMNI</a>
          <a href="/big-questions">Big Questions</a>
        </nav>
      </header>

      <section className={`${styles.hero} ${styles.topicHeader}`}>
        <p className={styles.eyebrow}>{topic.id} · {topic.domain}</p>
        <h1>{topic.label}</h1>
        <p>{topic.summary}</p>
        <span className={styles.status}>{topic.status} · metadata only</span>
        <p className={styles.boundary}><strong>Evidence boundary:</strong> this is an unreviewed discovery record, not an authoritative article. Connections are hypotheses until supported by record-level sources.</p>
      </section>

      <section className={styles.content}>
        <div className={styles.sections}>
          <article className={styles.panel}>
            <h2>Documentary trace</h2>
            <p>{topic.origin.documentary_trace ?? "Not yet established."}</p>
            <p><strong>Ultimate-origin status:</strong> {topic.origin.ultimate_status}</p>
            <p>{topic.origin.evidence_note}</p>
          </article>

          <article className={styles.panel}>
            <h2>Entities</h2>
            {topic.entities.length ? (
              <ul>{topic.entities.map((entity) => <li key={entity.id ?? entity.label}>{entity.label} · {entity.entity_status} · {entity.ontological_status}</li>)}</ul>
            ) : <p>No entity record has been assigned. Absence of an entity is not evidence for or against agency.</p>}
          </article>

          <article className={`${styles.panel} ${styles.wide}`}>
            <h2>Candidate connections</h2>
            {topic.connections.length ? (
              <ul>
                {topic.connections.map((connection) => {
                  const internal = findTopic(connection.target);
                  return (
                    <li key={`${connection.target}-${connection.relation}`}>
                      {internal ? <a href={`/topics/${connection.target}`}>{internal.label}</a> : labelForSlug(connection.target)}
                      {" · "}{connection.relation} · {connection.edge_status}
                    </li>
                  );
                })}
              </ul>
            ) : <p>No candidate connections recorded.</p>}
          </article>

          {topic.solution_space && (
            <article className={`${styles.panel} ${styles.wide}`}>
              <h2>Possible solutions and alternatives</h2>
              <p><strong>Assessment status:</strong> {topic.solution_space.status}. These candidates are options for comparison, not universal prescriptions.</p>
              <p><strong>Quality dimensions:</strong> {topic.solution_space.quality_dimensions.join(" · ")}</p>
              {topic.solution_space.candidates.map((candidate) => (
                <section key={candidate.label}>
                  <h3>{candidate.label}</h3>
                  <p>{candidate.level} · evidence: {candidate.evidence_status}</p>
                  <p><strong>Potential benefits:</strong> {candidate.potential_benefits.join(", ")}</p>
                  <p><strong>Tradeoffs:</strong> {candidate.tradeoffs.join(", ")}</p>
                </section>
              ))}
            </article>
          )}

          <article className={styles.panel}>
            <h2>Open questions</h2>
            <ul>{topic.open_questions.map((question) => <li key={question}>{question}</li>)}</ul>
          </article>

          <article className={styles.panel}>
            <h2>Sources and rights</h2>
            {topic.sources.length ? (
              <ul>{topic.sources.map((source) => <li key={source.id}><a href={source.url}>{source.id}</a> · {source.source_type} · {source.evidence_role}</li>)}</ul>
            ) : <p>No record-level sources have passed review yet.</p>}
            <p><strong>Reuse mode:</strong> {topic.rights.mode}</p>
            <p>{topic.rights.note}</p>
          </article>

          <article className={`${styles.panel} ${styles.wide} ${styles.warning}`}>
            <h2>Review state</h2>
            <p>{topic.review.notes}</p>
            <p><strong>Human reviewed:</strong> {topic.review.human_reviewed ? "yes" : "no"} · <strong>Last reviewed:</strong> {topic.review.last_reviewed ?? "not yet"}</p>
          </article>
        </div>
      </section>

      <footer className={styles.footer}>
        <a href="/topics">← Universal Topic Atlas</a>
        <p>Unknown is a valid answer.</p>
      </footer>
    </main>
  );
}
