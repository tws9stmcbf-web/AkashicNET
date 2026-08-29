# AkashicNET Drive technical and duplicate integrity audit — v0.4.9

Date: 2026-08-29
Scope: nominated Akashic Library Google Drive tree only
Validation gate: `TECHNICAL_AND_DUPLICATE_INTEGRITY`

## Denominator and evidence

This audit uses the complete Stage-A screened corpus denominator of 2,144 physical document objects together with the persisted canonicalisation family ledger in `drive-canonicalisation-candidates.csv` and the technical-exclusion inventory recorded in `drive-canonicalisation-checkpoint-v0.4.6.md`.

Known document-level technical exclusions are explicitly retained in the physical-object audit denominator rather than silently dropped:

- one zero-byte Magick PDF
- one zero-byte Buddhism PDF
- five zero-byte `PDF/Bookz` objects
- one `.crdownload` artefact in Black's Law Dictionary

Three `.DS_Store` artefacts in Theosophy remain tracked outside the document-only denominator.

## Duplicate / edition integrity procedure

The 29 persisted canonicalisation families are reviewed by relation class rather than flattened into a generic duplicate label.

Required invariants:

1. `DUPLICATE_COPY` remains a strong duplicate-copy candidate unless byte/hash identity has actually been established.
2. `DUPLICATE_WORK`, `DUPLICATE_SERIES` and `WORK_FAMILY` may share a canonical work/volume relationship while retaining separate physical Drive manifestations.
3. `TRANSLATION_EDITION_FAMILY`, `EDITION_OR_COLLECTION_FAMILY`, `EDITION_OR_COPY_FAMILY` and `ALTERNATE_COPY_SERIES` must not be collapsed as byte-identical copies.
4. Multi-volume structures remain volume-aware.
5. Every manifestation preserves collection/Drive provenance.
6. Technical exclusions remain auditable and are not promoted to usable canonical content.

## Result

The persisted candidate ledger conforms to those invariants:

- 29 candidate families recorded
- 27 `REVIEWED`
- 2 `CANDIDATE`
- strong same-title/same-size duplicate-copy cases are explicitly described as pending hash verification rather than asserted byte-identical
- edition, translation, collection and volume families are explicitly preserved as distinct manifestation structures
- no reviewed family is represented as proof of byte identity merely from filename/title equivalence
- technical exclusions remain represented in the audit denominator and separately identified

Hash verification is still required before replacing strong duplicate-copy candidates with byte-identity assertions. That is a deeper canonical-resolution task, not a prerequisite for this integrity gate, whose purpose is to verify safe handling and prevent destructive over-deduplication.

**Gate result: PASS — 2.000000 / 2 points.**
