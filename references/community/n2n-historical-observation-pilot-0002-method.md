# Historical Observation Pilot: Second 25

Continue the separate provenance overlay, not the 1,000-record staging series.
Select eligible historical feed IDs at lexical ranks 26–50, excluding the first
validated 25. Same PR #376 source boundary, dated manual delta CSV receipts and
source hashes. The first pilot and all five staging manifests remain unchanged.

Result: 25 additional records, 50 cumulative unique receipt-backed records, zero
overlap, 75 eligible historical-feed candidates remaining. Staging remains 5,000;
curated remains three; new titles, authorship and current verifications remain zero.
The receipts record past repository observations, not fresh independent verification.
Their original CSV row values, dates, URLs and ordinals are preserved. Missing title,
author, current flair, evidence status and rights status stay null.

Run `python tools/build_n2n_provenance_pilot.py --batch 2 --write` to reproduce;
omit `--write` to validate. The previous pilot is validated and linked by SHA-256.
Focused tests cover reproduction, prior-pilot dependency, 50-ID uniqueness, overlap
rejection, current-verification rejection and retained first-pilot protections.
Validation receipt: `n2n-batch-0001-research/ara/evidence/provenance-pilot-0002-validation.txt`.

Live Reddit access remains HOLD. All rights, privacy, evidence, publication and
promotion gates remain CLOSED. No title inference, source-body/comment/media
capture, canonical metadata writes, search integration, merge or deployment.
Source snapshots with field-level receipts are still needed for descriptive enrichment.
