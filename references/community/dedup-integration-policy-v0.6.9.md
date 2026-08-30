# AkashicNET v0.6.9 — Canonical dedup integration

Milestone: **verified byte identity becomes retrieval capacity, not semantic identity**.

This checkpoint integrates the cumulative P1 SHA-256 evidence from v0.6.8 into the retrieval architecture without exposing private object rows or inventing object-level mappings.

## Current verified capacity

- 25 duplicate families are `BYTE_IDENTICAL_VERIFIED`.
- Those families cover 50 compared physical objects.
- If the private family→object mapping is supplied to a dedup builder, those 50 physical copies can occupy 25 logical retrieval slots.
- Therefore the verified potential reduction is 25 redundant physical copies.

## What v0.6.9 does

- preserves the v0.17 rule that only verified SHA-256 identity may collapse physical manifestations;
- records aggregate dedup capacity in a machine-readable checkpoint;
- keeps the public graph unchanged because public aggregate summaries do not expose the object membership required for a safe collapse;
- requires a private mapping before any object-level retrieval mutation;
- performs no Drive access and computes no new hashes.

## What v0.6.9 does not do

Byte identity does **not** establish:

- canonical work identity;
- edition or translation identity;
- semantic equivalence;
- scientific validity;
- truth;
- redistribution/publication rights.

The retrieval, semantic, evidence, provenance, and rights dimensions remain independently governed.

## Next safe transition

A future private-to-public build step may consume the private family membership table, create opaque logical retrieval-unit identifiers, and publish only non-sensitive aggregate retrieval units. That transition must preserve every physical manifestation as provenance while suppressing duplicate retrieval presentation.
