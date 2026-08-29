# AkashicNET canonical resolution checkpoint v0.5.1

Date: 2026-08-29
Status: **PRE-ALPHA v0.5.1-dev**
Scope: last successful pagination-complete Drive census snapshot, GitHub Actions run `33247025163`
Source artefact digest: `sha256:d0a1c3d0a83a6367f086097c5bdab9880c990754a3f1226e6714b141b7f4717b`

## Stage-1 result

The new conservative canonical resolver was validated against the successful live corpus snapshot.

- live objects read: **2,459**
- unique Drive IDs: **2,459**
- stable manifestation IDs derivable: **2,459 / 2,459**
- deterministic technical exclusions: **28**
  - zero-byte: **16**
  - `.DS_Store`: **11**
  - `.crdownload`: **1**
- exact `filename + size` duplicate-candidate families: **127**
- objects participating in those candidate families: **269**
- canonical work IDs automatically assigned: **0**
- unsupported equivalence assertions: **0**

## Meaning

v0.5.1 Stage 1 now has a deterministic identity layer for manifestations and a reproducible adjudication queue.

It deliberately does **not** claim that matching filename and size proves:

- byte identity;
- edition identity;
- translation identity;
- canonical-work identity;
- claim identity;
- or truth/evidence status.

Those promotions require stronger evidence or explicit adjudication.

## CI state

The workflow is wired so a successful fresh `Drive full recursive census` immediately runs `drive_canonical_resolution_stage1.py` and uploads the canonical-resolution artefacts alongside the census.

The most recent fresh-census attempt failed before canonical resolution because the temporary Google OAuth access token had expired and Drive returned HTTP errors for all 66 roots. This is an authentication-lifetime issue, not a canonical-resolution failure.

Until durable Drive authentication is installed, this checkpoint is anchored to the last successful live census snapshot and its immutable GitHub Actions artefact digest above.

## Next promotion gate

The next v0.5.1 step is **candidate-family evidence resolution**:

1. separate technical artefact families from document families;
2. obtain cryptographic hashes where practical;
3. enrich candidate families with bibliographic metadata;
4. ACCEPT equivalence only when evidence supports it;
5. retain editions, translations, volumes and adaptations separately when evidence differs;
6. write every decision with provenance and reason.

Integrity rule:

`same filename != same file != same edition != same work != same claim != same truth`
