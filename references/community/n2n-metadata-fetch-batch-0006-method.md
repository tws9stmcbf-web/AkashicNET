# Larger N2N metadata fetch tranche — 2 October 2026

Source boundary: PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`; integrated in PR #393.

Selection: the first 100 uncurated IDs in ascending lexicographic order, excluding 22 prior source-observed IDs and 14 previously failed IDs. The three canonical curated records are excluded. This order is reproducible from the pinned archive and five previous pilot receipts; it is not chronological or representative.

Result: 100 selected, 100 requested through the web reader, 100 `DisabledError` results, zero accessible pages and zero newly captured metadata fields. The selection and per-URL reader reference are in `n2n-metadata-fetch-batch-0006.json`. One preliminary reader probe was outside this selection and is excluded from all batch counts.

Reader access failure does not mean a post was deleted or never existed. URL slugs are not used to infer titles, usernames or flair. Archived URLs, IDs, source locations and historical annotations are retained unchanged. No bodies, comments or media are stored. Rights, evidence, verified authorship and current flair remain unknown.

Cumulative descriptive enrichment remains 22 source-observed records and 66 observed values; canonical curated coverage remains three. The website receives no metadata update from this tranche because no new metadata was captured.

Validation: three focused tests cover the deterministic 100-record selection, exact URL/provenance preservation and zero invented metadata. Run `python tests/test_n2n_metadata_fetch_batch_0006.py` from the repository.

Next meaningful enrichment requires an accessible source: an authorized metadata export or successful reader access for these exact archived URLs. Repeated failures should not be counted as enrichment.
