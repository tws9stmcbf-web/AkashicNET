export type EvidenceLabel =
  | 'Established Evidence'
  | 'Interpretation'
  | 'Lived Experience/Testimony'
  | 'Hypothesis'
  | 'Speculation';

export const EVIDENCE_LABELS: readonly EvidenceLabel[] = [
  'Established Evidence', 'Interpretation', 'Lived Experience/Testimony',
  'Hypothesis', 'Speculation',
];

export type Article = {
  id: string;
  title: string;
  canonicalUrl: string;
  summary: string;
  evidenceLabels: EvidenceLabel[];
  reviewStatus: string;
  sourceUrls: string[];
  checkedOn: string;
  boundary: string;
};

export type Flair = { id: string; text: string };

export type Snapshot = {
  schemaVersion: 1;
  catalogVersion: string;
  article: Article;
  title: string;
  summary: string;
  flair: Flair | null;
  body: string;
};

export type Preview = {
  previewId: string;
  expiresAt: number;
  targetSubreddit: string;
  snapshot: Snapshot;
};

export type Published = {
  postId: string;
  url: string;
  duplicate: boolean;
  receiptSaved: boolean;
};

export type Session = {
  subredditName: string;
  isModerator: boolean;
  articles: Article[];
  flairs: Flair[];
  currentSnapshot: Snapshot | null;
  catalogVersion: string;
};

export const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value);

export const isEvidenceLabel = (value: unknown): value is EvidenceLabel =>
  EVIDENCE_LABELS.some((label) => label === value);

export const isFlair = (value: unknown): value is Flair =>
  isRecord(value) && typeof value.id === 'string' && typeof value.text === 'string';

export const isArticle = (value: unknown): value is Article =>
  isRecord(value) && typeof value.id === 'string' &&
  typeof value.title === 'string' && typeof value.canonicalUrl === 'string' &&
  typeof value.summary === 'string' && typeof value.reviewStatus === 'string' &&
  typeof value.checkedOn === 'string' && typeof value.boundary === 'string' &&
  Array.isArray(value.evidenceLabels) && value.evidenceLabels.every(isEvidenceLabel) &&
  Array.isArray(value.sourceUrls) && value.sourceUrls.every((url: unknown) => typeof url === 'string');

export const isSnapshot = (value: unknown): value is Snapshot =>
  isRecord(value) && value.schemaVersion === 1 &&
  typeof value.catalogVersion === 'string' && isArticle(value.article) &&
  typeof value.title === 'string' && typeof value.summary === 'string' &&
  typeof value.body === 'string' && (value.flair === null || isFlair(value.flair));
