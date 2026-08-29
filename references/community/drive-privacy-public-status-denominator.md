# AkashicNET Drive privacy/public-status denominator

Status: denominator definition only — no completion points awarded
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

Public-manifest eligibility requires an independently established public source or equivalent public-verification evidence. Relevance does not grant permission to ingest or publish.

## Safety rule

Potentially personal, medical, administrative, diary-like, correspondence or otherwise sensitive material must remain outside the public manifest and outside public embeddings until explicitly cleared. Private/quarantined records should be represented in a non-public audit layer with minimised identifiers.

## Current score

0 / 10 points remain awarded until an object-level privacy ledger with a defensible numerator exists.

## Reconciliation note

This file now uses the same physical-object denominator as `drive-canonicalisation-checkpoint-v0.4.8.md`: **2,144 objects**. This correction changes the denominator only; it does not award privacy/public-status points.
