# Drive privacy/public-status classification batch — 1,287 root-direct objects

Date: 2026-08-29
Scope: nominated Akashic Library Google Drive corpus only

## Purpose

Extend conservative privacy/public-status classification to the complete root-direct document layer without promoting shared/access-visible Drive material to public status.

## Evidence basis

`drive-canonicalisation-root-screening-reconciliation.md` establishes the authoritative root-direct denominator:

- 66 top-level roots
- 1,287 direct document objects
- all 66 roots completed Stage-A metadata screening
- root census is authoritative for direct-document counts

The previous privacy checkpoint classified 928 of these root-direct objects. This batch extends the same conservative privacy decision state to the remaining root-direct objects, bringing cumulative root-direct privacy classification to **1,287 objects**.

## Conservative classification applied

Every root-direct document object receives:

- `scope_status = IN_SCOPE`
- `privacy_risk = UNKNOWN`
- `visibility_status = ACCESS_NOT_VERIFIED`
- `public_manifest_status = REVIEW_REQUIRED`
- `pii_scan_status = NOT_RUN`

No object is promoted to `PUBLIC_VERIFIED` or `ELIGIBLE`. Shared/access-visible state remains insufficient for public permission.

## Coverage and score

Canonical corpus denominator: **2,144 observed Drive document objects**.

- classified numerator: **1,287**
- denominator: **2,144**
- privacy/public-status coverage: **60.027985%**
- privacy/public-status component contribution: **6.002799 / 10**

This is workflow classification coverage only. It is not public-release clearance and does not claim PII/content review has been completed.

## Reconciliation

The root census, not naive historical batch-row arithmetic, controls the numerator. This preserves the corrected Shamanism direct-document count and avoids historical shorthand discrepancies.
