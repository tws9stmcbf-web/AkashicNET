# N2N Metadata Review Batch 0001

Source boundary: PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
This is a staged offline review queue, not completed metadata enrichment.

## Selection

Use the existing annotation-aware parser and community-search loader. Group archived
N2N locations by lowercase post ID. Exclude the three records already present in
`n2n-index.csv`. Sort eligible records with historical annotations first, then by
ascending lexical lowercase post ID within each group. Select the first 1,000.
This prioritizes inspectable existing annotations; it is not a random, chronological,
representative, quality-ranked or evidence-ranked sample. No inference from URL slugs.

The archive contains exactly 7,399 unique N2N records: 3 curated and 7,396 uncurated.
Of these, 1,000 have historical annotations, including all three curated records.
The batch therefore contains 997 annotated and 3 unannotated uncurated records.
It preserves 3,033 source-row references and 2,033 historical annotation values.
There are 6,396 uncurated records outside the batch. Curated metadata remains at 3;
newly curated titles, authors, current flairs and rights determinations remain at zero.

## Representation and provenance

`n2n-metadata-batch-0001.json` stores the selection, exact counts, distribution,
source commit and SHA-256 pins for both CSVs, the parser and the existing loader.
Each item preserves the post ID, first archived canonical URL, all distinct archived
canonical source locations, historical annotations and every original CSV field
value with its CSV record ordinal (header is record 1, not a physical line offset).
The manifest's source path, commit and hash apply to every row reference.
Comma-bearing composite annotations remain intact, never split into current flairs.

Missing title, current flair, author, evidence status and rights status are JSON null;
metadata is empty. Null means uncaptured/unassessed, not clearance or negative evidence.
Existing curated descriptions and placeholder author labels are excluded, not propagated.
A structurally valid archived ID or URL does not verify a live post, ownership,
authorship, public visibility, independent study or evidence status.

## Reproduce and validate

```bash
python tools/stage_n2n_metadata_batch.py --write
python tools/stage_n2n_metadata_batch.py
python -m unittest tests.test_n2n_metadata_batch tests.test_search_reddit_archive tests.test_reddit_corpus_census -v
```

All 15 focused tests passed, including 5 new batch tests. Mutation subtests reject
invented fields, damaged provenance, duplicate/missing/reordered records, every
boundary change and changes to each of the four pinned source files. Validation
rebuilds the entire expected representation and rejects extra or altered fields.
Intentional future enrichment requires a separately reviewed artifact/schema change;
this staging manifest must not silently become a curated-metadata input.

## Follow-up and closed boundaries

Review archived annotations against their original row references first. Further
captured metadata needs an authorized, inspectable source and field-level provenance;
unavailable fields stay uncaptured. This batch does not import the pilot category
assignments, consult later branches, access Reddit or automate future retrieval.
All source bodies, comments and media remain uningested. Live Reddit access is HOLD;
rights, privacy, evidence, publication and promotion gates remain CLOSED. Accepted
canonical edges remain zero and model support remains empty. No website change,
merge, deployment, Big Question maturity update or truth inference is authorized here.
