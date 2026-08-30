# AkashicNET expanded community search policy v0.44

## Milestone
Make the expanded 9,340-record r/NeuronsToNirvana metadata corpus searchable internally without turning ranking into semantic adjudication, evidence validation, truth, or rights clearance.

## Ranking
The deterministic ranking uses only explicit metadata:
- exact query phrase in title: 100
- query-token hit in title: 10 each
- query-token hit in tracked topics: 1 each
- stable `community_id` breaks ties

The score is a retrieval relevance score only. It is not confidence, evidence quality, scientific validity, safety, efficacy, truth, popularity, or rights status.

## Result status
Every v0.44 result remains:
- `review_state=unreviewed`
- `semantic_status=UNADJUDICATED`
- `rights_status=UNKNOWN_UNVERIFIED`
- `scientific_evidence_status=NOT_EVALUATED`

## Visibility
v0.44 is an internal metadata-research CLI. It is not wired into the public browser/service and does not bypass the v0.29+ `PUBLIC_VERIFIED` gate.

## Guardrails
- no Reddit body reads
- no Drive body reads
- no embeddings
- no semantic auto-acceptance
- no truth inference
- no rights promotion
- no scientific-evidence promotion
