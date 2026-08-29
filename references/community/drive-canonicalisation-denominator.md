# AkashicNET Drive canonicalisation denominator

Status: PRE-ALPHA v0.4.6-dev
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Purpose

This checkpoint establishes the first defensible denominator for the 15-point canonicalisation/deduplication component of AKASHICNET-004.

The denominator is based on physical document objects observed in the complete metadata census. Folder nodes are not part of this denominator because traversal and metadata-node completeness are already scored separately.

## Document-object denominator

- Direct document objects at 66 top-level roots: 1,287
- Document objects represented in the descendant census: 865
- Total observed document-object denominator: 2,152

The descendant total preserves the already-reconciled Gospels subtree total of 46 documents: the former parent-level 46 count was later decomposed into 30 direct Gospels documents plus 16 documents in seven terminal child collections, so the corpus document total is unchanged by that structural correction.

## Known technical exclusions

Known technical artefacts must not be confused with canonical works.

Document-level exclusions currently known inside the 2,152 document-object denominator:

- Magick: at least 1 zero-byte PDF
- Buddhism: at least 1 zero-byte PDF
- PDF/Bookz: 5 zero-byte document objects
- Law/Black's Law Dictionary: 1 `.crdownload` artefact

Known document-level exclusions represented in the denominator: 8

Therefore the current candidate usable-document count after only already-known exclusions is 2,144.

Three `.DS_Store` artefacts previously observed in Theosophy author folders are tracked separately but are not subtracted from the 2,152 denominator because the document-only metadata counts already exclude those non-document objects.

This is not a claim that only eight technical exclusions exist. It is the current verified minimum.

## Canonicalisation numerator

`drive-canonicalisation-candidates.csv` currently represents:

- 29 identified canonicalisation families
- 27 REVIEWED families
- 2 CANDIDATE families
- 130 physical Drive manifestations actively reconciled inside those families
- 61 logical units represented after work/volume-level reconciliation
- 69 redundant, alternate-copy, translation, edition, or cross-collection manifestations exposed inside those identified clusters

Only the 130 physical manifestations that have been explicitly placed into a canonicalisation family are counted in the conservative numerator. Documents that may have been inspected informally but are not represented in the screening/canonicalisation ledger receive zero credit.

## Canonicalisation coverage score

Conservative physical-object reconciliation coverage:

130 / 2,152 = 6.0409%

The canonicalisation/deduplication component is worth 15 points, therefore:

6.0409% × 15 = 0.9061 verified completion points

Combined with the already verified 65.0 points from complete traversal and metadata inventory:

65.0 + 0.9061 = 65.9061% verified AKASHICNET-004 completion

## Version gate

- v0.4.6 / 60% remains earned
- v0.4.7 / 70% is not yet earned
- gap to v0.4.7: 4.0939 percentage points

If canonicalisation were the only remaining workstream contributing to the next gate, 70% would require at least 5.0 canonicalisation points in total, equivalent to one third of the 15-point canonicalisation component. On the current 2,152-object denominator that corresponds to at least 718 physical document objects explicitly screened/reconciled under the same conservative object-coverage rule.

Privacy/public-status classification and validation remain scored at zero until they receive independent denominators; progress in those components can also contribute to the 70% gate.

## Screening classes for corpus-wide normalisation

Every physical document object should ultimately receive one of these screening outcomes:

- UNIQUE_CANDIDATE: no matching canonicalisation candidate found under current metadata-normalisation rules
- DUPLICATE_COPY: likely duplicate physical copy; hash required for byte identity
- SAME_DRIVE_OBJECT_MULTICOLLECTION: one Drive object associated with more than one collection path; do not create duplicate manifestation nodes
- DUPLICATE_WORK: same work under separate physical objects; edition identity unresolved
- EDITION_VARIANT: same canonical work, distinct edition or packaging
- TRANSLATION_VARIANT: same canonical work, distinct translation
- MULTI_VOLUME_MEMBER: one logical volume in a multi-volume canonical work/series
- AGGREGATE_COLLECTION: one file bundles several logical works or volumes
- TECHNICAL_EXCLUSION: zero-byte, incomplete download, system artefact, or other non-usable object
- REVIEW_REQUIRED: metadata is insufficient or ambiguous

These classes are screening states, not evidence-quality states.

## Canonicalisation hierarchy

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

The canonicalisation layer must preserve provenance and must never infer that a folder placement makes a claim true, scientific, religiously authoritative, or empirically supported.
