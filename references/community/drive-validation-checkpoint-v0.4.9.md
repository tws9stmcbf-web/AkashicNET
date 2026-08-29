# AKASHICNET-004 validation checkpoint — v0.4.9 preparation

Date: 2026-08-29
Scope: nominated Akashic Library Google Drive tree only

## Validation model

The validation denominator defines five gates worth 2 points each. This checkpoint executes only gates for which the repository already contains an explicit denominator, procedure, exceptions and reconcilable result. No privacy/public-status credit is inferred from shared Drive access.

## Gate 1 — TOPOLOGY_RECONCILIATION

Status: NOT YET CREDITED

The traversal layer reports all 66 top-level roots closed in the v0.4.8 checkpoint, but this validation gate also requires all known descendant folder nodes to reconcile with no unresolved access/error states and an explicit persisted test procedure. That full descendant-level audit is not established by this checkpoint, so no 2-point credit is awarded here.

## Gate 2 — OBJECT_COUNT_RECONCILIATION

Status: PASS
Credit: 2.000000 / 2

Procedure:

1. Use the authoritative top-level direct-document total recorded by the corrected v0.4.8 checkpoint: 1,287.
2. Use the corrected descendant-document total: 857.
3. Confirm the physical/document-object denominator: 1,287 + 857 = 2,144.
4. Independently reconcile against the cumulative Stage-A screening ledgers:
   - initial Stage-A root batches: 750
   - remaining 51 root batches: 537
   - non-PDF descendant expansion: 722
   - corrected PDF descendant batch: 135
5. Confirm 750 + 537 + 722 + 135 = 2,144.
6. Preserve the documented Montalk correction: the previous 2,152 denominator double-counted eight documents in `PDF/Montalk/Not Important`; those eight are represented once in the corrected 2,144 denominator.

Result:

- census-derived denominator: 2,144
- screening-ledger total: 2,144
- discrepancy: 0
- gate result: PASS

This validates object-count consistency only. It does not assert byte-level identity, public visibility, canonical-work completeness or descendant pagination integrity.

## Gate 3 — PAGINATION_AND_TERMINALITY_AUDIT

Status: NOT YET CREDITED

No new credit is awarded until provider pagination state and terminal-folder claims are explicitly audited across the counted nodes.

## Gate 4 — TECHNICAL_AND_DUPLICATE_INTEGRITY

Status: NOT YET CREDITED

Stage-A dispositions exist, but byte-level hashing and technical-exclusion integrity are not complete enough to pass this gate.

## Gate 5 — PROVENANCE_AND_PRIVACY_INTEGRITY

Status: NOT YET CREDITED

Public-manifest eligibility still requires independent public verification. `ACCESS_NOT_VERIFIED` is not treated as `PUBLIC_VERIFIED`.

## Validation score

- OBJECT_COUNT_RECONCILIATION: 2.000000 points
- all other validation gates: 0.000000 points

Validation component = **2.000000 / 10** under the five-gate validation model.

## Global scoring note

The v0.4.8 checkpoint separately recorded 3.384615 validation points under an earlier node-coverage convention. This file does not add the two schemes together. To avoid double counting, a future global checkpoint must choose one validation convention as authoritative and reconcile the historical score before changing the overall project percentage.

## Next action

Execute `TOPOLOGY_RECONCILIATION` or `PAGINATION_AND_TERMINALITY_AUDIT` against all known folder nodes, then replace the historical node-coverage validation score with the five-gate score only when that convention is explicitly adopted for global milestone scoring.
