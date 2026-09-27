# Public status contract

The authoritative display record is `website/data/public-status.json`. Its closed,
typed values distinguish the sealed baseline, unsealed candidate, site checkpoint,
and unreleased target. BQ001 remains UNRESOLVED, accepted edges remain zero,
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
layout and visible content are unchanged by this migration. Edit the templates,
not the generated pages. Releasing v0.17 still requires the separate release
process, exact-head validation and human approval.
