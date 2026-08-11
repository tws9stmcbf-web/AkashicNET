# Structured Reference Format

## Purpose

This document defines a standard format for references used by the Noetic Sciences Toolkit.
A structured reference format improves clarity, traceability, and consistency across the bibliography.

## Recommended fields

Each reference entry should include the following information where available:

- `id` — stable short identifier for the reference
- `title` — publication title or source name
- `authors` — list of author names
- `year` — publication year
- `publication` — journal, book, report or source outlet
- `doi_or_url` — DOI, stable URL, or identifier
- `type` — source type (e.g. research article, review, dataset, book)
- `area` — primary domain (e.g. consciousness, neuroscience, contemplative science)
- `status` — evidence status label
- `relevance` — brief statement of why the source matters for the Toolkit
- `notes` — important limitations, context, or caveats
- `tags` — keywords for indexing and discovery
- `related_entries` — linked research or question identifiers

## Example entry template

```markdown
---
id: reference-2026-001
title: Example source title
authors:
  - First Author
  - Second Author
year: 2026
publication: Example Journal
doi_or_url: https://doi.org/10.1234/example
type: research article
area: consciousness
status: emerging
relevance: This source offers evidence relevant to the Toolkit's exploration of altered states.
notes:
  - Preliminary sample size.
  - Findings require replication.
tags:
  - altered states
  - neuroimaging
related_entries:
  - research-2026-001
  - question-2026-002
---

## Summary

Provide a concise summary of the source and its relevance to Toolkit topics.
```

## Usage guidelines

- Store references in `references/` using consistent file names and structured frontmatter.
- Use the `status` label to indicate evidence strength and current interpretation.
- Link references to related research entries and open questions.
- Avoid adding unsupported interpretations in the reference summary.

## Notes

The structured reference format is a living guideline.
Update it as the Toolkit's research process evolves.
