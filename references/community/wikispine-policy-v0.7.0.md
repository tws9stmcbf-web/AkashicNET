# AkashicNET WikiSpine policy v0.7.0

## Milestone

**WikiSpine reference backbone pilot**

AkashicNET may use Wikidata and Wikipedia as a public reference spine for stable entity resolution, aliases, disambiguation, navigation and provenance-aware context.

## What WikiSpine is

WikiSpine is a controlled enrichment layer, not an indiscriminate crawler. It starts from approved AkashicNET concepts, works, authors, places and traditions; resolves stable Wikidata identifiers first; then attaches Wikipedia reference metadata where useful.

## What WikiSpine is not

Wikipedia or Wikidata presence does not establish truth, scientific validity, safety, efficacy, rights clearance or endorsement. Wikipedia is treated as `REFERENCE_ENCYCLOPEDIA`, not scientific evidence. Wikidata is treated as structured public reference metadata, not an authority that automatically overrides AkashicNET review states.

## Pilot rules

1. Wikidata-first entity resolution.
2. Maximum expansion depth: two explicitly typed hops.
3. No arbitrary recursive following of all Wikipedia links.
4. Full article-body ingestion is off by default.
5. If article snapshots are stored later, revision ID and retrieval timestamp are required.
6. New cross-source semantic edges default to `HOLD` unless identity is deterministic and separately reviewed.
7. No rights promotion from public accessibility.
8. No scientific-evidence promotion from encyclopedic inclusion.
9. No truth inference from Wikipedia/Wikidata statements.
10. Existing AkashicNET provenance, uncertainty and review states remain authoritative for AkashicNET decisions.

## Pilot seed

The v0.7.0 pilot resolves five high-value concepts: Consciousness, Buddhism, Hinduism, Alchemy and Mysticism. The purpose is to prove stable reference identity and policy boundaries before scaling.

## Future crawler contract

A future WikiSpine fetcher should use public Wikimedia APIs, identify itself with a clear user agent, respect API limits, cache responses, retain revision provenance and build deterministic outputs. Network-dependent enrichment should be separable from deterministic CI validation so normal CI does not depend on Wikimedia availability.

## Principle

> A reference spine can improve identity and navigation without becoming a truth engine.
