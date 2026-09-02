# Reddit Manual Delta Batch 0004

## Scope

Metadata-only capture of public `new` feed page 3 for `r/NeuronsToNirvana`, observed on 2026-09-01.

## Checkpoint

- Feed rows observed: **25**
- Directly accessible public post URLs: **25**
- Historical `reddit-uri-index.csv` matches: **0**
- Prior manual batch matches: **1**
- New manual candidates: **24**
- Deleted/private/unavailable records observed: **0**
- Import status for new candidates: **HOLD**
- Canonical corpus modification: **none**
- Usernames, bodies and comments stored: **none**

## Deduplication

Post `1vrwp5r` was already present in Manual Delta Batch 0001 and receives no new candidate identity.
 and provenance

All post IDs were checked against `references/community/reddit-uri-index.csv` at blob `6b6184b0f981928abb34f4b7d8bd262f3b5b48ca` and against prior manual delta batches.


## Pagination boundary

- Page: **3**
- Input cursor: `dDNfMXZ0d3QzdA==`
- Rows: **25**
- First post ID: `1vtwh2m`
- Last post ID: `1vpp5v8`
- Recorded next cursor: `dDNfMXZwcDV2OA==` (boundary `t3_1vpp5v8`)
- Next public URL: `https://www.reddit.com/r/NeuronsToNirvana/new/?after=dDNfMXZwcDV2OA%3D%3D&sort=new&t=DAY`
- Pagination beyond this boundary: **continued**

## Guardrails

- Public accessibility confirms URL identity at observation time; it does not establish permanence, authorship, rights or scientific validity.
- No unavailable record is classified as false or deleted without stronger evidence.
- No candidate enters the canonical corpus until provenance, duplicate and approved import gates pass.
- Automated truth inference, scientific-evidence promotion and rights promotion remain off.

## Next review action

Continue from the recorded cursor while preserving metadata-only HOLD status.
