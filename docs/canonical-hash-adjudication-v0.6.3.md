# Canonical hash adjudication v0.6.3

Date: 2026-08-30
Status: sanitised public checkpoint

## Security boundary

This document intentionally contains no Google Drive IDs, provider URLs, private filenames, private folder paths, timestamps, file-linked hashes or raw canonicalisation ledgers. Those values are private by default under `SECURITY.md`.

## Verified private-runtime result

The first priority hash wave covered six three-member candidate families, for 18 physical objects in total.

All six families produced complete three-way SHA-256 agreement when raw bytes were obtained through the authorised connected Drive runtime.

Public aggregate result:

- families tested: **6**
- physical objects hashed: **18**
- complete family hash matches: **6 / 6**
- byte-identical family determinations: **6**
- hash mismatches: **0**
- canonical work IDs promoted from this wave: **0**
- edition IDs promoted from this wave: **0**
- rights states promoted: **0**
- scientific-evidence states promoted: **0**

## Interpretation

Matching SHA-256 establishes byte identity only for the privately recorded manifestations in each family. It does not establish canonical work identity, edition identity, public-release rights, endorsement, scientific truth or evidential quality.

Each family therefore advances from metadata-only duplicate candidacy to privately verified byte-copy identity while canonical work resolution remains `HOLD` pending independent adjudication.

## Next step

Continue the private hash queue in deterministic priority order. Public repository updates should remain aggregate/sanitised unless a source independently clears the repository's public-release gates.
