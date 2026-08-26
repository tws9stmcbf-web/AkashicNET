# Read-only Reddit Bridge

The Reddit Bridge extends the existing N2N ingestion architecture into a small,
read-only, multi-subreddit normalization layer. It preserves canonical Reddit
URLs, Reddit post IDs, source attribution, deduplication signals, and cross-post
lineage without mirroring Reddit or publishing back to Reddit.

## Sources

Sources are configured in `references/community/reddit-source-registry.json`.
The MVP registry includes:

- `r/NeuronsToNirvana`
- `r/TribalGathering`
- `r/microdosing`
- `r/microDJPanPSYchic`

Additional subreddits should be added to the registry rather than hard-coded in
bridge logic.

## Safety model

- Reddit access is read-only.
- No automatic publishing, commenting, replying, voting, moderation, or deletion
  APIs are implemented.
- The bridge stores metadata and provenance records, not a Reddit mirror.
- Canonical Reddit URLs and post IDs remain the source of record.
- Duplicate and near-duplicate records are labeled for review instead of being
  silently merged into the archive.

## MVP usage

The MVP uses local JSON fixtures for deterministic tests and dry runs:

```bash
python tools/reddit_bridge/cli.py validate-registry
python tools/reddit_bridge/cli.py sources
python tools/reddit_bridge/cli.py ingest --fixture tools/reddit_bridge/fixtures/sample_listing.json --source all --limit 25
```

Use `--write-records` only when intentionally writing local bridge artifacts;
that flag still does not publish anything to Reddit.
