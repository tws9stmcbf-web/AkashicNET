# Audited cross-source orchestrator v0.1.8

The orchestrator removes the repeated draft/ready/check/merge mechanics while retaining one explicit human semantic-review gate.

## Event flow

1. A validated public Reddit index or Drive seed changes on `main`, or the workflow is dispatched manually.
2. A deterministic extractor searches only for exact full-title and explicit family-identifier anchors.
3. The extractor writes a review packet. It does not use thematic similarity, graph proximity, reverse edges, representation counts, or inferred candidates.
4. If the packet changed, GitHub opens a draft pull request and dispatches exact-head validation.
5. The repository owner reviews the packet and adds `human-reviewed`.
6. The merge gate verifies that the pull request changes only the review packet, waits for the exact-head validator, rechecks the head SHA, and squash-merges.

The `human-reviewed` label approves only the mechanical merge of a proposal packet. It does not accept any candidate as true and cannot create an accepted graph edge.

## Permanent boundaries

- Every proposal remains `INFERRED_CANDIDATE`.
- Every proposal remains `REVIEW_REQUIRED`.
- Every `accepted_edge` remains `false`.
- `accepted_edges` remains empty.
- Automated truth inference and acceptance remain off.
- Scientific-evidence, rights, and canonical-identity promotion remain off.
- Private Drive metadata and circular confidence remain prohibited.
- Absence or rejection of a candidate is not negative evidence.
