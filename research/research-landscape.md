# Research Landscape

## Purpose

This document describes the current Noetic Sciences Toolkit research landscape and how research is organised by evidence status.
It distinguishes established evidence, emerging/promising evidence, mixed or contested evidence, and speculative/open questions while staying aligned with existing Toolkit domains.

## Scope

The landscape is intentionally aligned with the Toolkit's domains:

- Consciousness
- Neuroscience
- Psychology
- Contemplative science
- Psychedelic science
- Human development and wellbeing
- Systems science

It is designed to work with the Toolkit's existing research process and metadata structure:

- `research/research-database-framework.md`
- `research/evidence-rating-methodology.md`
- `references/REFERENCE_FORMAT.md`
- `research/open-research-questions.md`

## Evidence categories

The Toolkit uses a formal evidence-rating methodology that includes:

- Established
- Emerging
- Working hypothesis
- Speculative
- Historical / cultural

For the purposes of the research landscape, the following practical categories are used to describe the current state of documented material:

- Established evidence
- Emerging / promising evidence
- Mixed or contested evidence
- Speculative / open questions

This landscape does not invent new citations or unsupported findings. It presents the current repository's documented research material and the categories that help place it in context.

## Established evidence

### Description

Established evidence refers to findings that are supported by multiple independent sources, replication, systematic review, or a strong consensus within a field.

### Current repository status

- At present, the Toolkit's documented research materials do not yet include a clearly catalogued example of established evidence within the repository itself.
- This section is therefore reserved for future entries that meet the established criteria and are linked to verifiable primary sources.

### Future guidance

When adding established evidence, document:

- source provenance
- evidence strength
- replication status
- the difference between the evidence and any broader interpretation

## Emerging / promising evidence

### Description

Emerging evidence includes research that is promising but requires further replication, larger samples, or stronger methodological confirmation.

### Current repository examples

- **Katlowitz et al. (2026)** — *Plasticity and language in the anaesthetized human hippocampus* (documented in `research/consciousness-processing-under-anaesthesia-2026.md` and `references/katlowitz-2026-anaesthetized-hippocampus.md`)
  - This source is currently classified in the repository as emerging evidence.
  - It provides a documented case study of neural processing during anaesthesia without claiming that the findings prove conscious subjective experience.

### Interpretation guidance

Emerging evidence should be documented with:

- neutral summaries of the findings
- explicit limitations
- evidence status rationale
- links to related questions and references

## Mixed or contested evidence

### Description

Mixed or contested evidence refers to sources where the evidence is uncertain, methodologically complex, or subject to debate.
This category can include working hypotheses, community-based observations, and materials that are valuable for research questions but not yet settled.

### Current repository examples

- **r/microdosing FAQ and community corpus** (`research/microdosing-research-2026.md`)
  - This source represents naturalistic community observation and working hypotheses rather than controlled clinical research.
  - It is useful for generating questions about dosing, set and setting, and subjective experience, but it is not treated as established pharmacology.

- **r/NeuronsToNirvana discourse mapping** (`research/r-neurons-to-nirvana-consciousness-discourse-2026.md`)
  - This source documents a community synthesis of themes, questions and frameworks.
  - It is exploratory and reflective, and its value lies in mapping ideas rather than proving specific claims.

### Interpretation guidance

For mixed or contested evidence, document:

- the evidence source type
- the reasons the evidence is uncertain or contested
- the relevant methodological or interpretive caveats
- any alternative perspectives or conflicting signals

## Speculative / open questions

### Description

Speculative material and open questions document the boundaries of current understanding and the topics that remain unresolved.
This category is not evidence of a claim; it is an invitation for further inquiry.

### Current repository examples

- `research/open-research-questions.md`
  - This document records how the Toolkit tracks open research questions, including research gaps and methodological needs.

### Interpretation guidance

Speculative items should be documented as questions or hypotheses, not as established findings.
Where possible, connect them to:

- existing references
- emerging evidence entries
- research questions that can be investigated further

## Structured landscape overview

Use the following template to document each landscape item:

```yaml
category: emerging
id: research-landscape-2026-001
title: Example source or theme
domain:
  - consciousness
  - neuroscience
status: emerging
summary: A concise description of the current evidence status.
current_repository_example:
  - research/consciousness-processing-under-anaesthesia-2026.md
  - references/katlowitz-2026-anaesthetized-hippocampus.md
key_gaps:
  - replication across methods
  - clearer distinction between neural processing and conscious experience
notes:
  - This entry documents the current repository's available evidence without inventing new claims.
```

## Recommended workflow

1. Identify a source or theme.
2. Determine the appropriate category using the evidence-rating methodology.
3. Document the source with structured metadata and neutral language.
4. Link to references, research entries and open questions.
5. Update the landscape when new evidence clarifies the status.

## Notes on consistency

- Preserve the Toolkit's evidence hierarchy: Evidence → Observation → Interpretation → Hypothesis → Speculation.
- Do not treat mixed or contested evidence as established.
- Do not treat speculative questions as evidence.
- Keep the landscape aligned with the Toolkit's existing domains and documented sources.
