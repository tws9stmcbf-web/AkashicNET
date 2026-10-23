import './style.css';
import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { navigateTo } from '@devvit/web/client';
import { loadSession, request } from './api.js';
import type { Article, Preview, Published, Session, Snapshot } from '../shared/model.js';
import { EVIDENCE_LABELS } from '../shared/model.js';

const ArticleView = ({ snapshot }: { snapshot: Snapshot }) => <section className="panel published">
  <p className="eyebrow">PUBLISHED DISCUSSION · SAVED SNAPSHOT</p>
  <h2>{snapshot.title}</h2><p>{snapshot.summary}</p>
  <div className="badges">{snapshot.article.evidenceLabels.map((label) => <span key={label}>{label}</span>)}</div>
  <p className="status">{snapshot.article.reviewStatus}</p>
  <p className="boundary">{snapshot.article.boundary}</p>
  <button onClick={() => navigateTo(snapshot.article.canonicalUrl)}>Read the canonical article ↗</button>
  <details><summary>Read the exact published text and source trail</summary><pre>{snapshot.body}</pre></details>
</section>;

export const Companion = () => {
  const [session, setSession] = useState<Session | null>(null);
  const [selectedId, setSelectedId] = useState('');
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [flairId, setFlairId] = useState('');
  const [query, setQuery] = useState('');
  const [label, setLabel] = useState('');
  const [preview, setPreview] = useState<Preview | null>(null);
  const [published, setPublished] = useState<Published | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setError('');
    try { setSession(await loadSession()); } catch (failure) { setError(failure instanceof Error ? failure.message : 'Unable to load the companion.'); }
  };
  useEffect(() => { void load(); }, []);

  const selectArticle = (article: Article) => {
    setSelectedId(article.id); setTitle(article.title); setSummary(article.summary);
    setFlairId(''); setPreview(null); setPublished(null); setError('');
  };
  const change = (setter: (text: string) => void, text: string) => { setter(text); setPreview(null); setPublished(null); };
  const makePreview = async () => {
    setBusy(true); setError(''); setPublished(null); setPreview(null);
    try { setPreview(await request<Preview>('/api/preview', { articleId: selectedId, title, summary, flairId: flairId || null })); }
    catch (failure) { setError(failure instanceof Error ? failure.message : 'Unable to generate a preview.'); }
    finally { setBusy(false); }
  };
  const publish = async () => {
    if (!preview) return;
    setBusy(true); setError('');
    try { setPublished(await request<Published>('/api/publish', { previewId: preview.previewId })); }
    catch (failure) { setError(failure instanceof Error ? failure.message : 'Unable to confirm publication.'); }
    finally { setBusy(false); }
  };

  if (!session) return <main className="shell"><h1>Research Companion</h1><p role="status">{error || 'Loading public articles…'}</p>{error && <button onClick={() => void load()}>Retry</button>}</main>;
  const articles = session.articles.filter((article) => (!label || article.evidenceLabels.some((item) => item === label)) &&
    `${article.title} ${article.summary} ${article.reviewStatus}`.toLowerCase().includes(query.toLowerCase()));
  const selected = session.articles.find((article) => article.id === selectedId);

  return <main className="shell">
    <header><div><p className="eyebrow">AKASHICNET × COMMUNITY INQUIRY</p><h1>Research Companion <span aria-hidden="true">∞</span></h1></div><span className="mode">{session.isModerator ? 'Moderator' : 'Reader'} · r/{session.subredditName}</span></header>
    <p className="intro">Explore freely. Document carefully. Keep the uncertainty visible.</p>
    {session.currentSnapshot && <ArticleView snapshot={session.currentSnapshot} />}
    <section aria-labelledby="catalog-title">
      <h2 id="catalog-title">Explore the public library</h2>
      <p className="muted">A small curated snapshot. Open each article for its current wording and primary references.</p>
      <div className="filters"><label>Search articles<input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Consciousness, intention…" /></label>
        <label>Claim type<select value={label} onChange={(event) => setLabel(event.target.value)}><option value="">All claim types</option>{EVIDENCE_LABELS.map((item) => <option key={item}>{item}</option>)}</select></label></div>
      <div className="cards">{articles.map((article) => <article className={`panel ${selectedId === article.id ? 'selected' : ''}`} key={article.id}>
        <p className="eyebrow">{article.id.toUpperCase()}</p><h3>{article.title}</h3><p>{article.summary}</p>
        <div className="badges">{article.evidenceLabels.map((item) => <span key={item}>{item}</span>)}</div>
        <p className="status">{article.reviewStatus}</p><p className="boundary">{article.boundary}</p>
        <div className="actions"><button onClick={() => navigateTo(article.canonicalUrl)}>Read article ↗</button>{session.isModerator && <button disabled={busy} className="primary" onClick={() => selectArticle(article)}>Prepare discussion</button>}</div>
      </article>)}</div>
      {articles.length === 0 && <p role="status">No articles match these filters.</p>}
    </section>
    {session.isModerator && selected && <section className="panel composer" aria-labelledby="compose-title">
      <p className="eyebrow">MODERATOR WORKSPACE</p><h2 id="compose-title">Prepare a discussion</h2>
      <p>Publishing creates an interactive Reddit post under the app account in <strong>r/{session.subredditName}</strong>. The saved text and source trail also appear in its text fallback.</p>
      <fieldset disabled={busy || Boolean(published)}><label>Post title<input value={title} maxLength={300} onChange={(event) => change(setTitle, event.target.value)} /></label>
      <label>Plain-text summary<textarea value={summary} maxLength={2000} rows={5} onChange={(event) => change(setSummary, event.target.value)} /></label>
      <label>Subreddit flair<select value={flairId} onChange={(event) => change(setFlairId, event.target.value)}><option value="">No flair</option>{session.flairs.map((item) => <option value={item.id} key={item.id}>{item.text}</option>)}</select></label>
      <button className="primary" onClick={() => void makePreview()}>Preview exact post</button></fieldset>
      <p className="muted">Claim types, research status and source links are preserved from the curated article snapshot.</p>
      {preview && <section className="preview" aria-label="Exact publication preview">
        <p className="eyebrow">EXACT PREVIEW · r/{preview.targetSubreddit}</p><h3>{preview.snapshot.title}</h3>
        <p>Flair: {preview.snapshot.flair?.text ?? 'None'} · Preview expires {new Date(preview.expiresAt).toLocaleTimeString()}</p>
        <pre>{preview.snapshot.body}</pre>
        {!published && <button disabled={busy} className="primary" onClick={() => void publish()}>{busy ? 'Publishing…' : `Publish this post to r/${preview.targetSubreddit}`}</button>}
      </section>}
      {published && <div className="success" role="status"><p>{published.duplicate ? 'This exact post already exists.' : 'Your discussion was published.'}</p><button onClick={() => navigateTo(published.url)}>Open Reddit post ↗</button>{!published.receiptSaved && <p>The post exists, but its receipt could not be saved. Keep this link and check the subreddit before any further attempt.</p>}</div>}
    </section>}
    {error && <p role="alert" className="error">{error}</p>}
    <footer><p>Catalog {session.catalogVersion} · Public-page descriptions, not independent scientific appraisals.</p><p>Community discussion and vivid experiences do not establish a mechanism or settle an open question.</p><button onClick={() => navigateTo('https://akashicnet.org')}>Explore AkashicNET ↗</button></footer>
  </main>;
};

const root = document.getElementById('root');
if (root) createRoot(root).render(<Companion />);
