# v0.17 combined validation candidate

Status: PENDING_COMBINED_CI_REVIEW_AND_HUMAN_APPROVAL. This is not a release decision.

Integration base: `645cffad768e2591638c46934bc96555ad6abc40`, after the authorized squash merges:
#381 `44f2b38119eb3039028614dd3c493754344e82af`;
#382 `d6a6dc9a77ef78b9150d031526f3c344bbd4e536`;
#351 `645cffad768e2591638c46934bc96555ad6abc40`.

The combined workflow runs without path filters and checks out the exact PR head
(or push commit), records that SHA, and requires the integration base and inherited
v0.16 readiness pin `4867ca7c8c9a4e1bc139f630815ecf49c79a2ef7` as ancestors.
It runs inherited candidate validation, sealed/public status validation, inventory
and comparison validators with Git checks, mutation tests, and semantic-candidate
replay with the historical v0.2.0 byte guard. Tracked files must remain unchanged.

The underlying validators cover closed schemas, immutable provenance,
inventory projection and claim scope, counter-evidence/research-gap parity,
correction history, shared ancestry, uncertainty and no-promotion boundaries.
Their success is mechanical evidence for issue #295, not proof of scientific
claims or a replacement for independent review. Arbitrary website prose remains
subject to editorial review under docs/public-status-contract.md.

## Remaining decision gates

- All mandatory CI must pass for one recorded combined commit.
- Independent review must assess the combined candidate and any findings must close.
- A human must approve that exact candidate before READY or release.
- A later code change requires new validation/review evidence.

BQ001 remains UNRESOLVED / Never Final, accepted canonical edges remain 0,
Reddit live access remains HOLD, and all privacy/evidence/rights/publication/
promotion boundaries stay closed. Sealed v0.14/v0.15 references are not retargeted.
No release tag, publication, ingestion, analytics or multimedia action is authorized.
