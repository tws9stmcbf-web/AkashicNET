# AkashicNET Corpus Graph v0.1

Status: architecture implementation

## Purpose

Define the machine-readable knowledge graph that connects the Drive corpus with Reddit records while preserving provenance and epistemic status.

## Core entities

- `source` — external or internal origin
- `folder` — original Drive location
- `file` — physical Drive object
- `work` — canonical intellectual work
- `edition` — edition, translation, revision, or scan lineage
- `author` — creator or attributed creator
- `tradition` — religious, philosophical, cultural, scientific, artistic, or other tradition
- `domain` — broad corpus classification
- `concept` — topic or semantic concept
- `claim` — proposition extracted from a source
- `evidence` — supporting, contradicting, contextual, or otherwise relevant material
- `discussion` — Reddit/community discussion
- `application` — downstream use such as semantic search, ADAPT, learning, or synthesis

## Required relationships

- `folder CONTAINS file`
- `file REPRESENTS work`
- `file HAS_EDITION edition`
- `work CREATED_BY author`
- `author ASSOCIATED_WITH tradition`
- `work CLASSIFIED_AS domain`
- `work MENTIONS concept`
- `claim EXTRACTED_FROM work`
- `claim SUPPORTED_BY evidence`
- `claim CONTRADICTED_BY evidence`
- `discussion DISCUSSES work|concept|claim`
- `application DERIVED_FROM concept|claim|evidence`

## Provenance rule

Original Drive path and object identity are immutable provenance fields. Canonicalisation must never erase the physical location, filename, Drive ID, timestamp, or source lineage.

## Epistemic rule

Archive inclusion is not endorsement. A claim must remain distinct from evidence for that claim. Fiction, testimony, religious/esoteric teaching, historical documentation, scientific research, commentary, and speculation must have distinct source/evidence classes.

## Duplicate rule

Exact content duplicates should be grouped by content hash when available. Same-work/different-edition objects must remain separate physical records while sharing a canonical `work` node.

## V0.1 acceptance target

The graph is ready for implementation when it can preserve: provenance, canonical identity, edition lineage, cross-folder relationships, concepts, claims, evidence class, confidence, and Reddit discussion links without collapsing distinct epistemic categories.
