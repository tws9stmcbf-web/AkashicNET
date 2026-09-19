# AkashicOMNI v0.5.0: Claim Review Records

**UNRELEASED development proposal · 19 September 2026**

## Purpose and baseline

Add traceable claim records and comparison between independent assessments to the existing thirteen-perspective method. The baseline is AkashicOMNI v0.4.0 PRE-ALPHA, reconciled with the published source by PR #366. AkashicNET product versions and the legacy evidence/provenance v0.5 contract are separate.

This document is the canonical proposed specification for this development slice. The JSON Schema is its executable record contract. Passing validation or merging this packet does not release v0.5.0.

## Record contract

Every claim has a stable ID, exact wording, kind, source references, outcome definition, supporting observations, counter-evidence, counter-evidence search status, competing explanations, missing evidence, reviewer assessments and revision history. Sources retain a URL, location, access status, provenance note and explicit unassessed rights status.

- Separate observations, model estimates, projections, testimony, causal hypotheses and mechanism hypotheses.
- Separate different endpoints, baselines and time windows into distinct records.
- Corrected wording retains its claim ID and an appended revision. A substantially different proposition receives a new ID. Never recycle IDs.
- An empty support list means no supporting observations entered. An empty counter-evidence list with NOT_COMPLETED is an incomplete search, not evidence of absence.
- NOT_REINSPECTED sources require a missing-evidence entry and cannot populate supporting observations. Full-text access alone does not establish validity or reuse rights.
- Review decisions remain REVIEW_REQUIRED and claims remain UNRESOLVED throughout this draft contract.

The schema rejects unknown fields. Identifiers must be unique within their defined scope: claim and source IDs across the packet; assessment and current reviewer IDs within each claim. Source references must resolve. Revision numbering starts at one and is sequential; dates cannot move backwards. Git history supplies the prior snapshots needed to audit append-only history, which cannot be proven by a single packet.

## Independent assessment comparison

Assessments identify a pseudonymous reviewer, HUMAN or AI, a decision (SUPPORT, CHALLENGE or INSUFFICIENT), rationale, source locations and an independence declaration with a note. These are reviewer positions, not evidence-admission decisions.

The comparison function deterministically compares all pairs of distinct human reviewers who declare independence. It records decision agreement or disagreement. A recorded comparison requires at least two such reviewers and must include every computed pair. Decision agreement requires an explanatory agreement entry; decision disagreement requires a disagreement entry. Substantive differences can remain in the disagreement notes even when the categorical decisions agree.

AI assistance cannot declare independent human review. Two model responses are not two independent scientific reviews. Real reviewer identity, expertise, independence and source access require human verification; this validator does not authenticate them. No reviewer names, emails or private contact details are needed in the public record.

Pending comparisons contain no results. The real pilot contains no assessments and no claimed completed comparison. Synthetic reviewers appear only in regression tests. Independent methodological review and the release decision remain pending even if claim-level comparisons are later recorded.

This first slice supplies a format, validator and deterministic decision-comparison function. It does not supply a reviewer interface, recruitment, a scientific scoring system or an inter-rater reliability estimate. A reliability statistic would need a separately specified sampling and rating protocol with an adequate real assessment set.

## Meditation–crime pilot

The five records in `data/akashicomni/meditation-crime-pilot-v0.5.0.json` are derived from the 19 September article revision 0.1, not new primary research. Numerical statements are explicitly attributed to the editorial draft. Primary-paper inspection was not repeated for this implementation, and access is marked NOT_REINSPECTED.

The records distinguish two model estimates, a long-term projection, causal attribution and the proposed nonlocal mechanism. The 15.6% entry preserves the article's correction: final-week peak, not a gathering-wide average. It supersedes the earlier PDF's less precise wording for this pilot; the historical PDF is not silently rewritten. This is a bounded pilot, not exhaustive coverage of the article.

The inquiry has no BQ ID and does not reuse BQ011. Missing original-data reproduction and independent replication review remain explicit. An empty counter-evidence list reflects an unfinished search.

## Boundaries

The packet is UNRELEASED and REVIEW_REQUIRED. `accepted_edges` and `supports_models` remain empty. Truth, evidence, rights, public-synthesis, website and BQ-resolution promotion remain false. No maturity level is assigned. No historical assessment is recalculated and no product version or website changes.

The v0.4.0 Embodied Intelligence pathway and all thirteen perspectives remain intact. The proposed HIERATIC015C1 connection between embodied intelligence and wisdom is an interpretive application, not an empirical finding or an extra framework release.

The strict draft schema intentionally cannot represent a released or promoted packet. Release requires a separately reviewed change, not flipping a field. Structural validation does not verify scientific truth, prose accuracy, reviewer independence or legal reuse rights.

## Acceptance before release

- [x] Reconcile v0.4.0 current references with the published source (PR #366).
- [x] Implement a draft specification, schema, validator, decision comparison and bounded pilot.
- [ ] Review and adopt the canonical specification.
- [ ] Reinspect primary-source locations and record evidence and rights limits.
- [ ] Obtain real independent assessments and preserve their disagreements.
- [ ] Complete independent methodological review, including reviewer-independence verification.
- [ ] Pass validation on the exact reviewed commit.
- [ ] Record the project owner's explicit release decision and dated release note, including any effect on previous assessments.

## Run validation

Requires Python 3.11+ and jsonschema 4.26.0.

```sh
python scripts/validate_akashicomni_claim_review_v050.py
python -m unittest discover -s tests -p 'test_akashicomni_claim_review_v050.py'
```

The validator also accepts one packet path as a positional argument. Malformed, missing or invalid input fails. It never writes to the packet, a registry or a website.
