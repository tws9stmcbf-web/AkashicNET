import { createHash } from 'node:crypto';
import { N2N_MANIFEST } from './generated/n2n-manifest.js';
import { AppError } from './policy.js';
import { isRecord } from '../shared/model.js';
import type { MetadataBatch, MetadataObservation } from '../shared/metadata.js';
import type { Actor, Store } from './service.js';

export type MetadataPost = {
  id: string; subredditName: string; title: string; flair?: { text?: string };
  createdAt: Date; url: string; score: number; numberOfComments: number;
  removedByCategory?: string;
  isRemoved(): boolean; isSpam(): boolean; isNsfw(): boolean; isQuarantined(): boolean;
};
export type MetadataDependencies = {
  actor(): Promise<Actor>; store: Store; readPost(id: `t3_${string}`): Promise<MetadataPost>;
  now?: () => number;
};

// Stateless content capture: no titles, flair, submitted URLs or user data are
// retained in Redis. Only a short-lived rate-limit key is stored server-side.
// Each returned packet carries its own cursor; the operator keeps reviewed
// packets outside this app only under an approved deletion/refresh workflow.
export const createMetadataScanner = (deps: MetadataDependencies) => {
  const now = deps.now ?? Date.now;
  const requireActor = async () => {
    const actor = await deps.actor();
    if (!actor.userId || !actor.canPublish || !actor.subredditName || !actor.postId) throw new AppError(403, 'Open the companion as a moderator with post permissions.');
    return actor;
  };
  const plan = async () => {
    const actor = await requireActor();
    return { targetSubreddit: 'NeuronsToNirvana', knownIds: N2N_MANIFEST.known_id_count,
      manifestSha256: N2N_MANIFEST.ids_sha256, canScanKnownIds: actor.subredditName.toLowerCase() === 'neuronstonirvana',
      thisPostSha256: createHash('sha256').update(`${actor.subredditName.toLowerCase()}:${actor.postId!.replace(/^t3_/, '')}`).digest('hex'),
      scope: 'Known archived IDs only; not every post ever published.', batchSize: 5, cooldownSeconds: 30 };
  };
  const batch = async (input: unknown): Promise<MetadataBatch> => {
    const actor = await requireActor();
    if (!isRecord(input) || !['known-n2n', 'this-post'].includes(String(input.mode)) ||
        !Number.isInteger(input.cursor) || typeof input.cursor !== 'number' || input.cursor < 0) throw new AppError(400, 'Choose a scan mode and a valid saved cursor.');
    const mode = input.mode as MetadataBatch['mode'];
    if (mode === 'known-n2n' && actor.subredditName.toLowerCase() !== 'neuronstonirvana') throw new AppError(403, 'The N2N queue can only run in the N2N installation. Use this-post for a private playtest.');
    const currentId = actor.postId!.replace(/^t3_/, '');
    if (!/^[a-z0-9]{3,10}$/.test(currentId)) throw new AppError(400, 'A valid source post is required.');
    const ids: readonly string[] = mode === 'known-n2n' ? N2N_MANIFEST.ids : [currentId];
    if (input.cursor > ids.length) throw new AppError(400, 'The saved cursor is outside this queue.');
    const manifestHash = mode === 'known-n2n' ? N2N_MANIFEST.ids_sha256 : createHash('sha256').update(`${actor.subredditName.toLowerCase()}:${currentId}`).digest('hex');
    if (input.manifest_sha256 !== manifestHash) throw new AppError(409, 'The queue changed. Use the current manifest fingerprint before resuming.');
    if (input.cursor === ids.length) return { schema: 'akashicnet.devvit.metadata-batch.v1', mode, target_subreddit: actor.subredditName, manifest_sha256: manifestHash, known_ids: ids.length, from_cursor: input.cursor, next_cursor: input.cursor, pass_finished: true, retry_after_seconds: 30, records: [], public_merge_status: 'REVIEW_REQUIRED' };
    // Installation-wide limit, not a per-user allowance. No queue runs on load.
    const permitted = await deps.store.set(`metadata:cooldown:v1:${actor.subredditName.toLowerCase()}`, 'busy', { onlyIfAbsent: true, ttlSeconds: 30 });
    if (!permitted) throw new AppError(429, 'Wait 30 seconds between metadata batches.');
    const records: MetadataObservation[] = [];
    let cursor = input.cursor;
    for (const id of ids.slice(cursor, cursor + 5)) {
      const observation: MetadataObservation = { post_id: id, observed_at: new Date(now()).toISOString(), lookup_status: 'retry', metadata: null };
      try {
        const post = await deps.readPost(`t3_${id}`);
        if (post.id !== `t3_${id}` || post.subredditName.toLowerCase() !== actor.subredditName.toLowerCase()) {
          observation.lookup_status = 'out_of_scope';
        } else if (post.isRemoved() || post.isSpam() || post.isNsfw() || post.isQuarantined() || post.removedByCategory === 'deleted') {
          observation.lookup_status = 'suppressed';
        } else {
          let submittedUrl: string | null = null;
          try { const url = new URL(post.url); if (['http:', 'https:'].includes(url.protocol) && !url.username && !url.password && post.url.length <= 4096) submittedUrl = url.href; } catch { /* Leave unavailable values null. */ }
          observation.lookup_status = 'observed';
          observation.metadata = {
            canonical_permalink: `https://www.reddit.com/r/${actor.subredditName}/comments/${id}/`,
            subreddit: actor.subredditName,
            title: typeof post.title === 'string' && post.title.trim() ? post.title.slice(0, 300) : null,
            flair: typeof post.flair?.text === 'string' ? post.flair.text.slice(0, 300) : null,
            created_at: post.createdAt instanceof Date && Number.isFinite(post.createdAt.getTime()) ? post.createdAt.toISOString() : null,
            submitted_url: submittedUrl,
            // SDK score/comment defaults can be zero when unavailable. These
            // are explicitly snapshots of SDK-returned values, not exact votes.
            score_snapshot: Number.isFinite(post.score) ? post.score : null,
            comment_count_snapshot: Number.isFinite(post.numberOfComments) ? post.numberOfComments : null,
          };
        }
      } catch (error) {
        const status = isRecord(error) ? error.status ?? error.statusCode ?? error.code : undefined;
        observation.lookup_status = ['403', '404', '410'].includes(String(status)) ? 'unavailable' : 'retry';
      }
      records.push(observation);
      if (observation.lookup_status === 'retry') break;
      cursor += 1;
    }
    return { schema: 'akashicnet.devvit.metadata-batch.v1', mode, target_subreddit: actor.subredditName,
      manifest_sha256: manifestHash, known_ids: ids.length, from_cursor: input.cursor, next_cursor: cursor,
      pass_finished: cursor === ids.length, retry_after_seconds: 30, records, public_merge_status: 'REVIEW_REQUIRED' };
  };
  return { plan, batch };
};
