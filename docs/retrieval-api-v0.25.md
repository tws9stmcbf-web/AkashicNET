# AkashicNET Retrieval API — consumer contract v0.25

Status: PRE-ALPHA consumer interface documented in v0.26.

## Purpose

`query_api_v025.py` is the stable machine-readable boundary for retrieval consumers. Clients should depend on its documented JSON fields and schema identifier, not on internal knowledge-graph files or intermediate build scripts.

Schema ID: `akashicnet://schemas/retrieval/v0.25`

API name: `AKASHICNET_RETRIEVAL_API`

API version: `0.25`

## Invocation

```bash
python scripts/query_api_v025.py "Psychedelics"
python scripts/query_api_v025.py "Psychedelics" --domain reddit --state accepted
python scripts/query_api_v025.py "Consciousness" --state hold --limit 20
python scripts/query_api_v025.py "Golden Book of Wisdom" --state accepted
```

Arguments:

- `query`: required free-text query.
- `--domain`: `all`, `reddit`, or `library`.
- `--state`: `all`, `accepted`, or `hold`.
- `--limit`: positive integer; default 100.

## Stable top-level response fields

Consumers may rely on:

- `api`
- `api_version`
- `schema_id`
- `request`
- `policy`
- `summary`
- `results`
- `compatibility`

The authoritative machine-readable schema is `references/community/unified-retrieval-schema-v0.25.json`.

## Semantic decisions

Results can expose decisions inherited from the reviewed retrieval layer, including:

- `ACCEPT`
- `HOLD`
- `REJECT`
- `DIRECT_METADATA_LOOKUP`
- `UNSPECIFIED`

`DIRECT_METADATA_LOOKUP` is not semantic acceptance. A title/family match can therefore be directly retrievable without creating an `ABOUT` relationship.

## Provenance tiers

Retrieval ordering may use provenance support tiers:

- `P3_SHA256_IDENTITY_PROVENANCE`
- `P2_MANIFESTATION_PROVENANCE`
- `P1_REVIEWED_TOPICAL`
- `P0_TOPICAL_CANDIDATE`

These tiers rank provenance/retrieval support only. They are not truth, scientific-evidence, rights, efficacy, or safety scores.

## Epistemic and rights boundaries

The response policy must continue to state:

- archive mode is metadata and links only;
- truth inference is disabled;
- rights promotion is disabled;
- scientific-evidence promotion is disabled;
- ranking cannot change a semantic decision;
- direct metadata lookup is not semantic acceptance;
- HOLD results are explicitly addressable.

Public accessibility, catalogue membership, topical relation, SHA-256 identity, and rights clearance are separate questions.

## Compatibility

Consumer code should ignore unknown additional fields. Existing required fields will not be silently removed or repurposed within the same API version. Breaking changes require a new API/schema version under the v0.26 compatibility policy.

## Reproducible fixtures

`references/community/retrieval-fixtures-v0.25.json` defines stable behavioural fixtures checked in CI. They validate important semantics without requiring consumers to understand internal graph construction.
