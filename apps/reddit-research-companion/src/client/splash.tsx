import './style.css';
import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { requestExpandedMode } from '@devvit/web/client';
import { loadSession } from './api.js';
import type { Session } from '../shared/model.js';

export const Splash = () => {
  const [session, setSession] = useState<Session | null>(null);
  const [error, setError] = useState('');
  useEffect(() => { void loadSession().then(setSession).catch(() => setError('Open the companion to retry loading this post.')); }, []);
  const snapshot = session?.currentSnapshot;
  return <main className="splash">
    <div className="orb" aria-hidden="true">∞</div>
    <p className="eyebrow">AKASHICNET · RESEARCH COMPANION</p>
    <h1>{snapshot?.title ?? 'Follow the question.'}</h1>
    <p>{snapshot?.summary ?? 'Explore the sources. Keep the uncertainty visible.'}</p>
    <div className="badges">{snapshot?.article.evidenceLabels.map((label) => <span key={label}>{label}</span>)}</div>
    {snapshot && <p className="status">{snapshot.article.reviewStatus}</p>}
    <button className="primary" onClick={(event) => requestExpandedMode(event.nativeEvent, 'companion')}>Open Research Companion ↗</button>
    {error && <p role="status">{error}</p>}
    <small>Questions welcome. Claim labels are not scientific verdicts.</small>
  </main>;
};

const root = document.getElementById('root');
if (root) createRoot(root).render(<Splash />);
