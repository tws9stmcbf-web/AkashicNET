# PR #409 forward integration of PR #400 security corrections

Date: 20 October 2026 (America/Los_Angeles).

**KEEP DRAFT / INDEPENDENT HUMAN REVIEW REQUIRED.** This is AI-executed
integration and validation evidence, not independent approval. No merge to
main, release, deployment, auto-merge or repository-wide lock enforcement.

## Exact inputs and scope

| Input | Commit |
| --- | --- |
| Previous #409 head / first parent | `ff4b15c39ed22547615bc109eb9939bbb4126675` |
| Current #400 security head / second parent | `c927f46e41a58fca236009d421907e1e7d603c06` |
| Common ancestor | `28887d591b8c8bee52c4901d16437e5d0c8f2f20` |
| Current main, already contained in #400 | `e342c8fea7ef6da7ffe2a5efa8fca17de72df6a4` |

Live GitHub metadata and full local Git history agree: previous #409 is eight
commits ahead and twelve behind current #400. Both PRs were open and draft.
No AGENTS.md is present in the candidate repository tree.

The three-way merge is clean. The seven experiment paths and eighteen paths
changed on #400 since the common ancestor are disjoint. Every experiment blob
is byte-identical to previous #409, and every incoming blob is byte-identical
to current #400. The pure integration diff relative to current #400 is exactly
the original seven-file experiment. This report is the only additional file.

The integration retains the existing base-branch target
`test/filtered-retrieval-continuity-v01`. Its two ordered parents preserve both
histories. Publishing the candidate uses a non-force update of only
`experiment/actions-lock-retrieval-v01`, guarded by the exact old #409 head.
No #400 ref, metadata, source or review status is changed.

The inherited security changes reject lone surrogates, protect output encoding
and writes with the constant public diagnostic, screen the demonstrated local
path forms, and reject duplicate provenance-family membership before joins.
Their source and 29 regression/control cases are preserved without edits.
See [the original focused review](pr400-security-review-20261020.md).

## Preserved dependency and governance controls

| File | SHA-256, unchanged |
| --- | --- |
| `.github/workflows/actions.lock` | `d7f1fafc71ee89f943d577ca16f02a00c0418d36c98f85ab8dd3541c793c87ce` |
| `.github/dependency-records/retrieval-validation-python-v078.txt` | `9740f7b7a6fdd3c869fdc0387dbb7b8df4afad25f18063645aa2349d80c42a14` |

Both immutable Actions SHAs, the single-workflow Actions scope, requirement
roots, all distribution hash allowlists, path triggers, fresh venv, mandatory
hash verification, wheels-only installation, enabled dependency resolution,
`pip check` and the nine-file test command remain unchanged. No lock was
regenerated and no dependency or package manager was upgraded.

Source identities/classifications, historical Petranker binding and relocated
research, governed artifacts, sealed status, review-only edge acceptance,
privacy/rights gates, evidence/provenance separation, disabled truth inference
and disabled scientific-evidence promotion are preserved. Earlier experiment
documents remain historical checkpoints; their old-base statements are not
claims about this combined candidate.

## Local evidence and exact identities

The completed full local runs tested pure merge commit
`e4aea0cc6d27c2362bed59aff6a75d3908aa0c6a`, tree
`3dce30941f097fbca7d034570de307b67b3fbbe9`, with the ordered parents above.
The final proposed tree adds only this report. The published commit and fresh
hosted run identities must be recorded separately in the PR checkpoint; a
documentation change or different commit metadata does not silently inherit
another exact commit's validation identity.

Environment: Ubuntu 24.04.3 LTS, Linux x86_64, glibc 2.39, CPython 3.12.14,
pip 25.0.1, fresh isolated venv. Installation used the unchanged workflow
command with `--isolated`, the explicit PyPI index, `--require-hashes`,
`--only-binary=:all:` and `--no-cache-dir`; an installation report recorded the
selected wheel identities. All eleven package versions match the old baseline:

`attrs 26.1.0; iniconfig 2.3.1; jsonschema 4.25.1;
jsonschema-specifications 2025.9.1; packaging 26.3; pluggy 1.7.0;
Pygments 2.21.0; pytest 9.1.1; referencing 0.37.0;
rpds-py 2026.9.1; typing_extensions 4.16.0`.

| Check on the pure integration | Observed result |
| --- | --- |
| Same nine-file retrieval/privacy suite | **716 passed in 80.04s**, no failures or xfails |
| Preservation, Petranker binding, historical candidate, source-status and knowledge-graph suites | **272 passed, 3 subtests passed in 2.60s** |
| Retrieval bridge and API compatibility validators | PASS |
| Complete exact-head historical preservation entrypoint and dependencies | PASS |
| All validation run steps from the combined-candidate workflow | PASS |
| Tracked-file public-data boundary and immutable Actions-reference scanners | PASS |
| `pip check`, whitespace and clean tracked-file checks | PASS |
| Official Actions-lock v0.2.0 offline scoped coverage check | PASS |

The retrieval count is **687 previous tests + 29 inherited security cases =
716**, matching #400's expanded suite. No regression was observed in these
checks. The earlier 687-test green run remains evidence for its earlier base,
not evidence for these security corrections. The 272-test preservation group
is separate from the retrieval suite; repeated validators are not summed into
a new unique-test total.

The retrieval command is unchanged in
`.github/workflows/validate-retrieval-evidence-bridge-v078.yml`. The separate
preservation test command was:

```bash
python -m pytest -q tests/test_v016_preservation.py \
  tests/test_petranker_source_binding.py tests/test_v016_release_candidate.py \
  tests/test_source_status_v016.py tests/test_knowledge_graph_beta_v016.py
```

The complete preservation entrypoint used the exact local candidate in
`CANDIDATE_HEAD_SHA`, with full history and the recorded `origin/main`.

## Relevant negative controls

Controls operated on temporary copies or in-memory patches, not tracked files.

- The official v0.2.0 Linux AMD64 Actions-lock binary was verified against
  SHA-256 `79ec84c191667fd935a277e6fd3662cf5d3669cccc9e99998731d8f306f373b6`
  before execution. Intact scoped `--verify-local` checks passed before and
  after a temporary missing setup-python workflow entry. That mutation failed
  with `not-pinned` identifying the exact missing dependency.
- A hash-verified wheelhouse was downloaded from the unchanged requirements.
  Offline pip dry runs used `--ignore-installed --require-hashes
  --only-binary=:all: --no-cache-dir --no-index`. Replacing the attrs hash with
  zeros failed with the expected hash-mismatch diagnostic; intact controls
  succeeded before and after. Existing packages and caches could not mask it.
- Three intact negative-history tests passed. Bypassing ancestry enforcement
  in memory made all three fail at their expected assertions: advanced main,
  diverged main and an anchor outside main. This demonstrates detection of
  removed ancestry enforcement rather than merely exercising a positive path.

The official tool emits its existing `sha-as-ref` warnings for both immutable
inline SHAs. These are retained intentionally, consistent with the experiment;
they do not fail offline coverage. Online `--verify` could not run because
the local CLI has no GitHub token. No online CLI verification is claimed.
Fresh hosted Actions execution must be inspected separately, including its
use of the existing lockfile, checkout/tree, hashed installation and tests.

## Review and remaining limits

Keep both PRs draft and unreleased. An independent human must review the exact
combined candidate and satisfy each PR's approval requirements before further
integration or release. Green checks and a clean merge do not grant approval.

This remains bounded synthetic engineering validation. The package lock does
not freeze Python patch selection, pip bootstrap, runner images, system
libraries or index availability; it is not a hermetic or cross-platform build
and does not authenticate publishers or establish package safety. The local
online Actions-lock verification limitation is stated above.

Snapshot publisher authorization, actual source permissions, production
snapshot building, atomic durable publication/rollback, deployed access and
logging controls, resource limits and production data behavior remain outside
scope. Recognizable-path screening cannot establish arbitrary prose or opaque
identifiers are public. Further upstream movement requires renewed ancestry
inspection and validation. No new dependency-method research was needed.
