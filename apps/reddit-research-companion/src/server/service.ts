import { createHash, randomUUID } from 'node:crypto';
import { ARTICLES, CATALOG_VERSION } from '../shared/catalog.js';
import type { Flair, Preview, Published, Session, Snapshot } from '../shared/model.js';
import { isRecord, isSnapshot } from '../shared/model.js';
import { AppError, buildSnapshot, parseDraftInput } from './policy.js';

export type Actor = {
  userId: string | undefined;
  postId: string | undefined;
  subredditName: string;
  canPublish: boolean;
};

export type Store = {
  get(key: string): Promise<string | undefined>;
  set(key: string, value: string, options?: { ttlSeconds?: number; onlyIfAbsent?: boolean }): Promise<boolean>;
};

export type Dependencies = {
  actor(): Promise<Actor>;
  flairs(subredditName: string): Promise<Flair[]>;
  store: Store;
  publish(snapshot: Snapshot, snapshotId: string, subredditName: string): Promise<{ postId: string; url: string }>;
  createLauncher(subredditName: string): Promise<{ postId: string; url: string }>;
  snapshotId(): string | undefined;
  now?: () => number;
};

type StoredDraft = Preview & { userId: string; postId: string };
const parseJson = (raw: string): unknown => JSON.parse(raw);
const isStoredDraft = (value: unknown): value is StoredDraft =>
  isRecord(value) && typeof value.previewId === 'string' &&
  typeof value.expiresAt === 'number' && Number.isFinite(value.expiresAt) &&
  typeof value.targetSubreddit === 'string' && typeof value.userId === 'string' &&
  typeof value.postId === 'string' && isSnapshot(value.snapshot);

const requireModerator = (actor: Actor): string => {
  if (!actor.userId || !actor.canPublish || !actor.subredditName) {
    throw new AppError(403, 'A moderator with post permissions is required.');
  }
  return actor.userId;
};

const draftKey = (actor: Actor): string => `draft:v1:${actor.subredditName.toLowerCase()}:${actor.userId}:${actor.postId}`;
const digest = (snapshot: Snapshot): string => createHash('sha256').update(JSON.stringify(snapshot)).digest('hex');

const readReceipt = (raw: string | undefined): Published | null => {
  if (!raw) return null;
  const value = parseJson(raw);
  if (isRecord(value) && value.state === 'published' && typeof value.postId === 'string' && typeof value.url === 'string') {
    return { postId: value.postId, url: value.url, duplicate: true, receiptSaved: true };
  }
  throw new AppError(409, 'This publication is already processing or its outcome needs reconciliation. Check the subreddit before taking further action.');
};

export const createService = (deps: Dependencies) => {
  const now = deps.now ?? Date.now;

  const session = async (): Promise<Session> => {
    const actor = await deps.actor();
    const snapshotId = deps.snapshotId();
    let currentSnapshot: Snapshot | null = null;
    if (snapshotId) {
      const raw = await deps.store.get(`snapshot:v1:${snapshotId}`);
      const parsed = raw ? parseJson(raw) : null;
      if (!isSnapshot(parsed)) throw new AppError(410, 'This post\'s saved snapshot is unavailable. Please consult its text fallback or canonical article.');
      currentSnapshot = parsed;
    }
    return {
      subredditName: actor.subredditName,
      isModerator: Boolean(actor.userId && actor.canPublish),
      articles: ARTICLES,
      flairs: actor.userId && actor.canPublish ? await deps.flairs(actor.subredditName) : [],
      currentSnapshot,
      catalogVersion: CATALOG_VERSION,
    };
  };

  const preview = async (value: unknown): Promise<Preview> => {
    const actor = await deps.actor();
    const userId = requireModerator(actor);
    if (!actor.postId) throw new AppError(400, 'Open the companion inside a Reddit post.');
    const snapshot = buildSnapshot(parseDraftInput(value), ARTICLES, await deps.flairs(actor.subredditName));
    const result: StoredDraft = {
      previewId: randomUUID(), expiresAt: now() + 600_000,
      targetSubreddit: actor.subredditName, userId, postId: actor.postId, snapshot,
    };
    const stored = await deps.store.set(draftKey(actor), JSON.stringify(result), { ttlSeconds: 600 });
    if (!stored) throw new AppError(503, 'The preview could not be saved. Please try again.');
    return { previewId: result.previewId, expiresAt: result.expiresAt, targetSubreddit: result.targetSubreddit, snapshot };
  };

  const publish = async (value: unknown): Promise<Published> => {
    const actor = await deps.actor();
    const userId = requireModerator(actor);
    if (!actor.postId || !isRecord(value) || typeof value.previewId !== 'string' || value.previewId.length > 64) {
      throw new AppError(400, 'An exact preview is required before publication.');
    }
    const raw = await deps.store.get(draftKey(actor));
    const saved = raw ? parseJson(raw) : null;
    if (!isStoredDraft(saved) || saved.previewId !== value.previewId || saved.userId !== userId ||
        saved.postId !== actor.postId || saved.targetSubreddit !== actor.subredditName) {
      throw new AppError(404, 'This preview is unavailable. Generate a new preview.');
    }
    if (saved.expiresAt <= now()) throw new AppError(410, 'The preview expired. Review a new preview before publishing.');
    if (saved.snapshot.flair) {
      const expected = saved.snapshot.flair;
      const current = await deps.flairs(actor.subredditName);
      if (!current.some((flair) => flair.id === expected.id && flair.text === expected.text)) {
        throw new AppError(409, 'The selected flair changed. Generate a new preview.');
      }
    }

    const snapshotId = digest(saved.snapshot);
    const receiptKey = `publish:v1:${actor.subredditName.toLowerCase()}:${snapshotId}`;
    const previous = readReceipt(await deps.store.get(receiptKey));
    if (previous) return previous;

    // Persistent NX claim: never automatically release after an ambiguous Reddit failure.
    // This also protects identical previews created by different moderators.
    const claimed = await deps.store.set(receiptKey, JSON.stringify({ state: 'pending' }), { onlyIfAbsent: true });
    if (!claimed) {
      const existing = readReceipt(await deps.store.get(receiptKey));
      if (existing) return existing;
      throw new AppError(409, 'Publication is already processing.');
    }
    try {
      const stored = await deps.store.set(`snapshot:v1:${snapshotId}`, JSON.stringify(saved.snapshot));
      if (!stored) throw new Error('Snapshot persistence failed');
      const post = await deps.publish(saved.snapshot, snapshotId, actor.subredditName);
      let receiptSaved = false;
      try {
        receiptSaved = await deps.store.set(receiptKey, JSON.stringify({ state: 'published', ...post }));
      } catch {
        // The post already exists. Return its URL; do not retry submission.
      }
      return { ...post, duplicate: false, receiptSaved };
    } catch {
      throw new AppError(503, 'Publication could not be confirmed. This draft remains locked to prevent a duplicate. Check the subreddit and reconcile the outcome before another attempt.');
    }
  };

  const launcher = async (): Promise<Published> => {
    const actor = await deps.actor();
    requireModerator(actor);
    const key = `launcher:v1:${actor.subredditName.toLowerCase()}`;
    const previous = readReceipt(await deps.store.get(key));
    if (previous) return previous;
    const claimed = await deps.store.set(key, JSON.stringify({ state: 'pending' }), { onlyIfAbsent: true });
    if (!claimed) throw new AppError(409, 'The companion post is already being created.');
    try {
      const post = await deps.createLauncher(actor.subredditName);
      let receiptSaved = false;
      try { receiptSaved = await deps.store.set(key, JSON.stringify({ state: 'published', ...post })); } catch { /* Keep the pending claim. */ }
      return { ...post, duplicate: false, receiptSaved };
    } catch {
      throw new AppError(503, 'Companion post creation could not be confirmed. Check the subreddit before retrying.');
    }
  };

  return { session, preview, publish, launcher };
};
