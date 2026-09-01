# Reddit Manual Delta Batch 0006

## Scope

Metadata-only capture of public `new` feed page 5 for `r/NeuronsToNirvana`, observed on 2026-09-01.

## Checkpoint

- Feed rows observed: **25**
- Directly accessible public post URLs: **25**
- Historical `reddit-uri-index.csv` matches: **24**
- Prior manual batch matches: **0**
- New manual candidates: **1**
- Deleted/private/unavailable records observed: **0**
- Import status for new candidates: **HOLD**
- Canonical corpus modification: **none**
- Usernames, bodies and comments stored: **none**

## Deduplication and provenance

All post IDs were checked against `references/community/reddit-uri-index.csv` at blob `6b6184b0f981928abb34f4b7d8bd262f3b5b48ca` and against prior manual delta batches.

Historical matches receiving no new candidate identity: feed ranks 2–25.

## Pagination boundary

- Page: **5**
- Input cursor: `dDNfMXZtd3JwZw==`
- Rows: **25**
- First post ID: `1vmweht`
- Last post ID: `1vk0hxc`
- Historical overlap starts at feed rank **2** (`1vmam4h`)
- Remaining historical matches on page: **24 consecutive rows**
- Pagination beyond this boundary: **not required; validated corpus boundary reached**

## Guardrails

- Public accessibility confirms URL identity at observation time; it does not establish permanence, authorship, rights or scientific validity.
- No unavailable record is classified as false or deleted without stronger evidence.
- No candidate enters the canonical corpus until provenance, duplicate and approved import gates pass.
- Automated truth inference, scientific-evidence promotion and rights promotion remain off.

## Next review action

Stop pagination at the validated historical boundary. Review HOLD candidates separately before any approved import.
