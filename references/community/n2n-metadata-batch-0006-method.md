# N2N Metadata Review Batch 0006

This expands the 1,000-record staging queue, not the separate 25-record historical
observation pilot. Source remains PR #376 at
`808564658800a1ab230bbb837aa3b228911d671f`.

Select eligible ranks 5,001–6,000 in the original deterministic ordering: exclude
curated entries, prioritize historical annotations, then sort lowercase post IDs
lexically. Validate all five preceding batches and exclude their 5,000 IDs.
The preceding JSON manifests remain unchanged and are linked by SHA-256.

| Measure | Count |
|---|---:|
| New staging records | 1,000 |
| New batch archive-row references | 1,000 |
| New batch captured historical annotations | 0 |
| Overlap with prior staging batches | 0 |
| Cumulative unique staged records | 6,000 |
| Uncurated archive records outside queue | 1,396 |
| Curated records, unchanged | 3 |
| Newly curated metadata records | 0 |

Original IDs, archived URLs, source locations, CSV record values and ordinals are
preserved. Uncaptured titles, authors, current flairs, evidence and rights remain
null. Archive provenance remains subject to the pinned upstream audit; these are
structural archive candidates, not independently verified live posts. There is no
inference from URL slugs and no source-body/comment/media ingestion.

Live Reddit access remains HOLD; rights, privacy, evidence, publication and
promotion gates CLOSED; accepted edges zero; model support empty. No merge,
deployment, canonical metadata write or website/maturity change.

The separate historical-observation pilot remains at 50 records. Its embedded
5,000 queue count is its earlier creation checkpoint, not the current queue total.
No pilot data or past evidence receipts were rewritten.

Generate with `python tools/stage_n2n_metadata_batch.py --batch 6 --write`;
validate by omitting `--write`. Only reviewed staging batches 1–6 are enabled.
Focused tests verify exact selection, cumulative uniqueness, every new raw CSV
reference, overlap rejection, missing prior batch and rejected batch numbers.
Receipts: `n2n-batch-0001-research/ara/evidence/batch-0006-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0006-counts.json`.
