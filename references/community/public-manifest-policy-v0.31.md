# AkashicNET public manifest policy v0.31

The production public manifest is generated only from real production rights-ledger records that satisfy both conditions:

1. `public_status == PUBLIC_VERIFIED`
2. `public_manifest_eligible == YES`

Fixture-only records are never production-manifest eligible, including the synthetic R4 fixture introduced in v0.30.

`UNKNOWN_UNVERIFIED`, `PRIVATE`, and `SHARED_RESTRICTED` records are excluded. Public accessibility, semantic acceptance, provenance strength, collection membership, or SHA-256 identity cannot substitute for rights verification.

An empty production manifest is a valid and expected state when no real corpus item has completed R4 review. Empty does not mean the library mapping is incomplete; it means public redistribution clearance is incomplete.

Rights clearance remains independent of truth, scientific validation, safety, efficacy, topical relevance, and endorsement.
