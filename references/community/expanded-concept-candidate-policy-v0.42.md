# AkashicNET expanded concept-candidate policy v0.42

## Milestone
Use the reviewed 15-concept ontology to discover topical review candidates across the expanded r/NeuronsToNirvana metadata corpus without automatically accepting semantic edges.

## Why the acceptance rule changes at scale
The v0.11 pilot could auto-accept a small set of high-precision title aliases because the 1,000-record corpus was curated and its candidate surface was bounded. The v0.40/v0.41 expansion contains 9,340 canonical community records with `review_state=unreviewed`.

Therefore v0.42 treats every alias hit as `HOLD`, including high-precision title matches. Scale improves recall; it does not lower the semantic acceptance threshold.

## Candidate bases
- `HIGH_PRECISION_TITLE_MATCH`: reviewed narrow alias occurs explicitly in the title.
- `BROAD_TITLE_MATCH`: broad bridge term such as consciousness/self occurs in the title; contextual review is especially important.
- `TOPICS_METADATA_MATCH`: alias occurs only in tracked topic/navigation metadata.

These bases prioritize review. They do not represent evidence strength, truth, safety, efficacy or rights.

## Guardrails
- automatic semantic ACCEPT: 0
- every expanded candidate begins HOLD
- no Reddit body hydration
- no embeddings
- no truth inference
- no scientific-evidence promotion
- no rights promotion
- concept association remains topical only even after a future ACCEPT decision
