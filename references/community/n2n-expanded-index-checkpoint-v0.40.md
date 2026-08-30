# AkashicNET N2N expanded-index checkpoint v0.40

## Milestone
Expand the frozen 1,000-record r/NeuronsToNirvana pilot into a reproducible metadata-and-links-only descendant index derived from the tracked Akashic master index.

## Audited source counts
The v0.40 master-index audit measured:
- 12,058 master-index rows
- 9,401 Reddit rows
- 9,341 rows containing r/NeuronsToNirvana
- 7,357 unique canonical Reddit URLs after host/query/trailing-slash normalization
- 7,298 unique canonical r/NeuronsToNirvana URLs

The difference between row counts and canonical URL counts is retained as duplicate-source provenance, not discarded as an error.

## Expanded index
`scripts/build_n2n_expanded_index_v040.py` deterministically rebuilds `data/n2n-expanded-index-v0.40.csv` from `references/community/akashic-master-index.csv`.

Identity is based on the normalized canonical Reddit URL. Each canonical record receives a deterministic `community_id`; duplicate master rows retain their source-row count and source record IDs.

## Historical pilot preservation
The 1,000-record pilot remains a frozen historical checkpoint. v0.40 is a descendant expansion and does not rewrite the pilot or retroactively change earlier v0.7–v0.26 metrics.

## Epistemic and privacy boundaries
- metadata and links only
- no Drive document bodies
- no Reddit body crawling in this build
- no embeddings
- scientific-evidence default remains false
- truth inference remains off
- rights promotion remains off
- no automatic Reddit↔canonical work identity edges
- topic/category fields remain navigation metadata unless separately reviewed

## Count wording
Do not describe 9,401 as 9,401 unique Reddit URLs. The tracked master index contains 9,401 Reddit rows; the v0.40 canonicalization audit resolves 7,357 unique canonical Reddit URLs, including 7,298 unique canonical r/NeuronsToNirvana URLs.
