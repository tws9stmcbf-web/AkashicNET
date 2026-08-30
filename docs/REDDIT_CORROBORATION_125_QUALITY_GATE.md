# Reddit Corroboration — 125 Record Quality Gate

Status: ACTIVE

This gate is a targeted quality review. It does **not** reset or discard previously corroborated records.

## Evidence ladder

1. `structural_candidate` — canonical-looking historical Reddit post ID/URL.
2. `public_web_discovered` — independently surfaced through public-web discovery.
3. `id_intersection_corroborated` — independently discovered `(subreddit, post_id)` intersects the filtered historical corpus.
4. `provenance_audited` — discovery evidence has been reviewed and resolves to the intended subreddit/post identity rather than a bare incidental ID-string match.
5. `api_verified` — reserved for future verification through authorised Reddit API access.

`uncorroborated` does not mean invalid or nonexistent. `suspicious_pattern` does not mean fabricated. `generated_placeholder` must not be used without direct evidence of generation.

## 125 checkpoint review

- [ ] Confirm the combined seed uses exact `(subreddit, post_id)` deduplication.
- [ ] Preserve all historical seed/delta files as immutable evidence; corrections are additive.
- [ ] Audit schema consistency across earlier and newer corroboration batches.
- [ ] Investigate and document the known v0.11 metadata simplification.
- [ ] Review record-level provenance quality for older/weaker batches.
- [ ] Take a reproducible sample across early, middle and recent batches and confirm discovery evidence resolves to the intended r/NeuronsToNirvana post.
- [ ] Record mismatches or ambiguous cases without silently deleting them.
- [ ] Keep public-web corroboration distinct from live/API verification.
- [ ] Keep the 972 sequence-derived `suspicious_pattern` records outside automatic promotion.
- [ ] Publish quality-gate metrics before materially scaling the corroboration campaign.

## Recommended record-level provenance fields

Future discovery records should be able to carry, where available:

- `subreddit`
- `post_id`
- `canonical_url`
- `discovery_method`
- `discovery_source`
- `discovered_at`
- `source_reported_title`
- `source_reported_date`
- `evidence_status`
- `audit_status`
- `notes`

Do not require usernames, post bodies or comments for metadata-first corroboration.

## Counter semantics

The primary coverage denominator is the filtered candidate pool: **6,384**.

Only actual historical-corpus intersections count as independently corroborated. Public-web candidates outside the historical pool remain useful evidence but do not increment this counter.

The 125-record milestone is a quality checkpoint, not a claim of corpus completeness.
