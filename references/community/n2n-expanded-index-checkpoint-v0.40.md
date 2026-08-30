# AkashicNET N2N expanded-index checkpoint v0.40

## Milestone
Expand the frozen 1,000-record r/NeuronsToNirvana pilot into a reproducible metadata-and-links-only descendant index derived from the tracked Akashic master index.

## Audited source counts
The corrected v0.40 master-index audit uses the explicit tracked `source` and `url` columns and measured:
- 12,058 master-index rows
- 9,401 Reddit rows
- 9,399 unique canonical Reddit URLs after host/query/fragment/trailing-slash normalization
- 9,341 r/NeuronsToNirvana source rows
- 9,340 unique canonical r/NeuronsToNirvana URLs

The earlier provisional 7,298 N2N count was caused by an audit regex that parsed URLs from concatenated row text rather than the explicit `url` field. CI exposed the mismatch before the expanded-index milestone was accepted. That provisional undercount is not a canonical corpus statistic.

The one duplicate N2N source row is retained as duplicate-source provenance rather than discarded as an error.

## Expanded index
`scripts/build_n2n_expanded_index_v040.py` deterministically rebuilds `data/n2n-expanded-index-v0.40.csv` from `references/community/akashic-master-index.csv`.

Identity is based on the normalized canonical Reddit URL. Each of the 9,340 canonical N2N records receives a deterministic `community_id`; duplicate master rows retain their source-row count and source record IDs.

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
The tracked master index contains **9,401 Reddit rows**, not 9,401 unique canonical Reddit URLs. Under v0.40 canonical URL normalization those rows resolve to **9,399 canonical Reddit URLs**, including **9,340 canonical r/NeuronsToNirvana URLs** from 9,341 N2N source rows.
