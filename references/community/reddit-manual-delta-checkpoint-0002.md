# Reddit Manual Delta Batch 0002

## Scope

Metadata-only capture of the first public `new` feed page for `r/NeuronsToNirvana`, observed on 2026-09-01.

## Checkpoint

- Feed rows observed: **25**
- Directly accessible public post URLs: **25**
- Historical `reddit-uri-index.csv` matches: **0**
- Prior Manual Delta Batch 0001 matches: **2**
- New manual candidates: **23**
- Deleted/private/unavailable records observed: **0**
- Import status for new candidates: **HOLD**
- Canonical corpus modification: **none**
- Usernames, bodies and comments stored: **none**

## Deduplication

The following feed rows were already present in Manual Delta Batch 0001 and receive no new candidate identity:

- `1w1fcdx`
- `1vztbnl`

All 25 post IDs were checked against `references/community/reddit-uri-index.csv` at blob `6b6184b0f981928abb34f4b7d8bd262f3b5b48ca`; none matched the historical structural source.

## Pagination boundary

- Page: **1**
- Rows: **25**
- First post ID: `1w3jv17`
- Last post ID: `1vzph25`
- Recorded next cursor: `dDNfMXZ6cGgyNQ==` (boundary `t3_1vzph25`)
- Next public URL: `https://www.reddit.com/r/NeuronsToNirvana/new/?after=dDNfMXZ6cGgyNQ%3D%3D&sort=new&t=DAY`
- Pagination beyond this boundary: **unresolved**

## Guardrails

- Public accessibility confirms URL identity at observation time; it does not establish permanence, authorship, rights or scientific validity.
- No unavailable record is classified as false or deleted without stronger evidence.
- No candidate enters the canonical corpus until provenance, duplicate and approved import gates pass.
- Automated truth inference, scientific-evidence promotion and rights promotion remain off.

## Next review action

Capture the next public feed page from the recorded cursor and stop when a validated historical or already-reviewed boundary is reached.
