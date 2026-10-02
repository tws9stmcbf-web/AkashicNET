# N2N Metadata Review Batch 0007

Source remains PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
Continue the staging queue at eligible ranks 6,001–7,000, excluding all 6,000
validated IDs in batches 0001–0006. Ordering remains uncurated records, historical
annotations first, then lowercase post ID in ascending lexical order. All earlier
manifests remain unchanged; the prior-batch SHA-256 preserves the validation chain.

Batch 0007 adds 1,000 unique records with 1,000 original CSV row references and no
captured historical annotations. Cumulative staging count: 7,000 unique records.
Overlap: zero. Uncurated records outside the queue: 396. Archive total: 7,399.
Curated metadata remains at three, with zero newly curated records.

Original IDs, archived URLs, source locations, CSV values and record ordinals are
preserved. Missing titles, authors, current flairs, evidence and rights stay null.
These are structural archive candidates, not independently verified live posts.
No title inference, source-body/comment/media ingestion, or historical-to-current
verification promotion. The separate 50-record receipt pilot remains unchanged;
its queue-size figures are creation-time checkpoints rather than current totals.

Live Reddit access remains HOLD. Rights, privacy, evidence, publication and
promotion gates remain CLOSED. Accepted canonical edges stay zero; model support
empty. No merge, deployment, canonical metadata write, website or maturity change.

Generate: `python tools/stage_n2n_metadata_batch.py --batch 7 --write`.
Validate: omit `--write`. Only staging batches 1–7 are enabled. Tests check exact
selection, cumulative uniqueness, every raw CSV reference, prior-overlap rejection,
missing sixth batch and unreviewed batch-number rejection. Receipts:
`n2n-batch-0001-research/ara/evidence/batch-0007-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0007-counts.json`.
