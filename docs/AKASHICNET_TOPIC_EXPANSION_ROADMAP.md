# AkashicNET Topic Expansion Roadmap

Status: ACTIVE
Date: 2026-08-30

## Objective

Increase the number of *auditable, genuinely distinct* topics represented in AkashicNET without inflating the count through aliases, duplicate collections, or unsupported inferred concepts.

Current working estimate: ~310 distinct interdisciplinary topics.
Public-safe claim until deterministic census: **300+ interconnected interdisciplinary topics**.

## Counting rule

A topic is countable when it has:

1. a stable canonical topic label;
2. at least one source-backed node (Reddit metadata, library/Drive metadata, canonical document, or another provenance-bearing source);
3. a distinction from aliases and narrower/broader duplicates;
4. provenance sufficient to reconstruct why it was admitted.

Statuses:
- `candidate_topic`
- `canonical_topic`
- `alias`
- `merged_duplicate`
- `needs_evidence`

## Expansion lanes

### Lane A — Existing metadata decomposition
Extract latent topics already present below broad roots. High-yield roots include Buddhism, Hinduism, Philosophy, Ancient Religions, Metaphysics, Psychology, PDF/author collections, World History, Alchemy and related traditions.

### Lane B — Reddit metadata discovery
Continue historical r/NeuronsToNirvana corroboration and extract topic candidates from source-reported titles and existing metadata. Do not treat search-engine discovery as API verification.

### Lane C — Cross-source topic intersection
Map library topics to Reddit/canonical topics. A cross-source occurrence strengthens provenance but should not create a second topic when labels are synonymous.

### Lane D — Gap discovery
Identify well-supported interdisciplinary subjects represented in source material but absent from the canonical topic registry. Prioritise consciousness science, neuroscience, psychedelics, contemplative traditions, philosophy of mind, noetic science, ecology/adaptation, physics/cosmology, anthropology/indigenous knowledge, history and ethics.

## Immediate checkpoints

- [ ] Build deterministic topic census script.
- [ ] Create canonical topic registry with aliases and provenance.
- [ ] Parse the 66 root metadata collections.
- [ ] Parse descendant collection metadata.
- [ ] Parse N2N metadata labels/topics.
- [ ] Normalise spelling and obvious aliases (e.g. collection spelling variants) without silently rewriting source metadata.
- [ ] Produce raw-label count vs canonical-topic count.
- [ ] Generate candidate topics found in only one source.
- [ ] Generate cross-source topic intersections.
- [ ] Review top 25 high-confidence expansion candidates.
- [ ] Target audited checkpoints: 333, 400, 500 topics.

## Guardrails

- Topic count is not a quality score.
- Never split one concept merely to increase the number.
- Preserve original source labels alongside canonical labels.
- Distinguish a topic from an author, book title, collection name, framework and individual post.
- New topics require provenance; speculative framework concepts can be retained separately as candidates.
- Report exact counts only after the deterministic census is reproducible.

## Next target

**333 audited canonical topics** is the first expansion checkpoint. It is a checkpoint, not a numerological target: if normalisation produces fewer genuine topics, do not manufacture additional ones to reach it.
