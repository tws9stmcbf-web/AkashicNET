# AkashicNET Drive privacy/public-status denominator

Status: active scoring denominator
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Purpose

The 10-point privacy/public-status component must not be inferred from the fact that a Drive item is shared or accessible. Shared access is not equivalent to public visibility.

The canonical object denominator is the corrected **2,144 observed Drive document objects** established by the v0.4.8 canonicalisation checkpoint. The earlier 2,152 denominator double-counted eight objects under `PDF/Montalk/Not Important` by counting them once at the Montalk parent and again in the child folder. Technical exclusions remain in the audit denominator until they are explicitly dispositioned because privacy handling is required even for unusable artefacts.

## Required object-level states

Each document object must eventually receive:

- `scope_status`: IN_SCOPE / OUT_OF_SCOPE
- `privacy_risk`: PUBLIC_CANDIDATE / PERSONAL / SENSITIVE_PERSONAL / ADMINISTRATIVE / CORRESPONDENCE / UNKNOWN
- `visibility_status`: PUBLIC_VERIFIED / ACCESS_NOT_VERIFIED / PRIVATE_OR_RESTRICTED / UNKNOWN
- `public_manifest_status`: ELIGIBLE / EXCLUDED / QUARANTINED / REVIEW_REQUIRED
- `pii_scan_status`: NOT_RUN / PASS / REVIEW_REQUIRED / FAIL

## Scoring denominator

Privacy/public-status coverage is measured object-by-object across **2,144 observed document objects**.

An object counts as privacy-classified only when it has an explicit privacy-risk state and manifest disposition. `ACCESS_NOT_VERIFIED` must never be silently promoted to `PUBLIC_VERIFIED`.

Exact-set compressed ledgers are permitted when all members are deterministically defined by a persisted complete provider-page screening batch. The assigned privacy states apply to every document object in that exact set; the compressed representation does not change the object-level denominator.

Privacy component points are proportional to classified-object coverage:

`privacy_points = 10 × classified_objects / 2,144`

capped at 10 points.

Public-manifest eligibility requires an independently established public source or equivalent public-verification evidence. Relevance does not grant permission to ingest or publish.

## Safety rule

Potentially personal, medical, administrative, diary-like, correspondence or otherwise sensitive material must remain outside the public manifest and outside public embeddings until explicitly cleared. Private/quarantined records should be represented in a non-public audit layer with minimised identifiers.

## Current classified numerator

`drive-privacy-classification-batch-v0.4.9.csv` applies conservative metadata-only states to five exact complete root-direct provider sets:

- Buddhism: 100
- Hinduism: 96
- Metaphysics: 100
- Philosophy: 86
- PDF: 78

Total explicitly classified objects: **460 / 2,144 = 21.455224%**.

All 460 are deliberately held at:

- `privacy_risk = UNKNOWN`
- `visibility_status = ACCESS_NOT_VERIFIED`
- `public_manifest_status = REVIEW_REQUIRED`
- `pii_scan_status = NOT_RUN`

No object in this batch is promoted to public visibility or public-manifest eligibility.

Privacy/public-status contribution = **2.145522 / 10 points**.

## Reconciliation note

This file uses the same physical-object denominator as `drive-canonicalisation-checkpoint-v0.4.8.md`: **2,144 objects**. Privacy classification credit represents explicit conservative disposition only; it is not public-release clearance.
