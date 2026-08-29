# AkashicNET canonical work and evidence layer v0.1

Status: PRE-ALPHA design contract
Date: 2026-08-29

## Purpose

This layer sits between the physical Drive corpus and higher-level semantic/retrieval systems. It prevents file similarity, folder placement, semantic proximity or community discussion from being promoted automatically into factual equivalence or scientific support.

## Canonicalisation pipeline

`Drive object -> usable document -> copy / edition / translation -> logical volume -> canonical work -> appears_in collection`

### Non-negotiable rules

- A Drive object is a physical/provenance object, not automatically a canonical work.
- Same title and file size are candidate signals only; they are not byte identity.
- `SAME_WORK_AS` requires explicit adjudication or stronger evidence than generic lexical similarity.
- Editions and translations remain distinct manifestations unless explicitly resolved.
- Multi-volume works remain distinct volume members beneath a work/aggregate structure.
- Folder placement is provenance, not semantic truth.
- Technical artefacts remain auditable but are excluded from usable-document promotion.

Allowed dispositions are defined by `data/canonical_resolution_v01.schema.json`.

## Evidence model

Evidence is represented separately from provenance and semantic relationships.

Evidence tiers:

1. `EMPIRICAL_REFERENCE`
2. `HISTORICAL`
3. `CONTEMPLATIVE_PHILOSOPHICAL`
4. `EXPERIENTIAL_ESOTERIC`

A source can be valuable at any tier. The tier describes the kind of support it can provide; it is not a ranking of human worth or cultural importance.

### Core maxim

**Archive inclusion is not endorsement. Semantic connection is not scientific evidence. Historical provenance is not Indigenous authorship. Provenance is not evidence.**

## Claim handling

Claims are atomic statements with explicit status and provenance. Evidence links may support, contradict, contextualise, report experience, or provide historical attestation.

No claim becomes `SUPPORTED` merely because:

- many documents mention it,
- a Reddit discussion repeats it,
- two texts are semantically similar,
- a source is ancient or culturally important,
- an AI system assigns a high similarity score.

The evidence contract is defined by `data/evidence_claim_v01.schema.json`.

## Reddit integration boundary

Drive and Reddit remain separate provenance graphs.

Reddit discussions can:

- discuss a work or claim,
- surface lived experience,
- generate candidate questions/relationships,
- contextualise how ideas are understood in a community.

Reddit discussion must not automatically:

- promote a claim to empirical support,
- collapse a Drive manifestation into a canonical work,
- create authorship or cultural provenance claims,
- override privacy/public-status controls.

## V1 acceptance path

`Drive crawl -> corpus manifest -> canonical resolution -> semantic graph -> evidence graph -> Reddit bridge -> validation -> retrieval`

The completed Drive census/Stage-A gate supplies the physical corpus boundary. This v0.1 contract defines how the next layer may safely promote structure without turning association into truth.
