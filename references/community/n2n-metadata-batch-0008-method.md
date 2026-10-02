# Final N2N Staging Batch 0008

Source boundary: PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.
Take the final 396 eligible records at ranks 7,001–7,396 in the established
ordering. Validate and exclude the 7,000 IDs in earlier batches. Selection remains
uncurated records, historical annotations first, then lexical lowercase post ID.
All earlier staging manifests and the separate 50-record receipt pilot are unchanged.

The completed structural queue contains 7,396 unique records, with zero duplicate
or missing eligible IDs. Together with the three excluded curated records it
exactly covers all 7,399 unique pinned archive IDs. No uncurated records remain
outside the queue. Batch 0008 preserves 396 source-row references and no captured
historical annotations. IDs, archived URLs, original CSV values and ordinals remain
traceable; predecessor hashes retain the complete batch chain.

Completion means queue coverage, not completed enrichment or verified post existence.
Curated metadata remains three, new curated records zero. Missing title, author,
current flair, evidence and rights stay null. Unresolved historical archive
provenance remains a limitation. No title inference or source-body/comment/media
capture. Reddit access HOLD; all rights, privacy, evidence, publication and promotion
gates CLOSED; accepted edges zero and model support empty. No merge, deployment,
canonical metadata write, website change or maturity promotion.

Generate with `python tools/stage_n2n_metadata_batch.py --batch 8 --write`;
validate by omitting `--write`. Only the eight reviewed batches are enabled; there
is no automatic ninth batch. Tests check archive-set equality, exact final selection,
7,396-ID uniqueness, prior-chain reproduction, every raw source-row reference,
null fields, missing prior data, overlap mutation and invalid batch-number rejection.
Receipts: `n2n-batch-0001-research/ara/evidence/batch-0008-validation.txt` and
`n2n-batch-0001-research/ara/evidence/batch-0008-counts.json`.
