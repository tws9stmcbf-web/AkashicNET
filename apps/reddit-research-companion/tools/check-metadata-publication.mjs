import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const prohibited = /(^|\/)(captures|retention-data)(\/|$)|(^|\/)apps\/reddit-research-companion\/staging(\/|$)|(^|\/)(state\.json(?:\.next)?|suppression\.key)$/;
const sensitiveSchemas = new Set([
  'akashicnet.devvit.metadata-capture.v1', 'akashicnet.devvit.metadata-batch.v1',
  'akashicnet.n2n.metadata-review-staging.v1', 'akashicnet.n2n.private-retention.v1',
]);
function containsCapture(value) {
  if (!value || typeof value !== 'object') return false;
  if (sensitiveSchemas.has(value.schema) ||
      ('post_id' in value && ('observed_at' in value ||
        (value.metadata && Object.keys(value.metadata).length > 0) ||
        ['title', 'author', 'current_flair'].some(key => value[key] !== undefined && value[key] !== null))) ||
      ('origin_authentication' in value && value.origin_authentication === 'UNVERIFIED_OPERATOR_EXPORT') ||
      ('source_key' in value && 'suppressed_at' in value)) return true;
  return Object.values(value).some(containsCapture);
}
export function unsafeMetadataBlob(name, bytes) {
  if (prohibited.test(name)) return true;
  const source = bytes.toString('utf8').replace(/^\uFEFF/, '').trim();
  try { if (containsCapture(JSON.parse(source))) return true; } catch { /* Also inspect JSONL. */ }
  return source.split('\n').some(line => {
    try { return containsCapture(JSON.parse(line)); } catch { return false; }
  });
}
const git = (args, cwd) => execFileSync('git', args, { cwd, maxBuffer: 128 * 1024 * 1024 });

/** Checks actual index blobs and optional branch-history blobs, including deleted
 * files. No filename extension allowlist; no fixture bypass; no payload logging.
 */
export function checkPublication({ cwd = process.cwd(), range } = {}) {
  if (range !== undefined && !/^[0-9a-f]{40}\.\.[0-9a-f]{40}$/.test(range)) throw new Error('Use an exact base..head SHA range');
  const objects = new Map();
  for (const line of git(['ls-files', '--stage', '-z'], cwd).toString().split('\0').filter(Boolean)) {
    const match = line.match(/^\d+ ([0-9a-f]+) \d\t([\s\S]+)$/);
    if (!match) throw new Error('Cannot inspect index');
    const [, oid, name] = match;
    if (!objects.has(oid)) objects.set(oid, new Set());
    objects.get(oid).add(name);
  }
  if (range) {
    for (const line of git(['rev-list', '--objects', range], cwd).toString().trim().split('\n').filter(Boolean)) {
      const [oid, ...rest] = line.split(' '); const name = rest.join(' ');
      if (!objects.has(oid)) objects.set(oid, new Set());
      if (name) objects.get(oid).add(name);
    }
  }
  let blobs = 0;
  for (const [oid, names] of objects) {
    if (git(['cat-file', '-t', oid], cwd).toString().trim() !== 'blob') continue;
    const size = Number(git(['cat-file', '-s', oid], cwd).toString());
    if (size > 64 * 1024 * 1024) throw new Error('Blob exceeds publication inspection bound');
    const bytes = git(['cat-file', 'blob', oid], cwd); blobs++;
    if ([...names].some(name => unsafeMetadataBlob(name, bytes))) throw new Error('Captured/private metadata is blocked from Git publication; remove it from the index and unpublished history');
  }
  return { status: 'PASS', inspected_blobs: blobs };
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2);
    if (args.length && (args.length !== 2 || args[0] !== '--range')) throw new Error('Usage: check-metadata-publication.mjs [--range BASE_SHA..HEAD_SHA]');
    console.log(JSON.stringify(checkPublication({ range: args[1] })));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
