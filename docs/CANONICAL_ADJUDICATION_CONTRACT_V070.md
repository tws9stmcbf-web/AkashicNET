# Canonical Adjudication Contract v0.7.0

Status: PRE-ALPHA validation contract

## Purpose

This contract governs promotion of candidate relationships into AkashicNET canonical work and edition assertions. It is deliberately stricter than duplicate-byte verification.

## Decision states

Each candidate must end in exactly one state:

- `ACCEPT` — sufficient independent evidence exists for the asserted relationship.
- `HOLD` — evidence is incomplete, ambiguous, conflicting, or unavailable.
- `REJECT` — available evidence contradicts the asserted relationship or is insufficient under a deterministic rejection rule.

`HOLD` is the default state when confidence is not earned.

## Evidence boundaries

`SHA256_EQUAL` establishes byte identity only. It may support a duplicate-copy assertion, but by itself it MUST NOT establish canonical work identity, edition identity, translation identity, authorship, publication history, rights status, public-release permission, scientific validity, safety, efficacy, or endorsement.

`SHA256_MISMATCH` rejects byte-identical-copy identity only. It MUST NOT by itself prove that two objects represent different works or editions.

Filename, path, size, timestamps, lexical overlap, topic similarity, semantic similarity, or shared source location are nomination signals only. They MUST NOT independently promote a candidate.

## Minimum promotion rule

A canonical work or edition relationship may be `ACCEPT` only when:

1. the asserted relationship is explicit and narrowly defined;
2. at least one independent evidence source supports the relationship beyond private object metadata or byte identity;
3. provenance for the supporting evidence is recorded;
4. contradictory evidence has been checked and either resolved or documented;
5. the decision can be reproduced from the recorded evidence without exposing private corpus metadata; and
6. no separate rights, scientific-evidence, or safety status is inferred from the canonicalization decision.

If any required condition is unmet, the candidate remains `HOLD` unless a deterministic rejection rule applies.

## Allowed relationship classes

- `REPRESENTS_WORK`
- `REPRESENTS_EDITION`
- `DUPLICATE_COPY_OF`
- `TRANSLATION_OF`
- `DERIVED_FROM`

Relationship classes must not be silently conflated. In particular, `DUPLICATE_COPY_OF` does not imply `REPRESENTS_EDITION`, and `REPRESENTS_EDITION` does not establish rights or truth.

## Public/private boundary

Public adjudication records may contain aggregate counts, public bibliographic identifiers, public reference URLs, decision states, evidence classes, rationale, and uncertainty notes.

They MUST NOT contain private Drive IDs, private filenames or paths, private timestamps, private object sizes where they identify corpus objects, per-object private hashes, access tokens, or other private object-level metadata.

## Promotion guardrails

The following fields are independent and default to `false` unless separately adjudicated:

- `rights_promoted`
- `public_release_promoted`
- `scientific_evidence_promoted`
- `safety_or_efficacy_promoted`

Canonical identity decisions MUST NOT set these fields to `true` as a side effect.

## Audit requirement

Every `ACCEPT` or `REJECT` record must include a short rationale and evidence class. Every `HOLD` record should state the missing evidence or ambiguity where known.

The validator for this contract is fail-closed: malformed records, unknown states, implicit promotions, or forbidden private fields fail validation.
