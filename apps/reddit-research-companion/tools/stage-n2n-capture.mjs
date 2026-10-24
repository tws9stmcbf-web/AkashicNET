import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { assertOutsideGit } from './private-metadata-files.mjs';

const TARGET = 'NeuronsToNirvana';
export const MAX_AGE_MS = 24 * 60 * 60 * 1000;
const hash = value => createHash('sha256').update(value).digest('hex');
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const fail = message => { throw new Error(message); };
const exactKeys = (value, keys, label) => {
  if (!object(value) || Object.keys(value).length !== keys.length || !keys.every(key => Object.hasOwn(value, key))) fail(`Invalid ${label} fields`);
};
const timestamp = (value, label) => {
  if (typeof value !== 'string') fail(`Invalid ${label}`);
  const ms = Date.parse(value);
  if (!Number.isFinite(ms) || new Date(ms).toISOString() !== value) fail(`Invalid ${label}`);
  return ms;
};
const textOrNull = (value, max, label, allowEmpty = false) => {
  if (value !== null && (typeof value !== 'string' || (!allowEmpty && !value.trim()) || value.length > max || /[\u0000-\u0008\u000b-\u001f\u007f]/u.test(value))) fail(`Invalid ${label}`);
  return value;
};

export function loadManifest() {
  const source = readFileSync(new URL('../src/server/generated/n2n-manifest.ts', import.meta.url), 'utf8');
  const match = source.match(/export const N2N_MANIFEST = ([\s\S]+) as const;\s*$/);
  if (!match) fail('The generated manifest cannot be read');
  return JSON.parse(match[1]);
}

export function normaliseRecord(value, expectedId, now) {
  if (typeof expectedId !== 'string') fail('Observation is outside the known-ID manifest');
  exactKeys(value, ['post_id', 'observed_at', 'lookup_status', 'metadata'], 'observation');
  if (value.post_id !== expectedId) fail('Observation ID does not match its manifest position');
  const observed = timestamp(value.observed_at, 'observation timestamp');
  if (observed > now || now - observed >= MAX_AGE_MS) fail('Observation is stale or in the future; obtain a fresh capture');
  const statuses = ['observed', 'unavailable', 'suppressed', 'out_of_scope', 'retry'];
  if (!statuses.includes(value.lookup_status)) fail('Unknown lookup status');
  let metadata = null;
  if (value.lookup_status !== 'observed') {
    if (value.metadata !== null) fail('A non-observed outcome must not contain post content');
  } else {
    exactKeys(value.metadata, ['canonical_permalink', 'subreddit', 'title', 'flair', 'created_at', 'submitted_url', 'score_snapshot', 'comment_count_snapshot'], 'metadata');
    const m = value.metadata;
    if (typeof m.subreddit !== 'string' || m.subreddit.toLowerCase() !== TARGET.toLowerCase()) fail('Metadata belongs to another community');
    const expectedUrl = `https://www.reddit.com/r/${m.subreddit}/comments/${expectedId}/`;
    if (m.canonical_permalink !== expectedUrl) fail('Canonical permalink does not match the captured identity');
    const created = m.created_at === null ? null : timestamp(m.created_at, 'creation timestamp');
    if (created !== null && created > observed) fail('Creation timestamp is after the observation');
    if (m.submitted_url !== null) {
      if (typeof m.submitted_url !== 'string' || m.submitted_url.length > 4096) fail('Invalid submitted URL');
      let url;
      try { url = new URL(m.submitted_url); } catch { fail('Invalid submitted URL'); }
      if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) fail('Unsafe submitted URL');
    }
    if (m.score_snapshot !== null && !Number.isFinite(m.score_snapshot)) fail('Invalid score snapshot');
    if (m.comment_count_snapshot !== null && (!Number.isInteger(m.comment_count_snapshot) || m.comment_count_snapshot < 0)) fail('Invalid comment-count snapshot');
    metadata = { canonical_permalink: expectedUrl, subreddit: TARGET,
      title: textOrNull(m.title, 300, 'title'), flair: textOrNull(m.flair, 300, 'flair', true),
      created_at: m.created_at, submitted_url: m.submitted_url,
      score_snapshot: m.score_snapshot, comment_count_snapshot: m.comment_count_snapshot };
  }
  return { post_id: expectedId, observed_at: value.observed_at, lookup_status: value.lookup_status, metadata };
}

/** Validate and stage supplied packets. This function makes no network calls. */
export function stageCaptures(captures, manifest, { now = Date.now() } = {}) {
  if (!Number.isFinite(now)) fail('Invalid review clock');
  if (!object(manifest) || manifest.subreddit !== TARGET || !Array.isArray(manifest.ids) ||
      manifest.ids.length !== manifest.known_id_count || new Set(manifest.ids).size !== manifest.ids.length ||
      !manifest.ids.every(id => typeof id === 'string' && /^[a-z0-9]{3,10}$/.test(id)) ||
      hash(manifest.ids.join('\n') + '\n') !== manifest.ids_sha256) fail('Invalid known-ID manifest');
  if (!Array.isArray(captures) || !captures.length) fail('At least one capture file is required');
  const packets = [];
  for (const capture of captures) {
    exactKeys(capture, ['schema', 'packets'], 'capture envelope');
    if (capture.schema !== 'akashicnet.devvit.metadata-capture.v1' || !Array.isArray(capture.packets)) fail('Invalid capture envelope');
    packets.push(...capture.packets);
  }
  if (!packets.length || packets.length > 5000) fail('Capture must contain 1–5000 bounded packets');
  const latest = new Map();
  let observationCount = 0;
  for (const packet of packets) {
    exactKeys(packet, ['schema', 'mode', 'target_subreddit', 'manifest_sha256', 'known_ids', 'from_cursor', 'next_cursor', 'pass_finished', 'retry_after_seconds', 'records', 'public_merge_status'], 'packet');
    if (packet.schema !== 'akashicnet.devvit.metadata-batch.v1' || packet.mode !== 'known-n2n' ||
        typeof packet.target_subreddit !== 'string' || packet.target_subreddit.toLowerCase() !== TARGET.toLowerCase()) fail('Only N2N capture packets can enter this staging queue');
    if (packet.manifest_sha256 !== manifest.ids_sha256 || packet.known_ids !== manifest.ids.length) fail('Packet uses another manifest');
    if (packet.public_merge_status !== 'REVIEW_REQUIRED') fail('A packet cannot bypass metadata review');
    if (!Number.isInteger(packet.from_cursor) || !Number.isInteger(packet.next_cursor) ||
        packet.from_cursor < 0 || packet.next_cursor < packet.from_cursor || packet.next_cursor > manifest.ids.length ||
        !Array.isArray(packet.records) || packet.records.length > 5 || packet.retry_after_seconds !== 30) fail('Invalid batch bounds');
    let expectedCursor = packet.from_cursor;
    for (let i = 0; i < packet.records.length; i++) {
      const record = normaliseRecord(packet.records[i], manifest.ids[expectedCursor], now);
      observationCount++;
      const prior = latest.get(record.post_id);
      if (prior?.observed_at === record.observed_at && JSON.stringify(prior) !== JSON.stringify(record)) fail('Conflicting observations have the same timestamp; resolve the conflict explicitly');
      // Contentless safety outcomes dominate all supplied observations. A later
      // copied title is not permission to undo a removal/unavailability signal.
      const blocked = item => item && ['unavailable', 'suppressed', 'out_of_scope'].includes(item.lookup_status);
      if (!prior || (blocked(record) && !blocked(prior)) ||
          (blocked(record) === blocked(prior) && record.observed_at > prior.observed_at)) latest.set(record.post_id, record);
      if (record.lookup_status === 'retry') {
        if (i !== packet.records.length - 1) fail('A transient failure must end its batch');
      } else expectedCursor++;
    }
    const expectedFinished = expectedCursor === manifest.ids.length;
    if (packet.next_cursor !== expectedCursor || packet.pass_finished !== expectedFinished ||
        (!packet.records.length && !expectedFinished) ||
        (packet.records.length < Math.min(5, manifest.ids.length - packet.from_cursor) && packet.records.at(-1)?.lookup_status !== 'retry')) fail('Packet cursor or completion claim does not match its observations');
  }
  const counts = { observed: 0, unavailable: 0, suppressed: 0, out_of_scope: 0, retry: 0 };
  const unresolvedRanges = [];
  const records = [];
  let start = null;
  for (let i = 0; i < manifest.ids.length; i++) {
    const record = latest.get(manifest.ids[i]);
    if (record) { counts[record.lookup_status]++; records.push({ ...record, expires_at: new Date(Date.parse(record.observed_at) + MAX_AGE_MS).toISOString() }); }
    if (!record || record.lookup_status === 'retry') { if (start === null) start = i; }
    else if (start !== null) { unresolvedRanges.push({ from_cursor: start, to_cursor_exclusive: i }); start = null; }
  }
  if (start !== null) unresolvedRanges.push({ from_cursor: start, to_cursor_exclusive: manifest.ids.length });
  return {
    schema: 'akashicnet.n2n.metadata-review-staging.v1', generated_at: new Date(now).toISOString(),
    target_subreddit: TARGET, manifest_sha256: manifest.ids_sha256,
    provenance: { origin_authentication: 'UNVERIFIED_OPERATOR_EXPORT', live_retrieval_this_process: false,
      capture_fingerprints: captures.map(capture => hash(JSON.stringify(capture))) },
    integration: { public_eligibility: 'HOLD', evidence_promotion: 'OFF', rights_promotion: 'OFF',
      canonical_archive_modified: false, deletion_and_refresh_workflow: 'REQUIRED_BEFORE_EXTERNAL_CONTENT_USE',
      engagement_precision: 'SDK snapshots may contain zero defaults; exact votes are not established' },
    coverage: { known_ids: manifest.ids.length, received_packets: packets.length, received_observations: observationCount,
      unique_ids: latest.size, duplicate_or_superseded_observations: observationCount - latest.size, outcomes: counts,
      known_id_accounting_complete: unresolvedRanges.length === 0, all_ids_observed: counts.observed === manifest.ids.length,
      next_unresolved_cursor: unresolvedRanges[0]?.from_cursor ?? manifest.ids.length, unresolved_ranges: unresolvedRanges },
    records,
  };
}

function main(args) {
  const index = args.indexOf('--out');
  if (index < 1 || index !== args.length - 2) fail('Usage: node tools/stage-n2n-capture.mjs capture.json [more-captures.json] --out staging/review.json');
  const inputs = args.slice(0, index).map(file => path.resolve(file));
  const output = path.resolve(args[index + 1]);
  for (const file of [...inputs, output]) assertOutsideGit(file);
  if (!output.endsWith('.json') || existsSync(output) || inputs.includes(output)) fail('Choose a new .json output file; existing files are never overwritten');
  let totalBytes = 0;
  const captures = inputs.map(file => {
    const bytes = statSync(file).size; totalBytes += bytes;
    if (bytes > 20 * 1024 * 1024 || totalBytes > 64 * 1024 * 1024) fail('Capture files exceed the bounded import size');
    return JSON.parse(readFileSync(file, 'utf8'));
  });
  const staged = stageCaptures(captures, loadManifest());
  mkdirSync(path.dirname(output), { recursive: true, mode: 0o700 });
  writeFileSync(output, JSON.stringify(staged, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
  console.log(JSON.stringify({ status: 'STAGED_FOR_REVIEW', known_ids: staged.coverage.known_ids,
    staged_ids: staged.coverage.unique_ids, outcomes: staged.coverage.outcomes,
    next_unresolved_cursor: staged.coverage.next_unresolved_cursor, public_eligibility: 'HOLD', live_retrievals: 0 }));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(process.argv.slice(2)); } catch (error) {
    console.error(error instanceof SyntaxError ? 'Invalid capture JSON; no output was written.' : error.message);
    process.exitCode = 1;
  }
}
