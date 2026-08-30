# AkashicNET Public Client Policy v0.34

## Milestone

**A public client that cannot ask for private retrieval.**

## Contract

The v0.34 public clients consume only the hardened HTTP retrieval service and always request `visibility=public`.

They do not expose an internal/private visibility selector, do not call Drive directly, do not read document bodies, and do not infer redistribution permission from accessibility, provenance strength, semantic review state, canonicalisation state, or SHA-256 identity.

Only records admitted by the executable `PUBLIC_VERIFIED` gate may be rendered as public search results.

## Public display semantics

The client may display public-safe identifiers and metadata such as title/label, semantic decision, review state, query path, provenance tier/rank, logical/physical manifestation counts, and explicit rights/public status.

These dimensions remain independent:

- semantic ACCEPT means reviewed topical relationship, not truth;
- HOLD remains unresolved and is never promoted by the client;
- provenance tier describes retrieval/provenance support, not scientific validity;
- SHA-256 identity establishes byte identity where verified, not rights or truth;
- `PUBLIC_VERIFIED` controls public visibility only.

## Current corpus state

The production public manifest remains intentionally empty until a real corpus manifestation completes the R0→R4 workflow and is marked both `PUBLIC_VERIFIED` and production-manifest eligible. A zero-result public UI is therefore a valid and expected state.

## Security boundary

The browser client must not contain `visibility=internal` or provide UI controls that can request it. The Python public client must reject responses that do not confirm public visibility and the `PUBLIC_VERIFIED` gate.

No new Google Drive raw-file access, document-body reads, or hashing are authorised by v0.34.
