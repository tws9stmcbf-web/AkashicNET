import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, statSync, writeFileSync, mkdirSync, symlinkSync, chmodSync, existsSync, linkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync, execFileSync } from 'node:child_process';
import test from 'node:test';
import { MAX_AGE_MS, loadManifest, stageCaptures } from '../tools/stage-n2n-capture.mjs';
import { reconcileRetention, sourceKey } from '../tools/retain-n2n-metadata.mjs';
import { unsafeMetadataBlob, checkPublication } from '../tools/check-metadata-publication.mjs';
import { assertOutsideGit } from '../tools/private-metadata-files.mjs';

const manifest = loadManifest();
const now = Date.parse('2026-10-24T12:00:00.000Z');
const secret = Buffer.alloc(32, 7); // Synthetic suppression key, never credentials.
const makeCapture = (date = now - 1000, status = 'observed') => ({ schema: 'akashicnet.devvit.metadata-capture.v1', packets: [{
  schema: 'akashicnet.devvit.metadata-batch.v1', mode: 'known-n2n', target_subreddit: 'NeuronsToNirvana', manifest_sha256: manifest.ids_sha256,
  known_ids: manifest.ids.length, from_cursor: 0, next_cursor: status === 'retry' ? 0 : 5, pass_finished: false, retry_after_seconds: 30,
  public_merge_status: 'REVIEW_REQUIRED', records: manifest.ids.slice(0, status === 'retry' ? 1 : 5).map((id: string) => ({
    post_id: id, observed_at: new Date(date).toISOString(), lookup_status: status,
    metadata: status === 'observed' ? { canonical_permalink: `https://www.reddit.com/r/NeuronsToNirvana/comments/${id}/`, subreddit: 'NeuronsToNirvana',
      title: 'Synthetic retained title', flair: 'Synthetic flair', created_at: '2025-01-01T00:00:00.000Z', submitted_url: 'https://example.com/synthetic', score_snapshot: 1, comment_count_snapshot: 2 } : null,
  })),
}] });
const apply = (previous: any = null, captures: any[] = [], options: any = {}) => reconcileRetention(previous, captures, manifest, { now, secret, ...options });
const retained = () => apply(null, [makeCapture()]);
const projection = () => ({ projection_id: 'synthetic-card', source_keys: [sourceKey(manifest.ids[0], secret), sourceKey(manifest.ids[1], secret)], content: 'Synthetic derived title and summary' });

test('fresh capture stays private HOLD with fixed source-based expiry and no authentication promotion', () => {
  const state = retained();
  assert.equal(state.records.length, 5);
  assert.equal(Date.parse(state.records[0].expires_at), now - 1000 + MAX_AGE_MS);
  assert.equal(state.provenance.origin_authentication, 'UNVERIFIED_OPERATOR_EXPORT');
  assert.equal(state.provenance.public_eligibility, 'HOLD');
  assert.deepEqual(state.provenance, { origin_authentication: 'UNVERIFIED_OPERATOR_EXPORT', public_eligibility: 'HOLD', evidence_promotion: 'OFF', rights_promotion: 'OFF' });
});

test('expiry at exact boundary purges content and all dependent projections', () => {
  const state = apply(retained(), [], { projections: [projection()] });
  const before = apply(state, [], { now: now - 1000 + MAX_AGE_MS - 1 });
  assert.equal(before.records.length, 5); assert.equal(before.projections.length, 1);
  const expired = apply(before, [], { now: now - 1000 + MAX_AGE_MS });
  assert.equal(expired.records.length, 0); assert.equal(expired.projections.length, 0);
  assert.equal(expired.suppressions.length, 5);
  assert.ok(!JSON.stringify(expired).includes('Synthetic'));
  assert.ok(!JSON.stringify(expired).includes('example.com'));
});

for (const reason of ['request', 'deleted', 'unavailable', 'suppressed', 'out_of_scope', 'retry']) {
  test(`${reason} removes source and derived content and blocks older AND newer re-imports`, () => {
    const before = apply(retained(), [], { projections: [projection()] });
    const after = apply(before, [], { removals: [{ post_id: manifest.ids[0], reason }] });
    assert.equal(after.records.length, 4); assert.equal(after.projections.length, 0);
    assert.ok(!JSON.stringify(after.suppressions).includes(manifest.ids[0]));
    assert.deepEqual(Object.keys(after.suppressions[0]), ['source_key', 'reason', 'suppressed_at']);
    for (const date of [now - 1000, now]) {
      const replayed = apply(after, [makeCapture(date)]);
      assert.equal(replayed.records.some((r: any) => r.post_id === manifest.ids[0]), false);
      assert.equal(replayed.provenance.public_eligibility, 'HOLD');
    }
    assert.equal(apply(after).records.length, 4); // restart/reload round-trip
  });
}

for (const status of ['unavailable', 'suppressed', 'out_of_scope', 'retry']) {
  test(`captured ${status} propagates into previously retained state`, () => {
    const state = apply(retained(), [makeCapture(now, status)]);
    assert.equal(state.records.some((r: any) => r.post_id === manifest.ids[0]), false);
    assert.equal(state.provenance.public_eligibility, 'HOLD');
  });
}

test('safety outcomes in mixed packets cannot be overridden by a newer observed title or ordering', () => {
  const missing = makeCapture(now - 500, 'unavailable'); const observed = makeCapture(now);
  for (const packets of [[missing, observed], [observed, missing]]) {
    assert.equal(apply(retained(), packets).records.length, 0);
    assert.equal(stageCaptures(packets, manifest, { now }).records[0].metadata, null);
  }
});

test('expiry never becomes a rolling TTL and replay cannot restore an expired payload', () => {
  const state = retained(); const next = apply(state, [makeCapture()], { now: now + 1000 });
  assert.equal(state.records[0].expires_at, next.records[0].expires_at);
  const expired = apply(state, [], { now: now + MAX_AGE_MS });
  assert.equal(apply(expired, [makeCapture(now + MAX_AGE_MS)], { now: now + MAX_AGE_MS }).records.length, 0);
});

test('tampered origin, extended expiry, foreign IDs, unknown content and missing keys are refused', () => {
  const original = retained();
  for (const change of [
    (s: any) => { s.provenance.public_eligibility = 'APPROVED'; },
    (s: any) => { s.provenance.origin_authentication = 'AUTHENTICATED'; },
    (s: any) => { s.records[0].expires_at = new Date(now + MAX_AGE_MS).toISOString(); },
    (s: any) => { s.records[0].post_id = 'foreign'; },
    (s: any) => { s.records[0].metadata.author = 'forbidden'; },
    (s: any) => { s.history = ['forbidden']; },
  ]) { const altered = structuredClone(original); change(altered); assert.throws(() => apply(altered)); }
  assert.throws(() => apply(original, [], { secret: undefined }), /suppression key/);
  assert.throws(() => apply(original, [], { now: now - 1 }), /clock/);
  assert.throws(() => apply(original, [makeCapture(now + 1)]), /future/);
});

test('invalid notices and derivative references cannot escape known-ID bounds', () => {
  assert.throws(() => apply(retained(), [], { removals: [{ post_id: 'unknown', reason: 'request' }] }));
  assert.throws(() => apply(retained(), [], { removals: [{ post_id: manifest.ids[0], reason: 'free text' }] }));
  assert.throws(() => apply(retained(), [], { projections: [{ ...projection(), source_keys: ['unknown'] }] }));
});

test('CLI private state persists removals across invocations and outputs counts only', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'akn-retention-'));
  try {
    const workspace = path.join(dir, 'private'); const input = path.join(dir, 'input.json');
    writeFileSync(input, JSON.stringify(makeCapture(Date.now() - 1000)), { mode: 0o600 });
    const script = new URL('../tools/retain-n2n-metadata.mjs', import.meta.url).pathname;
    const run = (...args: string[]) => spawnSync(process.execPath, [script, '--workspace', workspace, ...args], { encoding: 'utf8' });
    const imported = run('import', input); assert.equal(imported.status, 0, imported.stderr);
    assert.equal(statSync(workspace).mode & 0o777, 0o700);
    assert.equal(statSync(path.join(workspace, 'state.json')).mode & 0o777, 0o600);
    assert.equal(statSync(path.join(workspace, 'suppression.key')).mode & 0o777, 0o600);
    assert.ok(!imported.stdout.includes('Synthetic')); assert.ok(!imported.stdout.includes(manifest.ids[0]));
    assert.equal(run('remove', manifest.ids[0]).status, 0);
    assert.equal(run('import', input).status, 0);
    assert.equal(JSON.parse(readFileSync(path.join(workspace, 'state.json'), 'utf8')).records.length, 4);
    assert.equal(run('status').status, 0);
    assert.equal(existsSync(path.join(workspace, 'state.json.next')), false);
    chmodSync(input, 0o644); assert.equal(run('import', input).status, 1);
    chmodSync(input, 0o600);
    mkdirSync(path.join(workspace, 'operation.lock')); assert.equal(run('sweep').status, 1);
    rmSync(path.join(workspace, 'operation.lock'), { recursive: true });
    writeFileSync(path.join(workspace, 'state.json.next'), 'Synthetic crash content', { mode: 0o600 });
    assert.equal(run('status').status, 1); assert.equal(existsSync(path.join(workspace, 'state.json.next')), false);
    rmSync(path.join(workspace, 'suppression.key')); assert.equal(run('status').status, 1);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('paths reject Git worktrees, bare repositories, symlink aliases and unsafe storage modes', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'akn-retention-path-'));
  try {
    mkdirSync(path.join(dir, 'repo')); writeFileSync(path.join(dir, 'repo', '.git'), 'gitdir: elsewhere');
    assert.throws(() => assertOutsideGit(path.join(dir, 'repo', 'nested', 'capture.json')), /Git/);
    mkdirSync(path.join(dir, 'bare')); mkdirSync(path.join(dir, 'bare', 'objects')); writeFileSync(path.join(dir, 'bare', 'HEAD'), 'ref: refs/heads/main');
    assert.throws(() => assertOutsideGit(path.join(dir, 'bare', 'capture.json')), /Git/);
    symlinkSync(dir, path.join(dir, 'alias')); assert.throws(() => assertOutsideGit(path.join(dir, 'alias', 'capture.json')), /symlink/);
    const unsafe = path.join(dir, 'unsafe'); mkdirSync(unsafe); chmodSync(unsafe, 0o755);
    const script = new URL('../tools/retain-n2n-metadata.mjs', import.meta.url).pathname;
    assert.equal(spawnSync(process.execPath, [script, '--workspace', unsafe, 'status']).status, 1);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('CLI purges expired persisted data before a malformed import fails', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'akn-retention-expiry-'));
  try {
    const workspace = path.join(dir, 'private'); mkdirSync(workspace, { mode: 0o700 });
    const stateFile = path.join(workspace, 'state.json');
    writeFileSync(path.join(workspace, 'suppression.key'), secret, { mode: 0o600 });
    const oldClock = Date.now() - MAX_AGE_MS - 1000;
    const oldState = apply(null, [makeCapture(oldClock - 1000)], { now: oldClock });
    const stale = apply(oldState, [], { now: oldClock, projections: [projection()] });
    writeFileSync(stateFile, JSON.stringify(stale), { mode: 0o600 });
    const malformed = path.join(dir, 'malformed.json'); writeFileSync(malformed, '{bad', { mode: 0o600 });
    const script = new URL('../tools/retain-n2n-metadata.mjs', import.meta.url).pathname;
    const result = spawnSync(process.execPath, [script, '--workspace', workspace, 'import', malformed], { encoding: 'utf8' });
    assert.equal(result.status, 1);
    const purged = JSON.parse(readFileSync(stateFile, 'utf8'));
    assert.equal(purged.records.length, 0); assert.equal(purged.projections.length, 0);
    assert.ok(!JSON.stringify(purged).includes('Synthetic'));
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('hardlinked capture inputs and stage outputs inside Git are refused', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'akn-retention-alias-'));
  try {
    const input = path.join(dir, 'capture.json'); writeFileSync(input, JSON.stringify(makeCapture(Date.now() - 1000)), { mode: 0o600 });
    const alias = path.join(dir, 'alias.json'); linkSync(input, alias);
    const retainScript = new URL('../tools/retain-n2n-metadata.mjs', import.meta.url).pathname;
    assert.equal(spawnSync(process.execPath, [retainScript, '--workspace', path.join(dir, 'private'), 'import', input]).status, 1);
    const repo = path.join(dir, 'repo'); mkdirSync(repo); mkdirSync(path.join(repo, '.git'));
    const stageScript = new URL('../tools/stage-n2n-capture.mjs', import.meta.url).pathname;
    const output = path.join(repo, 'renamed.json');
    assert.equal(spawnSync(process.execPath, [stageScript, input, '--out', output]).status, 1);
    assert.equal(existsSync(output), false);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('Git content guard catches renamed/minified/nested/JSONL exports without blocking source code', () => {
  for (const data of [makeCapture(), retained(), { nested: { post_id: 'synthetic', observed_at: 'synthetic' } }]) {
    assert.equal(unsafeMetadataBlob('innocent.txt', Buffer.from(JSON.stringify(data))), true);
    assert.equal(unsafeMetadataBlob('innocent.txt', Buffer.from('{}\n' + JSON.stringify(data))), true);
  }
  assert.equal(unsafeMetadataBlob('captures/innocent.txt', Buffer.from('{}')), true);
  assert.equal(unsafeMetadataBlob('source.ts', Buffer.from("const schema = 'akashicnet.devvit.metadata-capture.v1';")), false);
  assert.equal(unsafeMetadataBlob('preflight.json', Buffer.from('{"known_ids":7463}')), false);
  assert.equal(unsafeMetadataBlob('historical.json', Buffer.from('{"post_id":"synthetic","metadata":{},"title":null,"author":null,"current_flair":null}')), false);
  assert.equal(unsafeMetadataBlob('historical.json', Buffer.from('{"post_id":"synthetic","metadata":{"title":"Synthetic title"}}')), true);
  assert.equal(unsafeMetadataBlob('references/research/ara/staging/observations.yaml', Buffer.from('observations: []')), false);
});

test('Git guard checks staged blobs and capture commits even after working-tree deletion', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'akn-retention-git-'));
  const git = (...args: string[]) => execFileSync('git', args, { cwd: dir, encoding: 'utf8' }).trim();
  try {
    git('init', '-q'); git('config', 'user.email', 'synthetic@example.invalid'); git('config', 'user.name', 'Synthetic Test');
    writeFileSync(path.join(dir, 'safe.txt'), 'synthetic'); git('add', '.'); git('commit', '-qm', 'Synthetic base'); const base = git('rev-parse', 'HEAD');
    writeFileSync(path.join(dir, 'renamed.txt'), JSON.stringify(makeCapture())); git('add', '.');
    assert.throws(() => checkPublication({ cwd: dir }), /blocked/);
    git('commit', '-qm', 'Synthetic unsafe fixture'); git('rm', '-q', 'renamed.txt'); git('commit', '-qm', 'Synthetic deletion');
    assert.equal(checkPublication({ cwd: dir }).status, 'PASS');
    assert.throws(() => checkPublication({ cwd: dir, range: `${base}..${git('rev-parse', 'HEAD')}` }), /blocked/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
