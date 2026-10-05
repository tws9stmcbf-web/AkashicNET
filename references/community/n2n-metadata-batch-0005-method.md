# N2N Metadata Review Batch 0005

Pinned source remains PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
Take eligible ranks 4,001–5,000 from the original ordering: uncurated records,
historical annotations first, then ascending lexical lowercase post ID. Revalidate
and exclude all earlier batches. Prior manifests remain unchanged; the SHA-256
chain identifies the complete exclusion set.

Batch 0005 adds exactly 1,000 unannotated records and 1,000 original CSV row
references, with zero overlap. Cumulative staged count: 5,000 unique records.
Uncurated records outside the queue: 2,396. Archive total: 7,399. Curated: three.
No newly curated metadata is claimed. The queue is not a representative sample.

Post IDs, original archive values, CSV record ordinals, canonical archived URLs
and source locations are preserved. Titles, authors, current flairs, evidence and
rights remain null; no inference from slugs. Live Reddit access remains HOLD.
Rights, privacy, evidence, publication and promotion gates remain CLOSED. Bodies,
comments and media remain uningested. Accepted edges zero; model support empty.
No merge, deployment, website or Big Question maturity change.

Generate with `python tools/stage_n2n_metadata_batch.py --batch 5 --write`;
validate by omitting `--write`. Only reviewed batches 1–5 are enabled.
Focused fifth-batch validation checks cumulative uniqueness, exact selection,
reproduction, all raw CSV provenance references, overlap rejection, a missing
fourth batch and rejection of unreviewed batch numbers. Results are retained in
`n2n-batch-0001-research/ara/evidence/batch-0005-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0005-counts.json`. The preceding full
25-test run remains in the batch-0004 validation receipt.
