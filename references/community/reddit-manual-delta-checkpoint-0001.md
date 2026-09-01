# Reddit Manual Delta Batch 0001

## Scope

Review-only holding queue for public Reddit post IDs already present in the independently assembled `reddit-corroboration-seed-v0.3.json` but absent from the historical structural candidate pool.

## Checkpoint

- Candidate records: **7**
- Distinct canonical Reddit post IDs / URLs: **7 / 7**
- Subreddit: **r/NeuronsToNirvana**
- Original discovery source: **reddit-corroboration-seed-v0.3.json**
- Original per-record discovery date: **not recorded by the source seed**
- Batch assembly date: **2026-09-01**
- Web-index corroboration date: **2026-09-01 UTC**
- State: **public_web_index_corroborated**
- Import status: **HOLD**
- Public-web index corroboration: **7 / 7**
- Reddit API verification: **not performed**
- Pagination completeness: **unresolved**
- Historical-corpus deduplication: **all 7 absent from the validated historical candidate pool**
- Canonical corpus modification: **none**
- Provenance review: **corrected and verified against seed v0.3**

## Guardrails

- No usernames, post bodies, comments, private messages or private-subreddit content are collected.
- Public-web corroboration is not equivalent to current direct Reddit or API verification.
- Missing source dates remain unknown; the batch assembly or corroboration date must not be substituted as discovery time.
- Unavailable or unindexed sources must not be interpreted as false or deleted.
- No candidate may enter the canonical corpus until direct accessibility, pagination and remaining release checks pass.
- Automated truth inference, scientific-evidence promotion and rights promotion remain off.
- Pagination cannot be declared complete until an approved Reddit API crawl replays the recorded boundary.

## Next review action

Verify the seven held records through approved direct read-only Reddit/API access without rerunning completed historical ingestion.
