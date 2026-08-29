# AKASHICNET-005 — Canonical Knowledge Resolution

Date: 2026-08-29

Status: Stage B started after completion of the 195 / 195 Drive validation census.

## Objective

Resolve screened Drive document objects into defensible work-level structures while preserving every physical Drive object as provenance.

Canonical hierarchy:

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Stage B is deliberately stricter than Stage A. Title similarity and equal collection counts may establish a work-family relationship, but they do not establish byte identity. Hash evidence would be required for a byte-identical duplicate claim.

## Batch 0001

Two high-value cross-collection families were advanced.

### Abramelin

Three independently catalogued three-document collections were re-queried metadata-only:

- Grimoire/Abramelin: three PDFs numbered 1–3.
- Alchemy/The Sacred Magic of Abramelin the Mage: three Book 1–3 PDFs.
- Magick/Ceremonial Beginners/The Sacred Magi of Abramelin the Mage: three 01–03 PDFs.

Stage-B determination: **SAME_LOGICAL_WORK_FAMILY** with high confidence at the work-family level. The nine Drive objects remain distinct manifestations. Copy/edition identity is not collapsed without hashes or stronger manifestation evidence.

### Forbidden History of Europe

World History and Secret Societies each contain twelve correspondingly titled volumes. Fresh metadata re-query confirms the work-level relationship, but same-number volumes are not uniformly identical in file size. Some pairs match while others differ substantially.

Stage-B determination: **EDITION_OR_COPY_VARIANT_SET**. The two collections are represented as one logical twelve-volume work family with alternate physical manifestations. No blanket `DUPLICATE_COPY` disposition is assigned.

## Privacy and epistemic boundary

All Stage-B work in this checkpoint is metadata-only. No document bodies were fetched, no embeddings were generated, and no accessibility state was promoted to `PUBLIC_VERIFIED`. Catalogue membership is provenance, not endorsement or truth validation.

## Next candidate families

Next metadata-resolution targets are the already-screened cross-collection families for Mushrooms Russia and History, Techniques of Modern Shamanism, Lovecraft/Necronomicon, Agrippa, and other flagged duplicate/edition families.
