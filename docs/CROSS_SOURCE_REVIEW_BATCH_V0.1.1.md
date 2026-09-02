# Cross-Source Review Batch v0.1.1

Status: **review candidate only**  
Issue: #205

## Scope

This is the first deliberately small Drive↔Reddit candidate batch produced under the cross-source edge-provenance v0.1 contract. It uses only two committed public-safe inputs:

- `references/community/n2n-test-batch-25.csv`
- `references/community/knowledge-graph-seed-v0.1.md`

No private Drive identifiers, filenames, paths, timestamps, content, or object-linked hashes are included.

## Candidate review table

| Edge | Reddit record | Drive public family | Basis for review | Required disposition |
|---|---|---|---|---|
| `edge:review-batch-0001` | Wisdom traditions as cognitive maps | `VIVEKANANDA-001` | Broad thematic correspondence between a public discussion of wisdom traditions and a public canonical family label. This is not evidence that the Reddit record discusses the publication. | `REVIEW_REQUIRED` |
| `edge:review-batch-0002` | Visual symbolism and the sacred | `ABRAMELIN-001` | Weak lexical overlap on “sacred”; the term is too broad for acceptance and is retained only to test conservative rejection/hold review. | `REVIEW_REQUIRED` |
| `edge:review-batch-0003` | HIERATIC as interpretive scaffolding | `GNOSIS-ECHOES-001` | Possible interpretive-context overlap; no title-level or content-level evidence establishes a relationship. | `REVIEW_REQUIRED` |

## Non-promotion statement

All three records are inferred candidates, not asserted relationships. They are unaccepted by construction and must not affect retrieval confidence, evidence classification, rights status, canonical identity, scientific status, or truth claims.

The batch deliberately contains borderline candidates so a reviewer can test `HOLD` / `REJECT` handling. It proposes **zero** automatic acceptances.

## Provenance and independence

Each edge cites immutable SHA-256 digests for both public-safe source artifacts. The two artifacts have distinct `independence_key` values. Multiple representations of either input must reuse its existing independence key and cannot increase confidence.

## Review gate

A future adjudication artifact may classify each candidate as `HOLD` or `REJECTED`. Promotion to an accepted edge requires a separate explicit human adjudication record satisfying the v0.1 schema. Automated truth inference remains off.
