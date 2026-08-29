# AkashicNET Drive validation denominator

Status: denominator definition only — no completion points awarded
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Purpose

The 10-point validation component measures independent consistency and integrity checks. Validation is not the same as traversal, inventory or canonicalisation, and no points are awarded merely because those earlier stages exist.

## Five validation gates

Each gate is worth 2 points and must be explicitly executed and recorded before credit is awarded.

1. `TOPOLOGY_RECONCILIATION` — confirm all 66 top-level roots and all known descendant folder nodes reconcile with the traversal ledger, with no unresolved access/error states.
2. `OBJECT_COUNT_RECONCILIATION` — compare root and descendant direct-document counts against screening ledgers and resolve discrepancies such as document-versus-folder shorthand.
3. `PAGINATION_AND_TERMINALITY_AUDIT` — verify provider pagination state and terminal-folder claims for all counted nodes; incomplete provider pages cannot count as exact.
4. `TECHNICAL_AND_DUPLICATE_INTEGRITY` — verify technical exclusions, zero-byte/incomplete artefacts and high-confidence duplicate-copy families without collapsing editions/translations incorrectly.
5. `PROVENANCE_AND_PRIVACY_INTEGRITY` — verify every public-facing record preserves source collection/provenance and does not bypass privacy/public-status controls.

## Pass criteria

A validation gate passes only when its test procedure, denominator, exceptions and result are persisted. Partial gates receive no automatic proportional credit unless a future version explicitly defines a sub-denominator before testing begins.

## Current score

0 / 10 points remain awarded. The next validation pass should execute the gates rather than retroactively crediting previous work.
