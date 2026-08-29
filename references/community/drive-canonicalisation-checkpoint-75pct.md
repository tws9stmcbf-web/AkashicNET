# AkashicNET Drive canonicalisation checkpoint — 75% verified floor

Status: PRE-ALPHA v0.4.7-dev
Scope: nominated Akashic Library Drive tree only

## Verified global completion

- traversal: 66 / 66 top-level roots closed = 40.0 / 40 points
- metadata inventory: 195 / 195 known folder nodes exact = 25.0 / 25 points
- canonicalisation screening denominator: 2,152 observed document objects
- all root direct-document batches reconciled: 1,287 / 1,287 direct root documents screened at Stage A
- first descendant screening tranche: 150 documents across H. G. Wells (50), Dostoevsky (29), Manly P. Hall (27), Alice A. Bailey (26), and Friedrich Nietzsche (18)
- total Stage-A screened document objects: 1,437 / 2,152 = 66.7751%
- canonicalisation contribution: 66.7751% × 15 = 10.0163 points
- privacy/public-status classification: 0 / 10 points awarded globally
- validation: 0 / 10 points awarded globally

Verified AKASHICNET-004 lower bound = 40.0 + 25.0 + 10.0163 = **75.0163%**.

The project therefore remains **PRE-ALPHA v0.4.7-dev**. The 70% gate is comfortably exceeded, but the 80% gate for v0.4.8 is not yet awarded.

## Root-screening reconciliation

The root census establishes 1,287 direct documents across all 66 roots. The union of `drive-canonicalisation-screening-batches.csv` and `drive-canonicalisation-root-screening-completion.csv` covers all 66 root collections. Root coverage is therefore measured against the root census rather than by summing overlapping batch files.

One correction is required when the primary screening ledger is next safely rewritten: Shamanism has **14 direct documents plus one child folder**, not 15 direct documents. The root census is authoritative for the direct-document denominator.

## First descendant tranche

The first descendant Stage-A screening file contains five terminal author/collection batches:

- Literature / H. G. Wells — 50
- Literature / Dostoevsky — 29
- PDF / Manly P. Hall — 27
- PDF / Alice A. Bailey — 26
- Biographies / Friedrich Nietzsche — 18

Total descendant tranche = **150 documents**.

Stage-A means title/size/provenance metadata has been brought into the canonicalisation workflow. It does not mean every item is hash-verified or finally resolved. Uncertain items remain REVIEW_REQUIRED rather than being silently treated as unique.

## Canonicalisation ontology

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Cross-folder recurrence remains provenance information. A work appearing under different traditions or thematic collections should normally map to one canonical work with multiple `appears_in` relationships while preserving copy, edition and translation distinctions.

## Next gate

With privacy and validation still scored conservatively at zero, v0.4.8 cannot be awarded yet. The next long pass should continue descendant screening in large batches and establish explicit privacy/public-status and validation denominators rather than awarding unmeasured credit.
