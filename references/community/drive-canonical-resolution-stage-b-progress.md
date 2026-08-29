# AKASHICNET-005 — Canonical Knowledge Resolution

Date: 2026-08-29

Status: Stage B active after completion of the 195 / 195 Drive validation census.

## Objective
Resolve screened Drive document objects into defensible work-level structures while preserving every physical Drive object as provenance.

Canonical hierarchy:
`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Stage B is deliberately stricter than Stage A. Title similarity and equal collection counts may establish a work-family relationship, but they do not establish byte identity. Hash evidence would be required for a byte-identical duplicate claim.

## Batch 0001
- Abramelin — **SAME_LOGICAL_WORK_FAMILY**.
- Forbidden History of Europe — **EDITION_OR_COPY_VARIANT_SET**.

## Batch 0002
- Mushrooms Russia and History — **SAME_LOGICAL_WORK_FAMILY**.
- Techniques of Modern Shamanism — **SAME_LOGICAL_WORK_FAMILY**.
- Necronomicon / H. P. Lovecraft parallel collections — **PARALLEL_COLLECTION_MANIFESTATION_SET**.
- Agrippa Occult Philosophy — **OVERLAPPING_WORK_FAMILY**.

## Batch 0003
- Echoes From the Gnosis — **PARALLEL_COLLECTION_MANIFESTATION_SET**.
- Alice A. Bailey / Discipleship in the New Age — **INTRA_COLLECTION_DUPLICATE_COPY_CANDIDATES**.
- Franz Bardon / Initiation Into Hermetics — **EDITION_OR_COPY_VARIANT_SET**.
- Franz Bardon / Golden Book of Wisdom — **INTRA_COLLECTION_DUPLICATE_COPY_CANDIDATE**.
- Franz Bardon / Practice of Magical Evocation — **EDITION_OR_COPY_VARIANT_SET**.
- Franz Bardon / Key to the True Qabbalah — **EDITION_OR_COPY_VARIANT_SET**.

## Batch 0004

### Ramayana
Buddhism/Ramayana is independently confirmed as a coherent four-volume sequence: Vol 1 *Bala-Ayodhya Kanda*, Vol 2 *Aranya-Kishkindha-Sundara Kanda*, Vol 3 *Yuddha Kanda*, and Vol 4 *Uttara Kanda*.

The frozen census explicitly flags this as a cross-collection candidate with Hinduism. However, the current known descendant ledger contains no second Hinduism/Ramayana parent-folder identity, and a global metadata-only title search did not recover the expected counterpart.

Stage-B determination: **CROSS_COLLECTION_RELATION_UNRESOLVED**, medium confidence. The four Buddhism objects are retained as four logical volumes. The proposed Hinduism relationship remains provenance debt and is not credited as a resolved cross-collection family.

### Swami Vivekananda
Hinduism/Complete works of Swami Vivekananda contains nine numbered Complete Works volumes. Yoga/Swami Vivekananda contains four standalone works: *Raja Yoga*, *Bhakti Yoga*, *Karma Yoga*, and *Jnana Yoga*.

Stage-B determination: **RELATED_AUTHOR_COLLECTIONS_NOT_DUPLICATES**, high confidence. Thirteen physical objects remain thirteen immediate logical units. Author overlap does not justify duplicate collapse. The four standalone Yoga works may later be related to content contained within the Complete Works aggregate, but establishing that requires evidence beyond metadata-only filenames.

## Stage-B progress

Batches completed: **4**.

Resolved/advanced canonical families: **13**.

Explicit unresolved candidate families retained: **1** (Ramayana cross-collection relation).

The Vivekananda relationship is counted as an advanced Stage-B classification because the metadata is sufficient to reject a false duplicate collapse and establish the correct relationship class.

The existing global verified milestone remains **90.000000%**. Stage B is intentionally not converted into extra global points yet; it refines the canonical knowledge model rather than inflating Stage-A screening completion.

## Privacy and epistemic boundary
All Stage-B work remains metadata-only. No document bodies were fetched, no embeddings were generated, and no accessibility state was promoted to `PUBLIC_VERIFIED`. Catalogue membership is provenance, not endorsement or truth validation. Equal titles and sizes are strong duplicate-copy evidence but are not proof of byte identity without hashes.

## Next candidate families
Continue folder-scoped resolution of remaining Stage-A aggregate, duplicate, edition, translation and provenance-anomaly candidates. Preserve ambiguous relationships as `REVIEW_REQUIRED` or explicit unresolved provenance debt rather than forcing canonical collapse.
