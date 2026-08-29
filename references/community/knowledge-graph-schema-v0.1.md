# AkashicNET Knowledge Graph Schema v0.1

Date: 2026-08-29
Status: PRE-ALPHA DESIGN

## Purpose

Define the provenance-first graph layer built on the reconciled Drive library. The graph must preserve physical source objects while allowing defensible canonical relationships.

## Core nodes

- `source` — originating system or publication source.
- `collection` — Drive/library collection or imported corpus grouping.
- `drive_object` — immutable physical object identity and provenance anchor.
- `manifestation` — a specific file/scan/edition/translation instance.
- `edition` — edition-level bibliographic identity where known.
- `work` — logical intellectual work.
- `volume` — logical volume or part within a work.
- `author` — creator/attributor where established.
- `concept` — topic/entity/concept node added by later semantic processing.
- `evidence` — evidence record supporting a claim or relationship.
- `rights_record` — rights/publication-status evidence.

## Core edges

`source CONTAINS collection`

`collection CONTAINS drive_object`

`drive_object REALIZES manifestation`

`manifestation INSTANCE_OF edition`

`edition MANIFESTS work`

`volume PART_OF work`

`manifestation REPRESENTS volume`

`author CREATED work`

`work RELATED_TO work`

`work ABOUT concept`

`evidence SUPPORTS relationship`

`rights_record QUALIFIES manifestation`

## Relationship confidence

Every inferred relationship should carry:

- `confidence`: high / medium / low
- `basis`: exact_metadata / title_normalisation / collection_alignment / bibliographic_source / content_evidence / hash / explicit_rights
- `observed_at`
- `review_state`: accepted / provisional / unresolved / rejected

## Identity rules

1. Never delete a `drive_object` because another object appears equivalent.
2. Never equate equal filenames or sizes with byte identity.
3. A work may have many editions and manifestations.
4. An aggregate work may contain logical works without becoming identical to them.
5. Translation identity is separate from underlying-work identity.
6. Ambiguous relationships remain explicit `unresolved` edges.
7. Rights state is independent of canonical identity and scientific evidence status.

## Public retrieval gate

A retrieval layer may return provenance metadata for private/internal records only where authorised. Public redistributable content requires the manifestation to pass the rights gate and have `public_status=PUBLIC_VERIFIED`.

## Initial graph seed

The graph seed is the Stage-B canonical family ledger. Current known resolved/advanced families: 13. Current explicit unresolved cross-collection candidate: Ramayana/Hinduism counterpart. The 195/195 structural census remains the authoritative imported-object boundary for this milestone.

## Future semantic layer

Concept and evidence edges should not be generated merely from filenames. They require content-level processing, source citations, or explicit human-reviewed assertions. This prevents the knowledge graph from converting association into fact.
