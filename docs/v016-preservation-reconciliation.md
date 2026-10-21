# Historical v0.16 CI reconciliation

Status: engineering correction for review; no merge, release or deployment decision.

## Isolated extraction, 18 October 2026

PR #407 reuses the workflow, preservation entry point and tests verbatim from PR #400 at `28887d591b8c8bee52c4901d16437e5d0c8f2f20`. The original diagnosis below is retained as historical context. The extraction is based on main `e920533004eb8b7a10031c0b38ec20576250a665` and follows source-binding repair `17c2f42bd7cad4f685f9193d14a7b203a10c9b69`. Its failed run [39131979989](https://github.com/tws9stmcbf-web/AkashicNET/actions/runs/39131979989), inspected job 117688831189, reports the same actual-candidate-base error.

The current review scope is the source-binding and historical-preservation repairs in #407. PR #400 retrieval/public-boundary work remains outside this extraction. Fresh validation belongs to the new head; previous test counts and CI successes are not reused as current results. No historical validator, manifest, original tests or governed blob pins are modified. Keep #407 draft pending review; no merge or deployment is implied.

## Diagnosis and ancestry

The original failing run was [38664475066](https://github.com/tws9stmcbf-web/AkashicNET/actions/runs/38664475066).
Both Ubuntu jobs checked out `da5430c3b4df5d984506468dc41aded9a05a2243`
and failed on `v0.16-release-candidate: FAIL: actual candidate base commit`.
The failure was reproduced locally at that exact head.

| Identity | Commit | Meaning |
| --- | --- | --- |
| Historical beta.2 base | `5fb99152524b57948aa10662a1467944fea706c6` | Immutable identity in the existing v0.16 manifest |
| Historical candidate integration | `8e5b9e2e072f743bb0f51b036d7352bb463f754b` | PR #328, which deliberately reinstated current-main equality for that candidate |
| Current main at investigation | `9cf967a7a9ed7921e6220189e46f4dc51c845a88` | PR #400 integration base |
| Original PR #400 head | `da5430c3b4df5d984506468dc41aded9a05a2243` | Contains current main and the historical base |

The full Git history establishes:

```text
git merge-base --is-ancestor 5fb99152524b57948aa10662a1467944fea706c6 9cf967a7a9ed7921e6220189e46f4dc51c845a88
git merge-base --is-ancestor 9cf967a7a9ed7921e6220189e46f4dc51c845a88 da5430c3b4df5d984506468dc41aded9a05a2243
```

Both commands exit 0. The merge-base of main and that PR head is exactly
`9cf967a7a9ed7921e6220189e46f4dc51c845a88`. This failure therefore does not
identify missing main integration at the inspected head. It identifies application
of the original candidate's repository-position rule to a later descendant.

PR #336 (`bcbfbd7fadfbb63202787c052d7d64014803b636`) previously adopted anchor
ancestry for the earlier beta.1 candidate. PR #328 subsequently changed the base
identity and required current-main equality for beta.2. Neither decision is
silently reversed here. The later [v0.17 combined-validation record](v017-combined-validation.md)
already documents reuse of the historical manifest and dependencies without the
original CLI's obsolete repository-position assumption.

## Smallest scoped correction

Keep `scripts/validate_v016_release_candidate.py`, its original tests and
`manifests/v0.16-release-candidate.json` unchanged. Add the explicit
`python -m scripts.validate_v016_preservation` entry point and route the existing
two-runner workflow to it, with a name that describes historical preservation.
The original CLI still enforces exact historical base equality when intentionally
invoked. No automatic fallback after a validation error is used.

The preservation entry point requires:

- a full `CANDIDATE_HEAD_SHA` matching the checked-out commit;
- the unchanged historical base identity, present in both main and candidate history;
- freshly fetched `origin/main` as an ancestor of the exact candidate head;
- the unchanged historical manifest validator, all eleven governed artifact blob
  pins, sealed baseline locks and every existing dependency and mutation suite.

Missing history/refs, a wrong or absent expected head, an unrelated historical
anchor, unintegrated main, manifest drift and dependency failure all fail closed.
Tests use real temporary Git histories, including a candidate containing two
unrelated histories: the historical anchor must belong to main itself, not merely
to the candidate. The original candidate-binding tests remain active unchanged.

The historical manifest continues to record `UNRELEASED_REVIEW_CANDIDATE` and
`PENDING_EXACT_HEAD_CI_AND_REVIEW`. BQ001 remains UNRESOLVED, accepted edges remain
zero, and all truth/evidence/rights/identity/safety/private-data/edge/publication
promotion boundaries remain false. This change does not create a new v0.16 candidate
identity or certify a release.

## Review and release requirements

- Verify the workflow results for the published correction SHA, including both
  Ubuntu preservation jobs, retrieval validation, public-data checks and the
  combined-candidate workflow. Older green runs do not certify a changed head.
- Independently review the correction and the full PR #400 retrieval/public-boundary
  changes; resolve any findings. No review submission was present at investigation.
- Reintegrate and revalidate if main advances beyond the candidate. The preservation
  gate intentionally rejects an unintegrated newer main.
- Obtain explicit human approval for the exact candidate before merge or release.
  Keep PR #400 draft; auto-merge and deployment are not authorized.
- Production publisher authenticity, source permissions, approved snapshot building,
  atomic publication, deployed authorization/logging and independent security review
  remain outside these synthetic and repository checks.

The earlier 907-test result belongs to its recorded local commit/tree; it is not
relabeled as a result for this correction. Current validation evidence and workflow
links are recorded separately in the PR's reconciliation checkpoint.


## PR #400 integration checkpoint, 20 October 2026 UTC

The text above records the earlier investigation and isolated extraction. PR #407
was subsequently merged as `85af5b6eb7a086a0a330575552b7eb1b82b92abf`;
PR #406 then brought the STARGATE metadata index into main at
`e342c8fea7ef6da7ffe2a5efa8fca17de72df6a4`. Earlier draft/pending wording is
historical and is not a statement of those merged PRs' current status.

This reconciliation brings that main into draft PR #400 without rewriting its
history. The existing source split, historical validator, preservation entry
point, associated tests, workflows and governed pins are unchanged. This note
retains main's extraction record; the original PR #400 version remains available
at [`28887d591b8c8bee52c4901d16437e5d0c8f2f20`](https://github.com/tws9stmcbf-web/AkashicNET/blob/28887d591b8c8bee52c4901d16437e5d0c8f2f20/docs/v016-preservation-reconciliation.md).

The retrieval improvements are retained from PR #400 and require fresh validation
against the integrated head. Earlier test counts are historical evidence only.
PR #409's dependency-locking experiment remains separate. See the
[reconciliation scope and stack plan](pr400-main-reconciliation-20261020.md).
No merge to main, release, deployment, scientific or rights promotion is approved
by this reconciliation; PR #400 remains draft pending independent review.
