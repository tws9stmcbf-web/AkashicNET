# AKASHICNET-006 — Rights Audit Evidence Standard v0.2

Date: 2026-08-29

## Decision

Do not promote a Drive object to `PUBLIC_VERIFIED` from author death date, title age, filename, folder membership, or search-engine discovery alone.

## Evidence ladder

R0 — Drive provenance only.

R1 — Work-level historical/public-domain candidate.

R2 — Exact manifestation identified: title, author/translator/editor, publication year/edition and source record align.

R3 — Authoritative rights evidence supports the identified manifestation in the intended jurisdiction.

R4 — Independent corroboration or explicit licence/permission plus jurisdiction and access date are recorded.

Only R4 may be promoted to `PUBLIC_VERIFIED` for redistribution.

## Current authoritative guidance

Project Gutenberg states that works published in 1930 or earlier generally have no US copyright restrictions under its Rule 1, but also warns that each edition may have its own copyright restriction and every translation has independent copyright. Source: Project Gutenberg Copyright How-To, accessed 2026-08-29.

Project Gutenberg also states that its eBooks are generally public-domain in the United States, while users outside the US must check the law of their own country. Source: Project Gutenberg License and Terms/Permission guidance, accessed 2026-08-29.

The US Copyright Office Circular 15A states that works published in the United States before January 1, 1931 are in the public domain under the applicable historical term rules. This is US-specific and does not itself clear a later translation or edition.

## Implication for AkashicNET

A historical work may be eligible while the exact PDF in Drive is not cleared. Conversely, a permissively licensed modern edition can be cleared even though its underlying work is old. The rights ledger therefore records rights at manifestation level and keeps the original Drive object as provenance.

## Public-manifest gate

`PUBLIC_VERIFIED` requires:

1. Exact manifestation identity.
2. Rights basis.
3. Jurisdiction.
4. Evidence source and retrieval/access date.
5. Evidence strength R4.
6. No conflicting rights evidence.

If any element is missing, status remains `UNKNOWN_UNVERIFIED` or another restrictive state.

## Important separation

Copyright clearance does not imply scientific validity. A work can be public-domain and still contain unsupported, historical, religious, occult, pseudoscientific or otherwise contested claims. AkashicNET maintains independent `rights_status`, `provenance_status`, and `evidence_status` fields.
