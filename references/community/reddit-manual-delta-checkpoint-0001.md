# Reddit Manual Delta Batch 0001

## Scope

Review-only holding queue for public Reddit post IDs already present in the independently assembled `reddit-corroboration-seed-v0.6.json` but absent from the historical structural candidate pool.

## Checkpoint

- Candidate records: **7**
- Subreddit: **r/NeuronsToNirvana**
- State: **manual_incremental_candidate**
- Import status: **HOLD**
- Live/API verification: **not completed**
- Pagination completeness: **unresolved**
- Canonical corpus modification: **none**

## Guardrails

- No usernames, post bodies, comments, private messages or private-subreddit content are collected.
- Public-web corroboration is not equivalent to current live verification.
- Unavailable or unindexed sources must not be interpreted as false or deleted.
- No candidate may enter the canonical corpus until URL identity, accessibility state, deduplication and provenance checks pass.
- Automated truth inference, scientific-evidence promotion and rights promotion remain off.
- Pagination cannot be declared complete until an approved Reddit API crawl replays the recorded boundary.

## Next review action

Verify the seven candidate URLs through approved read-only access, then capture the newest 25 public links as Batch 0002 and continue backwards until an existing validated corpus boundary is reached.
