# AkashicNET Knowledge Graph Seed v0.1

Date: 2026-08-29
Status: PRE-ALPHA — Stage B seed

## Purpose

Provide the first executable, provenance-preserving seed manifest for the AkashicNET knowledge graph. This seed is derived from the completed 195/195 Drive validation census and Stage-B canonical resolution work.

## Graph boundary

The seed begins with the Stage-B canonical family ledger. Every physical Drive object remains provenance-bearing; canonicalisation occurs only at the defensible work/family level.

## Seeded work families

| family_id | canonical work | disposition | confidence |
|---|---|---|---|
| ABRAMELIN-001 | The Sacred Magic of Abramelin the Mage | SAME_LOGICAL_WORK_FAMILY | HIGH |
| FORBIDDEN-HISTORY-001 | Forbidden History of Europe | EDITION_OR_COPY_VARIANT_SET | HIGH |
| MUSHROOMS-RUSSIA-001 | Mushrooms Russia and History | SAME_LOGICAL_WORK_FAMILY | HIGH |
| MODERN-SHAMANISM-001 | Techniques of Modern Shamanism | SAME_LOGICAL_WORK_FAMILY | HIGH |
| NECROMONICON-LG-001 | Necronomicon / H. P. Lovecraft parallel collection | PARALLEL_COLLECTION_MANIFESTATION_SET | HIGH |
| AGRIPPA-OCCULT-001 | Agrippa Occult Philosophy | OVERLAPPING_WORK_FAMILY | HIGH |
| GNOSIS-ECHOES-001 | Echoes From the Gnosis | PARALLEL_COLLECTION_MANIFESTATION_SET | HIGH |
| BAILEY-DISCIPLESHIP-001 | Discipleship in the New Age | INTRA_COLLECTION_DUPLICATE_COPY_CANDIDATES | HIGH |
| BARDON-INITIATION-001 | Initiation Into Hermetics | EDITION_OR_COPY_VARIANT_SET | HIGH |
| BARDON-GOLDEN-001 | Golden Book of Wisdom | INTRA_COLLECTION_DUPLICATE_COPY_CANDIDATE | HIGH |
| BARDON-EVOCATION-001 | Practice of Magical Evocation | EDITION_OR_COPY_VARIANT_SET | HIGH |
| BARDON-QABBALAH-001 | Key to the True Qabbalah | EDITION_OR_COPY_VARIANT_SET | HIGH |
| VIVEKANANDA-001 | Swami Vivekananda works | RELATED_AUTHOR_COLLECTIONS_NOT_DUPLICATES | HIGH |

## Explicit unresolved relationship

`Ramayana` remains a four-volume logical work sequence in Buddhism, with a candidate relationship to an expected Hinduism manifestation that has not yet been located. This is retained as an unresolved provenance edge and is not canonically collapsed.

## Required relationship attributes

Every inferred graph relationship must retain:

- confidence: high / medium / low
- basis: exact_metadata / title_normalisation / collection_alignment / bibliographic_source / content_evidence / hash / explicit_rights
- observed_at
- review_state: accepted / provisional / unresolved / rejected

## Retrieval and rights boundary

This seed is catalogue/provenance data, not an endorsement of the works or their claims. Content-level semantic edges must not be inferred from filenames alone. Public retrieval requires the relevant manifestation to pass the rights gate with `public_status=PUBLIC_VERIFIED`.

## Next stage

Build machine-readable node and edge records from the Stage-B ledger, then add content-derived concept/evidence relationships only after authorised document-body access and provenance/rights checks.
