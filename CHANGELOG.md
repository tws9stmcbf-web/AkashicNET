# Changelog

## v0.14.0-beta.1 — Automation & Reproducibility Beta

Sealed: 2026-09-02

v0.14 makes AkashicNET release readiness independently reconstructable from repository state and CI while preserving the evidence, privacy, rights and provenance boundaries inherited from v0.13.

### Added

- Append-only exact-commit release ledger preserving immutable historical release targets.
- Repository-state + CI release-readiness reconstruction without conversational or manual-memory dependencies.
- Deterministic repository-derived source denominator covering **18,490 external HTTP(S) URLs** across the declared public release boundary.
- Machine-readable source-coverage inventory with SHA-256 audit checkpoint.
- Release-wide source-integrity provenance guards preserving original URLs and the rule that unavailable or changed does not mean false.
- Cross-source candidate-separation and anchor-evidence validation in the final release gate.
- One end-to-end v0.14 readiness workflow recursively re-running release-ledger, reconstruction, source coverage, provenance, Big Questions, privacy, immutable-Actions, v0.13 and v0.12 gates.

### Validated release anchors

- **Validated release commit:** `7b6cfd89de570c4b945d574dad570c37825645fe`
- **READY metadata provenance:** `24c7d3d214e31a8de1357edaf02fe191b12872f5`
- **Final seal bookkeeping merge:** `eea1904f86d3ac5e8aec6a67c9a22c30abdb467f`
- **Source inventory checkpoint SHA-256:** `6ea009b4534595f3f486a93fee4c17f23023e941e8faf47bb5c73edde19f9605`

### Release state

**READY / SEALED**

The metadata and seal commits do not retarget the exact validated release commit.

### Invariants preserved

- Truth inference: **OFF**
- Rights promotion: **OFF**
- Scientific-evidence promotion: **OFF**
- Private Drive promotion: **OFF**
- API-unverified Reddit promotion: **OFF**
- Circular confidence amplification: **OFF**
- Forced BQ001 resolution: **OFF**

Source availability, link changes and redirects remain provenance observations rather than truth judgments.

## PRE-ALPHA v0.10 — Evidence-Governed Knowledge Pipeline

Release candidate: 2026-08-30

PRE-ALPHA v0.10 is an integration and governance milestone. It connects canonical adjudication, reference identity, retrieval, ontology and evidence boundaries under deterministic tests while keeping uncertainty and provenance explicit.

### Added

- End-to-end synthetic/public-safe integration gate across ingestion, canonical resolution, WikiSpine/reference resolution, retrieval, graph/ontology candidate handling and evidence classification.
- Fail-closed ontology ↔ canonical/evidence boundary tests.
- Canonical five-label public epistemic taxonomy: **Established Evidence · Interpretation · Lived Experience/Testimony · Hypothesis · Speculation**.
- Repository-wide release audit with deterministic denominator and checkpoint validation.
- Explicit supersession mapping for independently evidenced canonical work-level adjudications.

### Verified state

- Canonical duplicate review: **81 / 126 families adjudicated; 45 unresolved**.
- WikiSpine: **53 unique seeds; 50 high-precision resolutions; 3 pending**.
- Audited public-metadata topic census: **68 unique normalized topics**.
- Broader **300+** topic figure remains an estimate, not an audited exact count.
- Public epistemic taxonomy: **5 canonical labels**.
- Truth inference: **OFF**.
- Rights promotion: **OFF**.
- Scientific-evidence promotion: **OFF**.

### Canonicalisation boundary

SHA-256 equality establishes byte identity only. Hash equality or mismatch does not by itself establish or promote canonical work identity, edition identity, rights/public-release status, truth, scientific-evidence status, safety or efficacy.

Drive rows 82–86 remain blocked until an authoritative private mapping is available. No mapping is guessed. Object-level Drive identifiers and per-object digests remain private.

### Repository visibility

The GitHub repository is a **private engineering workspace** at this release point. Public-facing AkashicNET material is released separately through approved public surfaces. This release does not change repository privacy posture.

### Remaining release gate

- Create the PRE-ALPHA v0.10 tag and GitHub release after this metadata change passes CI and is merged.

## PRE-ALPHA v0.9

The v0.9 checkpoint established conservative relationship adjudication: 9 v0.8 candidates were evaluated as **0 ACCEPT · 1 HOLD · 8 REJECT**, with generic lexical overlap explicitly insufficient for graph promotion. Automated truth inference, rights promotion and scientific-evidence promotion remained off.
