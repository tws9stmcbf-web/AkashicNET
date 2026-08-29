# Reddit ingestion

AkashicNET's Reddit crawler is deliberately metadata-first. It uses Reddit's OAuth Data API, writes append-only JSONL, canonicalises post URLs, skips duplicate Reddit IDs, and stores a pagination checkpoint so interrupted runs can resume.

## Credentials

Create/obtain a Reddit API application that is approved for your use case, then set credentials locally. Do not commit them.

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

## Pagination and historical coverage

The crawler follows Reddit listing cursors and can resume from a saved `after` value. Reddit listing endpoints do not guarantee an exhaustive archive of every historical post, so this crawler should be treated as an incremental discovery/refresh source rather than the sole mechanism for reconstructing the full historical r/NeuronsToNirvana corpus.

For the existing AkashicNET historical URL corpus, a later enrichment stage should take known canonical Reddit URLs/IDs as seeds and refresh only the metadata required by the unified index.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Data hygiene

Runtime JSONL and checkpoint files are ignored by Git. Promote only deliberately reviewed, documented derived datasets into the repository.
