# v0.18 Research Integration: first bounded adapter

22 October 2026. **DRAFT / REVIEW_REQUIRED. Real BQ001 pilot: HOLD.**
Tracks #411; does not close it. No release, tag, merge, live Site update or source publication.

## What works

`research_integration_v018.py` imports the existing `akashicprism.framework-input.v1`
file export without network access or changing PRISM. It verifies the exact packet
SHA-256, revision, all table hashes/counts, primary keys, compound foreign keys,
assessment chains and current-assessment view. It checks the selected community
ID using the existing `tools/search_reddit.py` archive loader, preserving that
tool's metadata-only boundary. No new crawler or live Reddit connector is added.

The versioned closed source/review contract and separate public-export schema
use `0.18.0-pilot.1`, **an interface version, not a released software version**.
Native `source_url`, `record_id` and `assessment_id` remain unchanged. URLs are
locators; matching URLs never merge records, establish work families or count
independent studies. Duplicate primary IDs are errors. Work-family identity stays
unknown, and source relationships support only unadjudicated candidates.

The adapter preserves original URLs, observation dates, provenance, input
hashes, native assessment IDs, superseding history, reading depth, access scope,
evidence status, rationale, uncertainty, integration status, context visibility
and each assessment's five restriction categories. Integration status means
storage/workflow status, never evidence acceptance. Missing retrieval dates
remain null; observation dates are not relabelled retrieval dates. A primary
metadata row has `metadata_only` import depth, with its prior partial-read scope
retained separately; this import claims no additional reading.

OMNI output is a **pending manual-review worksheet**, with twelve perspective
dispositions, separate direct-evidence / interpretation / synthesis / hypothesis
sections, counter-evidence, missing information and uncertainty. It does not
implement the full OMNI method or assert human review occurred. Record substantive
appraisal only after reading the sources; keep outcomes unresolved where warranted.

## Reused work and exact pins

Base: `e342c8fea7ef6da7ffe2a5efa8fca17de72df6a4`. `input-lock.json` records the
Git blob and SHA-256 of source-status v0.16, OMNI public status, v0.17 gate document,
archive loader/dependency and both archive CSVs. The adapter refuses changed
foundation bytes; intentional upgrades require a reviewed new lock.

Inherited published v0.17.0 target: `677abddc472322621adf54697ac31c383be3b3c3`.
The v0.17 release remains a published prerelease, distinct from this planned work.
All exact-commit CI, independent review, human acceptance, seal and separate release
approval gates in #281/#411 and `docs/v017-combined-validation.md` remain required.
No sealed reference is retargeted.

Real packet: r190, SHA-256
`cbce536a124f0170b6d93ed8974cbe2c0110dc5409b986ddfb594cce91a7e71a`.
Its 14 table contracts are pinned; private packet/database bytes and selected
assessment text are **not committed**. The database hash is reported provenance,
not a claim to have rehashed the database. Obtain the authorized existing
`PRISM-Framework-Input-r190.json` from the curation bundle to replay the real run.

Earlier preparation reused: `AkashicNET-v018-Offline-Review-2026-10-22.zip`, version 2.
Its eight synthetic tests and unsigned candidate worksheet were preparation, not
real import or human acceptance. This adapter adds actual r190 import and native
integrity validation. Its OMNI retrieved-text checksum is retained in the lock as
representation-specific provenance; original HTML and linked component bytes
remain unpinned. The main-branch public-status document is a reference, not the
complete current manual. PR #367 remains separate, open, unreleased work.

The ambiguous collection-release label is explicitly **deprecated as an integration
release signal**. Dataset revision is used for replay. Neither conflicting historical
label is rewritten or treated as a software/evidence release.

## Retained bounded selection

- Primary: Stevenson, Pasricha and Samararatne's *Deception and Self-Deception in
  Cases of the Reincarnation Type: Seven Illustrative Cases in Asia* (1988), native
  ID equal to its original UVA `STE23.pdf` URL in the lock.
- Community citation: `PRISM-REDDIT-1tlcanb`, prior assessment 43, an N2N lecture
  synthesis. This is a contextual community citation; **no claim that it cites
  this particular primary paper** or concerns the same cases is made.

The earlier pair deliberately contrasts negative-case methodology with community
interpretation relevant to BQ001. It is a bounded engineering case, not a sample
representative of the literature. Exclude source bodies, participant files,
posting-account identities, comments, media and uninspected lectures. No same-case,
cohort-independence, cultural-authority or canonical identity conclusion follows.

Recorded access is partial primary reading and a prior AI-assisted visible-post
read, not fresh full-source appraisal. Fresh primary URL retrieval on 22 October
again failed with 404; the prior bundle also records a direct 403. These responses
do not prove deletion. The community locator was found in the pinned archive;
current availability was not tested, respecting the live Reddit HOLD. Links are
not labelled currently verified. Full primary text, rights/cultural review,
complete method pins and a genuine human assessment remain outstanding.

## Public projection and corrections

The checked-in real-run result is `references/integration/v018/real-public-status.json`.
It is a status artifact, not a substantive research result: **HOLD, no source rows,
no review content**. The real sources are candidates for link-metadata review;
they are not cleared public records. The adapter does not infer disclosure permission
from public visibility, a URL, an existing reading record or user selection.

Projection requires an actual `HUMAN_REVIEWED` record with reviewer identity,
exact source/history bindings and latest-observation disclosures, explicit `LINK_METADATA_ONLY` decisions for
both sources, public visibility and all five inherited restrictions cleared for
scope. A sidecar decision cannot override unknown/held upstream restrictions.
Independent decisions must first be recorded upstream with their evidence. A
fixture uses `SIMULATED_REVIEW` and always exports `SYNTHETIC_NOT_FOR_PUBLICATION`.
This tool trusts authored review/disclosure records; it does **not** authenticate
reviewer identities or independently verify permissions. Deployment would need
an authenticated, governed review service and its own approval.

The export is an allowlist: source IDs, original/current locators, source role,
recorded reading/evidence status (this pilot accepts unassessed only), hashes, dated observation-chain identifiers,
review ID/hash/date and explicit limits. It excludes all private narrative,
reviewer identity, claim text, restriction explanations and raw records. A blocked
pair emits no IDs, input fingerprint, review, or private failure details. Missing
sources fail validation. Failed CLI validation removes the previous output, so
stale cleared projections cannot survive that run. Runtime outputs must be outside
the repository; private output uses mode 0600. Caller-controlled output directories
must themselves be trusted; this is a local tool, not a hardened multi-user service.

Synthetic `before.json` -> `after-awaiting-review.json` -> `after.json` demonstrates
an appended, dated locator correction with the original stable source ID retained.
The old approval becomes stale and yields HOLD. Only a new simulated review bound
to the new observation restores the synthetic projection. The original observation
and prior review remain in the file; evidence status and BQ001 do not change.
Native assessment chains are also validated; cross-packet primary metadata history
still requires curated append-only observations rather than automatic reconciliation.

## Reproduce offline

Install `pytest==8.3.5` and `jsonschema==4.23.0` once. Execution makes no network calls.
The dependency versions are fixed; a transitive dependency hash lock is not included.
From the repository root, use an output directory outside the repository:

```bash
python -m pytest -q tests/test_research_integration_v018.py tests/test_search_reddit_archive.py tests/test_bq001_public_status_boundary.py
python scripts/research_integration_v018.py --contract tests/fixtures/research_integration_v018/before.json --public-out /tmp/v018-before.json
python scripts/research_integration_v018.py --contract tests/fixtures/research_integration_v018/after.json --public-out /tmp/v018-after.json
cmp /tmp/v018-before.json tests/fixtures/research_integration_v018/before-public.json
cmp /tmp/v018-after.json tests/fixtures/research_integration_v018/after-public.json
# Private authorized input, absolute path supplied by its holder:
python scripts/research_integration_v018.py --packet /path/to/PRISM-Framework-Input-r190.json --private-out /tmp/v018-private.json --public-out /tmp/v018-real-status.json
```

Local validation: **59 passed** (43 pilot cases and 16 inherited cases); real-packet
import and byte-for-byte correction replay also passed. See `validation-receipt.json`.

Tests cover deterministic replay, missing sources, duplicate identity versus shared
URL, all restriction categories, context visibility, source/review correction chains,
stale approval, PK/FK failures, native history cycles, current-view inconsistency,
private-text sentinels, credential/query locators, output path aliasing, foundation
pins and unchanged inherited archive/BQ001 boundaries. CI records and checks out the
exact PR head, then compares the synthetic exports byte-for-byte. Public fixtures
are invented `example.invalid` records, not sanitized real PRISM rows.

Rollback: remove this additive pilot or discard generated previews; retain pinned
inputs and earlier observations. No database, accepted graph edge, source evidence
label, live Site, release tag or sealed checkpoint is changed. Offline green tests
prove bounded mechanical behavior, not scientific validity or release readiness.
