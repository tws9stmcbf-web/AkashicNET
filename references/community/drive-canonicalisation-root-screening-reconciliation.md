# AkashicNET root-level canonicalisation screening reconciliation

Status: PRE-ALPHA v0.4.7-dev
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Result

All 66 top-level roots now have a completed Stage-A metadata screening pass for their direct document objects.

The authoritative direct-document denominator is the reconciled root census:

- 66 top-level roots
- 1,287 direct document objects
- 115 immediate child folders
- no root-level pagination gaps in the root census

The canonicalisation corpus denominator remains 2,152 observed document objects across the full tree.

Therefore root-direct Stage-A screening coverage is:

`1,287 / 2,152 = 59.8048%`

Canonicalisation contribution under the fixed 15-point weighting:

`59.8048% × 15 = 8.9707 points`

Combined verified lower bound:

- traversal: 40.0000 / 40
- metadata inventory: 25.0000 / 25
- canonicalisation Stage-A coverage: 8.9707 / 15
- privacy/public-status: 0 / 10
- validation: 0 / 10

`overall verified lower bound = 73.9707%`

The project therefore remains PRE-ALPHA v0.4.7-dev. v0.4.8 is not yet awarded.

## Reconciliation notes

The screening-batch ledger reached 65 root batches before Golden Dawn. Golden Dawn was then screened explicitly and contains three direct document objects.

The root census is authoritative for object counts. One earlier screening row used the old Shamanism shorthand of 15 objects, but the reconciled root census establishes 14 direct documents plus one child folder. Canonicalisation coverage therefore uses 1,287 direct documents rather than a naive sum of historical screening-batch rows.

This file does not claim that all 1,287 objects are fully canonicalised. Stage-A means title/size/provenance metadata has been screened and each object is inside the canonicalisation workflow. Final disposition, hash verification, edition discrimination and work-level merging remain downstream work.

## Next step

Move Stage-A screening into descendant collections, prioritising high-volume terminal corpora. Then define and freeze independent denominators for privacy/public-status classification and validation before awarding points from those workstreams.
