# AkashicNET Retrieval API Compatibility Policy v0.26

## Scope

This policy governs consumer-facing compatibility for `AKASHICNET_RETRIEVAL_API` beginning with API/schema version 0.25.

It does not freeze internal graph structure, builders, intermediate JSON files, candidate-generation algorithms, or review workflows.

## Compatibility promise

Within one API version, AkashicNET may:

- add optional response fields;
- add new results that are supported by reviewed evidence;
- improve deterministic ordering within the documented provenance semantics;
- add internal graph representations or provenance records;
- correct historical metadata while retaining provenance of the correction.

Within one API version, AkashicNET must not silently:

- remove a required top-level field;
- change the meaning of an existing required field;
- reinterpret `DIRECT_METADATA_LOOKUP` as semantic `ACCEPT`;
- make provenance ranking alter semantic decisions;
- turn HOLD into ACCEPT without an explicit reviewed/adjudicated change;
- treat provenance tier as truth, scientific evidence, rights, safety, or efficacy;
- promote inaccessible/unverified Drive material into a public redistribution manifest;
- collapse physical manifestations without verified byte identity where byte identity is the stated collapse basis.

## Breaking changes

A breaking change requires:

1. a new API version;
2. a new schema identifier;
3. migration notes describing changed fields or semantics;
4. updated reproducible fixtures;
5. CI demonstrating the old contract remains reproducible where intentionally supported, or explicitly documenting its retirement.

## Consumer behaviour

Consumers should:

- validate `api`, `api_version`, and `schema_id`;
- depend on documented stable fields rather than internal graph files;
- ignore unknown optional fields;
- interpret `semantic_decision` separately from provenance ranking;
- preserve explicit HOLD and unresolved states;
- avoid inferring truth, scientific validity, safety, efficacy, endorsement, or rights from catalogue/retrieval presence.

## Version 0.25 baseline

Stable identifiers:

- API: `AKASHICNET_RETRIEVAL_API`
- API version: `0.25`
- schema: `akashicnet://schemas/retrieval/v0.25`

Baseline reproducible fixtures are maintained in `references/community/retrieval-fixtures-v0.25.json`.

## Epistemic invariants

These remain independent of API compatibility:

- truth inference: OFF;
- rights promotion: OFF unless independently established by the rights ladder;
- scientific-evidence promotion: OFF unless separately reviewed under an evidence framework;
- catalogue membership is not endorsement;
- topical relation is not work identity;
- SHA-256 equality proves byte identity only;
- rights status is not changed by hashing;
- public accessibility is not scientific validation.
