# Historical Reddit Corpus Provenance Audit v0.7

## Scope

This audit examines the historical N2N ingestion machinery at commit `5dc2700c182a489a8488414d863b69ee142178f2`, following the v0.6 corroboration audit.

The purpose is narrow: determine whether repository evidence proves that the 972 consecutive-ID records flagged by the v0.2 heuristic were generated placeholders, rather than merely suspicious provenance patterns.

## Sources inspected

- `tools/n2n/ingest_n2n.py`
- `references/community/N2N_INGESTION_ARCHITECTURE.md`
- `references/community/n2n-pilot-index.csv`
- `tools/n2n/dryrun/25_post_test.jsonl`
- `references/community/reddit-semantic-index.csv` (path/blob identified; content was not usable through the repository connector during this audit)
- commit history immediately preceding and including `af0555d26abcd90d1dac685f67290cfdd772d1f9`
- repository searches for early suspicious IDs and generation-related terms

## Findings

### 1. The ingestion script does not generate Reddit post IDs

`tools/n2n/ingest_n2n.py` reads candidate rows from an existing CSV. `extract_post_id()` extracts an ID already present in a Reddit URL using `/comments/([A-Za-z0-9]+)`. The script does not contain base-36 increment logic, sequential-ID generation, placeholder-ID construction, or synthetic URL generation.

`pick_batch()` selects rows already present in the source CSV. `canonicalize_record()` normalises fields and derives the post ID from the supplied URL; it does not invent an ID.

**Conclusion:** this script is not evidence that the suspicious consecutive IDs were generated.

### 2. The dry-run explicitly operated without live Reddit verification

The script records `api_blocked = True`, labels processed records `dry_run_processed`, and states that public Reddit access was blocked with HTTP 403. Its summary says the prototype used a curated record set rather than direct live scraping.

The historical dry-run JSONL likewise contains `api_access_state: Public Reddit access blocked in this environment (HTTP 403)` and `import_mode: dry_run`.

**Conclusion:** dry-run processing proves that a row could pass through the prototype without the corresponding Reddit post being independently retrieved or verified.

### 3. The pilot CSV is an input dataset, not proof of source existence

`n2n-pilot-index.csv` already contains post IDs, canonical-looking URLs, titles, summaries, framework labels and research questions before the ingestion script processes them. The inspected ingestion code does not document how those rows were originally produced.

Several pilot records use `date=unknown`, while attribution is represented generically as `Original poster as listed on Reddit`. This is compatible with a curated metadata seed but does not independently establish that every URL was retrieved from Reddit.

**Conclusion:** provenance of the pilot rows remains upstream and unresolved.

### 4. The architecture document required a constrained, reviewed pilot

`N2N_INGESTION_ARCHITECTURE.md` says the canonical source should remain Reddit, large-scale extraction should not begin before review, and the next permitted phase should be a constrained curated pilot. It also requires documented API access, retrieval timestamps/status and provenance tracking for production ingestion.

**Conclusion:** the architecture describes intended safeguards; it is not evidence that the historical 9,401-row URI archive was API-derived or externally verified.

### 5. No inspected code proves placeholder generation

No inspected source contains a generator that produces the historical `1000...` ID sequences or formulaic URL/title families. Therefore the current evidence does **not** justify reclassifying the 972 records as `generated_placeholder`.

The appropriate classification remains `suspicious_pattern` / sequential-ID provenance anomaly until a generating source, commit, script or other direct provenance evidence is found.

### 6. The 9,401-row URI archive entered GitHub as a single externally assembled artefact

Commit `af0555d26abcd90d1dac685f67290cfdd772d1f9` added `references/community/reddit-uri-index.csv` in one operation: 9,402 lines were added and none deleted. Its immediate parent does not contain an earlier version of this dataset. Repository and commit searches did not locate an earlier generator, fixture, placeholder script, or staged expansion explaining the `1000...` sequences.

**Conclusion:** the construction method of the 9,401-row historical URI archive is undocumented in the repository. Its corpus-level provenance state is therefore `origin_unresolved`.

`origin_unresolved` is not a claim that records are false. It means the repository does not currently contain sufficient evidence to reconstruct how the bulk artefact was assembled.

## Evidence-state decision

Do **not** promote the 972 sequence anomalies to proven generated placeholders.

Current defensible ladder remains:

`9,401 historical URI rows -> 7,356 structurally unique candidates -> 972 suspicious sequential-ID provenance anomalies -> 6,384 candidates after the sequence filter -> 32 independently corroborated by the v0.6 public-web seed -> 6,352 not yet corroborated by that seed.`

The historical bulk artefact as a whole carries `origin_unresolved` until its pre-Git construction provenance is recovered.

`uncorroborated` does not mean nonexistent. `suspicious_pattern` does not mean fabricated. `origin_unresolved` does not mean synthetic.

## Provenance-state model

The historical ingestion prototype can transform pre-existing curated CSV rows into `dry_run_processed` records while live Reddit access is blocked. Consequently, `dry_run_processed` must never be interpreted as `source_verified` or `reddit_verified`.

Recommended state separation:

- `origin_unresolved`: construction provenance of the source artefact cannot currently be reconstructed from repository evidence.
- `structural_candidate`: syntactically valid Reddit post URL/ID.
- `suspicious_pattern`: structural candidate carrying a provenance anomaly.
- `corroborated`: matched to independent public-web evidence.
- `api_verified`: reserved for a successful authorised Reddit API retrieval.
- `generated_placeholder`: reserved for records whose generation is directly demonstrated by provenance evidence.

## Next phase

Because repository history does not currently expose the pre-Git construction source, further historical classification should remain conservative. The productive next phase is to expand independent public-web corroboration of the filtered candidate corpus while retaining the unresolved-origin flag, and later use authorised Reddit API retrieval to promote accessible records to `api_verified`.

If an external/local generation source is recovered later, it can be audited separately and exact proven ranges can then be reclassified without rewriting the current evidence history.
