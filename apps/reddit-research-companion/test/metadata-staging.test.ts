import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, statSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { loadManifest, stageCaptures } from '../tools/stage-n2n-capture.mjs';

const manifest = loadManifest();
const now = Date.parse('2026-10-24T12:00:00.000Z');
const record = (id: string, observed = '2026-10-24T11:00:00.000Z') => ({
  post_id: id, observed_at: observed, lookup_status: 'observed', metadata: {
    canonical_permalink: `https://www.reddit.com/r/NeuronsToNirvana/comments/${id}/`, subreddit: 'NeuronsToNirvana',
    title: 'Synthetic test title', flair: 'Research', created_at: '2025-01-01T00:00:00.000Z',
    submitted_url: 'https://doi.org/10.1234/synthetic', score_snapshot: 0, comment_count_snapshot: 0,
  },
});
const packet = (cursor = 0, observed?: string) => ({
  schema: 'akashicnet.devvit.metadata-batch.v1', mode: 'known-n2n', target_subreddit: 'NeuronsToNirvana',
  manifest_sha256: manifest.ids_sha256, known_ids: manifest.ids.length,
  from_cursor: cursor, next_cursor: Math.min(cursor + 5, manifest.ids.length),
  pass_finished: cursor + 5 >= manifest.ids.length, retry_after_seconds: 30,
  records: manifest.ids.slice(cursor, cursor + 5).map((id: string) => record(id, observed)), public_merge_status: 'REVIEW_REQUIRED',
});
const capture = (...packets: unknown[]) => ({ schema: 'akashicnet.devvit.metadata-capture.v1', packets });
const run = (...packets: unknown[]) => stageCaptures([capture(...packets)], manifest, { now });

test('staging validates real manifest identity and reports honest partial coverage', () => {
  const staged = run(packet());
  assert.equal(staged.coverage.known_ids, 7463); assert.equal(staged.coverage.unique_ids, 5);
  assert.equal(staged.coverage.next_unresolved_cursor, 5);
  assert.deepEqual(staged.coverage.unresolved_ranges, [{ from_cursor: 5, to_cursor_exclusive: 7463 }]);
  assert.equal(staged.coverage.known_id_accounting_complete, false);
  assert.equal(staged.records[0].metadata.title, 'Synthetic test title');
});

test('duplicate copied packets are idempotent and retain duplicate accounting', () => {
  const p = packet(); const staged = run(p, p);
  assert.equal(staged.records.length, 5); assert.equal(staged.coverage.received_observations, 10);
  assert.equal(staged.coverage.duplicate_or_superseded_observations, 5);
});

test('out-of-order resumed batches reveal gaps instead of claiming completion', () => {
  const staged = run(packet(10), packet(0));
  assert.equal(staged.coverage.next_unresolved_cursor, 5);
  assert.deepEqual(staged.coverage.unresolved_ranges, [{ from_cursor: 5, to_cursor_exclusive: 10 }, { from_cursor: 15, to_cursor_exclusive: 7463 }]);
});

test('altered identity, mismatched community and stale manifest are rejected', () => {
  const a = packet(); a.records[0].post_id = 'wrongid'; assert.throws(() => run(a), /manifest position/);
  const b = packet(); b.records[0].metadata.subreddit = 'different'; assert.throws(() => run(b), /another community/);
  const c = packet(); c.manifest_sha256 = 'forged'; assert.throws(() => run(c), /another manifest/);
  const d = packet(); d.records[0].metadata.canonical_permalink = 'https://example.com/'; assert.throws(() => run(d), /permalink/);
});

test('truncated packets, forged progress and invented full coverage are rejected', () => {
  const a = packet(); a.records.pop(); a.next_cursor = 4; assert.throws(() => run(a), /cursor or completion/);
  const b = packet(); b.next_cursor = 7; assert.throws(() => run(b), /cursor or completion/);
  const c = packet(); c.pass_finished = true; assert.throws(() => run(c), /cursor or completion/);
});

test('retry remains unresolved and cannot be followed by silently skipped IDs', () => {
  const p = packet(); p.records = [{ ...record(manifest.ids[0]), lookup_status: 'retry', metadata: null }]; p.next_cursor = 0;
  const staged = run(p); assert.equal(staged.coverage.next_unresolved_cursor, 0); assert.equal(staged.coverage.outcomes.retry, 1);
  const invalid = structuredClone(p); invalid.next_cursor = 1; assert.throws(() => run(invalid), /cursor or completion/);
  const resumed = run(p, packet(0, '2026-10-24T11:01:00.000Z')); assert.equal(resumed.coverage.outcomes.retry, 0);
});

test('a newer suppressed outcome drops the prior captured payload from staging', () => {
  const old = packet(); const newer = packet(0, '2026-10-24T11:01:00.000Z');
  newer.records[0] = { ...newer.records[0], lookup_status: 'suppressed', metadata: null };
  const staged = run(old, newer);
  assert.equal(staged.records[0].lookup_status, 'suppressed'); assert.equal(staged.records[0].metadata, null);
  assert.equal(staged.coverage.outcomes.suppressed, 1);
});

test('same-timestamp contradictions require explicit resolution', () => {
  const a = packet(); const b = packet(); b.records[0].metadata.title = 'Contradictory synthetic title';
  assert.throws(() => run(a, b), /Conflicting observations/);
});

test('stale, future and malformed timestamps are refused', () => {
  for (const date of ['2026-10-23T12:00:00.000Z', '2026-10-24T12:00:00.001Z', 'not-a-date']) assert.throws(() => run(packet(0, date)), /timestamp|stale|future/);
  const p = packet(); p.records[0].metadata.created_at = '2026-10-24T11:30:00.000Z'; assert.throws(() => run(p), /Creation timestamp/);
});

test('post bodies, author fields and forged review approvals cannot enter staging', () => {
  const a = packet(); Object.assign(a.records[0].metadata, { body: 'Unexpected content' }); assert.throws(() => run(a), /metadata fields/);
  const b = packet(); Object.assign(b.records[0], { author: 'unexpected' }); assert.throws(() => run(b), /observation fields/);
  const c = packet(); c.public_merge_status = 'APPROVED'; assert.throws(() => run(c), /bypass metadata review/);
  const d = packet(); d.records[0].lookup_status = 'suppressed'; assert.throws(() => run(d), /must not contain/);
});

test('unsafe URLs and impossible engagement values are rejected; empty flair stays explicit', () => {
  const a = packet(); a.records[0].metadata.submitted_url = 'https://user:secret@example.com/'; assert.throws(() => run(a), /Unsafe/);
  const b = packet(); b.records[0].metadata.comment_count_snapshot = -1; assert.throws(() => run(b), /comment-count/);
  const c = packet(); c.records[0].metadata.flair = ''; assert.equal(run(c).records[0].metadata.flair, '');
});

test('a well-formed supplied packet is never claimed as authenticated Reddit evidence', () => {
  const staged = run(packet());
  assert.equal(staged.provenance.origin_authentication, 'UNVERIFIED_OPERATOR_EXPORT');
  assert.equal(staged.provenance.live_retrieval_this_process, false);
  assert.deepEqual([staged.integration.public_eligibility, staged.integration.evidence_promotion, staged.integration.rights_promotion], ['HOLD', 'OFF', 'OFF']);
  assert.equal(staged.integration.canonical_archive_modified, false);
});

test('private playtest packets cannot contaminate the N2N review queue', () => {
  const p = packet(); p.mode = 'this-post'; p.target_subreddit = 'private_test';
  assert.throws(() => run(p), /Only N2N capture/);
});

test('CLI writes a private new review file without altering inputs or overwriting outputs', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'akn-staging-test-'));
  try {
    const input = path.join(dir, 'synthetic-capture.json'); const output = path.join(dir, 'review.json');
    const fresh = new Date(Date.now() - 1000).toISOString();
    const original = JSON.stringify(capture(packet(0, fresh))); writeFileSync(input, original);
    const script = new URL('../tools/stage-n2n-capture.mjs', import.meta.url);
    const result = spawnSync(process.execPath, [script.pathname, input, '--out', output], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr); assert.equal(statSync(output).mode & 0o777, 0o600);
    assert.equal(readFileSync(input, 'utf8'), original); assert.ok(!result.stdout.includes('Synthetic test title'));
    const before = readFileSync(output, 'utf8');
    assert.equal(spawnSync(process.execPath, [script.pathname, input, '--out', output], { encoding: 'utf8' }).status, 1);
    assert.equal(readFileSync(output, 'utf8'), before);
    const invalid = path.join(dir, 'invalid.json'); writeFileSync(invalid, '{bad');
    const denied = path.join(dir, 'not-created.json');
    assert.equal(spawnSync(process.execPath, [script.pathname, invalid, '--out', denied], { encoding: 'utf8' }).status, 1);
    assert.equal(existsSync(denied), false);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
