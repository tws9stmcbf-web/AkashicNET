# Offline historical provenance enrichment: final 75

Source boundary: PR #376 at `808564658800a1ab230bbb837aa3b228911d671f`.

This overlay adds receipt linkage for the remaining 75 records in the 125-ID historical feed population. Select lowercase post IDs lexically, ranks 51–125, after validating both prior 25-record overlays. The JSON preserves archive IDs, URLs, source locations and exact historical feed rows with CSV record ordinals. Input SHA-256 pins and prior overlay digests support reproduction.

The feeds are repository-recorded historical observations, not independently verified source snapshots. Status values inside `historical_observation` apply only to the recorded observation. They do not establish current visibility, authenticity, authorship, title, evidence quality or rights. The pinned audit still reports unresolved archive provenance. Unverified pilot CSV titles and summaries are excluded.

Counts: 75 added, 50 previous, 125 cumulative unique receipt-linked IDs, zero overlap and zero remaining candidates in these five feeds. These are existing staged records; no queue entries are added. The full queue remains 7,396 records plus three curated records. The original first-five-manifest checkpoint is explicitly separated from current coverage in the new JSON. Earlier overlays remain byte-for-byte reproducible.

No new curated title, author, current flair, evidence status or rights status is asserted. Live Reddit remains HOLD. No source bodies, comments or media are ingested. All rights, evidence, privacy, publication, promotion and deployment boundaries remain closed. No merge or deployment is authorized.

Reproduce:

```sh
python tools/build_n2n_provenance_pilot.py --batch 3 --write
python -m unittest tests.test_n2n_provenance_pilot tests.test_n2n_provenance_pilot_0002 tests.test_n2n_provenance_completion -v
```

Nine tests cover prior reproduction, exact 125-ID coverage, all 75 new records' raw receipt fidelity and staging membership, unknown fields, and rejection of invented titles, altered gates, overlap and omission. Validation and counts are recorded under `n2n-batch-0001-research/ara/evidence/provenance-completion-*`.

Descriptive enrichment requires attributable source snapshots or field-level retrieval receipts supporting each new value. This operation adds provenance only; it does not resolve that remaining source gap.
