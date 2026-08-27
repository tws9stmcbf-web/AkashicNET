
## 🔎 Search the Community Archive

The toolkit includes a searchable index of the archived r/NeuronsToNirvana community record.

Search by title, topic, category, author, framework, summary, evidence classification, or URL:

    python tools/search_reddit.py consciousness
    python tools/search_reddit.py Akashic
    python tools/search_reddit.py HOMESENSE

The canonical Reddit archive currently contains **9,401 unique Reddit URLs**, with richer metadata available through the community index. A broader unified Akashic search index now contains **12,058 records** across the wider research and archival layers.

The search tool is read-only: it searches the local public archive and does not make requests to Reddit.

# 🕸️ AkashicNET

## Noetic Sciences Toolkit · PRE-ALPHA v0.4.0

AkashicNET is an open, provenance-first knowledge network for building an auditable living commons around consciousness, psychedelics, interdisciplinary research, and community knowledge.

The **Noetic Sciences Toolkit** is the current research and archival toolkit within AkashicNET, providing the practical infrastructure for provenance, validation, reproducibility, and community-source preservation.

### Current Archive

**9,401 unique canonical Reddit URLs indexed**

Sources currently include:

- `r/NeuronsToNirvana`
- `u/NeuronsToNirvana`
- `r/TribalGathering`

The Reddit URL index is designed to preserve canonical source locations while supporting metadata collection, validation, deduplication, and future enrichment.

### Status

**PRE-ALPHA · Public · Actively Developing**

Current capabilities include:

- Reddit URL harvesting
- URL canonicalisation and deduplication
- Community-source provenance
- Metadata validation
- Reproducible archive workflows
- Automated testing
- Unified Akashic search indexing
- Research evidence layers
- Google Drive inventory and audit workflows
- A validated, provenance-aware multidimensional framework registry

### Framework Registry

The first curated framework-registry seed is available at
`data/framework-registry.json`, with its data model and curation rules documented
in `data/framework-registry.md`. It represents six established names only and is
not an archive-wide discovery result or verification of a provisional count.

Validate it with:

    python -m tools.framework_registry.validate

### Data Sources

The current publication focuses on Reddit community sources.

**Google Drive inventory and audit infrastructure is now part of the project. Full Google Drive ingestion is not yet presented as a completed public archive layer. Inventory, provenance, validation, and ingestion remain deliberately distinct stages.**

## For Normal Users

You do not need to be a developer to explore the project.

- **Browse the toolkit:** open the public GitHub repository.
- **Explore the archive:** open `references/community/reddit-uri-index.csv`.
- **Follow source URLs:** use the indexed Reddit URLs to explore the original community material.
- **Explore the project:** read the README and documentation to understand the provenance and validation approach.
- **Run the toolkit:** technical users can clone the repository and use the documented tools locally.

The current release is a **public PRE-ALPHA research archive**, not yet a standalone consumer application.

### Principles

The toolkit is being developed around:

**Provenance · Transparency · Reproducibility · Validation · Open Knowledge**

The goal is not to present the archive as complete or definitive, but to make the process of building and validating a living knowledge commons transparent and inspectable.

### Publication Snapshot

- Version: **PRE-ALPHA v0.4.0**
- Canonical Reddit URLs: **9,401**
- Unified Akashic search index: **12,058 records**
- Validation/tests: **Passed**
- Repository: **Public**
- Primary branch: `main`
- Snapshot date: **2026-08-25**

### Contributing

The project is under active development. Future phases will expand source ingestion, metadata enrichment, provenance tracking, validation, and research tooling.

---

*Living archive · Under active cultivation*
