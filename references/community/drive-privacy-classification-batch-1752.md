# Drive privacy/public-status classification batch — 1,752 objects

Date: 2026-08-29
Scope: nominated Akashic Library Google Drive corpus only

## Purpose

Extend the fail-closed privacy/public-status classification from the complete 1,287-object root-direct layer into a non-overlapping descendant-document block, without promoting shared/access-visible material to public status.

## Denominator

Canonical corpus denominator: **2,144 observed Drive document objects**.

## Previously classified

All 66 root-direct Stage-A sets are covered:

- root-direct classified objects: **1,287**

## New descendant block

This checkpoint adds the exact descendant scope groups `EXPAND-0002` through `EXPAND-0013` from `drive-canonicalisation-screening-expansion-v0.4.7.csv`:

- Philosophy descendants — 43
- Psychology descendants — 8
- Buddhism descendants — 63
- Hinduism descendants — 36
- Yoga descendants — 17
- Metaphysics descendants — 7
- Grimoire descendants — 5
- World History descendants — 18
- Native America descendants — 4
- Ancient Religions descendants — 131
- Biographies descendants — 35
- Literature descendants — 98

Newly classified descendant objects: **465**.

Cumulative classified objects: **1,287 + 465 = 1,752**.

## Conservative classification applied

Every represented object receives the same non-permissive state:

- `scope_status = IN_SCOPE`
- `privacy_risk = UNKNOWN`
- `visibility_status = ACCESS_NOT_VERIFIED`
- `public_manifest_status = REVIEW_REQUIRED`
- `pii_scan_status = NOT_RUN`

No object is promoted to `PUBLIC_VERIFIED` or `ELIGIBLE` by this operation.

## Coverage and score

- classified numerator: **1,752**
- denominator: **2,144**
- coverage: **81.716418%**
- privacy/public-status contribution: **8.171642 / 10**

This is classification coverage only. It does not claim public-release clearance, completed PII review, or public-domain/licensing verification.

## Evidence basis

The root-direct denominator is fixed by the 66-root reconciliation at 1,287 direct document objects. The new descendant block is taken from exact Stage-A scope groups EXPAND-0002 through EXPAND-0013, which total 465 non-overlapping descendant document objects.