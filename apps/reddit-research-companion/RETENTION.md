# N2N metadata retention contract

24 October 2026 · America/Los_Angeles. **Offline safeguards implemented;
external live-content integration remains blocked.** This work extends draft
PR #414, separately from the private Devvit playtest. No live scan, Reddit
authentication, hosted installation or public graph merge was performed.

## Primary requirements checked

- [Developer Terms](https://redditinc.com/policies/developer-terms), §§3.3,
  7.2–7.4 and 8.2: act as soon as possible on content deletion, protected status,
  suspension, withholding, modification/removal and relevant requests; remove
  related App Content where applicable. Supply a clear privacy policy and an
  accessible removal process. Minimise retention and secure data, including
  encryption at rest. Stop-operation/termination also requires deletion.
- [Devvit Rules](https://developers.reddit.com/docs/devvit_rules), “Enable and
  respect user deletions”: delete post/comment content in the app and external
  services on deletion events. Limited metadata necessary to contextualise
  related content may be retained; this does not permit keeping deleted titles,
  embedded URLs, derivatives or content hashes. Account deletion requires
  removal of author-identifying data. The rules recommend auto-deletion within
  30 days; that recommendation does not permit delaying known deletions.
- [Data API Wiki](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)
  recommends routine deletion within 48 hours and requires deletion of removed
  user content; [Data API Terms](https://redditinc.com/policies/data-api-terms)
  §3.2 restrict use/retention to the approved use case and §6 covers termination
  and derived data. The wiki expressly defers to current terms.
- [Public Content Policy](https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy)
  and [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy)
  remain applicable. Moderator authorisation does not substitute for Reddit
  access/use approval, owner permissions or a lawful processing basis.

These documents have different scopes, not a single universal retention
period. The **24-hour** cutoff below is a conservative project policy retained
from staging. It does not certify compliance or permit waiting 24 hours after
a known removal. Recheck primary rules and the approved use case before
activating external storage. No policy exception is assumed.

## Minimum contract and implementation boundary

| Control | Local implementation | Before real external storage or incorporation |
| --- | --- | --- |
| Purpose/minimisation | Known N2N IDs and whitelisted metadata only. No bodies, comments, account IDs, author names or user flair; unexpected fields fail validation. | Confirm Reddit-approved purpose, permissions, notice/privacy policy and applicable processing basis. No sensitive-person profiling. |
| Time limit | Expiry is observation time + 24h; reimporting the same observation never extends it. Every CLI operation reconciles expiry before returning counts or processing new input. | Storage-enforced TTL and monitored deletion scheduling that works when this CLI is stopped; documented deletion latency and expiry checks at every access boundary. |
| Source status | Purge managed metadata and dependent projections. 403/404/410 mean unavailable, not proven deletion. Suppressed, protected, removed, mature, quarantined, wrong-community and transient outcomes fail closed. Deleted/removed title sentinels are suppressed. | Authenticated deletion/status events plus authorised revalidation; handle missed events, edits, permissions loss and account deletion. |
| Requests | `remove POST_ID` immediately suppresses locally, without arbitrary free-text reasons or extra requester data. | Accessible verified request channel, escalation to Reddit where required, response ownership and processing audit. Suppress pending verification. No channel is created here. |
| Propagation | One managed state file plus dependency-keyed private projections. Loss of any source drops the entire dependent object. Atomic replacement removes the old managed payload. | Inventory and purge raw packets, staging, clipboard/downloads, caches, search, rendered pages, citations, graphs, queues, logs, backups and third-party copies. Acknowledge/retry each sink; keep serving blocked until covered. |
| Provenance | Exact manifest, ID, community, canonical permalink, cursor, schema and timestamps validated. State cannot declare stronger provenance. | Authenticated capture identity, installation/actor authorisation, integrity and replay protection using a trusted transport/signature verifier. Operator JSON is not Reddit authentication. |
| Access | State outside Git; owner-only directory (0700), files (0600), ownership checks, no symlink ancestors/hardlinked files, exclusive operation lock, atomic replacement, bounded reads and counts-only CLI output. | Encrypted storage, restricted service identities, key management, operator RBAC, incident handling and reviewed processors. POSIX permissions are not encryption or hosted access control. |
| Publication | No public-content exporter or promotion operation. Origin UNVERIFIED_OPERATOR_EXPORT, public eligibility HOLD, evidence/rights OFF. Git barriers below. | Separately reviewed adapter with live expiry/revocation checks and downstream deletion acknowledgements. None is enabled here. |

## Local lifecycle tool

`tools/retain-n2n-metadata.mjs` is bounded and network-free. All payloads in
`test/metadata-retention.test.ts` are constructed in memory using **synthetic**
titles, URLs, derived content and a synthetic suppression key. No captured
Reddit-content fixtures belong in Git.

The CLI keeps only `state.json` and a random `suppression.key` in an owner-only
non-Git directory. It does not copy input captures. For synthetic verification:

```sh
npm run metadata:retain -- --workspace /absolute/private/n2n-retention import /absolute/private/synthetic-capture.json
npm run metadata:retain -- --workspace /absolute/private/n2n-retention status
npm run metadata:retain -- --workspace /absolute/private/n2n-retention sweep
npm run metadata:retain -- --workspace /absolute/private/n2n-retention remove POST_ID
```

Use a known manifest ID only in private requests, never attach removed content
to public issues. Inputs must be owner-only regular files outside Git, without
symlinks/hardlinks. Import bounds: 20 files, 20 MiB each, 64 MiB total. State
reads: 64 MiB. State collections: 7,463 records/tokens, 1,000 projections,
20 sources and 10,000 characters per projection. No CLI projection publisher
exists; the pure reconciler tests future private dependency propagation.

All operations, including `status`, first sweep managed state. Thus expired
payloads are purged even if a subsequent import contains malformed JSON.
Clock rollback, altered schema/manifest, forged origin/expiry, missing key,
unsafe permissions or concurrent operations deny access. A crash can leave
`operation.lock`; investigate before removing a stale lock, never remove an
active one. An interrupted `state.json.next` is purged on recovery, and that
invocation fails for operator review. No old-state backup or content digest
is deliberately written. Filesystem snapshots and physical media erasure are
external responsibilities; atomic replacement is not secure disk erasure.

Expiry, requests and contentless safety signals remove the payload, including
permalink, title, flair, creation timestamp, submitted URL and engagement, and
remove dependent projections. Persistent suppression dominates older and
newer copied observations across invocations. Staging also makes unavailable,
suppressed and out-of-scope observations dominate observed payloads in mixed
imports, regardless of order.

There is **no automatic reinstatement or ledger-reset command**. Expired or
unavailable sources require a separately reviewed reauthorisation path before
fresh retention. Losing the key is an error, not permission to regenerate it
over existing state. Never restore an older ledger backup to bypass suppression.

### What may remain after suppression

Only an HMAC of the source ID, an enumerated reason and suppression time remain.
This operational token prevents re-import; it contains no title, URL, content
digest, author identity, raw ID or creation time. It is **not anonymous data**,
a scientific finding, a public historical reference or permission to retain
deleted content. Its necessity, lawful basis, access and duration must be
approved in the operating contract. Keep it only while necessary to suppress
the authorised queue; delete it and the key when retiring the workflow. If
retaining even that identifier is prohibited, disable the queue and delete the
workspace rather than erase the block and permit replay.

The tool preserves no historical public references for suppressed sources.
The pre-existing structural manifest and website citation register are separate
historical inputs. This patch neither grants continued publication rights nor
changes them. They require source-by-source review against applicable rules
and permissions before affected references remain public. Never reconstruct
deleted titles from URL slugs or retain fingerprints of removed content.

## Git publication barriers

Staging refuses inputs/outputs inside Git worktrees/bare repositories and
symlink aliases. Use private absolute paths outside the checkout instead of
the old in-repository `captures/` / `staging/` examples. Ignore rules remain
defence in depth. Install the supplied hook in an authorised checkout:

```sh
git config core.hooksPath .githooks
npm run metadata:git-check
```

The guard scans index **blobs**, not filenames alone: capture/batch/staging/
retention schemas and characteristic records in JSON, nested JSON and JSONL
are rejected even when renamed or minified, along with known private paths.
Fixtures are constructed in TypeScript; there is no test-data bypass. A range
check also examines intermediate commits after working-tree deletion:

```sh
node tools/check-metadata-publication.mjs --range BASE_COMMIT_SHA..HEAD_COMMIT_SHA
```

Use full 40-character SHAs. PR CI fetches history and checks the proposed range
and index. Require this check in separately managed branch-protection settings.
Hooks are opt-in/bypassable; CI occurs after push and cannot erase disclosure.
The detector covers this workflow's JSON outputs, not archives, arbitrary
encodings or deliberate evasion. Never upload live captures to Git, CI
artifacts, comments or public logs. If disclosed, stop publication, restrict
access and execute a verified history/cache purge; deleting the latest revision
alone is inadequate.

## Remaining activation gate — NOT SATISFIED

No authenticated Reddit event source, integrity-verifying transport, external
TTL service, continuously running sweeper, takedown inbox, encrypted external
datastore, downstream purge adapters or backup-restore suppression is provisioned.
Raw inputs and stand-alone staging exports are not managed by the local vault;
their owners must delete/refresh them and clipboard/download copies under an
approved lifecycle. The CLI cannot remove someone else's copy or prevent a
text editor from reading a stale file.

Until those controls operate and are verified, keep real copied metadata out
of external storage and AkashicNET incorporation. Use synthetic data for these
commands. All local results remain HOLD; offline tests clear no evidence,
reuse-rights, release or Reddit-compliance gate. The companion's separate
public-discussion snapshots/receipts and private-playtest work are outside
this metadata patch and are not certified by it.
