# Canonical hash adjudication v0.6.4

Date: 2026-08-30
Status: sanitised public checkpoint

## Security boundary

Private corpus identifiers, filenames, folder paths, timestamps and file-linked digests remain outside the public repository under `SECURITY.md` and `.gitignore`.

## Verified private-runtime result

The first low-cost P1 tranche processed the next ten deterministic two-member candidate families through authorised connected-Drive raw downloads and SHA-256 comparison.

Public aggregate result:

- families tested: **10**
- physical objects hashed: **20**
- bytes hashed: **2,522,992**
- complete family hash matches: **10 / 10**
- byte-identical family determinations: **10**
- hash mismatches: **0**
- canonical work IDs promoted from this tranche: **0**
- edition IDs promoted from this tranche: **0**
- rights states promoted: **0**
- scientific-evidence states promoted: **0**

Combined with v0.6.3, the private runtime has now hash-verified **16 candidate families / 38 physical objects** with complete within-family SHA-256 agreement in every processed family.

## Interpretation

Matching SHA-256 establishes byte identity only for the compared physical manifestations. It does not establish canonical work identity, edition identity, public-release rights, endorsement, scientific truth or evidential quality.

The ten families therefore move from metadata-only duplicate candidacy to privately verified byte-copy identity while work resolution remains `HOLD` pending independent adjudication.

## Remaining queue

The original non-technical review queue contained 126 families. Six P0 families and ten P1 families have now received byte-level verification, leaving **110 families** without byte-level adjudication.

The next private-runtime step is the next deterministic low-cost P1 tranche. Public repository updates remain aggregate and sanitised unless an individual source independently clears the public-release gates.
