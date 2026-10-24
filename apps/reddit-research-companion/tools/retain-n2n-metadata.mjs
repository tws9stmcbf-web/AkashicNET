import { createHmac, randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync, renameSync, unlinkSync, rmdirSync, openSync, closeSync, fsyncSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { MAX_AGE_MS, loadManifest, normaliseRecord, stageCaptures } from './stage-n2n-capture.mjs';
import { assertOutsideGit, assertPrivate } from './private-metadata-files.mjs';

const SCHEMA = 'akashicnet.n2n.private-retention.v1';
const fail = message => { throw new Error(message); };
const exact = (v, keys) => {
  if (!v || Array.isArray(v) || typeof v !== 'object' || Object.keys(v).length !== keys.length || !keys.every(k => Object.hasOwn(v, k))) fail('Invalid private retention fields');
};
const time = value => {
  const ms = typeof value === 'string' ? Date.parse(value) : NaN;
  if (!Number.isFinite(ms) || new Date(ms).toISOString() !== value) fail('Invalid retention timestamp');
  return ms;
};
const iso = ms => new Date(ms).toISOString();
const reasons = ['request', 'deleted', 'unavailable', 'suppressed', 'out_of_scope', 'retry', 'expired'];
const token = (id, secret) => createHmac('sha256', secret).update(`n2n:${id}`).digest('hex');
const provenance = () => ({ origin_authentication: 'UNVERIFIED_OPERATOR_EXPORT', public_eligibility: 'HOLD', evidence_promotion: 'OFF', rights_promotion: 'OFF' });

export function emptyRetention(manifest, now) {
  return { schema: SCHEMA, manifest_sha256: manifest.ids_sha256, evaluated_at: iso(now),
    provenance: provenance(), records: [], suppressions: [], projections: [] };
}

/** Pure, bounded local reconciliation; never authenticates Reddit or emits public content.
 * Suppression tokens contain no content hashes, titles, URLs, timestamps of creation,
 * author identities or raw post IDs. They exist solely to prevent re-import.
 */
export function reconcileRetention(previous, captures, manifest, { now = Date.now(), secret, removals = [], projections = [] } = {}) {
  // Validate the manifest even when there is no new capture.
  stageCaptures([{ schema: 'akashicnet.devvit.metadata-capture.v1', packets: [{
    schema: 'akashicnet.devvit.metadata-batch.v1', mode: 'known-n2n', target_subreddit: manifest.subreddit,
    manifest_sha256: manifest.ids_sha256, known_ids: manifest.ids.length, from_cursor: manifest.ids.length,
    next_cursor: manifest.ids.length, pass_finished: true, retry_after_seconds: 30, records: [], public_merge_status: 'REVIEW_REQUIRED',
  }] }], manifest, { now });
  if (!Buffer.isBuffer(secret) || secret.length !== 32) fail('A private 32-byte suppression key is required');
  const state = previous ?? emptyRetention(manifest, now);
  exact(state, ['schema', 'manifest_sha256', 'evaluated_at', 'provenance', 'records', 'suppressions', 'projections']);
  if (state.schema !== SCHEMA || state.manifest_sha256 !== manifest.ids_sha256 || now < time(state.evaluated_at)) fail('Retention identity changed or clock moved backwards; deny access');
  exact(state.provenance, Object.keys(provenance()));
  if (JSON.stringify(state.provenance) !== JSON.stringify(provenance())) fail('Retention provenance cannot be promoted');
  const ids = new Set(manifest.ids);
  const validTokens = new Set(manifest.ids.map(id => token(id, secret)));
  for (const list of [state.records, state.suppressions, removals]) if (!Array.isArray(list) || list.length > ids.size) fail('Retention collection exceeds known-ID bound');
  for (const list of [state.projections, projections]) if (!Array.isArray(list) || list.length > 1000) fail('Too many derived projections');
  const blocked = new Map();
  for (const item of state.suppressions) {
    exact(item, ['source_key', 'reason', 'suppressed_at']);
    if (!validTokens.has(item.source_key) || !reasons.includes(item.reason) || time(item.suppressed_at) > now || blocked.has(item.source_key)) fail('Invalid suppression token');
    blocked.set(item.source_key, { ...item });
  }
  const records = new Map();
  const suppress = (id, reason) => {
    const key = token(id, secret);
    if (!blocked.has(key)) blocked.set(key, { source_key: key, reason, suppressed_at: iso(now) });
    records.delete(id);
  };
  for (const item of state.records) {
    exact(item, ['post_id', 'observed_at', 'lookup_status', 'metadata', 'expires_at']);
    if (!ids.has(item.post_id) || records.has(item.post_id) || item.lookup_status !== 'observed') fail('Invalid retained source identity');
    const observed = time(item.observed_at);
    const record = normaliseRecord({ post_id: item.post_id, observed_at: item.observed_at, lookup_status: item.lookup_status, metadata: item.metadata }, item.post_id, observed);
    if (observed > now || time(item.expires_at) !== observed + MAX_AGE_MS) fail('Retention expiry cannot be extended');
    if (now >= time(item.expires_at)) suppress(item.post_id, 'expired');
    else if (!blocked.has(token(item.post_id, secret))) records.set(item.post_id, { ...record, expires_at: item.expires_at });
  }
  // Removal notices need not claim authenticated origin: uncertain notices cause
  // suppression, never disclosure or automatic reinstatement. No free-text reason.
  for (const item of removals) {
    exact(item, ['post_id', 'reason']);
    if (!ids.has(item.post_id) || !reasons.includes(item.reason)) fail('Invalid removal request');
    suppress(item.post_id, item.reason);
  }
  if (captures.length) {
    const staged = stageCaptures(captures, manifest, { now });
    for (const record of staged.records) {
      if (record.lookup_status !== 'observed') suppress(record.post_id, record.lookup_status);
      else if (!blocked.has(token(record.post_id, secret))) {
        const prior = records.get(record.post_id);
        if (prior?.observed_at === record.observed_at && JSON.stringify(prior) !== JSON.stringify(record)) fail('Conflicting retained observation');
        if (!prior || record.observed_at > prior.observed_at) records.set(record.post_id, { ...record });
      }
    }
  }
  const sourceKeys = new Set([...records.keys()].map(id => token(id, secret)));
  const derived = new Map();
  for (const p of [...state.projections, ...projections]) {
    exact(p, ['projection_id', 'source_keys', 'content']);
    if (typeof p.projection_id !== 'string' || !/^[a-z0-9_-]{1,64}$/.test(p.projection_id) ||
        !Array.isArray(p.source_keys) || !p.source_keys.length || p.source_keys.length > 20 ||
        !p.source_keys.every(k => validTokens.has(k)) || typeof p.content !== 'string' || p.content.length > 10000) fail('Invalid private projection');
    if (derived.has(p.projection_id)) fail('Duplicate projection identity');
    // Drop the entire dependent object, including content derived from other sources.
    if (p.source_keys.every(k => sourceKeys.has(k) && !blocked.has(k))) derived.set(p.projection_id, structuredClone(p));
  }
  return { schema: SCHEMA, manifest_sha256: manifest.ids_sha256, evaluated_at: iso(now), provenance: provenance(),
    records: [...records.values()], suppressions: [...blocked.values()], projections: [...derived.values()] };
}

export function sourceKey(id, secret) { return token(id, secret); }

function readPrivateJson(file, maxBytes = 20 * 1024 * 1024) {
  assertOutsideGit(file);
  if (assertPrivate(file).size > maxBytes) fail('Private input exceeds bounded size');
  return JSON.parse(readFileSync(file, 'utf8'));
}

// Rename replaces the only managed state file. No old payload version or audit
// digest is kept. This does not promise physical erasure from SSDs or snapshots.
function persist(file, state) {
  const temporary = `${file}.next`;
  const fd = openSync(temporary, 'wx', 0o600);
  try { writeFileSync(fd, JSON.stringify(state) + '\n'); fsyncSync(fd); } finally { closeSync(fd); }
  renameSync(temporary, file);
  const parent = openSync(path.dirname(file), 'r');
  try { fsyncSync(parent); } finally { closeSync(parent); }
}

export function runRetention(args) {
  if (args[0] !== '--workspace' || !args[1] || !['import', 'sweep', 'remove', 'status'].includes(args[2])) fail('Usage: --workspace /private/non-git/directory import capture.json [more.json] | sweep | status | remove POST_ID');
  const workspace = assertOutsideGit(args[1]);
  const command = args[2];
  const rest = args.slice(3);
  if ((command === 'import' && (!rest.length || rest.length > 20)) || (command === 'remove' && rest.length !== 1) || (['sweep', 'status'].includes(command) && rest.length)) fail('Invalid retention command arguments');
  if (!existsSync(workspace)) mkdirSync(workspace, { mode: 0o700 });
  assertPrivate(workspace, true);
  const lock = path.join(workspace, 'operation.lock');
  mkdirSync(lock, { mode: 0o700 }); // Concurrent invocations fail closed.
  try {
    const keyFile = path.join(workspace, 'suppression.key');
    const stateFile = path.join(workspace, 'state.json');
    const pending = `${stateFile}.next`;
    // An interrupted replacement is never served. It may contain old content.
    // Delete only this managed temporary file; keep failing until operator review.
    if (existsSync(pending)) { assertPrivate(pending); unlinkSync(pending); fail('Interrupted retention transaction; pending file purged. Review storage before retry'); }
    if (!existsSync(keyFile)) {
      if (existsSync(stateFile)) fail('Missing suppression key; do not reset the ledger');
      writeFileSync(keyFile, randomBytes(32), { flag: 'wx', mode: 0o600 });
    }
    assertPrivate(keyFile);
    const secret = readFileSync(keyFile);
    const manifest = loadManifest();
    const now = Date.now();
    const previous = existsSync(stateFile) ? readPrivateJson(stateFile, 64 * 1024 * 1024) : null;
    // Purge expired data even if the later import/removal request is malformed.
    const swept = reconcileRetention(previous, [], manifest, { now, secret });
    persist(stateFile, swept);
    let total = 0;
    const captures = command === 'import' ? rest.map(file => {
      const size = assertPrivate(assertOutsideGit(file)).size; total += size;
      if (total > 64 * 1024 * 1024) fail('Private inputs exceed total size bound');
      return readPrivateJson(file);
    }) : [];
    const removals = command === 'remove' ? [{ post_id: rest[0], reason: 'request' }] : [];
    const next = reconcileRetention(swept, captures, manifest, { now, secret, removals });
    persist(stateFile, next);
    return { status: 'PRIVATE_HOLD', retained_records: next.records.length, suppression_count: next.suppressions.length,
      private_projections: next.projections.length, public_eligibility: 'HOLD', origin_authentication: 'UNVERIFIED_OPERATOR_EXPORT', live_retrievals: 0 };
  } finally { rmdirSync(lock); }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { console.log(JSON.stringify(runRetention(process.argv.slice(2)))); }
  catch { console.error('Retention operation denied; no content was exported. Check private paths, permissions, schema, clock and lock state.'); process.exitCode = 1; }
}
