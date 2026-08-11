# Integration Framework: HIERATIC & HOMESENSE (Phase 3)

## Purpose

Provide a Phase 3 experimental/application-layer integration framework that keeps the Noetic Sciences Toolkit's evidence base separated from symbolic, conceptual or applied projects named HIERATIC (meaning-making/symbolic) and HOMESENSE (lived-environment application). This document defines layers, epistemic safeguards, a per-concept mapping template and an operational workflow for moving from community observation to testable propositions without presenting symbolic content as established scientific evidence.

## Scope and separation of layers

1. Noetic Sciences Toolkit — evidence and research infrastructure
   - The canonical repository of research records, evidence ratings, structured references, data and reproducible analytic artifacts. Uses Phase 2 evidence standards (`research/evidence-rating-methodology.md`) and the research database framework.

2. HIERATIC — symbolic, conceptual and meaning-making framework
   - A separate layer for symbolic, ritual, conceptual or narrative propositions. HIERATIC contents are explicitly labelled as symbolic, interpretive, or conceptual and are not merged into the Toolkit's evidence records.

3. HOMESENSE — lived-environment / human–environment application framework
   - An application-oriented layer describing interventions, environment-design, and lived-practice proposals. HOMESENSE proposals are treated as candidate interventions requiring the same experimental safeguards as other propositions.

4. Community observations — naturalistic hypothesis generation
   - Aggregated, anonymised community signals used for hypothesis generation only. These remain distinct from structured evidence until tested, preregistered and independently assessed.

5. Citizen-science protocols — methods for testing propositions
   - Protocols, N-of-1 templates, and citizen-science designs (stored under `experiments/`) used to test HIERATIC/HOMESENSE propositions.

6. Empirical evidence — measured and independently assessable results
   - Data, analysis code, preregistration records, and evidence-rated research entries stored and managed under the Toolkit's research infrastructure.

## Integration principles and epistemic safeguards

- Clear labels: every HIERATIC or HOMESENSE page or proposal must include a prominent label: `Layer: HIERATIC` or `Layer: HOMESENSE` and `EvidenceStatus: conceptual|application|untested`.
- Do not merge: symbolic or applied propositions must not be copied into `research/` or `references/` as evidence entries unless they have been tested, preregistered, analysed, and rated using Phase 2 standards.
- Mapping before testing: for any proposition proposed for empirical evaluation, create a mapping document (use the template below) that identifies measurable outcomes and an appropriate protocol before data collection begins.
- Preregistration and reproducibility: confirmatory or population-level claims require preregistration, analysis code, environment specifications and a data-release plan per `experiments/citizen-science-protocol-template.md` and `experiments/n-of-1-methodology.md`.
- Maintain provenance: keep a clear provenance trail linking a HIERATIC/HOMESENSE proposition to its origin (author, community-source, version) and to any downstream experiment IDs (e.g., `experiment-YYYY-NNN`).
- Ethical firewall: ensure consent, privacy, and safety procedures are applied to any study derived from these layers. Symbolic content may have sensitive personal meaning — treat disclosures with care.

## Per-concept mapping template (use for each HIERATIC or HOMESENSE concept)

Fill one mapping per concept. Store mappings under `experiments/mappings/` with YAML frontmatter matching the research schema and a stable `id`.

- `concept_id`: (unique id)
- `layer`: HIERATIC | HOMESENSE
- `proposition`: Short plain-language statement of the proposition (avoid emotive or normative language)
- `underlying_assumption`: The conceptual assumption(s) that must hold for the proposition to be meaningful
- `relevant_established_research`: List repository entries (e.g., [research/...](research/)) or external citations that directly bear on the proposition. Do not invent citations — list only verifiable sources.
- `relevant_emerging_research`: List preliminary studies, pilot data or ongoing work (as verifiable references). If none known, state `None identified in repository`.
- `unknowns`: Concise list of what is currently unknown or untested about the proposition
- `testable_hypothesis`: A clearly operationalised hypothesis suitable for preregistration (one primary hypothesis; optional secondary hypotheses)
- `measurable_variables_outcomes`: Primary outcome(s) with units, secondary outcomes, and recommended instruments or sensors
- `possible_confounders`: Known potential biases or alternative explanations that could explain observed effects
- `recommended_design`: Suggested citizen-science or N-of-1 design (e.g., N-of-1 ABAB, repeated-measures citizen-science cohort with preregistered analysis)
- `ethical_privacy_considerations`: Specific ethical points (e.g., sensitive symbolism, community norms, risk thresholds, consent language, data minimisation needs)
- `criteria_supporting`: What empirical pattern or result would increase confidence in the proposition (avoid claiming proof)
- `criteria_weakening`: What results would weaken confidence
- `falsification_criteria`: Results that would falsify the proposition or render it implausible
- `provenance`: Author, date, origin (community thread, HIERATIC doc, HOMESENSE design)

Example mapping file name: `experiments/mappings/concept-hieratic-001.md`

## Operational workflow for integration

1. Proposal: HIERATIC/HOMESENSE author drafts proposition and mapping using the template and stores it in `experiments/mappings/`.
2. Triage & tagging: maintainers or community reviewers check the mapping for clarity, ethical concerns, duplication, and tag it `ready-for-pilot` or `needs-revision`.
3. Pilot / N-of-1: if appropriate, run small-scale N-of-1 pilots (link to `experiments/n-of-1-methodology.md`) or limited citizen-science pilots with preregistration.
4. Analyse & document: publish analysis code, raw/anonymised data, and an evidence summary using Phase 2 research schema. Do not update the Toolkit evidence records until the entry is rated via Phase 2 methodology.
5. Rating & repository action: if an independent assessment rates the result as `emerging` or stronger, create a `research/` entry with full metadata and evidence rationale; if not, mark the mapping as `exploratory` and archive data appropriately.

## Ethical and privacy guidance (summary)

- Treat symbolic or spiritual content as potentially identifying; default to conservative anonymisation and aggregated reporting.
- Use the `experiments/consent-template.md` (create if not present) and require explicit informed consent for any data used beyond aggregated signals.
- Define retention periods and deletion workflows in the mapping's `ethical_privacy_considerations` field.

## Documentation, filenames and storage

- Mappings: `experiments/mappings/<concept_id>.md` (use YAML frontmatter and the mapping fields above).
- Pilots/experiments: use `experiment-YYYY-NNN` IDs stored under `data/experiments/<id>/` plus a protocol file under `experiments/protocols/<id>.md` using the citizen-science template.
- N-of-1 records: follow `experiments/n-of-1-methodology.md` data schema and store under `data/experiments/<id>/raw.csv` with `data-dictionary.yaml`.

## Epistemic clarity checklist (review before publishing any integration mapping)

- Is the proposition explicitly labelled as HIERATIC or HOMESENSE (not a research claim)?
- Is the underlying assumption made explicit and separable from observed data?
- Are proposed measurable outcomes clearly defined with units and instruments?
- Is a plausible causal pathway stated, and are likely confounders listed?
- Has a design been chosen that can distinguish signal from bias (given constraints)?
- Are preregistration, analysis code, and data-release plans specified for confirmatory claims?
- Are ethical, safety and privacy considerations explicitly documented?

## Next steps (recommended, not implemented)

- Create `experiments/mappings/` directory and example mapping entries for initial HIERATIC/HOMESENSE propositions.
- Add `experiments/consent-template.md`, `experiments/privacy-and-ethics.md`, and `experiments/citizen-science-operational-guidance.md` as supporting artifacts.

---

This integration layer preserves the Toolkit's evidence integrity while enabling conceptual and applied projects to propose testable ideas. Use the mapping template as the authoritative mechanism for moving from symbolic or applied proposals to empirically testable protocols.
