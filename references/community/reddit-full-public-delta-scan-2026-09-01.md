# Reddit Full Public Delta Scan — 2026-09-01

## Outcome

The public `new` feed for `r/NeuronsToNirvana` was followed from the newest page through the first validated historical corpus boundary.

- Pages scanned: **5**
- Feed rows checked: **125**
- Directly accessible public post URLs: **125**
- New review-only candidates: **94**
- Prior manual HOLD matches: **7**
- Historical canonical-index matches: **24**
- Deleted/private/unavailable records observed: **0**
- Provenance failures in captured metadata: **0**
- Canonical imports: **0**

## Boundary

Page 5 begins with one new candidate, `1vmweht`, followed by **24 consecutive** records already present in `references/community/reddit-uri-index.csv`. This establishes the historical overlap boundary at feed rank 2 (`1vmam4h`).

Pagination stopped at that boundary. No older page was required.

## Batch map

- Batch 0002 / page 1: 23 new HOLD, 2 prior-held duplicates
- Batch 0003 / page 2: 23 new HOLD, 2 prior-held duplicates
- Batch 0004 / page 3: 24 new HOLD, 1 prior-held duplicate
- Batch 0005 / page 4: 23 new HOLD, 2 prior-held duplicates
- Batch 0006 / page 5: 1 new HOLD, 24 historical matches

## Integrity posture

This was a public, metadata-only scan. It verifies that each captured URL was publicly reachable at observation time and that IDs were compared against the frozen historical index blob `6b6184b0f981928abb34f4b7d8bd262f3b5b48ca` and prior manual batches.

It does not establish permanent availability, authorship, content authenticity, reuse rights, or scientific validity. Usernames, post bodies and comments were not stored. All 95 new candidates remain `HOLD`.

## Canonical checkpoint

- Unique Reddit URLs: **9,401**
- Unified-index records: **12,058**
- Canonical changes from this scan: **none**
