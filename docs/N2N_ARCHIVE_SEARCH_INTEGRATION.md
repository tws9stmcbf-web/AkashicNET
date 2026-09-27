# N2N archive search integration

The community search previously queried three enriched rows only. It now reads the existing archived URI collection through the established annotation-aware parser, selects r/NeuronsToNirvana, deduplicates by post ID, and overlays curated metadata for matching IDs.

The checked-in archive yields 7,399 unique N2N source records, including three enriched records. This remains an archive denominator, not a live total or a claim that every source body has been read. Historical annotation strings are searchable, but are not asserted to be current post flairs. Missing titles remain explicitly uncaptured; URL slugs are not promoted to titles.

Usage from the repository:

```
python tools/search_reddit.py HOMESENSE
python tools/search_reddit.py consciousness --json -n 50
python tools/search_reddit.py --json -n 7399
```

No query returns all matches beyond the supplied limit; the JSON response reports total archive, matching and returned counts separately. The last command returns all existing structural N2N records, without network access or additional content ingestion. The command also works when launched by absolute path outside the repository directory.

The 7,399-record count establishes structural archive coverage only. No durable, inspectable owner attestation covering all these records is cited here; archive-wide authorship is not established. Curated author fields, where captured, are metadata rather than independent per-post authorship verification or rights clearance for quoted or linked third-party works.

No article bodies, comments or media are copied. No website build, deployment, public manifest, evidence classification, canonical graph edge, supports_models value, Big Question state, release state or promotion gate is changed. Live automated Reddit intake remains HOLD. Presence in the archive or search output does not establish current public visibility or PUBLIC_VERIFIED/ELIGIBLE status; publication requires the existing sensitivity, rights and public-manifest reviews. Results expose source discovery records only; claim_review is NOT_ASSESSED_BY_THIS_TOOL even where curated metadata exists.

Validation: ten archive census/search tests passed locally, including exact 7,399-record coverage, preservation of three enriched records, annotation deduplication, exclusion of other subreddits and malformed hosts, title/annotation search, and text-output regressions for captured annotations and curated fields without invented metadata. CI remains a separate review gate.
