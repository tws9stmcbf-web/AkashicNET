# Reddit JSONL metadata audit — v0.7.12

## Scope

This checkpoint audits the first available 25-record Reddit JSONL metadata batch at `tools/n2n/dryrun/25_post_test.jsonl`.

Only explicit structured fields are inspected. Titles, URL slugs, summaries, research questions, toolkit frameworks, and semantic similarity are excluded from topic discovery.

## Results

- 25 records and 25 unique Reddit post IDs.
- 12 normalized project category values.
- No `topic`, `flair`, `link_flair_text`, or `link_flair_template_id` field.
- The JSONL Reddit URL set exactly matches the previously audited `n2n-test-batch-25.csv`.
- Every record declares `import_mode: dry_run`.

The JSONL category labels are therefore transformed project metadata in an existing lineage, not Reddit-native flair evidence. They cannot be double-counted as an independent source.

## Census decision

No new top-level topic is promoted. The audited public-safe count remains **73**.

This is a metadata and lineage determination only. It does not establish truth, rights clearance, or scientific evidence status.
