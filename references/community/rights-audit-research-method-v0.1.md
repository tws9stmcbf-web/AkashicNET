# Rights Audit Research Method v0.1

Date: 2026-08-29

## Objective

Identify rights evidence for exact manifestations in the AkashicNET corpus without confusing the status of an underlying historical work with the status of a particular translation, edition, scan, or compilation.

## Evidence levels

`R0` — no rights evidence; provenance only.
`R1` — historical/public-domain candidate, but manifestation not identified sufficiently.
`R2` — authoritative source identifies the exact or sufficiently matching edition as public domain / unrestricted in a specified jurisdiction.
`R3` — explicit licence or documented permission applies to the exact manifestation.
`R4` — independently corroborated rights basis, jurisdiction and manifestation identity; eligible for PUBLIC_VERIFIED subject to final policy checks.

## Rules

1. Work identity and manifestation identity are separate fields.
2. Every translation is treated as potentially independently copyrighted.
3. A later edition can contain new copyrightable authorship even when the underlying work is public domain.
4. Drive accessibility is never rights evidence.
5. Search-engine discovery is never rights evidence.
6. Filename and file-size matches are not licence evidence and do not prove byte identity.
7. Public-domain status is jurisdiction-specific; Germany/EU and US status must not be conflated.
8. Only R4 evidence may promote an object to `PUBLIC_VERIFIED`.
9. When evidence is incomplete, retain `UNKNOWN_UNVERIFIED`.

## Authoritative research anchors

Project Gutenberg states that, in the US, works first published before 1930 can qualify under its 95-year rule as of 2026, while also warning that each edition may have its own copyright period and every translation has independent copyright. It further states that its own eBooks should not be assumed identical to a particular paper edition. Source: Project Gutenberg Copyright How-To and License.

Library of Congress collection-level rights statements can explicitly state that particular digitised items are public domain and free to use/reuse; such statements are useful evidence only when tied to the actual item/manifestation being assessed.

## First research batch

Seven historical candidates were screened: The Talmud – Complete; Black's Law Dictionary; Ante-Nicene Fathers; Nicene and Post-Nicene Fathers; Book of Enoch; Dostoevsky complete works; H. G. Wells complete works.

No candidate was promoted to R4 from work-level metadata alone.

## Next step

For each candidate, identify the exact edition/translation where possible, locate authoritative rights evidence for that manifestation and jurisdiction, and record source URL, access date, evidence text/metadata, jurisdiction and confidence in the rights ledger. Public-manifest promotion remains blocked until R4.
