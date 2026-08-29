# AkashicNET Drive privacy/public-status denominator

Status: active scoring denominator
Scope: nominated Akashic Library Drive tree only
Date: 2026-08-29

## Purpose

The 10-point privacy/public-status component must not be inferred from the fact that a Drive item is shared or accessible. Shared access is not equivalent to public visibility.

The canonical live denominator is now **2,459 unique non-folder Drive objects**, established by the pagination-complete recursive provider crawl in GitHub Actions run `33247025163`.

The earlier 2,144-object denominator is superseded. It was incomplete because historical provider pages had been treated as exhaustive in some high-volume folders; the live recursive crawl exposed additional objects and folders, including Buddhism, Metaphysics and Occultism.

Technical artefacts remain in the privacy/audit denominator until dispositioned because privacy handling is required even for unusable objects.

## Required object-level states

Each object must receive:

- `scope_status`: IN_SCOPE / OUT_OF_SCOPE
- `privacy_risk`: PUBLIC_CANDIDATE / PERSONAL / SENSITIVE_PERSONAL / ADMINISTRATIVE / CORRESPONDENCE / UNKNOWN
- `visibility_status`: PUBLIC_VERIFIED / ACCESS_NOT_VERIFIED / PRIVATE_OR_RESTRICTED / UNKNOWN
- `public_manifest_status`: ELIGIBLE / EXCLUDED / QUARANTINED / REVIEW_REQUIRED
- `pii_scan_status`: NOT_RUN / PASS / REVIEW_REQUIRED / FAIL

## Scoring denominator

Privacy/public-status coverage is measured object-by-object across **2,459 unique live Drive objects**.

An object counts as privacy-classified only when it has an explicit privacy-risk state and manifest disposition. `ACCESS_NOT_VERIFIED` must never be silently promoted to `PUBLIC_VERIFIED`.

Exact-set compressed ledgers are permitted when all members are deterministically defined by a persisted complete provider crawl or provider-page screening batch. The assigned privacy states apply to every object in that exact set; compressed representation does not change the object-level denominator.

Privacy component points are proportional to classified-object coverage:

`privacy_points = 10 × classified_objects / 2,459`

capped at 10 points.

Public-manifest eligibility requires independently established public-source or equivalent public-verification evidence. Relevance does not grant permission to ingest or publish.

## Current classified numerator

The v0.5.0 full-corpus rescreen applies conservative fail-closed states to the exact live provider set from run `33247025163`:

**2,459 / 2,459 = 100% classified**.

All objects are deliberately held at:

- `scope_status = IN_SCOPE`
- `privacy_risk = UNKNOWN`
- `visibility_status = ACCESS_NOT_VERIFIED`
- `public_manifest_status = REVIEW_REQUIRED`
- `pii_scan_status = NOT_RUN`

No object is promoted to public visibility or public-manifest eligibility by this classification.

Privacy/public-status contribution = **10 / 10 points**.

## Safety rule

Potentially personal, medical, administrative, diary-like, correspondence or otherwise sensitive material must remain outside the public manifest and outside public embeddings until explicitly cleared. Private/quarantined records should be represented in a non-public audit layer with minimised identifiers.

## Reconciliation note

This file uses the same live physical-object denominator as `drive-live-full-census-checkpoint-v0.5.0.md`: **2,459 objects**. Privacy classification credit represents explicit conservative disposition only; it is not public-release clearance.
