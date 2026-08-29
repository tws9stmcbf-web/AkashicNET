# AkashicNET live Drive census checkpoint v0.5.0

Date: 2026-08-29
Scope: AKASHICNET-004 nominated Akashic Library Drive corpus
Supersedes: the earlier 195-folder / 2,144-object census model.

## Provider execution

GitHub Actions run `33247025163` executed `scripts/drive_full_census.py` using read-only Google Drive OAuth access.

Result:

- roots: **66**
- unique folder IDs: **199**
- folder occurrences: **199**
- unique non-folder object IDs: **2,459**
- non-folder object occurrences: **2,459**
- folder errors: **0**
- all pagination chains exhausted: **true**
- execution status: **PASS**

The crawl starts from the 66 nominated top-level roots, follows every discovered child folder recursively, follows every Google Drive `nextPageToken`, and records each discovered object by provider Drive ID.

## Correction to previous denominator

The previous 2,144-object denominator was incomplete. A live pagination-complete audit exposed capped historical counts, including:

- Buddhism: historical direct count 100; live audit 357 direct objects plus additional child-folder structure.
- Metaphysics: historical direct count 100; live audit 127 direct objects.
- Occultism: historical child-folder count 0; live audit 3 child folders.

The 2,144 denominator must therefore not be used for current completion scoring.

## Full Stage-A rescreen

The live object manifest is used as an exact provider-defined set of **2,459 unique non-folder objects**.

Every object receives a metadata-screen state:

- `SCREENED`
- `REVIEW_REQUIRED` by default
- `TECHNICAL_EXCLUSION` when a deterministic technical rule applies

This is Stage-A screening coverage, not canonical-work resolution and not a byte-identity assertion.

Technical exclusions found by deterministic metadata rules:

- zero-byte objects: **16**
- `.DS_Store`: **11**
- `.crdownload`: **1**
- total technical exclusions: **28**

## Duplicate-integrity rescreen

Exact `name + size` grouping over the full live object set yields:

- candidate families with more than one manifestation: **127**
- objects participating in those candidate families: **269**

These remain candidates only. No byte identity is asserted without hashing; no edition, translation, work-family or manifestation is collapsed automatically.

## Privacy/public-status rescreen

All **2,459 / 2,459** live objects are explicitly assigned the conservative fail-closed state:

- `scope_status = IN_SCOPE`
- `privacy_risk = UNKNOWN`
- `visibility_status = ACCESS_NOT_VERIFIED`
- `public_manifest_status = REVIEW_REQUIRED`
- `pii_scan_status = NOT_RUN`

This is classification coverage only. It grants **zero** public-release permission.

## Provenance

Each object retains:

- root title
- parent collection path
- parent Drive ID
- object Drive ID
- filename
- MIME type
- size
- created time
- modified time

Folder-level provenance and pagination evidence are persisted separately in `drive-live-full-folder-census.csv`.

## Integrity rule

`archive inclusion ≠ endorsement; semantic connection ≠ scientific evidence; provenance is not evidence`.
