# Research Database Framework

## Purpose

This document defines the structure and organization for the Toolkit's research database.
It is intended to support transparent classification, easier navigation, and better connection between evidence, hypotheses, sources and open questions.

## Core principles

- Keep research metadata consistent and machine-readable.
- Separate evidence statements from interpretation.
- Track source provenance clearly.
- Preserve limitations, uncertainty and open questions.
- Support both qualitative summaries and structured metadata.

## Recommended structure

Each research entry should capture:

- `id` — a stable short identifier for the record
- `title` — concise research topic or source title
- `authors` — contributors or source authors
- `year` — publication or release year
- `type` — source type (e.g. research article, review, dataset, book, report)
- `area` — primary research domain (e.g. consciousness, neuroscience, contemplative science)
- `status` — evidence rating category
- `summary` — short neutral description of what the source reports
- `findings` — key observations or results, stated without over-interpretation
- `limitations` — known weaknesses, gaps, or constraints
- `references` — related Toolkit records or external sources
- `open_questions` — research questions linked to this entry
- `tags` — keywords for indexing and filtering
- `notes` — additional context or commentary

## File organization

Recommended repository structure for research metadata:

- `research/` — structured research documentation and guidance
- `references/` — standardized citation entries and bibliography metadata
- `data/` — optional structured datasets or tables that support research analysis

Within `research/`, documents can be grouped by topic or evidence status, for example:

- `research/consciousness/`
- `research/neuroscience/`
- `research/contemplative-science/`
- `research/open-questions/`

## Metadata format options

Use clear, consistent metadata headers for each research entry.
Markdown with YAML frontmatter is a practical option for a research repository because it is both human-readable and machine-parseable.

Example frontmatter schema:

```yaml
id: research-2026-001
title: Example study title
authors:
  - First Author
  - Second Author
year: 2026
type: research article
area: consciousness
status: emerging
summary: A concise neutral summary of the source.
findings:
  - Finding 1 in plain language.
  - Finding 2 in plain language.
limitations:
  - Limitation 1.
  - Limitation 2.
references:
  - reference-id-001
open_questions:
  - question-001
tags:
  - attention
  - neural correlates
notes: This entry documents the source without assigning interpretation beyond the evidence.
```

## Connecting the database

- Link each research entry to a structured reference in `references/`.
- Link each research entry to open questions where evidence is incomplete or emerging.
- Use tags and categories to support discovery across domains.

## Maintenance guidance

- Update the metadata when source details change or new evidence appears.
- Avoid adding conclusions that exceed the evidence presented in the source.
- Preserve the distinction between evidence, observation, interpretation, hypothesis and speculation.
- Document why each evidence rating was chosen.
