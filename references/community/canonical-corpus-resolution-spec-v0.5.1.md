# AkashicNET canonical corpus resolution spec v0.5.1

Date: 2026-08-29
Status: PRE-ALPHA
Scope: 2,459-object live Drive census established by v0.5.0

## Goal

Move from a closed object census to defensible work/manifestation resolution without inventing equivalence.

The first v0.5.1 pass creates stable manifestation identities and a review queue. It does **not** automatically promote metadata similarity into canonical-work identity.

## Entity levels

- `manifestation_id`: stable ID for one observed Drive object.
- `candidate_family_id`: stable ID for a group that deserves equivalence review.
- `canonical_work_id`: assigned only after sufficient evidence or adjudication.

## Stage-1 rules

1. Every unique Drive object receives one stable `AKM-*` manifestation ID.
2. Deterministic technical artefacts remain explicit exclusions.
3. Exact `filename + size` matches produce `AKCF-*` candidate families only.
4. Exact metadata does **not** prove byte identity.
5. Byte identity does **not** by itself prove edition/work identity where surrounding metadata conflicts.
6. Translations, editions, volumes, adaptations and compilations must remain distinct unless explicitly resolved.
7. `canonical_work_id` stays blank when evidence is insufficient.
8. Every unresolved semantic decision remains `REVIEW_REQUIRED`.

## Promotion evidence

A candidate may eventually be promoted using one or more of:

- matching cryptographic content hash;
- trusted bibliographic identifiers (ISBN, DOI, OCLC, catalogue IDs);
- explicit edition/translation metadata;
- title/author/publisher/year concordance;
- document-body fingerprinting;
- manual adjudication with provenance.

Promotion must record the evidence used. No truth, scientific-validity or public-rights claim follows from canonical equivalence.

## Stage-1 outputs

`scripts/drive_canonical_resolution_stage1.py` generates:

- `drive-canonical-resolution-ledger-v0.5.1.csv`
- `drive-canonical-candidate-families-v0.5.1.csv`
- `drive-canonical-resolution-summary-v0.5.1.json`

## Expected live baseline

From v0.5.0 metadata screening:

- live Drive objects: 2,459
- deterministic technical exclusions: 28
- exact `name + size` candidate families: 127
- objects in candidate families: 269

The Stage-1 run must reproduce these figures from the fresh live census or fail visibly through changed output.

## Integrity principle

`same filename != same file != same edition != same work != same claim != same truth`
