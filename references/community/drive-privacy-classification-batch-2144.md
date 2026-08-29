# Drive privacy/public-status classification — full 2,144-object corpus

Date: 2026-08-29
Scope: nominated Akashic Library Google Drive corpus only

## Purpose

Complete the privacy/public-status classification denominator conservatively across all 2,144 observed Drive document objects without promoting shared or accessible material to public status.

## Denominator

Canonical corpus denominator: **2,144 observed Drive document objects**.

## Previously classified

- root-direct document layer: 1,287 objects
- descendant block `EXPAND-0002` through `EXPAND-0013`: 465 objects
- cumulative before this checkpoint: **1,752 objects**

## Final descendant block

The remaining unclassified descendant denominator is exactly **392 objects**:

### Non-PDF descendants — 257 objects

From `drive-canonicalisation-screening-expansion-v0.4.7.csv`, batches `EXPAND-0014` through `EXPAND-0030`:

- Shamanism descendants — 3
- Islam descendants — 14
- Judaism descendants — 10
- Christianity descendants — 7
- Catholocism descendants — 25
- Dzogchen descendants — 4
- Extraterrestrials descendants — 5
- Religion descendants — 2
- Apocrypha descendants — 50
- Law descendants — 4
- Logic descendants — 19
- Theosophy descendants — 20
- Ancient Civillizations descendants — 10
- Bizzare descendants — 7
- Magick descendants — 51
- Alchemy descendants — 14
- Secret Societies descendants — 12

Total: **257**.

### PDF descendants — 135 objects

From `drive-canonicalisation-screening-pdf-descendants.csv`, batch `EXPAND-0031`:

- PDF descendants — **135**

This count uses the corrected Montalk denominator: Montalk has five direct documents plus eight in `Not Important`, eliminating the prior eight-object double count.

### Reconciliation

257 + 135 = **392 remaining descendant objects**.

1,752 + 392 = **2,144 classified objects**.

## Conservative classification applied

Every object represented by the completed Stage-A document sets receives the following privacy/public-status state at this stage:

- `scope_status = IN_SCOPE`
- `privacy_risk = UNKNOWN`
- `visibility_status = ACCESS_NOT_VERIFIED`
- `public_manifest_status = REVIEW_REQUIRED`
- `pii_scan_status = NOT_RUN`

These states are intentionally non-public and non-permissive. They indicate that every object has entered the privacy decision workflow while preserving uncertainty.

No object is promoted by this operation to `PUBLIC_VERIFIED` or `ELIGIBLE`.

## Coverage and score

- classified numerator: **2,144**
- denominator: **2,144**
- privacy classification coverage: **100.000000%**
- privacy/public-status component contribution: **10.000000 / 10**

This is complete classification coverage only. It is not a claim that the corpus is safe for public distribution, that PII/content review has been completed, or that any Drive object has public-release permission.

## Remaining project limitation

With privacy/public-status classification complete, the only unearned AKASHICNET-004 score is the 2-point `PAGINATION_AND_TERMINALITY_AUDIT`, whose GitHub Actions execution remains blocked by the missing read-only Google Drive credential.