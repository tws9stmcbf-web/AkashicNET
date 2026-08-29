# AkashicNET Drive validation denominator

Status: active validation definition
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Purpose

The 10-point validation component measures independent consistency and integrity checks. Validation is not the same as traversal, inventory or canonicalisation, and no points are awarded merely because those earlier stages exist.

The former fixed 195-folder / 2,144-object denominator is superseded by the pagination-complete recursive provider crawl in GitHub Actions run `33247025163`.

Current authoritative live denominators:

- top-level nominated roots: **66**
- unique folder nodes: **199**
- unique non-folder Drive objects: **2,459**

## Five validation gates

Each gate is worth 2 points and must be explicitly executed and recorded before credit is awarded.

1. `TOPOLOGY_RECONCILIATION` — confirm all 66 top-level roots and every recursively discovered descendant folder reconcile with the live provider crawl, with no unresolved access/error states.
2. `OBJECT_COUNT_RECONCILIATION` — confirm the provider crawl's object occurrences reconcile to unique Drive object IDs and resolve historical capped-page/double-count discrepancies.
3. `PAGINATION_AND_TERMINALITY_AUDIT` — follow every provider `nextPageToken` for every recursively discovered folder until absent; incomplete provider pages cannot count as exact.
4. `TECHNICAL_AND_DUPLICATE_INTEGRITY` — verify technical exclusions and metadata duplicate candidates without promoting metadata equality to byte identity or collapsing editions/translations incorrectly.
5. `PROVENANCE_AND_PRIVACY_INTEGRITY` — verify every object preserves source/parent provenance and remains subject to fail-closed privacy/public-status controls.

## Pass criteria

A validation gate passes only when its test procedure, denominator, exceptions and result are persisted. Partial gates receive no automatic proportional credit unless a future version explicitly defines a sub-denominator before testing begins.

## Current result

The v0.5.0 live recursive census and full-corpus rescreen satisfy all five gates:

- Gate 1: PASS 2/2
- Gate 2: PASS 2/2
- Gate 3: PASS 2/2
- Gate 4: PASS 2/2
- Gate 5: PASS 2/2

Validation score: **10 / 10**.

Authoritative result: `references/community/drive-validation-checkpoint-v0.5.0.md`.
