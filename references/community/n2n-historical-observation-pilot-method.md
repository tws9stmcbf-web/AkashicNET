# N2N Historical Observation Pilot

This is a 25-record provenance review overlay, separate from the five staging
batches. The source boundary remains PR #376 at
`808564658800a1ab230bbb837aa3b228911d671f`. No live Reddit access occurred.

## Why this step

The pinned `REDDIT_HISTORICAL_PROVENANCE_AUDIT_V0.7.md` reports unresolved upstream
provenance for the pilot CSV and historical bulk archive. Its 972 sequential-ID
anomalies are suspicious patterns, not proof of fabrication. Accordingly, the
5,000 queued records are archived structural candidates, not 5,000 independently
verified posts. Do not transfer the larger pilot's titles, summaries, generic author
placeholders or project classifications into curated metadata as observed facts.

The five dated manual feed-observation files (0002–0006) contain 125 distinct N2N
IDs matching uncurated records in the pinned archive. None overlap the first five
staging batches. Those receipts record observations on 2026-09-01; their status
strings must stay inside historical-observation objects, never become current
verification. Their existence in the repository is inspectable provenance, not a
new independent verification of the observations themselves.

## Deterministic pilot and result

Choose the first 25 matching IDs in lexical lowercase order. Copy every selected
receipt as an explicitly historical observation, preserving source path, CSV record
ordinal, observation date, URL, source label and original status fields. Pin all
input bytes with SHA-256. The preceding archive/parser/loader pins are checked by
the first-batch generator. Original inputs remain unchanged.

Results: 25 records with inspectable historical observation provenance; zero new
titles, authorship verifications or current Reddit requests. The staging queue
remains 5,000; this overlay is not another 25 queued records and does not change
its 2,396-record remainder. Curated metadata stays at three. Rights, privacy,
evidence, publication and promotion gates remain CLOSED; Reddit access HOLD.
No canonical metadata write, search integration, source-body/comment/media ingestion,
merge, deployment, website update or evidence/maturity promotion.

Generate: `python tools/build_n2n_provenance_pilot.py --write`.
Validate: omit `--write`. Tests: `python -m unittest tests.test_n2n_provenance_pilot -v`.
The tests verify all 25 receipt mappings and reject source drift, invented titles,
changed dates, present-day verification claims, canonical writes and gate changes.

## What unlocks descriptive enrichment

A title or author needs an authorized source snapshot/export or an existing explicit
field-level retrieval receipt for that post ID. For these 25 records, the inspected
feed CSVs provide no such fields. Keep them uncaptured until that source exists.
Live collection remains outside this task while Reddit access is HOLD. No larger
pilot field may substitute for the missing receipt merely because it looks plausible.
