# Universal Topic Pages — architecture v0.1

Status: exploratory  
Scope: public-safe metadata and discovery pages  
Truth inference: off

## Goal

AkashicNET can represent any describable topic through one governed route:

```
/topics/{slug}
```

A topic page is generated from a validated record rather than authored as an unsupported essay. A stub may carry empty display arrays and an explicit pending review record. The schema requires every field consumed by the page; richer publication requires a dated human review, record-level sources and a known reuse mode. A status label alone never promotes evidence or rights.

## Page contract

Every topic page separates:

1. **What it is** — neutral description and aliases.
2. **What is documented** — traceable records and dated sources.
3. **Origin** — documentary origin, claimed origins and ultimate-origin status.
4. **Entities** — verified people or organisations, documented claimed entities, unnamed reported presences or unknown agents.
5. **Connections** — typed edges with independent evidence status.
6. **Competing interpretations** — including conventional, cultural and unresolved accounts.
7. **Open questions** — what is not known.
8. **Rights and provenance** — metadata-only, link-only, licensed reuse or public domain.
9. **Review state** — stub, discovery, reviewed or public.

## Publication states

| State | Meaning | Public behaviour |
|---|---|---|
| stub | Identifier and minimal provenance only | Clearly labelled, no synthesis |
| discovery | Machine-collected metadata awaiting review | Searchable only if public-safe |
| reviewed | Sources, rights and connections checked | Eligible for a topic page |
| public | Reviewed record intentionally released | Indexed and linked |

## Origin rule

A record can have a traceable first publication while its ultimate origin remains unknown. The system must never collapse those fields.

Examples:

- quantum mechanics: documentary history is traceable; the underlying nature of reality remains an open philosophical and scientific question;
- an unnamed reported entity: the report may be dated and sourced; independent existence remains unresolved;
- a traditional practice: textual records may be dated, while the living lineage may be older and plural.

## Connection rule

Similarity is not corroboration. Each edge carries one status: documented, taxonomic, co-occurrence, hypothesised, contested or unknown. Pages may display candidate connections without asserting causation.

## Discovery sources

Initial adapters may use Wikidata, Library of Congress, UNESCO Thesaurus, MeSH, NASA Thesaurus, AGROVOC, Getty vocabularies, OpenAlex, Crossref, DataCite, PubMed and selected institutional or declassified archives.

Registry availability never overrides item-level rights, privacy, cultural sovereignty or source-specific terms.

## Scaling path

1. Validate the seed against `schemas/global_topic_v01.schema.json`.
2. Assign stable slugs and external identifiers.
3. Deduplicate conservatively; ambiguity produces separate candidates.
4. Generate static or cached pages from reviewed records.
5. Add topic search and graph navigation.
6. Permit continuous discovery without automatic public promotion.
7. Maintain tombstones and redirects when identifiers merge.

## Hard boundaries

- No private Drive, personal, paywalled or restricted content is copied into public records.
- No topic becomes evidence merely by being indexed.
- No unknown entity is treated as verified.
- No spiritual interpretation is silently converted into a scientific claim.
- No scientific explanation is presented as disproving the meaning of an experience.
- Indigenous and community-held knowledge requires context, consent and cultural-sovereignty review.
- BQ001 remains UNRESOLVED.
