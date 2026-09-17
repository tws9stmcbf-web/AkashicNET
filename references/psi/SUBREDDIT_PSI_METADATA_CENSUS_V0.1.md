# PSI subreddit metadata census v0.1

Status: **REVIEW_REQUIRED**  
Related issue: #354

## Scope

This artifact screens the current governed `r/NeuronsToNirvana` metadata index for seven requested lanes: `TEL`, `CHN`, `MED`, `PRE`, `RV`, `PK` and `PSI-PERSON`. It is not a complete historical subreddit census and it does not retrieve or copy post bodies, transcripts, papers, images or audio.

The source index contains **7298 unique post IDs**. Census counts are discovery counts, not findings.

## Deduplication

1. Canonical Reddit manifestations are deduplicated by post ID.
2. Repeated normalized title slugs share a provisional source-lineage key.
3. Existing governed source IDs override provisional title keys.
4. One source may carry multiple claim-lane classifications.
5. Cross-lane linkage never transfers evidence, corroboration, disposition or model support.
6. Missing outbound URLs remain unresolved rather than inferred.

A shared title is only a review lead. Full provenance review must confirm the publisher, creator, publication date, canonical URL, version, rights status and whether apparently repeated posts actually point to the same underlying source.

## Bounded selections

| Lane | Reddit post | Selection boundary |
|---|---|---|
| TEL | `1kqolp4` | Official secondary source resolved; controlled evidence not established |
| CHN | `1vyr82r` | Multi-paper channeling packet; source identity remains open |
| MED | `1bqlf7z` | Spirits/channeling title only; deceased-communicator proposition unresolved |
| PRE | `1fnhbs3` | Interview provenance and cited-study trail require review |
| RV | `1g1layl` | Military remote-viewing title; exact programme/source unresolved |
| PK | `15rxs24` | BIO-PK/fMRI subtype; existing HOLD preserved |
| PSI-PERSON | `1g2ok6c` | Named-person index test; person label is non-evidential |

Each selection is a queue item for full provenance review. Selection authorizes no content import, public synthesis or evidential advancement.

## Full-provenance checklist

- resolve canonical Reddit and underlying source URLs;
- verify creator, publisher, date, version and manifestation lineage;
- separate every exact proposition into its proper series;
- retrieve only rights-permitted material;
- record transcript/full-text availability without reproducing protected content;
- preserve counter-sources and ordinary explanations;
- audit privacy, bereavement, disability and protected-population risks;
- record protocol, blinding, target generation, scoring, exclusions and preregistration where applicable;
- keep every lane's assessment independent;
- stop before import or publication unless a later reviewed gate explicitly authorizes it.

## Governance

BQ001, BQ002 and BQ003 remain **UNRESOLVED**. Accepted canonical edges remain **0** and `supports_models` remains empty. Truth inference, scientific-evidence promotion, model-support promotion, rights promotion, source/content import, public synthesis and website promotion remain **OFF**.
