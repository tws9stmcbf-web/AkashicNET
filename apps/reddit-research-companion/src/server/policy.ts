import type { Article, Flair, Snapshot } from '../shared/model.js';
import { isRecord } from '../shared/model.js';
import { CATALOG_VERSION } from '../shared/catalog.js';

export class AppError extends Error {
  constructor(public readonly status: 400 | 403 | 404 | 409 | 410 | 413 | 429 | 503, message: string) {
    super(message);
  }
}

export type DraftInput = { articleId: string; title: string; summary: string; flairId: string | null };

const plainText = (value: unknown, label: string, minimum: number, maximum: number): string => {
  if (typeof value !== 'string') throw new AppError(400, `${label} is required.`);
  const text = value.trim();
  if (text.length < minimum || text.length > maximum || /[\u0000-\u0008\u000b-\u001f\u007f]/u.test(text)) {
    throw new AppError(400, `${label} must contain ${minimum}–${maximum} printable characters.`);
  }
  return text;
};

export const parseDraftInput = (value: unknown): DraftInput => {
  if (!isRecord(value)) throw new AppError(400, 'A draft object is required.');
  const articleId = plainText(value.articleId, 'Article', 1, 64);
  const title = plainText(value.title, 'Title', 10, 300);
  if (/[\r\n\t]/u.test(title)) throw new AppError(400, 'Title must fit on one line.');
  const summary = plainText(value.summary, 'Summary', 40, 2000);
  const flairId = value.flairId === null ? null : plainText(value.flairId, 'Flair', 1, 100);
  return { articleId, title, summary, flairId };
};

// Moderator prose is deliberately plain text: it cannot replace the fixed source links.
const escapeMarkdown = (text: string): string => text.replace(/([\\`*_{}\[\]()<>#+.!|~>-])/gu, '\\$1');

export const buildSnapshot = (input: DraftInput, articles: Article[], flairs: Flair[]): Snapshot => {
  const article = articles.find((item) => item.id === input.articleId);
  if (!article) throw new AppError(400, 'Select an article from the public catalog.');
  const canonical = new URL(article.canonicalUrl);
  if (canonical.protocol !== 'https:' || canonical.hostname !== 'akashicnet.org' || canonical.username || canonical.password) {
    throw new AppError(400, 'The catalog article does not have an approved canonical URL.');
  }
  const flair = input.flairId === null ? null : flairs.find((item) => item.id === input.flairId);
  if (flair === undefined) throw new AppError(400, 'Select a current subreddit flair.');
  const body = [
    escapeMarkdown(input.summary),
    `**Claim types:** ${article.evidenceLabels.join(' · ')}`,
    `**Research status:** ${escapeMarkdown(article.reviewStatus)}`,
    `**Boundary:** ${escapeMarkdown(article.boundary)}`,
    `**Canonical article:** ${article.canonicalUrl}`,
    '**Source trail:**\n' + article.sourceUrls.map((url) => `- ${url}`).join('\n'),
    `Public-page snapshot checked ${article.checkedOn}; catalog ${CATALOG_VERSION}. This is an editorial description, not an independent scientific appraisal. Consult the article for its primary references and later corrections.`,
    'Prepared with the AkashicNET Research Companion and reviewed for publication by a community moderator. Posted by the app account. Claim labels do not establish truth or confer scientific endorsement.',
  ].join('\n\n');
  return { schemaVersion: 1, catalogVersion: CATALOG_VERSION, article, title: input.title, summary: input.summary, flair, body };
};
