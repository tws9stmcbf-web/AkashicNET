# AKASHICNET-007 — Evidence / Provenance Scoring v0.1

Date: 2026-08-29
Status: PRE-ALPHA scoring specification

## Scope
This score measures confidence in a canonical/provenance relationship derived from the existing metadata-only reconciliation layer. It does **not** measure whether a work's claims are true, scientifically valid, spiritually valid, safe, or legally redistributable.

Rights remain independent. No score in this layer may promote an object to `PUBLIC_VERIFIED`. No score in this layer may promote a claim or source to scientific-evidence status.

## Score components
Maximum raw score: 100.

### Reconciliation status (max 40)
- `STAGE_B_ADVANCED`: 40
- `REVIEWED_RETAINED`: 30
- `REVIEW_REQUIRED`: 15
- `UNRESOLVED_PROVENANCE`: 10

### Confidence label (max 40)
- `HIGH`: 40
- `MEDIUM_HIGH`: 30
- `MEDIUM`: 20
- other/unknown: 10

### Evidence basis (max 20)
- Stage-B batch evidence: 20
- title + size evidence: 15
- canonicalisation candidate ledger / metadata normalisation: 10
- other metadata-only basis: 5

## Hard uncertainty caps
- `UNRESOLVED_PROVENANCE`: score cannot exceed 45
- `REVIEW_REQUIRED`: score cannot exceed 55

These caps are intentional. A numerical score must never make an unresolved relationship appear settled.

## Evidence tiers
- 85–100: `E3_STRONG_METADATA_RELATIONSHIP`
- 70–84: `E2_REVIEWED_METADATA_RELATIONSHIP`
- 50–69: `E1_PROVISIONAL_METADATA_RELATIONSHIP`
- 0–49: `E0_UNRESOLVED_OR_WEAK`

Even E3 is still metadata-level evidence unless stronger evidence such as hashes, bibliographic sources, or content-level citations is explicitly added later.

## Invariants
1. Every scored relationship retains its evidence basis and source ledger.
2. Hash identity is never inferred from equal filename/title/size alone.
3. Rights status remains independent and unchanged.
4. Scientific/epistemic truth is not inferred from catalogue membership or canonical confidence.
5. Scientific-evidence status is never promoted from provenance or canonical-confidence scoring alone.
6. Unresolved and review-required states remain visible in machine-readable output.
