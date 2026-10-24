import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { createRequire } from 'node:module';
import { ARTICLES } from '../src/shared/catalog.js';
import { createApp } from '../src/server/app.js';
import { AppError, buildSnapshot, parseDraftInput } from '../src/server/policy.js';
import { createService, type Actor, type Dependencies, type Store } from '../src/server/service.js';
import type { Flair, Snapshot } from '../src/shared/model.js';

const input = { articleId: 'intention-awareness', title: 'Before The Words: Intention Awareness (Telepathy?)', summary: 'A proposed blinded experiment with sending and no-sending controls. No experiment has been conducted.', flairId: null };

const fixture = () => {
  const values = new Map<string, { value: string; expiresAt: number | undefined }>();
  let clock = 1_800_000_000_000;
  let actor: Actor = { userId: 't2_mod', postId: 't3_companion', subredditName: 'test_community', canPublish: true };
  let flairs: Flair[] = [{ id: 'flair-hypothesis', text: 'Hypothesis' }];
  let snapshotId: string | undefined;
  const calls: { snapshot: Snapshot; subredditName: string; snapshotId: string }[] = [];
  let publicationFails = false;
  let receiptFails = false;
  let launcherCalls = 0;
  let finish: (() => void) | undefined;
  let pause: Promise<void> | undefined;
  const store: Store = {
    async get(key) {
      const entry = values.get(key);
      if (entry?.expiresAt !== undefined && entry.expiresAt <= clock) { values.delete(key); return undefined; }
      return entry?.value;
    },
    async set(key, value, options) {
      if (receiptFails && value.includes('"state":"published"')) throw new Error('Receipt unavailable');
      if (options?.onlyIfAbsent && values.has(key)) return false;
      values.set(key, { value, expiresAt: options?.ttlSeconds ? clock + options.ttlSeconds * 1000 : undefined });
      return true;
    },
  };
  const deps: Dependencies = {
    actor: async () => ({ ...actor }),
    flairs: async () => [...flairs], store, now: () => clock,
    async publish(snapshot, id, subredditName) {
      calls.push({ snapshot, snapshotId: id, subredditName });
      if (pause) await pause;
      if (publicationFails) throw new Error('Reddit response lost after submission');
      snapshotId = id;
      return { postId: 't3_published', url: 'https://www.reddit.com/r/test_community/comments/published/' };
    },
    async createLauncher() {
      launcherCalls += 1;
      return { postId: 't3_launcher', url: 'https://www.reddit.com/r/test_community/comments/launcher/' };
    },
    snapshotId: () => snapshotId,
  };
  return {
    service: createService(deps), app: createApp(deps), calls, values,
    setActor: (next: Partial<Actor>) => { actor = { ...actor, ...next }; },
    setFlairs: (next: Flair[]) => { flairs = next; },
    advance: (ms: number) => { clock += ms; },
    failPublication: () => { publicationFails = true; },
    failReceipt: () => { receiptFails = true; },
    pausePublication: () => { pause = new Promise<void>((resolve) => { finish = resolve; }); },
    finishPublication: () => finish?.(),
    launcherCalls: () => launcherCalls,
    setSnapshotId: (id: string) => { snapshotId = id; },
  };
};

const status = (expected: number) => (error: unknown): boolean => error instanceof AppError && error.status === expected;

test('the published Devvit schema accepts the actual configuration', () => {
  const require = createRequire(import.meta.url);
  const { parseAppConfig } = require('../node_modules/@devvit/shared-types/schemas/config-file.v1.js');
  const config = readFileSync(new URL('../devvit.json', import.meta.url), 'utf8');
  assert.doesNotThrow(() => parseAppConfig(config, false));
  const parsed = JSON.parse(config);
  assert.equal(parsed.permissions.http.enable, false);
  assert.equal(parsed.permissions.reddit.asUser, undefined);
  assert.equal(parsed.scheduler, undefined);
  assert.equal(parsed.triggers, undefined);
  assert.equal(parsed.server.externalEndpoints, undefined);
});

test('public catalog URLs are HTTPS, canonical, and independently safe to navigate', () => {
  for (const article of ARTICLES) {
    const url = new URL(article.canonicalUrl);
    assert.equal(url.hostname, 'akashicnet.org');
    assert.equal(url.protocol, 'https:');
    for (const source of article.sourceUrls) assert.equal(new URL(source).protocol, 'https:');
    assert.ok(!article.evidenceLabels.includes('Established Evidence'));
  }
  assert.match(ARTICLES.find((article) => article.id === 'bq001')?.reviewStatus ?? '', /Open question/);
  assert.match(ARTICLES.find((article) => article.id === 'intention-awareness')?.reviewStatus ?? '', /no experimental results/);
});

test('validation rejects arbitrary articles, forged flairs, multiline titles and oversized prose', () => {
  assert.throws(() => buildSnapshot(parseDraftInput({ ...input, articleId: 'private-drive' }), ARTICLES, []), status(400));
  assert.throws(() => buildSnapshot(parseDraftInput({ ...input, flairId: 'forged' }), ARTICLES, []), status(400));
  assert.throws(() => parseDraftInput({ ...input, title: 'Title\nwith a newline' }), status(400));
  assert.throws(() => parseDraftInput({ ...input, summary: 'x'.repeat(2001) }), status(400));
  assert.throws(() => parseDraftInput(null), status(400));
});

test('snapshot preserves status and sources while treating moderator prose as plain text', () => {
  const snapshot = buildSnapshot(parseDraftInput({ ...input, summary: '[Changed source](https://evil.example) <script>alert(1)</script> is a hypothetical string for this test.' }), ARTICLES, []);
  assert.match(snapshot.body, /Untested hypothesis/);
  assert.ok(snapshot.body.includes('https://akashicnet.org/intention-awareness'));
  assert.ok(snapshot.body.includes('\\[Changed source\\]'));
  assert.ok(!snapshot.body.includes('<script>'));
});

test('anonymous readers can browse without receiving private drafts or flair administration', async () => {
  const f = fixture();
  await f.service.preview(input);
  f.setActor({ userId: undefined, canPublish: false });
  const session = await f.service.session();
  assert.equal(session.isModerator, false);
  assert.deepEqual(session.flairs, []);
  assert.equal(session.articles.length, 2);
  assert.ok(!JSON.stringify(session).includes('t2_mod'));
  assert.ok(!JSON.stringify(session).includes('previewId'));
});

test('direct endpoint calls reject forged moderator flags and subreddit overrides', async () => {
  const f = fixture();
  f.setActor({ canPublish: false });
  for (const path of ['/api/preview', '/api/publish']) {
    const response = await f.app.request(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...input, canPublish: true, isModerator: true, subredditName: 'NeuronsToNirvana' }) });
    assert.equal(response.status, 403);
  }
  assert.equal(f.calls.length, 0);
});

test('request size and malformed JSON are rejected before mutation', async () => {
  const f = fixture();
  const big = await f.app.request('/api/preview', { method: 'POST', body: JSON.stringify({ ...input, summary: 'x'.repeat(9000) }) });
  const bad = await f.app.request('/api/preview', { method: 'POST', body: '{broken' });
  assert.equal(big.status, 413);
  assert.equal(bad.status, 400);
  assert.equal(f.values.size, 0);
});

test('previewing creates no Reddit post and cannot promote the article evidence status', async () => {
  const f = fixture();
  const preview = await f.service.preview({ ...input, evidenceLabels: ['Established Evidence'], reviewStatus: 'Proven', canonicalUrl: 'https://evil.example' });
  assert.equal(f.calls.length, 0);
  assert.deepEqual(preview.snapshot.article.evidenceLabels, ['Hypothesis']);
  assert.match(preview.snapshot.body, /no experimental results/);
  assert.ok(!preview.snapshot.body.includes('evil.example'));
});

test('publication is bound to the authenticated actor, source post and installation', async () => {
  for (const override of [{ userId: 't2_other_mod' }, { postId: 't3_other_post' }, { subredditName: 'other_community' }]) {
    const f = fixture(); const preview = await f.service.preview(input);
    f.setActor(override);
    await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(404));
    assert.equal(f.calls.length, 0);
  }
});

test('moderator permission revocation is checked again at publication', async () => {
  const f = fixture(); const preview = await f.service.preview(input);
  f.setActor({ canPublish: false });
  await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(403));
  assert.equal(f.calls.length, 0);
});

test('a changed, expired or replaced preview cannot publish', async () => {
  const f = fixture(); const original = await f.service.preview(input);
  await f.service.preview({ ...input, title: 'A revised title for a new preview' });
  await assert.rejects(() => f.service.publish({ previewId: original.previewId }), status(404));
  const latest = await f.service.preview(input);
  f.advance(600_001);
  await assert.rejects(() => f.service.publish({ previewId: latest.previewId }), (error) => error instanceof AppError && [404, 410].includes(error.status));
  assert.equal(f.calls.length, 0);
});

test('an outdated flair must be previewed again', async () => {
  const f = fixture(); const preview = await f.service.preview({ ...input, flairId: 'flair-hypothesis' });
  f.setFlairs([{ id: 'flair-hypothesis', text: 'Different label' }]);
  await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(409));
  assert.equal(f.calls.length, 0);
});

test('publication uses the frozen preview, ignores replacement fields and returns the same receipt on retry', async () => {
  const f = fixture(); const preview = await f.service.preview(input);
  const post = await f.service.publish({ previewId: preview.previewId, title: 'Do not use this', summary: 'Do not use this', subredditName: 'wrong_subreddit', evidenceLabels: ['Established Evidence'] });
  assert.equal(post.duplicate, false);
  assert.equal(f.calls[0]?.snapshot.title, input.title);
  assert.equal(f.calls[0]?.subredditName, 'test_community');
  const retry = await f.service.publish({ previewId: preview.previewId });
  assert.equal(retry.duplicate, true);
  assert.equal(retry.url, post.url);
  assert.equal(f.calls.length, 1);
});

test('concurrent double-clicks and identical previews cannot create two posts', async () => {
  const f = fixture(); const preview = await f.service.preview(input);
  f.pausePublication();
  const first = f.service.publish({ previewId: preview.previewId });
  // Drain microtasks until the first request reaches the controlled publisher.
  for (let i = 0; i < 20 && f.calls.length === 0; i += 1) await Promise.resolve();
  assert.equal(f.calls.length, 1);
  await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(409));
  f.finishPublication(); await first;
  const another = await f.service.preview(input);
  assert.equal((await f.service.publish({ previewId: another.previewId })).duplicate, true);
  assert.equal(f.calls.length, 1);
});

test('ambiguous Reddit failure keeps a persistent claim and never retries the submission', async () => {
  const f = fixture(); const preview = await f.service.preview(input);
  f.failPublication();
  await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(503));
  await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(409));
  const pending = [...f.values.entries()].find(([key]) => key.startsWith('publish:'));
  assert.equal(pending?.[1].expiresAt, undefined);
  assert.equal(f.calls.length, 1);
});

test('receipt failure reports the real post URL and keeps duplicate protection', async () => {
  const f = fixture(); const preview = await f.service.preview(input);
  f.failReceipt();
  const post = await f.service.publish({ previewId: preview.previewId });
  assert.equal(post.receiptSaved, false);
  assert.ok(post.url.includes('published'));
  await assert.rejects(() => f.service.publish({ previewId: preview.previewId }), status(409));
  assert.equal(f.calls.length, 1);
});

test('published readers receive the saved snapshot, and missing snapshots fail visibly', async () => {
  const f = fixture(); const preview = await f.service.preview(input);
  await f.service.publish({ previewId: preview.previewId });
  f.setActor({ userId: undefined, canPublish: false });
  assert.deepEqual((await f.service.session()).currentSnapshot, preview.snapshot);
  f.setSnapshotId('missing');
  await assert.rejects(() => f.service.session(), status(410));
});

test('the moderator menu creates one companion and checks permission on every call', async () => {
  const f = fixture(); const first = await f.service.launcher();
  assert.equal((await f.service.launcher()).url, first.url);
  assert.equal(f.launcherCalls(), 1);
  f.setActor({ canPublish: false });
  await assert.rejects(() => f.service.launcher(), status(403));
});

test('a direct internal-menu request cannot bypass server-side moderator authorization', async () => {
  const f = fixture();
  f.setActor({ userId: undefined, canPublish: false });
  const response = await f.app.request('/internal/menu/companion', {
    method: 'POST', body: JSON.stringify({ isModerator: true, userId: 't2_mod' }),
  });
  assert.match((await response.json()).showToast, /moderator with post permissions/);
  assert.equal(f.launcherCalls(), 0);
});

test('identical content prepared by another moderator resolves to the existing publication', async () => {
  const f = fixture(); const firstPreview = await f.service.preview(input);
  const firstPost = await f.service.publish({ previewId: firstPreview.previewId });
  f.setActor({ userId: 't2_second_mod' });
  const secondPreview = await f.service.preview(input);
  const secondPost = await f.service.publish({ previewId: secondPreview.previewId });
  assert.equal(secondPost.url, firstPost.url);
  assert.equal(secondPost.duplicate, true);
  assert.equal(f.calls.length, 1);
});
