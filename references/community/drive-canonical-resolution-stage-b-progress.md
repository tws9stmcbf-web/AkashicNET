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

Three independently catalogued three-document collections were re-queried metadata-only: Grimoire/Abramelin, Alchemy/The Sacred Magic of Abramelin the Mage, and Magick/Ceremonial Beginners/The Sacred Magi of Abramelin the Mage.

Stage-B determination: **SAME_LOGICAL_WORK_FAMILY** with high confidence at the work-family level. The nine Drive objects remain distinct manifestations. Copy/edition identity is not collapsed without hashes or stronger manifestation evidence.

### Forbidden History of Europe

World History and Secret Societies each contain twelve correspondingly titled volumes. Fresh metadata re-query confirms the work-level relationship, but same-number volumes are not uniformly identical in file size.

Stage-B determination: **EDITION_OR_COPY_VARIANT_SET**. The two collections are represented as one logical twelve-volume work family with alternate physical manifestations. No blanket `DUPLICATE_COPY` disposition is assigned.

## Batch 0002

Four additional cross-collection families were advanced by fresh metadata-only queries.

### Mushrooms Russia and History

Ancient Religions and Bizzare each expose a two-volume collection with the same normalized Volume 1 and Volume 2 titles.

Stage-B determination: **SAME_LOGICAL_WORK_FAMILY** with high confidence. Four physical Drive objects map provisionally to two logical volume units. Object identity remains distinct pending hashes.

### Techniques of Modern Shamanism

Ancient Religions and Shamanism each expose the same three normalized volume titles, volumes 1–3 of *Walking Between The Worlds*.

Stage-B determination: **SAME_LOGICAL_WORK_FAMILY** with high confidence. Six physical Drive objects map provisionally to three logical volume units; no byte-identical duplicate claim is made.

### Necronomicon and complete works H. P. Lovecraft

The Bizzare and Literature collections each expose five documents with the same normalized title set: Complete Works of H.P. Lovecraft, John Dee Necronomicon, Simon Necronomicon, Necronomicon Spellbook, and Al-Azif Necronomicon.

Stage-B determination: **PARALLEL_COLLECTION_MANIFESTATION_SET** with high confidence at the title-family level. Ten physical objects map provisionally to five logical title units, with two manifestations per title pending stronger copy/edition evidence. Importantly, the five distinct titles are not collapsed into a single canonical work merely because they share a folder.

### Agrippa Occult Philosophy

Philosophy/Agrippa - Occult Philosophy exposes numbered Occult Philosophy 1–4 plus a *3 Books of Agrippa from 1651* compilation. Magick/Agrippa exposes Agrippa1–3 plus a fourth-book document.

Stage-B determination: **OVERLAPPING_WORK_FAMILY** with high confidence. The numbered books/volumes 1–4 form a strong cross-collection relationship, while the 1651 three-books compilation is retained as an aggregate manifestation rather than forced into a duplicate relationship.

## Stage-B progress

Batches completed: 2.

Families advanced in Stage B: 6.

- Abramelin
- Forbidden History of Europe
- Mushrooms Russia and History
- Techniques of Modern Shamanism
- Necronomicon / Lovecraft parallel collections
- Agrippa Occult Philosophy

Stage-B progress is not currently converted into additional global completion points. The existing 90% verified milestone remains intact; Stage B refines the canonical knowledge model rather than inflating the already-completed Stage-A screening score.

## Privacy and epistemic boundary

All Stage-B work remains metadata-only. No document bodies were fetched, no embeddings were generated, and no accessibility state was promoted to `PUBLIC_VERIFIED`. Catalogue membership is provenance, not endorsement or truth validation. Equal titles and sizes are not treated as proof of byte identity without hashes.

## Next candidate families

Continue through other flagged duplicate, edition, translation and aggregate families from the Stage-A screening ledger, prioritising high-confidence cross-collection relationships before ambiguous title-only candidates.
