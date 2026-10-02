# N2N Metadata Review Batch 0004

Source remains PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
Use eligible ranks 3,001–4,000 from the original ordering (uncurated records,
historical annotations first, then lexical lowercase post ID). Revalidate the
three earlier manifests and exclude their 3,000 IDs. The previous-batch SHA-256
links the complete validated chain. Earlier JSON manifests remain unchanged.

Exactly 1,000 new records and 1,000 original CSV row references; zero captured
annotations and zero overlap with any earlier batch. Cumulative staged count is
4,000 unique records. The uncurated remainder outside all batches is 3,396.
The archive denominator is 7,399; curated records remain three, newly curated zero.

This is an offline review queue. Original archive values, row ordinals, post IDs,
URLs and provenance are preserved. Titles, current flairs, authorship, evidence
and rights status remain uncaptured/unassessed. There is no title inference from
slugs, live existence verification, body/comment/media ingestion or evidence claim.
Reddit access is HOLD and all rights, privacy, evidence, publication and promotion
gates remain CLOSED. No merge, deployment, website update or maturity promotion.

Generate: `python tools/stage_n2n_metadata_batch.py --batch 4 --write`.
Validate: omit `--write`. Only batches 1–4 are enabled. Tests check reproduction of
all four manifests, cumulative uniqueness, exact selection, overlap with each
prior batch and a missing or tampered third batch, alongside prior boundary tests.
Evidence: `n2n-batch-0001-research/ara/evidence/batch-0004-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0004-counts.json`.
