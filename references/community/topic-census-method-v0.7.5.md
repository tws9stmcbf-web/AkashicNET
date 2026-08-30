# AkashicNET topic census v0.7.5

Date: 2026-08-30
Status: audited public-metadata lower bound

## Result

The deterministic census currently yields **68 unique normalized topic labels** from metadata that is reproducibly present in the repository.

Source label sets before cross-source overlap removal:

- WikiSpine: **53**
- reviewed ontology: **15**
- N2N pilot metadata categories: **15**

These are not additive because several labels occur in more than one source.

## What this number means

`68` is an audited **lower bound over the currently persisted topic-bearing public/repository metadata used by the census**. It is not a claim that AkashicNET contains only 68 subjects.

The live Drive audit records **199 unique folder IDs** and **2,459 unique non-folder objects**, but the privacy-safe live folder-label snapshot is not currently persisted in `main`. The census therefore does not reconstruct, guess, or count those unpublished labels.

The broader statement **“300+ interconnected interdisciplinary topics”** remains an estimate until a sanitized Drive topic-label snapshot and any additional reproducible N2N label sets are incorporated and normalized.

Exact claims such as `310`, `333`, or `347` are not supported by this v0.7.5 reproducible census.

## Normalisation

The census uses conservative formatting and spelling normalisation only. It does not merge concepts by semantic similarity. Explicit deterministic aliases are limited to known spelling/format variants such as Qabbalah/Kabbalah and Contemplative practice/Meditation.

## Boundaries

- folder count is not topic count
- document count is not topic count
- work/author entities are not automatically topic labels
- Wikipedia/Wikidata reference identity is not scientific evidence
- Reddit/community metadata is not scientific evidence by default
- archive inclusion is not endorsement
- no truth inference
- no rights promotion
- no Drive access was performed for this census

## Next completion step

Create and review a privacy-safe Drive topic-label snapshot containing only normalized collection labels and provenance-safe source identifiers. Incorporate that snapshot through the same deterministic normalisation pipeline, then publish the resulting full cross-source census as a new checkpoint rather than rewriting v0.7.5.
