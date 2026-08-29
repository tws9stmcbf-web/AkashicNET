# AkashicNET Drive canonicalisation checkpoint — v0.4.7-dev

Status: PRE-ALPHA v0.4.7-dev
Scope: nominated Akashic Library Drive tree only

## Verified global completion

- traversal: 66 / 66 top-level roots closed = 40.0 / 40 points
- metadata inventory: 195 / 195 known folder nodes exact = 25.0 / 25 points
- canonicalisation screening denominator: 2,152 observed document objects
- Stage-A metadata screening completed for 750 document objects across 15 high-volume roots
- canonicalisation screening coverage: 750 / 2,152 = 34.8513%
- canonicalisation contribution: 34.8513% × 15 = 5.2277 points
- privacy/public-status classification: 0 / 10 points awarded globally
- validation: 0 / 10 points awarded globally

Verified AKASHICNET-004 lower bound = 40.0 + 25.0 + 5.2277 = **70.2277%**.

Therefore the 70% release gate is earned and the project advances to **PRE-ALPHA v0.4.7-dev**.

## Screening definition

Stage-A screening is a metadata-only title/size/provenance pass. Every physical object in a completed batch has been brought inside the canonicalisation workflow and is no longer UNSCREENED at batch level. The allowed downstream dispositions are UNIQUE_CANDIDATE, DUPLICATE_COPY, SAME_DRIVE_OBJECT_MULTICOLLECTION, DUPLICATE_WORK, EDITION_VARIANT, TRANSLATION_VARIANT, MULTI_VOLUME_MEMBER, AGGREGATE_COLLECTION, TECHNICAL_EXCLUSION, or REVIEW_REQUIRED.

Stage-A screening does **not** mean every object is fully canonicalised or hash-verified. It establishes explicit corpus coverage and sends unresolved cases to REVIEW_REQUIRED rather than silently treating them as unique.

## Completed Stage-A root batches

Buddhism 100; Hinduism 96; Metaphysics 100; Philosophy 86; PDF 78; Literature 31; Ancient Religions 46; Religion 26; Secret Societies 26; Gnosticism 27; Astrology 26; Kabbalah 26; Christianity 24; Islam 23; Alchemy 35.

Total = **750 physical document objects**.

## Important findings from this pass

- Astrology contains two separate `Astrology (Zodiac Personalities).pdf` objects with identical sizes, a strong duplicate-copy candidate pending hash verification.
- Islam contains `Masnavi.pdf` and `Masnavi-I-Manavi-Teachings-of-Rumi.pdf`, both 1,124,417 bytes; title/author normalisation should test them as a same-work/copy candidate.
- Ancient Religions contains `CLF-TheEnneagram-Gurdjieff.pdf` at the same 106,179-byte size as the Philosophy copy, strengthening a cross-collection duplicate candidate.
- Christianity and Ancient Religions both contain Augustine's `City of God and On Christian Doctrine` family; compare physical metadata before copy-level collapse.
- Alchemy reconfirms identical-size duplicate-copy candidates for `Alchemy Ancient and Modern` and `Twelve Keys`.
- Cross-domain recurrence is common: the same work can legitimately appear in religious, philosophical, occult, historical or author-centric collections. `appears_in` therefore remains a provenance relation rather than an assertion of category truth.

## Next gate

v0.4.8 requires ≥80% overall verified completion. With privacy and validation still scored at zero, canonicalisation alone would need 15 points, i.e. 100% of the 2,152-object screening denominator. A more realistic path is to continue corpus screening while also creating defensible denominators for privacy/public-status classification and validation.

The next long pass should continue Stage-A screening into descendant collections and remaining roots, while starting systematic object-level disposition records for high-confidence duplicate and technical-exclusion clusters.
