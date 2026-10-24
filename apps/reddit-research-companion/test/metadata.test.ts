import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import test from 'node:test';
import { createMetadataScanner, type MetadataPost } from '../src/server/metadata.js';
import { N2N_MANIFEST } from '../src/server/generated/n2n-manifest.js';
import { AppError } from '../src/server/policy.js';
import type { Actor, Store } from '../src/server/service.js';
import { createApp } from '../src/server/app.js';
import type { Dependencies } from '../src/server/service.js';

const fixture = () => {
  let actor: Actor = { userId: 't2_mod', postId: 't3_abc123', subredditName: 'NeuronsToNirvana', canPublish: true };
  let clock = 1_800_000_000_000;
  const values = new Map<string, { value: string; expiry: number }>();
  const calls: string[] = [];
  let failure: unknown;
  let alter: (post: MetadataPost) => MetadataPost = post => post;
  const store: Store = {
    async get(key) { return values.get(key)?.value; },
    async set(key, value, options) {
      if (options?.onlyIfAbsent && (values.get(key)?.expiry ?? 0) > clock) return false;
      values.set(key, { value, expiry: clock + (options?.ttlSeconds ?? 0) * 1000 }); return true;
    },
  };
  const deps = { actor: async () => ({ ...actor }), store, now: () => clock,
    async readPost(id) {
      calls.push(id);
      if (failure) throw failure;
      const post = alter({ id, subredditName: actor.subredditName, title: 'A captured title', flair: { text: 'Research' },
        createdAt: new Date('2025-02-01T00:00:00Z'), url: 'https://doi.org/10.1234/example', score: 12, numberOfComments: 4,
        isRemoved: () => false, isSpam: () => false, isNsfw: () => false, isQuarantined: () => false });
      Object.defineProperty(post, 'body', { get() { throw new Error('Body must not be read'); } });
      Object.defineProperty(post, 'authorName', { get() { throw new Error('Author must not be read'); } });
      return post;
    },
  };
  const scanner = createMetadataScanner(deps);
  const companionDeps: Dependencies = { ...deps, flairs: async () => [], snapshotId: () => undefined,
    publish: async () => { throw new Error('No publication in metadata tests'); },
    createLauncher: async () => { throw new Error('No launcher in metadata tests'); } };
  return { scanner, app: createApp(companionDeps, deps), calls, values, setActor: (value: Partial<Actor>) => { actor = { ...actor, ...value }; },
    fail: (value: unknown) => { failure = value; }, alter: (value: typeof alter) => { alter = value; },
    advance: () => { clock += 31_000; } };
};
const input = (cursor = 0) => ({ mode: 'known-n2n', cursor, manifest_sha256: N2N_MANIFEST.ids_sha256 });
const hasStatus = (status: number) => (error: unknown) => error instanceof AppError && error.status === status;

test('known-ID manifest is unique, stable and bounded to the saved set', () => {
  assert.equal(N2N_MANIFEST.known_id_count, 7463);
  assert.equal(new Set(N2N_MANIFEST.ids).size, 7463);
  assert.equal(createHash('sha256').update(N2N_MANIFEST.ids.join('\n') + '\n').digest('hex'), N2N_MANIFEST.ids_sha256);
  assert.equal(N2N_MANIFEST.completeness, 'known_archive_ids_only');
});

test('read-only capture uses five known IDs, records provenance and stores no captured content', async () => {
  const f = fixture();
  const packet = await f.scanner.batch(input());
  assert.deepEqual(f.calls, N2N_MANIFEST.ids.slice(0, 5).map(id => `t3_${id}`));
  assert.equal(packet.next_cursor, 5);
  assert.equal(packet.pass_finished, false);
  assert.equal(packet.public_merge_status, 'REVIEW_REQUIRED');
  assert.ok(packet.records.every(record => record.lookup_status === 'observed' && record.metadata?.title === 'A captured title'));
  assert.equal(packet.records[0]?.observed_at, new Date(1_800_000_000_000).toISOString());
  assert.deepEqual([...f.values.values()].map(value => value.value), ['busy']);
  assert.ok(!JSON.stringify(packet).includes('author'));
});

test('non-moderators cannot inspect the queue or request content', async () => {
  const f = fixture(); f.setActor({ canPublish: false });
  await assert.rejects(f.scanner.plan(), hasStatus(403));
  await assert.rejects(f.scanner.batch(input()), hasStatus(403));
  assert.equal(f.calls.length, 0);
});

test('private playtests cannot run the N2N queue and only read their current post', async () => {
  const f = fixture(); f.setActor({ subredditName: 'private_test' });
  const plan = await f.scanner.plan(); assert.equal(plan.canScanKnownIds, false);
  await assert.rejects(f.scanner.batch(input()), hasStatus(403));
  assert.equal(f.calls.length, 0);
  const packet = await f.scanner.batch({ mode: 'this-post', cursor: 0, manifest_sha256: plan.thisPostSha256 });
  assert.deepEqual(f.calls, ['t3_abc123']); assert.equal(packet.pass_finished, true);
});

test('malicious cursors and stale manifest fingerprints fail before any read', async () => {
  const f = fixture();
  for (const cursor of [-1, 1.5, Infinity, '0', 7464]) await assert.rejects(f.scanner.batch({ ...input(), cursor }), hasStatus(400));
  await assert.rejects(f.scanner.batch({ ...input(), manifest_sha256: 'wrong' }), hasStatus(409));
  assert.equal(f.calls.length, 0);
});

test('installation cooldown survives a second moderator and permits bounded resume', async () => {
  const f = fixture(); await f.scanner.batch(input());
  f.setActor({ userId: 't2_secondmod' });
  await assert.rejects(f.scanner.batch(input(5)), hasStatus(429));
  f.advance(); const packet = await f.scanner.batch(input(5));
  assert.equal(packet.next_cursor, 10); assert.equal(f.calls.length, 10);
});

test('a transient failure does not advance or label a post deleted', async () => {
  const f = fixture(); f.fail(Object.assign(new Error('Rate limited'), { status: 429 }));
  const packet = await f.scanner.batch(input());
  assert.equal(packet.next_cursor, 0); assert.equal(packet.records[0]?.lookup_status, 'retry');
  assert.equal(packet.records[0]?.metadata, null); assert.equal(f.calls.length, 1);
});

test('inaccessible posts are accounted for separately from transient failures', async () => {
  const f = fixture(); f.fail(Object.assign(new Error('No access'), { status: 403 }));
  const packet = await f.scanner.batch(input());
  assert.equal(packet.next_cursor, 5);
  assert.ok(packet.records.every(record => record.lookup_status === 'unavailable' && record.metadata === null));
});

test('removed, deleted, mature and quarantined posts never leak their metadata', async () => {
  for (const patch of [{ isRemoved: () => true }, { removedByCategory: 'deleted' }, { isNsfw: () => true }, { isQuarantined: () => true }, { isSpam: () => true }, { title: '[deleted]' }, { title: ' [REMOVED] ' }]) {
    const f = fixture(); f.alter(post => ({ ...post, ...patch }));
    const packet = await f.scanner.batch(input());
    assert.ok(packet.records.every(record => record.lookup_status === 'suppressed' && record.metadata === null));
  }
});

test('wrong-community responses are suppressed and unsafe URLs stay null', async () => {
  const f = fixture(); f.alter(post => ({ ...post, subredditName: 'different_subreddit' }));
  assert.ok((await f.scanner.batch(input())).records.every(record => record.lookup_status === 'out_of_scope' && record.metadata === null));
  const g = fixture(); g.alter(post => ({ ...post, url: 'javascript:alert(1)', createdAt: new Date('invalid') }));
  const packet = await g.scanner.batch(input());
  assert.equal(packet.records[0]?.metadata?.submitted_url, null); assert.equal(packet.records[0]?.metadata?.created_at, null);
});

test('final partial batch and finished cursor do not invent extra work', async () => {
  const f = fixture(); const packet = await f.scanner.batch(input(7460));
  assert.equal(packet.records.length, 3); assert.equal(packet.next_cursor, 7463); assert.equal(packet.pass_finished, true);
  const done = await f.scanner.batch(input(7463)); assert.equal(done.records.length, 0); assert.equal(f.calls.length, 3);
});

test('HTTP scan routes enforce server identity, request limits and no-store responses', async () => {
  const f = fixture(); f.setActor({ canPublish: false });
  assert.equal((await f.app.request('/api/metadata/plan')).status, 403);
  const denied = await f.app.request('/api/metadata/batch', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...input(), isModerator: true, targetSubreddit: 'different' }) });
  assert.equal(denied.status, 403); assert.equal(f.calls.length, 0);
  f.setActor({ canPublish: true });
  const oversized = await f.app.request('/api/metadata/batch', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...input(), padding: 'x'.repeat(9000) }) });
  assert.equal(oversized.status, 413); assert.equal(f.calls.length, 0);
  const ok = await f.app.request('/api/metadata/batch', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input()) });
  assert.equal(ok.status, 200); assert.equal(ok.headers.get('cache-control'), 'no-store'); assert.equal(f.calls.length, 5);
});
