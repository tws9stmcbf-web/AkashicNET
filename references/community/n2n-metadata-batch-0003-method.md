# N2N Metadata Review Batch 0003

Pinned source remains PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
Select eligible ranks 2,001–3,000 using batch 0001's ordering: uncurated records,
historical annotations first, then lowercase post ID in ascending lexical order.
Validate both earlier batches against the pinned source files, exclude all their
IDs and retain the next 1,000. No random-sample, chronology or evidence claim.

Batch 0003 contains exactly 1,000 unannotated records with 1,000 original CSV row
references. It has zero overlap with either prior batch. The three batches contain
3,000 unique records; 4,396 uncurated records remain outside them. Curated metadata
remains at three, with zero newly curated records. The first two JSON files are unchanged.

Each record preserves its original archive values, CSV record ordinals, post ID,
canonical archived URL and source locations. The manifest pins the original source
files and links the prior batch by SHA-256. The generator validates the entire
preceding chain. Missing titles, current flairs, authors, evidence and rights status
remain null. Empty annotations mean uncaptured, not known absence of a live flair.

Live Reddit access remains HOLD. Rights, privacy, evidence, publication and promotion
gates remain CLOSED. Bodies, comments and media are not ingested. Accepted canonical
edges remain zero and model support empty. No merge, deployment or website change.

Generate using `python tools/stage_n2n_metadata_batch.py --batch 3 --write`;
validate using the same command without `--write`. Batches 1–3 alone are supported.
The focused suite adds tests for all-batch uniqueness, exact selection, reproduction
of all three manifests, overlap with either prior batch, and a missing/tampered
second batch. Test output and counts are retained in
`n2n-batch-0001-research/ara/evidence/batch-0003-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0003-counts.json`.
