# AkashicNET WikiSpine batch expansion policy v0.7.1

WikiSpine expands only from explicitly approved AkashicNET seed concepts.

- Wikidata identifiers are recorded only when resolution is high precision.
- Ambiguous or unverified concepts remain `PENDING_API_RESOLUTION`; identifiers are never guessed.
- Wikipedia/Wikidata are reference-encyclopedia sources, not scientific evidence and not truth authorities.
- New semantic relationships default to `HOLD`.
- Expansion remains capped at two typed hops; arbitrary recursive crawling is disabled.
- Full article-body ingestion is disabled by default.
- Future article snapshots must record revision provenance.
- WikiSpine does not promote rights, scientific evidence, or truth state.
- This batch expansion performs no Google Drive access.

Milestone: **More reference coverage without lowering the epistemic threshold.**
