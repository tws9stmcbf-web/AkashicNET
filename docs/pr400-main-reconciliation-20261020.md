# PR #400 reconciliation with main, 20 October 2026 UTC

Status: draft engineering integration; independent review and explicit approval
remain required. No merge to main, release, deployment or publication.

## Exact inputs

| Role | Commit |
| --- | --- |
| Previous PR #400 head | `28887d591b8c8bee52c4901d16437e5d0c8f2f20` |
| Current main, including #407 and #406 | `e342c8fea7ef6da7ffe2a5efa8fca17de72df6a4` |
| Merge base | `9cf967a7a9ed7921e6220189e46f4dc51c845a88` |
| Merged #407 | `85af5b6eb7a086a0a330575552b7eb1b82b92abf` |
| Separate PR #409 head | `ff4b15c39ed22547615bc109eb9939bbb4126675` |

Full local Git history reports **9 commits unique to #400 and 10 unique to
main**, correcting the reversed ahead/behind count in the task briefing.

## Actual conflicts and redundant work

A real three-way merge found only two add/add conflicts:

- `docs/petranker-source-digest-reconciliation-v0.1.md`
- `docs/v016-preservation-reconciliation.md`

The differences describe #407's isolated extraction and its provenance, rather
than divergent implementation. Retain main's complete notes and append a dated
checkpoint linking the original #400 versions. Earlier statuses and test counts
remain historical observations, not new validation or current release decisions.

The other eight overlapping paths have identical blobs at both inputs:

- `.github/workflows/validate-v016-release-candidate.yml`
- `.github/workflows/validate-v017-combined-candidate.yml`
- `research/README.md`
- `research/microdosing-research-2026.md`
- `research/rat-psilocybin-5ht2a-2026.md`
- `scripts/validate_v016_preservation.py`
- `tests/test_petranker_source_binding.py`
- `tests/test_v016_preservation.py`

They need no reimplementation or digest refresh. The distinct retrieval code,
fixtures, tests, schema, client and workflow are retained unchanged from #400:
public eligibility before retrieval, exact evidence-status filtering before
limits, deterministic tie ordering and verbatim Reddit review-reference
propagation. All intervening main files, including STARGATE and Consciousness
Library metadata, are retained. No newly missing runtime implementation was
identified by this conflict analysis; fresh regression checks are still required.

## Integration and stack safety

Use an additive two-parent commit with previous #400 first and current main
second. Do not rebase, squash or force-push #400: #409 already descends from its
old head. A fast-forward branch update preserves that ancestry and historical
commit identities. This integrates main into the draft branch only.

Keep #409's head and all seven of its unique files unchanged. Probe a disposable
merge of the reconciled #400 into #409, verify that its seven files remain
byte-identical, and validate that combined candidate locally. The dependency
experiment remains separately reviewable; neither its Actions lock nor its
hash-verified Python lock is imported into #400. No lock regeneration is needed
for the reconciliation. #409 will require its own reviewed forward integration
and renewed hosted validation before acceptance; its older green runs do not
validate a new stack. Do not force-push or silently retarget it.

The specific immutable lock digests at #409 are:

- requirements: `9740f7b7a6fdd3c869fdc0387dbb7b8df4afad25f18063645aa2349d80c42a14`
- Actions: `d7f1fafc71ee89f943d577ca16f02a00c0418d36c98f85ab8dd3541c793c87ce`

## Validation and limits

Record the resulting commit, tree, commands, runtime/package versions, outcomes
and actual CI checkout identities in the PR checkpoint after they exist. Do not
attribute local tests to a different connector-created commit merely because
the tree is identical. Scope comparisons must prove retrieval bytes unchanged
from #400 and integrated-main additions unchanged, with only these two note
appendices and this integration record newly authored.

Run the nine-file retrieval/privacy suite, historical source-binding and v0.16
preservation regressions, complete preservation entrypoint and the v0.17 combined
workflow's validation steps, retrieval/API validators, immutable-Actions audit
and public-data scanner. Verify governed artifacts remain clean. Probe the
stacked candidate against the unchanged #409 lock in a fresh environment.

Passing these checks is engineering evidence only. Independent review of the
full retrieval/public boundary, snapshot publisher authenticity, actual source
permissions, production building, atomic publication, deployed authorization and
logging, and security review remain outstanding. Scientific classifications,
source identities, historical bindings, rights restrictions, privacy gates,
review-only acceptance, disabled truth inference and promotion gates are not
changed. No reviewer attestations or human approvals are invented.
