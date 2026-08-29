# AkashicNET rights downgrade and revocation policy v0.32

## Purpose

Rights status is a current evidence state, not a permanent promotion. A manifestation that once satisfied R4 must lose `PUBLIC_VERIFIED` immediately when any required R4 condition becomes invalid, withdrawn, contradicted, expired, or revoked.

## Downgrade rules

- authoritative rights evidence withdrawn or contradicted -> no higher than R2;
- independent corroboration withdrawn or invalid -> no higher than R3;
- jurisdiction/licence scope expired or incompatible -> no higher than R2;
- reviewer approval revoked or re-review required -> no higher than R3;
- any state below R4 -> `UNKNOWN_UNVERIFIED` for public retrieval;
- `UNKNOWN_UNVERIFIED` -> excluded from production public manifest.

## Independence guarantees

A rights downgrade must not rewrite unrelated metadata. Semantic decisions, topical relationships, provenance tiers, SHA-256 identity evidence, and canonicalisation status remain independently recorded. None of those can preserve public visibility after R4 fails.

## v0.32 scope

All regression scenarios are synthetic and based on the v0.30 fixture-only R4 manifestation. No real corpus item is promoted, downgraded, or otherwise altered by this test.

## Epistemic boundary

Rights status expresses redistribution permission under the recorded scope only. It does not imply truth, scientific validation, safety, efficacy, or endorsement.
