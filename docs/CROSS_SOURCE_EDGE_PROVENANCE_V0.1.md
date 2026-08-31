# Cross-Source Edge Provenance v0.1

Status: review candidate for Issue #176

## Purpose

This contract makes every cross-source relationship traceable without exposing private Drive-derived object metadata. It separates direct metadata, inferred candidates and human adjudication, and prevents graph-derived relationships from recursively increasing their own confidence.

## Relationship classes

- `ASSERTED` — an explicitly asserted relationship with a traceable public-safe source record.
- `DIRECT_METADATA` — a relationship copied from an explicit curated metadata field.
- `INFERRED_CANDIDATE` — a machine-generated review candidate; never an accepted edge by default.
- `HUMAN_ADJUDICATED` — a reviewed candidate with an explicit adjudication record.
- `REJECTED_HOLD` — a rejected or unresolved candidate retained for auditability.

## Provenance envelope

Every edge records exact source and target record references, immutable artifact version and digest metadata, observation time, assertion class, review state, lineage parents and epistemic non-promotion flags. Inferred candidates also record generator name, version and a digest of their parameters. Promoted edges require an explicit adjudication reference.

## Anti-amplification rules

Confidence must not be increased by the same edge, its reverse, any descendant derived from it, duplicate manifestations of one underlying source, or representation count alone. Independence must be established from provenance lineage rather than assumed from record count.

Missing, ambiguous or cyclic lineage fails closed. Candidate generation does not infer truth, establish scientific evidence, clear rights, or change safety or efficacy claims.

## Privacy boundary

Only public-safe artifact identifiers and aggregate digests belong in this layer. Private Drive IDs, filenames, paths, timestamps and object-linked hashes must not enter public fixtures or generated review artifacts.

## Review state

The synthetic v0.1 fixture intentionally promotes zero edges. It exists to validate the contract and negative cases before any integration with private-derived graph artifacts.
