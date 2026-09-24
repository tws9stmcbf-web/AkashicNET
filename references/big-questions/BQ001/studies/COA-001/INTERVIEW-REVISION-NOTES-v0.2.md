# INT-001 v0.2 integration notes

Date: 24 September 2026. Status: DRAFT / STAGE 0.

The previous interview order presented recognition choices before its sole transcript lock. TS-001 and DFL-001 prohibited the target/candidate access needed for that order. This revision protects a primary account and audit at L1, locks transcript-only claims at C1, and keeps later structured material separately locked at L2. Recognition remains NOT AUTHORISED pending its own reviewed access and analysis contract.

The v0.1 manual remains as a labelled historical draft. The JSON contract and current companion references point to v0.2. The synopsis, TS-001, DFL-001, SDC-001, EAP-001, SAP-001 and ethics outline contain coordinated draft amendments. These are not operational permissions.

Completion and lock success are now distinct. A failed primary lock cannot be hidden by defining the interview out of the completion denominator or selecting a later cleaner account. Unknown blinding and exposure remain explicit. Post-lock contamination can block interpretation without rewriting the original source or score.

## Review holds

- Exact eligibility of prompted L1 claims, including audit-elicited and closing additions, remains unfrozen and requires independent statistical/methods review.
- L2 and recognition content cannot enter the primary claim packet.
- Recognition remains blocked; no new data-flow route is granted.
- Clinical windows, interrupted-session rules, consent, burden limits, implementation, schema enforcement and independent validation remain pending.
- Numerical endpoint, candidate count, alpha, effect thresholds, feasibility percentages and simulation outputs remain unchanged. Their applicability to the revised source set requires review.

## Checks performed

- Parsed the revised JSON and verified module paths, local document links and Markdown fences.
- Compared baseline and revised JSON: stages, eligibility, estimands, feasibility gates, primary statistical hypothesis, operating characteristics and falsification/classification contract are unchanged.
- Confirmed all existing parent-question status/edge/model/promotion fields remain unchanged except the bounded Level 8/10 to Level 6/10 reconciliation required by issue #363.
- Confirmed recognition execution and primary-source freeze remain false and permitted flow count stays 17.
- Reviewed fictional cases at document level: null recall, pre-interview disclosure, family cue, L2-added detail, early candidate exposure, failed first lock, uncertain timestamp order, late contamination, withdrawal and blocked recognition. This was not an implementation test or clinical rehearsal.
- Fictional denominator check: two compliant locks among three completed interviews is 2/3, not 2/2; a zero completed-interview denominator is NOT_EVALUABLE.

Repository-wide CI is reported separately for the resulting commit. No independent clinical, ethics, security or statistical sign-off is claimed.

## Static regression guards added

`scripts/validate_coa001_stage0_v02.py` checks the versioned Stage-0 subset of the JSON contract: closed authority and promotion fields, BQ001 unresolved at Level 6/10, primary sequence, unresolved source eligibility, recognition exclusion, reference/header consistency and flow-accounting rules. The new `flow_accounting` fields make explicit the existing restrictions on lock-filtered denominators, replacement interviews, unknown blindness and zero-denominator passes. No scientific or numerical endpoint changes are introduced.

Run from the repository root:

```sh
python scripts/validate_coa001_stage0_v02.py
python -m unittest discover -s tests -p 'test_coa001_stage0_v02.py' -v
```

The dedicated read-only GitHub workflow runs these checks on relevant PR changes and main-branch updates. Local validation and 32 regression tests passed when added. Negative cases cover missing/mistyped/open gates, old recognition/audit order, failed-lock selection, silent source freeze, stale references, missing/symlinked manuals, malformed/duplicate/non-finite JSON, and Python optimisation bypass.

Coverage is deliberately bounded. It does not validate every JSON field, arbitrary prose, statistical adequacy, actual access permissions, clinical conduct or hospital systems. Header checks are not semantic review. Exact versioned source and order values require a deliberate validator update if changed through governed review. CI configuration alone is not evidence that branch protection requires the check. Complete schemas, implementation and independent reviews remain pending; passing this validator grants no authority and cannot remove a review hold.

## Governance

COA-001 stays DRAFT / STAGE 0. Recruitment, live participant processing and recognition execution remain NOT AUTHORISED. BQ001 remains UNRESOLVED at Level 6/10. Accepted canonical edges are 0; supports_models is empty; truth inference, scientific-evidence promotion, rights/public synthesis, publication, deployment and other promotion gates stay closed. No results or participant data are introduced.
