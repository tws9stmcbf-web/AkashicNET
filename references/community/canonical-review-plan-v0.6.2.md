# Canonical family adjudication v0.6.2

Date: 2026-08-29
Status: ACTIVE

## Objective
Reduce the 126 non-technical exact-name+size review families using evidence-aware adjudication without converting metadata similarity into identity claims.

## Starting state
- Physical-object denominator: 2,459.
- Non-technical review families: 126 / 258 objects.
- Existing accepted canonical promotions: 3 works, backed by three SHA-256 MATCH records.
- Existing accepted graph promotions: 9 edges.
- Edition promotion remains disabled unless edition-specific evidence exists.

## First adjudication wave
The checked-in `canonical-review-queue-v0.6.2.csv` selects 19 high-value families for the first wave:
- six three-object families, prioritised because one successful three-way hash verification can collapse multiple copy candidates safely;
- six ordinary two-object families, including two Mushrooms Russia and History volumes already supported by Stage-B family adjudication;
- seven Forbidden History volume families, where byte-copy resolution must remain separate from edition/volume structure.

## Decision contract
For every family:
1. Metadata-only equality => REVIEW_REQUIRED, never DUPLICATE_COPY.
2. Matching SHA-256 for authorised raw bytes => BYTE_IDENTICAL_VERIFIED for those manifestations only.
3. A byte-identical result may create DUPLICATE_OF edges.
4. `REPRESENTS work:*` requires independent work-identity evidence in addition to byte identity when the work identity is not already adjudicated.
5. Edition IDs remain blank unless edition-specific evidence establishes the edition.
6. Rights state remains UNKNOWN_UNVERIFIED unless separately adjudicated.
7. Scientific-evidence state remains NOT_EVALUATED unless separately adjudicated.
8. A mismatch does not imply different works; it only rejects byte identity.
9. Ambiguity remains HOLD / REVIEW_REQUIRED.

## Priority strategy
Wave A: three-member exact-name+size families.
Wave B: two-member families with prior Stage-B context or high retrieval value.
Wave C: structured multi-volume/edition sets such as Forbidden History.
Wave D: remaining queue, processed deterministically by candidate_family_id.

## Completion criteria for v0.6.2
- every selected wave family has an explicit evidence state;
- every ACCEPT has machine-checkable evidence provenance;
- no HOLD emits graph promotion edges;
- duplicate-copy, work identity, edition identity, rights and scientific-evidence states remain orthogonal;
- queue statistics are reproducible from checked-in artefacts.
