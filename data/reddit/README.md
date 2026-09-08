# Reddit ingestion

**Status: Reddit API access is on HOLD.** Nothing in this repository crawls Reddit, calls Reddit, or holds an OAuth application/key by default. The crawler, workflow, and docs below describe the mechanism only; they do not authorize its use.

AkashicNET's Reddit crawler is deliberately metadata-first. It uses Reddit's OAuth Data API, writes append-only JSONL, canonicalises post URLs, skips duplicate Reddit IDs, and stores a pagination checkpoint so interrupted runs can resume.

## Explicit approval is required before any use

Any actual crawl or refresh run — locally or in CI — requires explicit, separately documented approval. In CI (`.github/workflows/reddit-pilot.yml`) this is enforced with a fail-closed gate: the job only reads Reddit credentials or makes a network request when the repository **variable** `REDDIT_API_APPROVED` equals the exact string `true`. Repository *secrets* (`REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`) being configured is never sufficient by itself; without the approval variable set, the job stops before secrets are read and before any network request is made. Ordinary unit tests (`tests/test_reddit_crawler.py`) always run and never require this approval or network access.

## Purpose and use limitations

- **Purpose:** read-only, non-commercial source indexing of publicly available Reddit post metadata for provenance/citation linking within AkashicNET.
- **No AI/model training:** records produced by this crawler must not be used to train or fine-tune AI/ML models. Reddit's Data API terms restrict retention/use of User Content and prohibit such training without rightsholder permission.
- **Data minimization:** only the minimum fields needed for source identity, canonical linking, time, safety/routing, and provenance are retained (see "Record boundary" below). Post bodies, comments and usernames are never stored.
- **Public counts:** any public-facing count or figure derived from Reddit-sourced records may only change after a validated, reviewed artifact (not from an unreviewed pilot/reconciliation run) is promoted into the repository.

## Credentials

Create/obtain a Reddit API application that is approved for your use case, then set credentials locally. Do not commit them. Credentials alone do not authorize a crawl; the `REDDIT_API_APPROVED` gate above must also be satisfied.

```bash
export REDDIT_CLIENT_ID='...'
export REDDIT_CLIENT_SECRET='...'
export REDDIT_USER_AGENT='AkashicNET-reddit-crawler/0.1 by <reddit-account>'
```

## Dry pilot

```bash
python3 scripts/reddit_crawler.py NeuronsToNirvana \
  --max-posts 25 \
  --output data/reddit/n2n-posts.jsonl \
  --checkpoint data/reddit/checkpoint-n2n.json
```

Then inspect the JSONL before increasing the crawl size.

## Record boundary

The v1 crawler intentionally excludes usernames, post bodies and comments. Each record contains post-level discovery/provenance metadata such as Reddit ID, title, canonical URL, external URL, timestamps, score/count fields, subreddit and retrieval time.

This boundary is intentional: Reddit's current Data API terms restrict retention/use of User Content and prohibit using User Content to train AI/ML models without the relevant rightsholder permission. Any future content-enrichment mode should therefore be separately reviewed and explicitly enabled rather than silently expanding this crawler.

### v2 minimized schema

`akashicnet.reddit.post.v2` (`normalize_post_v2`) is a new, narrower schema for future API-derived records. It is additive and never mutates or replaces the sealed historical `akashicnet.reddit.post.v1` schema/fixtures. Compared to v1, v2 additionally excludes engagement counters — `score`, `num_comments`, and `upvote_ratio` — as well as `stickied`/`locked`/`is_self` moderation flags. Only fields justified by source identity (`reddit_id`, `fullname`, `subreddit`, `title`), canonical linking (`canonical_url`, `external_url`), time (`created_utc`, `retrieved_at`), safety/routing (`over_18`), and provenance are retained.

## Deletion-aware refresh/reconciliation

`reconcile_post`/`reconcile_records` implement the smallest deletion-aware refresh path: when an approved refresh shows a Reddit post is removed, deleted, or no longer returned by the API, cached/output content fields (title, URLs, timestamps, etc.) are dropped rather than retained. What remains is a minimal, non-content tombstone record (`record_type: "post_metadata_removed"`) carrying only `reddit_id`, `status` (`removed` or `unavailable`), and `checked_at`. This is intentionally the minimum needed to audit that a check happened, without re-identifying the removed content or retaining any signal that could support re-identification or sensitive-trait inference.

## Pagination and historical coverage

The crawler follows Reddit listing cursors and can resume from a saved `after` value. Reddit listing endpoints do not guarantee an exhaustive archive of every historical post, so this crawler should be treated as an incremental discovery/refresh source rather than the sole mechanism for reconstructing the full historical r/NeuronsToNirvana corpus.

For the existing AkashicNET historical URL corpus, a later enrichment stage should take known canonical Reddit URLs/IDs as seeds and refresh only the metadata required by the unified index.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Data hygiene

Runtime JSONL and checkpoint files are ignored by Git. Promote only deliberately reviewed, documented derived datasets into the repository.
