# microINSIGHTS intake checkpoint

Status: DRAFT / HOLD. Discovery inventory prepared; content integration incomplete.

## Scope and observation

On 21 September 2026, user-authorised authenticated inspection of the r/microINSIGHTS newest-first listing identified 44 distinct post IDs. Repeated listing observations were deduplicated by post ID, including highlighted posts. No further entries loaded at the visible listing boundary. This is an observed listing census, not an API-certified complete historical total; deleted, removed, inaccessible or unlisted records are not established by it.

A separate private JSON intake inventory preserves all 44 observed source links and IDs, each marked REVIEW_REQUIRED and HOLD. It contains no article text, comments or media. Raw inventory remains outside this repository under the existing security boundary. This document deliberately contains no per-post identifiers, hashes or source titles.

## Reconciliation

| Measure | Count |
|---|---:|
| Unique discovered posts inventoried | 44 |
| Records awaiting source/privacy/rights review | 44 |
| Content bodies imported | 0 |
| New canonical nodes asserted | 0 |
| Accepted canonical edges | 0 |
| Website publications from this intake | 0 |

No source post is counted as independently verified evidence. A cross-post and its parent must remain distinguishable; two postings of the same source are not independent corroboration.

## Remaining integration work

- [ ] Independently verify public visibility and source identity per record.
- [ ] Check sensitivity, authorship and rights for text and media separately.
- [ ] Reconcile cross-post parents and existing archive entries; retain distinct post identities and provenance.
- [ ] Read source content and linked primary sources before claim assessment or topic assignment.
- [ ] Record exact observed flairs and missing flairs; do not infer them from titles or URL slugs.
- [ ] Prepare eligible public metadata and separately reviewed editorial adaptations.
- [ ] Pass PUBLIC_VERIFIED, sensitivity/PII, reuse-rights and explicit ELIGIBLE/public-manifest review before public build inclusion.
- [ ] Review website and magazine derivatives independently; retain evidence classifications and unresolved questions.

Existing archive denominators are unchanged. This document is not an import into the canonical index and does not enable a crawler or automated HTML scraping. Live automated Reddit access remains HOLD. supports_models remains empty; BQ001/BQ002/BQ003 remain UNRESOLVED; truth, evidence, rights, canonical-identity, website, public-synthesis and other promotion gates remain closed. No release or merge is authorised by this checkpoint.

Governed by [Data security boundary](DATA_SECURITY_BOUNDARY.md) and [Security policy](../SECURITY.md).
