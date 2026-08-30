# AkashicNET expanded community graph policy v0.41

## Milestone
Scale r/NeuronsToNirvana from the frozen 1,000-record curated pilot to the v0.40 canonical 7,298-record metadata index without converting corpus scale into semantic confidence.

## Construction
The v0.41 graph starts from the v0.5 library/provenance graph and overlays the v0.40 expanded N2N index as community nodes. The historical v0.7 1,000-record cross-source graph remains an immutable checkpoint rather than being rewritten.

## Review-state distinction
The earlier 1,000-record pilot was curated. The 7,298-record expansion is not assigned the same review status. Every new community node is:
- `review_state=unreviewed`
- `semantic_status=UNADJUDICATED`
- `rights_status=UNKNOWN_UNVERIFIED`
- `not_scientific_evidence_by_default=true`

## No scale-driven semantic promotion
v0.41 creates zero automatic Reddit↔canonical-work identity links and zero automatic semantic edges. `topics` are retained for navigation/audit only and do not validate subject matter, truth, evidence, safety, efficacy or rights.

A future review/indexing descendant may generate semantic candidates from the expanded corpus, but those candidates must remain HOLD/unreviewed until adjudicated under explicit rules.

## Privacy and rights
- Reddit bodies/comments/media are not fetched
- Drive document bodies are not accessed
- no embeddings are created
- public rights are not inferred from Reddit accessibility
- no expanded community node is `PUBLIC_VERIFIED` by this build
- rights and scientific evidence remain independent from topical relevance
