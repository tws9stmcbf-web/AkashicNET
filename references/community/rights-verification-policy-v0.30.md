# AkashicNET rights verification policy v0.30

## Purpose

This policy defines the evidence required to move a manifestation through the AkashicNET rights ladder. Rights status is independent of truth, scientific evidence, topical relevance, provenance strength, semantic acceptance, and SHA-256 identity.

## Rights ladder

- **R0 — provenance only**: source/object provenance is recorded. No public-use conclusion.
- **R1 — public-domain or licence candidate**: a plausible rights basis is identified, but not yet tied to an exact manifestation.
- **R2 — manifestation identified**: the exact edition/translation/manifestation is identified sufficiently for rights review.
- **R3 — authoritative rights evidence**: an authoritative rights or licence source is recorded for the identified manifestation and relevant jurisdiction.
- **R4 — independently corroborated public status**: R0–R3 are complete and a second independent corroborating source supports the same redistribution conclusion for the same manifestation and jurisdiction.

Only **R4** may map to `PUBLIC_VERIFIED`.

## Required R4 evidence bundle

A record may be promoted to `PUBLIC_VERIFIED` only when all of the following are explicit and non-empty:

1. stable manifestation identifier;
2. source/provenance reference;
3. exact manifestation/edition description;
4. rights basis (`PUBLIC_DOMAIN`, `EXPLICIT_LICENCE`, or `OWNER_AUTHORISED`);
5. authoritative rights evidence reference;
6. independent corroborating evidence reference distinct from the authoritative source;
7. jurisdiction or licence scope;
8. reviewer decision `APPROVE_R4`;
9. review timestamp/date;
10. public status explicitly set to `PUBLIC_VERIFIED`.

No field may be inferred from source accessibility, collection membership, title similarity, provenance tier, semantic ACCEPT, or SHA-256 identity.

## Downgrade / revocation rule

If any required R4 evidence becomes missing, contradicted, expired, withdrawn, or scope-incompatible, the record must cease to be `PUBLIC_VERIFIED` until re-reviewed. Rights promotion is never monotonic by assumption.

## Controlled fixture

v0.30 includes one synthetic fixture-only manifestation used solely to prove the R4 validator and v0.29 executable public gate. It is **not a corpus item**, does not establish rights to any real work, and is explicitly excluded from production public manifests.

## Epistemic separation

`PUBLIC_VERIFIED` means only that the recorded evidence bundle supports public redistribution under the recorded scope. It does **not** mean:

- the content is true;
- the content is scientifically validated;
- AkashicNET endorses the content;
- semantic relationships are correct beyond their separately reviewed status;
- the manifestation is byte-identical to another object unless separately SHA-256 verified.
