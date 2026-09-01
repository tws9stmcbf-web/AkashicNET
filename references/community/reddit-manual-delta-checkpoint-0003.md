# Reddit Manual Delta Batch 0003

## Scope

Metadata-only capture of public `new` feed page 2 for `r/NeuronsToNirvana`, observed on 2026-09-01.

## Checkpoint

- Feed rows observed: **25**
- Directly accessible public post URLs: **25**
- Historical `reddit-uri-index.csv` matches: **0**
- Prior manual batch matches: **2**
- New manual candidates: **23**
- Deleted/private/unavailable records observed: **0**
- Import status for new candidates: **HOLD**
- Canonical corpus modification: **none**
- Usernames, bodies and comments stored: **none**

## Deduplication and provenance

All post IDs were checked against `references/community/reddit-uri-index.csv` at blob `6b6184b0f981928abb34f4b7d8bd262f3b5b48ca` and against prior manual delta batches.

Prior-held matches receiving no new candidate identity: `1vzfhwd`, `1vxmjoc`.

## Pagination boundary

- Page: **2**
- Input cursor: `dDNfMXZ6cGgyNQ==`
- Rows: **25**
- First post ID: `1vzoa3j`
- Last post ID: `1vtwt3t`
- Recorded next cursor: `dDNfMXZ0d3QzdA==` (boundary `t3_1vtwt3t`)
- Next public URL: `https://www.reddit.com/r/NeuronsToNirvana/new/?after=dDNfMXZ0d3QzdA%3D%3D&sort=new&t=DAY`
- Pagination beyond this boundary: **continued**

## Guardrails

- Public accessibility confirms URL identity at observation time; it does not establish permanence, authorship, rights or scientific validity.
- No unavailable record is classified as false or deleted without stronger evidence.
- No candidate enters the canonical corpus until provenance, duplicate and approved import gates pass.
- Automated truth inference, scientific-evidence promotion and rights promotion remain off.

## Next review action

Continue from the recorded cursor while preserving metadata-only HOLD status.
