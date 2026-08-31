# 🕸️ AkashicNET

## Provenance-first living knowledge network · PUBLIC BETA

AkashicNET is an open, provenance-first knowledge network for building an auditable living commons around consciousness, psychedelics, interdisciplinary research, community knowledge, and related cultural archives.

**Current phase: PUBLIC BETA.** The immutable engineering checkpoint immediately preceding this phase is **PRE-ALPHA v0.10 — Evidence-Governed Knowledge Pipeline** (`v0.10.0-prealpha`). Public Beta is a project/deployment phase, not a retroactive rename of that sealed release.

The project now extends beyond collection and search into an **evidence-governed knowledge architecture**. Sources are canonicalised into inspectable records, candidate relationships are scored and adjudicated, and weak similarity is prevented from becoming graph truth by default.

The **Noetic Sciences Toolkit** is the current research and archival toolkit within AkashicNET. It provides the practical infrastructure for provenance, validation, reproducibility, community-source preservation, search, canonicalisation, candidate generation, adjudication, and future graph construction.

## 🔎 Search the Community Archive

The toolkit includes a searchable index of the archived r/NeuronsToNirvana community record.

Search by title, topic, category, author, framework, summary, evidence classification, or URL:

    python tools/search_reddit.py consciousness
    python tools/search_reddit.py Akashic
    python tools/search_reddit.py HOMESENSE

The public-safe canonical archive currently contains **9,401 unique Reddit URLs**.
Private Drive-derived records are intentionally excluded from the public index;
cross-source builds that use them must run inside the private data boundary.

The search tool is read-only: it searches the local public-safe archive and does not make requests to Reddit.

## Current Archive

**9,401 unique canonical Reddit URLs indexed**

Sources currently include:

- `r/NeuronsToNirvana`
- `u/NeuronsToNirvana`
- `r/TribalGathering`

The Reddit URL index is designed to preserve canonical source locations while supporting metadata collection, validation, deduplication, canonicalisation, relationship discovery, and future enrichment.

## Architecture

AkashicNET is being developed as a staged knowledge system:

    Sources
      ↓
    Ingestion
      ↓
    Normalisation + Deduplication
      ↓
    Canonical Nodes
      ↓
    Entities + Concepts
      ↓
    Candidate Relationships
      ↓
    Scoring + Adjudication
      ↓
    Evidence-Governed Knowledge Graph
      ↓
    Search · Compare · Visualise · Human Interpretation

The graph is intended to remain **multidimensional rather than purely hierarchical**. Relationships may connect sources, entities, concepts, frameworks, time periods, and domains across layers while retaining source provenance and adjudication state.

## Evidence Governance

AkashicNET does not promote a relationship merely because two records share words or themes.

Candidate edges pass through an explicit adjudication layer:

- **ACCEPT** — evidence is strong enough for promotion into the governed graph
- **HOLD** — potentially meaningful, but insufficiently supported
- **REJECT** — weak, spurious, or otherwise unsuitable for promotion

### v0.9 Adjudication Checkpoint

The first v0.9 adjudication pass evaluated nine v0.8 candidate relationships:

- **ACCEPT: 0**
- **HOLD: 1**
- **REJECT: 8**

The single HOLD is:

- `CANON-0015` — *Alchemy Ancient and Modern* ↔ “Relating ancient language to modern attention” — score **50.2**

The remaining candidates were rejected as weak lexical coincidences. Generic overlap such as **“life”**, **“source”**, **“paths”**, or **“witnessing”** is not sufficient to create an explicit relationship edge.

This checkpoint is intentionally conservative: **no Reddit ↔ canonical relationship was promoted from generic lexical overlap alone**.

### v0.10 Integration Milestone

PRE-ALPHA v0.10 is the sealed **Evidence-Governed Knowledge Pipeline** milestone that precedes the current Public Beta phase. It joins the canonical adjudication, WikiSpine/reference, retrieval, ontology and evidence boundaries under an end-to-end integration gate while preserving fail-closed promotion rules.

Verified release-state checkpoints include:

- **Canonical duplicate review:** 81 / 126 families adjudicated; 45 unresolved
- **WikiSpine:** 72 resolved high-precision typed reference identities (PERSON 60, WORK 12); 1 WORK identity pending
- **Audited public-metadata topic census:** 68 unique normalized topics
- **Public epistemic taxonomy:** Established Evidence · Interpretation · Lived Experience/Testimony · Hypothesis · Speculation
- **Broader 300+ topic figure:** estimate only; not an audited exact count

Drive rows 82–86 remain blocked until an authoritative private mapping is available. This is nonblocking release debt: no mapping is guessed and no private identifiers or per-object digests are published.

## Safety and Promotion Gates

The following automated promotions remain disabled:

- **Truth inference: OFF**
- **Rights promotion: OFF**
- **Scientific-evidence promotion: OFF**

These gates are deliberate. AkashicNET is designed to distinguish discovery, interpretation, hypothesis, and evidence rather than collapse them into a single claim layer.

## Google Drive Corpus

Google Drive inventory and audit infrastructure is part of the project. The
repository contains reusable code, schemas and aggregate validation reports only.
Provider IDs, filenames, paths, timestamps, file-linked hashes and raw census
outputs belong to a separate private audit layer and must not be committed or
uploaded as public workflow artefacts.

The project keeps these stages deliberately distinct:

1. inventory
2. provenance capture
3. ingestion
4. canonicalisation
5. validation
6. publication

**A Drive file being discovered or inventoried does not automatically make it a canonical public knowledge node.** The same provenance and evidence rules apply before records are promoted into later layers.

See [Data security boundary](docs/DATA_SECURITY_BOUNDARY.md) and
[Security policy](SECURITY.md).

## Current Capabilities

- Reddit URL harvesting
- URL canonicalisation and deduplication
- Community-source provenance
- Metadata validation
- Reproducible archive workflows
- Automated testing
- Unified Akashic search indexing
- Research evidence layers
- Google Drive inventory and audit workflows
- Public Wikipedia metadata pilot for discovery/reference use
- Canonical node generation
- Candidate relationship generation
- Relationship scoring
- ACCEPT / HOLD / REJECT adjudication
- Conservative evidence-gated promotion logic
- End-to-end canonical → reference → retrieval → ontology/evidence integration validation
- Five-label public epistemic taxonomy with promotion guards

## For Normal Users

You do not need to be a developer to explore AkashicNET's public-facing work.

- **Explore the public portal:** visit AkashicNET.org.
- **Follow public source URLs:** use published source links to explore original community material.
- **Understand the method:** provenance, validation, evidence boundaries and uncertainty are documented as part of the project.
- **Engineering workspace:** the GitHub repository is currently private; public-facing material is released separately through approved public surfaces.

AkashicNET is now in **PUBLIC BETA**. Features, interfaces and knowledge structures remain under active development; evidence, provenance, privacy and fail-closed promotion boundaries remain in force.

## Principles

The toolkit is being developed around:

**Provenance · Transparency · Reproducibility · Validation · Evidence Governance · Open Knowledge · Human Oversight**

The goal is not to present the archive as complete or definitive, but to make the process of building and validating a living knowledge commons transparent and inspectable.

## Conceptual Multidimensional Visualisation

Recent AkashicNET visual work explores the architecture as a **multidimensional pyramid / tetrahedral lattice** rather than a flat graph.

In that conceptual model:

- the **wide base** represents vast raw source data
- canonicalisation progressively reduces duplication and ambiguity
- entities and concepts form intermediate knowledge layers
- candidate relationships are tested through an evidence membrane
- adjudicated knowledge occupies a narrower, higher-confidence region
- accepted relationships remain connected back to their provenance

A symbolic **Primordial OM → Ω / Omega Point** axis has also been explored in artwork as a metaphor for the long arc from information toward increasingly integrated understanding.

This is a **conceptual and artistic design horizon**, not a claim that AkashicNET currently models cosmology, consciousness evolution, or an Omega Point as established scientific fact.

## Publication Snapshot

- Current phase: **PUBLIC BETA**
- Sealed engineering release: **PRE-ALPHA v0.10** (`v0.10.0-prealpha`)
- Release milestone: **Evidence-Governed Knowledge Pipeline**
- Canonical Reddit URLs: **9,401**
- Unified Akashic search index: **12,058 records**
- v0.9 relationship checkpoint: **0 ACCEPT · 1 HOLD · 8 REJECT**
- Canonical duplicate review: **81 / 126 adjudicated · 45 unresolved**
- WikiSpine: **72 resolved (PERSON 60 · WORK 12) · 1 WORK pending**
- Audited public-metadata topics: **68**
- Public epistemic labels: **5**
- Automated truth inference: **OFF**
- Rights promotion: **OFF**
- Scientific-evidence promotion: **OFF**
- Validation/tests: **Passed**
- Repository visibility: **Private engineering workspace**
- Primary branch: `main`
- Snapshot date: **2026-08-31**

## Contributing

The project is under active development. Near-term work includes continued fail-closed Drive corpus canonicalisation, stronger cross-source provenance, evidence-aware graph construction, relationship review tooling, and multidimensional exploration interfaces.

---

*Connect broadly · Infer cautiously · Preserve provenance · Keep the human in the loop*
