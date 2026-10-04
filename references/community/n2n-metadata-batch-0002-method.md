# N2N Metadata Review Batch 0002

Pinned source: PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
Continue batch 0001's eligible ordering: exclude the three curated records, sort
historically annotated records first and lowercase post IDs lexically within each
group. Validate the first batch against the pinned sources, exclude its 1,000 IDs,
and take the next 1,000: eligible ranks 1,001–2,000. This is a review queue, not
completed enrichment, a representative sample, chronological sorting or evidence ranking.

| Measure | Count |
|---|---:|
| Unique archived N2N records | 7,399 |
| Curated records, unchanged | 3 |
| Batch 0002 records | 1,000 |
| Batch 0002 annotated records | 0 |
| Batch 0002 archive-row references | 1,000 |
| Overlap with batch 0001 | 0 |
| Cumulative unique staged records | 2,000 |
| Uncurated records outside both batches | 5,396 |
| Newly curated records | 0 |

The new JSON retains original CSV values, CSV record ordinals, post IDs, canonical
URLs and all distinct archived source locations. Its prior-batch hash links the
exact exclusion set; both CSVs and the source parser/loader retain SHA-256 pins.
The first batch JSON is unchanged. `remaining_uncurated_outside_batch` counts
records outside this individual batch; `remaining_uncurated_outside_all_batches`
is the cumulative remainder and should be used for planning the next tranche.

Titles, authors, current flairs, evidence and rights status remain null. URL slugs
are never turned into titles. These records contain no captured historical
annotations; no annotations have been inferred. Live Reddit access remains HOLD.
Bodies, comments and media are not ingested. Rights, privacy, evidence, publication
and promotion gates remain CLOSED; accepted edges are zero and model support empty.
No merge, deployment, website change or Big Question maturity change.

Reproduce with `python tools/stage_n2n_metadata_batch.py --batch 2 --write`;
validate without rewriting by omitting `--write`. The default still validates
batch 0001. Only explicitly reviewed batches 1 and 2 are accepted.

Validation: 19 focused local tests passed (4 new, 15 retained), including rejection
of overlap, missing/damaged prior batch, invented metadata, provenance damage,
opened gates, wrong counts and wrong prior-batch hash. Evidence is in
`n2n-batch-0001-research/ara/evidence/batch-0002-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0002-counts.json`.
