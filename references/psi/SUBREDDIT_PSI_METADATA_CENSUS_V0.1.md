# PSI subreddit metadata census v0.1

Status: **REVIEW_REQUIRED**  
Related issue: #354

## Scope

This artifact screens the current governed `r/NeuronsToNirvana` metadata index for seven requested lanes: `TEL`, `CHN`, `MED`, `PRE`, `RV`, `PK` and `PSI-PERSON`. It is not a complete historical subreddit census and it does not retrieve or copy post bodies, transcripts, papers, images or audio.

The source index contains **7298 unique post IDs**. Census counts are discovery counts, not findings.

## Deduplication

1. Canonical Reddit manifestations are deduplicated by post ID.
2. Repeated normalized title slugs share a provisional source-lineage key.
3. Only the hash-verified pre-existing Ky Dickens repository source overrides its provisional title key. The three unsupported source mappings are provisional; their asserted URLs and elevated review states have been removed.
4. One source may carry multiple claim-lane classifications.
5. Cross-lane linkage never transfers evidence, corroboration, disposition or model support.
6. Missing outbound URLs remain unresolved rather than inferred.

A shared title is only a review lead. Full provenance review must confirm the publisher, creator, publication date, canonical URL, version, rights status and whether apparently repeated posts actually point to the same underlying source.

## Deterministic replay

The JSON `method.discovery` and validator encode the same versioned vocabulary, token boundaries, normalization, row filtering, seed IDs and lineage rules. The validator replays the full pinned CSV locally and checks exact lane membership, canonical URLs, slugs, counts and lineages. It requires the pinned index and provenance blobs to be present and byte-identical; it makes no network requests.

Bare `channel` is deliberately excluded from CHN: it also matches music-video source-channel titles. Thus `1ln91sj` is outside this bounded vocabulary. Supplemental `1vyr82r` is explicitly provisional metadata carried from the prior census, enters only its CHN seed lane, and has no asserted governed source identity. `15rxs24` is an indexed PK seed with provisional provenance.

The explicit broad PSI-PERSON vocabulary also matches music-title `1ubk0s5`; it is retained as a false-positive review candidate, with no inferred person identity. This corrects PSI-PERSON from 10 manifestations / 8 lineages to **11 / 9**. Other lane counts remain **TEL 28/25, CHN 15/14, MED 1/1, PRE 5/3, RV 1/1, PK 4/3**. The earlier prose did not establish a reproducible algorithm; these explicit rules now define the replay.

The Ky Dickens locator identifies `/sources/0` in the existing source-crawl artifact, with its Git blob hash and pre-existing base commit. This verifies repository source metadata only; it does not prove the Reddit post's outbound link or confer evidence status. Each selection must identify exactly one record in its lane and match every record field.

## Bounded selections

| Lane | Reddit post | Selection boundary |
|---|---|---|
| TEL | `1kqolp4` | Provisional title lead; underlying source provenance unresolved |
| CHN | `1vyr82r` | Provisional supplemental metadata; source identity remains open |
| MED | `1bqlf7z` | Spirits/channeling title only; deceased-communicator proposition unresolved |
| PRE | `1fnhbs3` | Interview provenance and cited-study trail require review |
| RV | `1g1layl` | Military remote-viewing title; exact programme/source unresolved |
| PK | `15rxs24` | Provisional seed lead; source identity and methods-review claim unresolved |
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

