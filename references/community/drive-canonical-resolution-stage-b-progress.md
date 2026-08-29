# AKASHICNET-005 — Canonical Knowledge Resolution

Date: 2026-08-29

Status: Stage B active after completion of the 195 / 195 Drive validation census.

## Objective

Resolve screened Drive document objects into defensible work-level structures while preserving every physical Drive object as provenance.

Canonical hierarchy:

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Stage B is deliberately stricter than Stage A. Title similarity and equal collection counts may establish a work-family relationship, but they do not establish byte identity. Hash evidence would be required for a byte-identical duplicate claim.

## Batch 0001

### Abramelin
Three independently catalogued three-document collections resolve to **SAME_LOGICAL_WORK_FAMILY**. Nine Drive objects remain distinct manifestations.

### Forbidden History of Europe
Two twelve-volume collections resolve to **EDITION_OR_COPY_VARIANT_SET** because corresponding volumes are not uniformly identical in size.

## Batch 0002

### Mushrooms Russia and History
Four physical objects across two collections map provisionally to two logical volumes: **SAME_LOGICAL_WORK_FAMILY**.

### Techniques of Modern Shamanism
Six physical objects across two collections map provisionally to three logical volumes: **SAME_LOGICAL_WORK_FAMILY**.

### Necronomicon and complete works H. P. Lovecraft
Ten physical objects map provisionally to five distinct logical title units: **PARALLEL_COLLECTION_MANIFESTATION_SET**. The five distinct titles are not collapsed into one work.

### Agrippa Occult Philosophy
Numbered books 1–4 form a strong cross-collection relationship while the 1651 three-books compilation remains aggregate: **OVERLAPPING_WORK_FAMILY**.

## Batch 0003

This batch used folder-scoped parent IDs from the frozen descendant census, avoiding noisy global Drive title searches.

### Echoes From the Gnosis
Ancient Religions/Echoes From the Gnosis and Ancient Religions/Gnosis independently expose the same six G.R.S. Mead volume/title identities: Vol I *The Gnosis of the Mind*, Vol II *The Hymns of Hermes*, Vol IV *The Hymn of Jesus*, Vol VI *A Mithriac Ritual*, Vol VII *The Gnostic Crucifixion*, and Vol X *The Hymn of the Robe of Glory*.

Stage-B determination: **PARALLEL_COLLECTION_MANIFESTATION_SET**, high confidence. Twelve Drive objects map provisionally to six logical title/volume units. Punctuation differences do not justify separate works, but byte identity is not claimed without hashes.

### Alice A. Bailey — Discipleship in the New Age
Within PDF/Alice A. Bailey, two Vol-1 objects normalize to the same title and both report 6,321,419 bytes; two Vol-2 objects normalize to the same title and both report 5,905,957 bytes.

Stage-B determination: **INTRA_COLLECTION_DUPLICATE_COPY_CANDIDATES**, high confidence. Four physical objects map provisionally to two logical volumes. Equal normalized titles and equal sizes are strong duplicate-copy evidence but are not hash proof.

### Franz Bardon — Initiation Into Hermetics
Three manifestations explicitly identify the same work: 2001, 1987, and 1987 (170 pages), with different file sizes.

Stage-B determination: **EDITION_OR_COPY_VARIANT_SET**, high confidence. Three physical objects map to one canonical-work candidate with separate manifestations.

### Franz Bardon — Golden Book of Wisdom
Two differently named objects normalize to *Golden Book of Wisdom* and both report exactly 45,965 bytes.

Stage-B determination: **INTRA_COLLECTION_DUPLICATE_COPY_CANDIDATE**, high confidence. Two physical objects map provisionally to one work; byte identity remains unverified without hashes.

### Franz Bardon — Practice of Magical Evocation
Two normalized title matches report different sizes, 5,058,666 and 4,999,370 bytes.

Stage-B determination: **EDITION_OR_COPY_VARIANT_SET**, high confidence.

### Franz Bardon — Key to the True Qabbalah
Two normalized title matches, including a Quabbalah/Qabbalah spelling variation, report different sizes, 657,049 and 692,462 bytes.

Stage-B determination: **EDITION_OR_COPY_VARIANT_SET**, high confidence.

## Stage-B progress

Batches completed: **3**.

Families advanced in Stage B: **12**.

The existing global verified milestone remains **90.000000%**. Stage B is intentionally not converted into extra global points yet; it refines the canonical knowledge model rather than inflating Stage-A screening completion.

## Privacy and epistemic boundary

All Stage-B work remains metadata-only. No document bodies were fetched, no embeddings were generated, and no accessibility state was promoted to `PUBLIC_VERIFIED`. Catalogue membership is provenance, not endorsement or truth validation. Equal titles and sizes are strong duplicate-copy evidence but are not proof of byte identity without hashes.

## Next candidate families

Continue folder-scoped resolution of flagged Stage-A families, especially remaining intra-folder duplicate/edition candidates and defensible cross-collection relationships. Preserve ambiguous candidates as `REVIEW_REQUIRED` rather than forcing canonical collapse.
