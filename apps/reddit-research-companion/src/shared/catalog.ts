import type { Article } from './model.js';

export const CATALOG_VERSION = '2026-10-22.1';

// A manually curated public-page snapshot, not a scientific appraisal or live feed.
// Source URLs are navigation links; this pilot makes no external HTTP requests.
export const ARTICLES: Article[] = [
  {
    id: 'bq001',
    title: 'Does Consciousness Continue Beyond The Individual?',
    canonicalUrl: 'https://akashicnet.org/big-questions/bq001',
    summary: 'BQ001 compares competing accounts of consciousness and records questions that could distinguish them. Its conclusion remains open, with mixed, non-decisive evidence.',
    evidenceLabels: ['Interpretation', 'Lived Experience/Testimony', 'Hypothesis'],
    reviewStatus: 'Open question; no definitive answer',
    sourceUrls: ['https://akashicnet.org/big-questions/bq001'],
    checkedOn: '2026-10-22',
    boundary: 'Research activity and the page\'s maturity indicators are not probabilities of survival, evidence grades or scientific verdicts.',
  },
  {
    id: 'intention-awareness',
    title: 'Before The Words: Intention Awareness (Telepathy?)',
    canonicalUrl: 'https://akashicnet.org/intention-awareness',
    summary: 'A proposed blinded experiment asks whether receivers can identify randomly assigned intended actions beyond ordinary cues. Sending trials would be compared with no-sending controls. No experiment has been conducted.',
    evidenceLabels: ['Hypothesis'],
    reviewStatus: 'Untested hypothesis; proposed protocol; no experimental results',
    sourceUrls: ['https://akashicnet.org/intention-awareness'],
    checkedOn: '2026-10-22',
    boundary: 'This is a design proposal, not a validated test of ability, recruitment invitation or established finding. The final protocol and analysis remain to be settled.',
  },
];
