# AkashicNET Drive canonicalisation checkpoint — v0.4.7-dev

Status: PRE-ALPHA v0.4.7-dev
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Verified global completion

- traversal: 66 / 66 top-level roots closed = 40.0000 / 40 points
- metadata inventory: 195 / 195 known folder nodes exact = 25.0000 / 25 points
- canonicalisation screening denominator: 2,152 observed document objects
- all 66 top-level roots now have Stage-A screening for their direct documents
- authoritative root-direct screened total: 1,287 document objects
- six large descendant collections add 164 screened document objects
- total Stage-A screened: 1,451 document objects
- canonicalisation screening coverage: 1,451 / 2,152 = 67.4257%
- canonicalisation contribution: 67.4257% × 15 = 10.1138 points
- privacy/public-status classification: 0 / 10 points awarded globally
- validation: 0 / 10 points awarded globally

Verified AKASHICNET-004 lower bound = 40.0000 + 25.0000 + 10.1138 = **75.1138%**.

The project remains **PRE-ALPHA v0.4.7-dev**. The 80% v0.4.8 gate is not yet awarded.

## Screening definition

Stage-A screening is a metadata-only title/size/provenance pass. Every physical object in a completed batch has been brought inside the canonicalisation workflow and is no longer UNSCREENED at batch level. Allowed downstream dispositions are UNIQUE_CANDIDATE, DUPLICATE_COPY, SAME_DRIVE_OBJECT_MULTICOLLECTION, DUPLICATE_WORK, EDITION_VARIANT, TRANSLATION_VARIANT, MULTI_VOLUME_MEMBER, AGGREGATE_COLLECTION, TECHNICAL_EXCLUSION, or REVIEW_REQUIRED.

Stage-A screening does not mean every object is fully canonicalised or hash-verified. It establishes explicit corpus coverage and sends unresolved cases to REVIEW_REQUIRED rather than silently treating them as unique.

## Root-level reconciliation

The root census is authoritative for direct-document counts. It contains 1,287 direct document objects across 66 roots. One historical screening row used the old Shamanism shorthand of 15 objects; the reconciled census establishes 14 direct documents plus one child folder. Coverage calculations therefore use the authoritative 1,287 figure rather than a naive sum of historical screening rows.

Golden Dawn was the final root to receive an explicit Stage-A pass. It contains three direct documents.

## Descendant Stage-A batches

The first descendant-screening set covers:

- Literature / H. G. Wells — 50
- Literature / Dostoevsky — 29
- PDF / Manly P. Hall — 27
- PDF / Alice A. Bailey — 26
- Biographies / Friedrich Nietzsche — 18
- Islam / In The Shade Of The Quran — 14 physical PDFs

Total descendant Stage-A coverage added = **164 physical document objects**.

Qutb illustrates why physical files and logical volumes remain separate layers: one physical PDF combines logical volumes 15-17. Nietzsche remains an 18-member logical-volume series. The Hall collection mixes authored works with archival/manuscript-box material. Bailey retains same-size duplicate-copy candidates for Discipleship in the New Age Volumes 1 and 2.

## Canonicalisation architecture

`Drive object -> usable document -> copy / edition / translation -> logical volume -> canonical work -> appears_in collection`

Cross-folder recurrence remains provenance rather than category truth. Metadata title/size equality can create a strong duplicate-copy candidate, but byte identity still requires hashing.

## Next gate

v0.4.8 requires >=80% overall verified completion. The current gap is **4.8862 percentage points**.

The next pass should continue Stage-A screening across the remaining 701 descendant document objects while separately freezing defensible denominators for privacy/public-status classification and validation. No privacy or validation points are awarded merely for defining those denominators.
