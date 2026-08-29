# AKASHICNET-004 validation checkpoint — v0.4.9 workstream

Date: 2026-08-29
Scope: nominated Akashic Library Google Drive tree only

## Validation model

This checkpoint uses the predeclared five-gate validation model in `drive-validation-denominator.md`. Each gate is worth 2 points and is credited only when its denominator, procedure, exceptions and result are persisted.

## Gate 1 — TOPOLOGY_RECONCILIATION — PASS (2/2)

Denominator:

- 66 top-level roots
- 115 immediate child folders
- 14 deeper descendant folders
- 195 known folder nodes total

Evidence:

- `drive-metadata-checkpoint-v0.4.6-final.md` records 66/66 structurally closed roots and exact direct-document/direct-child-folder counts for all 195 known folder nodes.
- `drive-traversal-ledger-corrections.csv` resolves the former Ancient Religions `ACCESS_UNRESOLVED` state to `COMPLETE` after a fresh metadata-only retry of `Ancient Religions/Gnosis` returned six direct documents and zero child folders.
- A fresh 2026-08-29 provider recheck of Drive folder `1KI6_vTeuNGSD4cs8mYrW_v8F4YOPUgYd` again returned exactly six PDF documents and zero child folders.

Result: PASS.

## Gate 2 — OBJECT_COUNT_RECONCILIATION — PASS (2/2)

Procedure:

1. Use the corrected v0.4.8 totals: 1,287 top-level direct documents plus 857 descendant documents = 2,144 physical document objects.
2. Independently reconcile against cumulative Stage-A screening ledgers: 750 + 537 + 722 + 135 = 2,144.
3. Preserve the Montalk correction: the previous 2,152 denominator double-counted eight documents in `PDF/Montalk/Not Important`.

Result:

- census-derived denominator: 2,144
- screening-ledger total: 2,144
- discrepancy: 0
- gate result: PASS

## Gate 3 — PAGINATION_AND_TERMINALITY_AUDIT — BLOCKED AFTER FIRST CI EXECUTION (0/2)

The executable audit is implemented by `scripts/drive_pagination_audit.py` and `.github/workflows/drive-pagination-audit.yml` against the frozen 195-node denominator.

First CI execution:

- workflow: `Drive pagination audit`
- run ID: `33243706508`
- trigger commit: `7fda3e8354e6ecdcf20b734bdd64c0ffb107e2e5`
- result: FAILURE before any folder-node audit began
- cause: GitHub Actions environment contained an empty `GOOGLE_DRIVE_ACCESS_TOKEN`
- script exit: code 2 with `GOOGLE_DRIVE_ACCESS_TOKEN is required`
- audit CSV: not produced
- validation credit: 0 / 2

This is an execution-environment blocker, not a corpus failure. The gate remains uncredited until the read-only Drive credential is available to CI and a complete 195-node audit passes the frozen criteria.

## Gate 4 — TECHNICAL_AND_DUPLICATE_INTEGRITY — PASS (2/2)

Persisted audit: `drive-technical-duplicate-integrity-v0.4.9.md`.

The audit verifies that known zero-byte/incomplete technical artefacts remain explicitly tracked and that the 29 persisted duplicate/work/edition families are represented without destructive over-deduplication. Strong same-title/same-size duplicate-copy candidates remain pending hash verification for byte identity; editions, translations, multi-volume structures and alternate copies remain distinct manifestations until stronger evidence exists.

This gate validates safe technical/duplicate handling. It does not claim that all duplicate-copy candidates are byte-identical.

Result: PASS.

## Gate 5 — PROVENANCE_AND_PRIVACY_INTEGRITY — PASS (2/2)

Persisted audit: `drive-provenance-privacy-integrity-v0.4.9.md`.

The publication boundary fails closed:

- 2,144 Drive document objects remain in the corpus/audit layer
- 0 are persisted as `PUBLIC_VERIFIED`
- 0 are persisted as `ELIGIBLE` for a public Drive manifest
- `ACCESS_NOT_VERIFIED` is explicitly not promoted to public permission
- Drive/collection provenance is preserved throughout canonicalisation

This gate verifies boundary integrity only. It does **not** award privacy/public-status classification points to the 2,144 objects.

Result: PASS.

## Reconciled validation score

Passed gates: 4 / 5

Validation component = **8.000000 / 10**.

The only remaining validation gate is `PAGINATION_AND_TERMINALITY_AUDIT`.

## Reconciled global completion

- traversal: 40.000000 / 40
- metadata inventory: 25.000000 / 25
- canonicalisation Stage-A: 15.000000 / 15
- privacy/public-status classification: 0.000000 / 10
- validation: 8.000000 / 10

Verified AKASHICNET-004 completion = **88.000000%**.

Project status remains **AkashicNET PRE-ALPHA v0.4.8-dev** because the repository-defined v0.4.9 gate is 90% and is not yet earned.

## Remaining path to v0.4.9

Exactly 2 percentage points remain to reach 90%.

Highest-leverage routes:

1. configure a read-only Drive credential for CI and pass the 195-node `PAGINATION_AND_TERMINALITY_AUDIT` (+2 validation points), or
2. earn at least 2 privacy/public-status points through a defensible object-level classification ledger without treating shared access as public permission.
