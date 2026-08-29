# AKASHICNET-004 validation checkpoint — v0.4.7-dev

Date: 2026-08-29

## Stage-A root screening

All 65 nominated top-level Drive collections have now received an explicit metadata-only TITLE_SIZE_METADATA_PASS.

- Top-level roots screened: 65 / 65
- Direct document objects represented by those screening batches: 1,285
- Existing working whole-corpus denominator: 2,152 document objects
- Conservative Stage-A canonicalisation coverage using the existing denominator: 1,285 / 2,152 = 59.7119%
- Canonicalisation component contribution: 8.9568 / 15
- Verified global floor using the existing denominator: 73.9568%

## Validation discrepancy discovered

The root screening sum is 1,285 direct document objects. The previously frozen denominator described 1,287 root/direct objects plus 865 descendant objects = 2,152. A fresh metadata-only query of the nominated library root returned no direct document objects, so the two-object difference must be reconciled before changing the denominator.

Judaism is one concrete correction: a fresh document-only provider pass returns two direct documents, with the Talmud represented separately as a descendant folder. Earlier shorthand described three direct records. This may explain one object of the discrepancy, but the denominator is NOT revised until the complete root census is compared row-by-row with the 65 screening batches.

Therefore:

- Keep 2,152 as the conservative frozen denominator for scoring until reconciliation is complete.
- Do not award validation-component points merely for discovering the discrepancy.
- Do not award v0.4.8 yet.
- Next validation task: row-level comparison of root census counts against screening-batch counts, then descendant Stage-A screening.

## Privacy boundary

All passes remain metadata-only. Shared/access-visible is not treated as PUBLIC_VERIFIED. No document bodies were fetched, no embeddings were generated, and no private/shared Drive material is promoted into the public manifest from this screening work.
