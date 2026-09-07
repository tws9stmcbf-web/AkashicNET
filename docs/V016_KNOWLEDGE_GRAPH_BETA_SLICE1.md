# v0.16 Knowledge Graph Beta — Slice 1

Issue: #277  
Status: review fixture only

## Outcome

This slice establishes the first forward-only v0.16 graph contract without modifying the sealed v0.14 or v0.15 release targets.

The BQ001 fixture contains:

- 6 public-safe typed nodes
- 4 typed relationships
- 2 inferred candidates requiring review
- 1 explicit competing-model candidate
- 1 author-correction relationship preserved as `CORRECTED_NOT_RETRACTED`
- 0 accepted edges
- 1 unresolved question

## Provenance boundary

Every node and edge records its repository source, immutable input digest, JSON record locator, independence key, derivation method, and public-safe status.

Generation is intentionally non-blocking: if a governed source changes but remains structurally readable, the builder can emit a new review-only packet carrying the actual digest. Validation then fails against the immutable audited pin and prevents promotion or readiness until the drift is explicitly reviewed.

## Epistemic boundary

- BQ001 remains `UNRESOLVED` and “Never Final.”
- `INFERRED_CANDIDATE` relationships remain `REVIEW_REQUIRED` and `accepted_edge: false`.
- Direct source metadata is distinguishable from inference.
- Competing models are not votes.
- A correction is not silently converted into a retraction.
- Relevance, repetition, connectivity, and retrieval rank do not upgrade truth or evidence class.
- Automated truth inference, acceptance, scientific-evidence promotion, rights promotion, canonical-identity promotion, and circular confidence remain OFF.

## Verification

`.github/workflows/validate-knowledge-graph-beta-v016.yml` reproduces the committed fixture, validates source pins and JSON locators, checks referential integrity and ancestry, runs fail-closed mutation tests, compiles the governed Python, and parses both JSON artifacts.

This slice is not a complete v0.16 readiness declaration. Scaling, richer retrieval, visualization, and broader graph coverage remain non-blocking future work.
