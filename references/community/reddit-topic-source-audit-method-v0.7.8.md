# Reddit topic-source audit v0.7.8

Date: 2026-09-03  
Status: audited checkpoint; no public count change

## Result

The sealed public count remains **71 audited top-level topics**.

- `reddit-uri-index.csv` contains 9,502 unique structural URI values and no topic field.
- `reddit-semantic-index.csv` contains 9,401 unique URLs across r/NeuronsToNirvana, r/TribalGathering and r/microdosing, but only source, URL, subreddit, URL type and post ID fields.
- `n2n-pilot-index.csv` contains 15 curated categories already included in the topic census.

These sources therefore contribute **zero automatically promotable topics**.

## Held explicit topic cells

The smaller curated `n2n-index.csv` has three free-text topic cells:

- Consciousness discourse mapping
- Akashic archive, codex, symbolic memory
- Unity, ego, multiple paths, meaning-making

They are preserved as HOLD candidates. Comma-separated phrases are not silently split, normalized or promoted because each cell may mix topics, descriptors and relationships.

## Boundaries

URLs and URL slugs are identifiers, not topic assertions. Titles, people, works and inferred themes are not promoted automatically. Private data remains excluded. Truth inference, rights promotion and scientific-evidence promotion remain off.
