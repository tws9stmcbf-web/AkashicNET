# Visualisation Protocol & Provenance (Phase 3)

## Purpose

This protocol defines how visualisations are created, documented and used within Phase 3 workflows. Visualisations are treated as research and hypothesis-generation tools, not as standalone evidence. The protocol covers author-created Noetic visuals, HIERATIC visuals, HOMESENSE visuals, community-sourced visuals (e.g., r/NeuronsToNirvana), and external research figures where reuse is legally permissible.

## Core principles

- Visualisations are hypothesis-generation aids: they can suggest patterns or guide measurement choices but do not constitute evidence without supporting data and analysis.
- Provenance is mandatory for every visual (who created it, where it came from, licensing and permission status).
- Respect copyright and platform terms: do not bulk-copy Reddit images and do not assume posts grant reuse rights.
- When in doubt, link to the source rather than embedding the visual; obtain explicit permission if embedding is required.
- Keep visuals and any personally identifying content anonymised unless explicit consent is documented.

## Types of visuals covered

- Noetic Sciences Toolkit author-created visuals (diagrams, infographics, plots)
- HIERATIC symbolic or ritual visuals
- HOMESENSE environment- or design-focused visuals
- Community-sourced visuals (screenshots, user-generated images) — treat with extra caution
- External research figures (only include if licence/permission allows reuse; prefer linking)

## Required metadata for every visual

Store a provenance file alongside each visual under `data/visuals/<concept_id>/<visual_id>/provenance.yaml` with at least these fields:

- `visual_id` — stable id
- `title` — short title
- `creator` — name or pseudonym of the creator
- `original_source` — platform or publication name
- `original_url` — link to original (if available)
- `access_date` — ISO 8601
- `license_or_permission_status` — e.g., CC-BY-4.0 | copyrighted - permission obtained | copyrighted - no permission
- `permission_evidence` — link to permission email or licence text (if obtained)
- `attribution_requirements` — text to include when displaying the visual
- `intended_use` — e.g., hypothesis-generation, illustrative only, included in dataset
- `contains_identifying_content` — true|false
- `consent_obtained` — true|false (required if identifying content true)
- `notes` — free text

Use the lightweight visual provenance template (`experiments/visual-provenance-template.md`) as a starting point.

## Best practices for externally sourced visuals

- Do not embed Reddit images unless explicit permission is obtained from the poster and the platform permits reuse.
- Prefer linking to community posts; if including excerpts, anonymise and paraphrase instead of screenshotting identifiable text.
- For published research figures, confirm the figure's licence. Many journals require permission for reuse; if reuse is not permitted, link and cite instead.
- Record licence and permission status in `provenance.yaml` and attach permission evidence when available.

## Using visuals in hypothesis generation and citizen-science workflows

- Visuals may be used to generate candidate hypotheses (document hypotheses in the mapping template and create a corresponding `experiments/mappings/<concept_id>.md`).
- Every visual used to justify an experiment must have a provenance file and be linked in the protocol's `background` section.
- Community-sourced visuals used as signals must be treated as exploratory input only per `experiments/community-signal-research-workflow.md`.

## Storage and file naming

- Recommended structure: `data/visuals/<concept_id>/<visual_id>/` containing `image.ext`, `thumbnail.ext`, `provenance.yaml`, and `README.md`.
- Use stable, short ids: `concept-hieratic-001-v1`.

## Display and redistribution rules

- When publishing visuals in repository pages or articles, include the `attribution_requirements` string and a link to `original_url` when available.
- If permission is required but not yet obtained, do not redistribute — link instead.

## Integration checklist (before using a visual as part of a protocol)

- Is provenance recorded in `provenance.yaml`? Yes/No
- Is license/permission adequate for the intended use? Yes/No
- If community-sourced, is consent documented? Yes/No
- Has the visual been anonymised if it contains personal data? Yes/No
- Is the visual linked in the protocol's background and mapping files? Yes/No

## Examples and templates

- See `experiments/visual-provenance-template.md` for a lightweight template to copy.

---

This protocol complements `experiments/citizen-science-protocol-template.md` and `experiments/community-signal-research-workflow.md`. Use it to ensure visual materials are used ethically, legally and transparently, and never as a substitute for empirical evidence.
