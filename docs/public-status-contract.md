# Public status contract

The authoritative display record is `website/data/public-status.json`. Its closed,
typed values distinguish the sealed baseline, unsealed candidate, site checkpoint,
and the v0.17.0 milestone. BQ001 remains UNRESOLVED, accepted edges remain zero,
Reddit access is HOLD, and promotion remains disabled.

`scripts/validate_public_status_consistency_v016.py` validates that record against
its reviewed contract and the governed v0.16 candidate manifest. It renders the
homepage and development-progress page from `website/status-templates/*.tsx.in`.
Run it with `--write` after editing a template, then run it without arguments to
check exact rendering consistency. CI checks the committed output; CI does not
rewrite files or make a release decision.

Every required status slot must occur once. Labels and limitations are generated
by reviewed renderer code, rather than supplied as arbitrary prose fields. Changes
to the status contract or renderer require review. The sealed v0.15 validator and
release records remain unchanged.

## What this check does and does not establish

The check proves that the typed display record, governed candidate facts and
committed generated surfaces agree. It does not infer meaning from arbitrary
sentences or establish that all website prose is consistent with those facts.
Templates and other public pages require editorial review for release claims,
BQ001 resolution claims, privacy, evidence and promotion language. A change to
a template can introduce contradictory prose even while the generated data
remains correct; passing this check is not editorial approval.

This scope replaces the regex-based product-name, negation, heading and sentence
classifiers. Independent framework versions and legitimate disclaimers no longer
need exception lists. The old mutation cases are preserved verbatim in
`docs/review-evidence/public-status-regex-tests-before-redesign.py.txt` as review
evidence, not as claims of exhaustive natural-language coverage.

The generated pages are committed for the existing website pipeline. Their
generated status wording reflects the reviewed snapshot. Edit the templates,
not the generated pages.


## v0.17.0 readiness and publication reconciliation

The existing `target` slot now records `status: READY` separately from `released`.
`readiness` pins the owner decision in issue #295 to commit
`677abddc472322621adf54697ac31c383be3b3c3`, approved on 27 September 2026 at
06:01:56 Europe/Berlin, for bounded review-only use. It does not approve later main.

`released: true` means a published GitHub release record exists, not a stable
release, website deployment, sealed baseline or evidence promotion. The GitHub
API independently confirmed release ID 397503809, `draft: false`,
`prerelease: true`, published at 04:06:55 UTC (06:06:55 Europe/Berlin), and
`refs/tags/v0.17.0` resolving directly to the same approved commit.
The separate `github_release` object retains that publication identity and URL.
A readiness approval alone must never set `released: true`.

Verification sources:
- https://github.com/tws9stmcbf-web/AkashicNET/issues/295
- https://api.github.com/repos/tws9stmcbf-web/AkashicNET/releases/397503809
- https://api.github.com/repos/tws9stmcbf-web/AkashicNET/git/ref/tags/v0.17.0

The validator pins this reviewed snapshot; it is not a general release state
machine or a live API check. Missing or contradictory readiness/publication
fields fail closed. Future transitions require separately verified evidence and
reviewed contract changes. The historical v0.16 manifest and sealed baselines
are unchanged. BQ001 remains UNRESOLVED, `supports_models=[]`, accepted canonical
edges 0, Reddit live access HOLD, and every existing promotion boundary closed.
