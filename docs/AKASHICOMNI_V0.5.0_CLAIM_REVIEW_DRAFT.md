# AkashicOMNI v0.5.0: Claim Review Records

**UNRELEASED development proposal · 19 September 2026**

## Purpose and baseline

Add traceable claim records and comparison between independent assessments to the existing thirteen-perspective method. The baseline is AkashicOMNI v0.4.0 PRE-ALPHA, reconciled with the published source by PR #366. AkashicNET product versions and the legacy evidence/provenance v0.5 contract are separate.

This document is the canonical proposed specification for this development slice. The JSON Schema is its executable record contract. Passing validation or merging this packet does not release v0.5.0.

## Record contract

Every claim has a stable ID, exact wording, kind, source references, outcome definition, supporting observations, counter-evidence, counter-evidence search status, competing explanations, missing evidence, reviewer assessments and revision history. Sources retain a URL, location, source kind, access status, inspection-verification record (or null), provenance note and explicit unassessed rights status. Each claim names its editorial lineage source, which must also occur in its source references. Editorial sources require a repository artifact and SHA-256 digest; validation rejects missing artifacts and digest mismatches.

- Separate observations, model estimates, projections, testimony, causal hypotheses and mechanism hypotheses.
- Separate different endpoints, baselines and time windows into distinct records.
- Corrected wording retains its claim ID and an appended revision. A substantially different proposition receives a new ID. Never recycle IDs.
- An empty support list means no supporting observations entered. An empty counter-evidence list with NOT_COMPLETED is an incomplete search, not evidence of absence.
- NOT_REINSPECTED sources require a missing-evidence entry and cannot populate supporting observations. SUPPORT assessments require every referenced source, including editorial lineage, to be FULL_TEXT_INSPECTED with a HUMAN_VERIFIED inspection record resolved through the repository trust registry. ABSTRACT_ONLY access or AI inspection is insufficient. Full-text access alone does not establish validity or reuse rights.
- Review decisions remain REVIEW_REQUIRED and claims remain UNRESOLVED throughout this draft contract.

The schema rejects unknown fields. Identifiers must be unique within their defined scope: claim and source IDs across the packet; assessment and current reviewer IDs within each claim. Source references must resolve. Revision numbering starts at one and is sequential; dates cannot move backwards. Git history supplies the prior snapshots needed to audit append-only history, which cannot be proven by a single packet.

## Independent assessment comparison

Assessments identify a pseudonymous reviewer, HUMAN or AI, a decision (SUPPORT, CHALLENGE or INSUFFICIENT), rationale, source locations and an independence declaration with a note. Provenance is explicitly REAL_REVIEW or SYNTHETIC_FIXTURE, and reviewer verification is null until a human verification record exists. These are reviewer positions, not evidence-admission decisions.

The comparison function deterministically compares all pairs of distinct real human reviewers who declare independence and have HUMAN_VERIFIED reviewer-verification records. Synthetic fixtures are categorically rejected in governed packets, including pending comparisons, and can never supply eligible pairs. Missing, null or unregistered verification does not qualify; packet-controlled HUMAN, REAL_REVIEW and HUMAN_VERIFIED labels never authenticate a reviewer. It records decision agreement or disagreement. A recorded comparison requires at least two such reviewers and must include every computed pair. Decision agreement requires an explanatory agreement entry; decision disagreement requires a disagreement entry. Substantive differences can remain in the disagreement notes even when the categorical decisions agree.

AI assistance cannot declare independent human review. Two model responses are not two independent scientific reviews. Reviewer verification records identify a pseudonymous human verifier and a resolvable HTTPS record URL attesting identity and independence; self-verification is rejected. Source inspection uses the same record shape to attest source access. Real reviewer identity, expertise, independence, record authenticity and source access require human verification. The validator authenticates packet attestations only by exact resolution against `references/akashicomni/trusted-verifications-v0.5.0.json`, a fixed repository policy input, never a packet-supplied path or a fetched URL. These fields must never be filled by an AI to simulate completed human work. Test-only positive controls explicitly mock the registry in memory; the same synthetic packet fails against the real registry. No reviewer names, emails or private contact details are needed in the public record.

The trusted registry starts with empty `reviewer_attestations` and `source_inspections` arrays. No verification is admitted by this change. Only a separately reviewed repository change after actual human verification may add records; repository maintainers are the trust boundary. Copying a fixture into that registry would fabricate human review and is prohibited. Packet input and its author cannot select or populate the registry. Missing or malformed registry input fails closed.

Each trusted record contains `packet_id`, `subject_sha256` and the exact `verification` object. The digest uses UTF-8 JSON with sorted keys, ASCII escaping and compact separators. For inspections the subject is the complete source record, including URL, location, artifact digest and verification. For reviewers it is an object containing `claim` (all fields except assessments/comparison), `sources` (the complete packet source list), and `assessment` (the complete assessment). This binds identity, independence, decision and provenance to the actual claim and sources; changed content requires fresh verification. Reviewer and inspection records live in separate arrays and cannot substitute for one another. The record URL is a reference, not proof of authenticity. Both non-null untrusted attestations and SUPPORT without trusted full-text inspection of every source are rejected even while comparison is pending.

Pending comparisons contain no results. The real pilot contains no assessments and no claimed completed comparison. Synthetic reviewers appear only in regression tests and are tested as invalid governed records. Independent methodological review and the release decision remain pending even if claim-level comparisons are later recorded.

This first slice supplies a format, validator and deterministic decision-comparison function. It does not supply a reviewer interface, recruitment, a scientific scoring system or an inter-rater reliability estimate. A reliability statistic would need a separately specified sampling and rating protocol with an adequate real assessment set.

## Meditation–crime pilot

The five records in `data/akashicomni/meditation-crime-pilot-v0.5.0.json` are derived from the 19 September article revision 0.1, not new primary research. Numerical statements are explicitly attributed to the editorial draft. The original 11,392-byte input is preserved unchanged at `references/akashicomni/Meditation-Crime-AkashicOMNI-Article-Draft-2026-09-19.md` and registered as SOURCE-EDITORIAL-20260919 with SHA-256 `b660b86660af0c3d38979830646f8652274490d2707fc74ae32446fa0e3346ad`. All five claims reference both that lineage source and the primary paper. The recovered draft was inspected by AI for lineage, with human inspection verification left null. Its historical publication-status statements describe the 19 September snapshot, not current website state. Archiving it is not scientific verification or publication approval. Primary-paper inspection was not repeated for this implementation, and access is marked NOT_REINSPECTED.

The records distinguish two model estimates, a long-term projection, causal attribution and the proposed nonlocal mechanism. The 15.6% entry preserves the article's correction: final-week peak, not a gathering-wide average. It supersedes the earlier PDF's less precise wording for this pilot; the historical PDF is not silently rewritten. This is a bounded pilot, not exhaustive coverage of the article.

The inquiry has no BQ ID and does not reuse BQ011. Missing original-data reproduction and independent replication review remain explicit. An empty counter-evidence list reflects an unfinished search.

## Boundaries

The packet is UNRELEASED and REVIEW_REQUIRED. `accepted_edges` and `supports_models` remain empty. Truth, evidence, rights, privacy, cultural-authority, public-synthesis, website and BQ-resolution promotion are all required false gates. No maturity level is assigned. No historical assessment is recalculated and no product version or website changes.

The v0.4.0 Embodied Intelligence pathway and all thirteen perspectives remain intact. The proposed HIERATIC015C1 connection between embodied intelligence and wisdom is an interpretive application, not an empirical finding or an extra framework release.

The strict draft schema intentionally cannot represent a released or promoted packet. Release requires a separately reviewed change, not flipping a field. Structural validation does not verify scientific truth, prose accuracy, reviewer independence or legal reuse rights.

## Acceptance before release

- [x] Reconcile v0.4.0 current references with the published source (PR #366).
- [x] Implement a draft specification, schema, validator, decision comparison and bounded pilot.
- [ ] Review and adopt the canonical specification.
- [x] Recover the original editorial lineage artifact and verify its recorded digest.
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

## Full candidate reconciliation · 2 October 2026

This dated engineering and scope receipt supplements this slice; it neither adopts the full candidate nor changes the historical acceptance checklist above. AkashicOMNI v0.5.0 remains UNRELEASED / REVIEW_REQUIRED. The PR remains draft.

### Version and evidence anchors

- Pilot: PR #367 at `e7efb9266e265f229623e37fd320abde8f1fe74a`. Its `framework_baseline: 0.4.0` describes the historical pilot origin and remains unchanged.
- Current main reference inspected: `1b9ec981233fec78fde8d3099fc9ce71f14eea25`; `website/lib/akashicomni-release.ts` identifies v0.4.5 PRE-ALPHA. The broader candidate builds on that documentation baseline.
- Full candidate source: `AkashicOMNI-v0.5.0-Candidate-Specification.md`, saved version 14, operative rc.4 A, 28 September 2026; SHA-256 `243679e2930942ef0225fa8a26079924a5e4ac5974857a0a00ab7f49a4fd6729`. Source locator: https://chatgpt.com/api/library/files/libfile_a4632c9dcf88819196ed307679005ead/download . This authenticated locator may require access; preserve the cited version and digest. A mutable download URL alone is not a version pin.
- October 2 component audit, recovered-source receipts and T06S comparison are supplementary design/test records. They do not populate the pilot or the trust registry. Later public-method wording is not a separately accepted release.

### What is complete at this head

The closed schema, validator, five-claim pilot, editorial artifact/digest check, deterministic decision comparison and repository-held attestation authentication are implemented. Fresh local verification using Python 3.12 and jsonschema 4.26.0 passes the pilot and all 24 focused tests. All 15 returned exact-head pull-request workflows succeed; the connector returns the first page only. All seven returned inline threads are resolved. The 28 September exact-head Codex comment reports no major issues. Owner engineering sign-off is bounded to this correction, not human verification or release acceptance.

These dated results supersede earlier engineering-status summaries for this head only. Preserve the old 20-test and ancestry-failure receipts with their original commit scope. Any subsequent commit, including application of this addendum, needs its own applicable checks/review; the above approval does not carry forward automatically.

### Broader method represented, not certified

The baseline is ten analytical families, twelve analytical entries and one separately counted AkashicNET synthesis. CUT contributes three temporal views within one family. A claimed full reading records APPLIED, NOT_RELEVANT or INSUFFICIENT_INFORMATION for every analytical entry, with reasons and inspected source scope. Missing sources must not be described as irrelevant. An explicitly narrower user request may reduce scope with disclosure.

EXPAND² remains DISCERN plus DEEPEN, followed by synthesis. Synthesis is an output, not a third review pass. NOTICE, QUESTION, INTEGRATE, SYNTHESISE, CHOOSE, ACT, REFLECT, SHARE and CULTIVATE are optional inquiry/practice prompts: they may be skipped, combined, reordered or revisited. They are not nine mandatory stages, new perspectives, proven capabilities or executed real-world actions. Omitting the explicit SYNTHESISE prompt does not remove the full reading's synthesis output. Perspectives describe where attention goes; prompts describe how inquiry proceeds.

HOMESENSE Phase 8 is the current perspective. HOMESENSE700 v1.1 plus its v1.1.1 addendum supplies charter context; it does not replace Phase 8 or add another family. HOMESENSE enriches what AkashicOMNI considers; AkashicOMNI helps examine, organise and apply those contributions. A cross-post synthesis must identify each inspected post/version, distinguish repeated material from independent sources, preserve disagreements and limits, and disclose omissions. Future posts are candidate inputs, not automatic changes to the framework or evidence status.

Keep experience, accuracy, usefulness and proposed source distinct. Advice requires situational assessment; a prediction requires its own outcome and timeframe. Added test conditions must be labelled as added. Meaning, coherence, usefulness or a later favourable outcome does not establish the experience's proposed origin.

The rc.4 A source-plus-addendum manifest is retained: ACTC v2.0 + v2.0.1, METAD v2.1 + v2.1.1, UMASC v7.2 + v7.2.1, CUT header v4.0.3 + v4.0.4, HOMESENSE700 v1.1 + v1.1.1, optional PP v1.0 + v1.0.1, and separately attributed QMM with its dated correction. These represent six historical clarification locations (ACTC/PP share one), not fresh verification of current mutable text. Do not overwrite source-defined names with abbreviated companion descriptions or relabel original post headers as rewritten.

DARK is optional and adds one analytical entry: fourteen entries including synthesis when used. QM, MM and PP are optional ACTC modules, not additional numbered families. QM means Quantum Mechanics Interface and MM means Meaning & Memory Module in their source context. QMM is a distinct external hypothesis, not QM plus MM, a numbered OMNI family, or an established bridge to PP or personal survival. PP non-use is valid.

The inspected Jigsaw contains 47 theme/question entries (seven groups of six plus five connectors), not 47 OMNI frameworks or implemented modules. Living Spectrum, Jigsaw and Flourishing Matrix retain distinct identities. New links require source/target identifiers, source versions, relation type, provenance, limits and PROPOSED/UNRESOLVED status. No mapping is forced. Historical route/status label drift must be checked against current publication receipts before any later correction; route existence does not certify a framework. This reconciliation performs no website change or mapping admission.

### Existing manual gates and missing implementation

The full candidate already defines M01–M12. Retain those identifiers. This receipt does not replace their evidence records or mark them passed.

| Gate | Smallest representation now | Remaining acceptance work |
|---|---|---|
| M01 | Keep candidate revision, exact inputs and source digests in a separate manual record | Adopt one canonical full-candidate revision; bind each reading to it |
| M02 | Preserve candidate domain/support labels alongside pilot kind/decision | Review semantics; no automatic enum equivalence |
| M03 | Preserve access dates, inspected scope, dependence and rights limitations | Primary-source reinspection and actual rights assessment; historical receipts are not fresh inspection |
| M04 | Preserve alternatives, contrary information and unfinished searches | Semantic adequacy review; empty lists do not prove absence |
| M05 | Separate twelve-entry coverage ledger and one synthesis | Full-candidate coverage review; no pilot coverage fields |
| M06 | Separate optional-module and relationship records | Verify source-specific relationships; no default QMM–PP bridge |
| M07 | Separate narrative/record consistency review and revision conditions | Check two passes, alternatives, optional action and caveats |
| M08 | Keep actual assessments and both trusted arrays empty | Real independent assessments, identity/independence and source verification; AI cannot supply them |
| M09 | Keep pending comparisons empty; preserve prior records | Actual disagreements and review history; single-packet validation is not append-only storage |
| M10 | Preserve eight false gates, empty edges/models and fixed draft statuses | Separate explicit release decision; engineering checks are not promotion authority |
| M11 | Retain existing manual exercises and T06S at their disclosed scope | Equal-input version acceptance and actual human editorial feedback; no demonstrated superiority |
| M12 | State that no full-record adapter or deployment is supplied here | Validate a PRISM adapter or website only if that capability is later claimed |

The pilot rejects additional top-level `candidate_revision`, `perspective_coverage` and `optional_modules` fields. This is intended scope protection. Do not relax `additionalProperties`, silently discard fields or coerce candidate enums to make a full record pass. Keep manual records separate; unknown mappings stop interchange for manual review. A future machine-readable full contract or adapter requires a separately reviewed change.

### Release remains blocked

Canonical full-spec adoption, primary-source reinspection and rights limits, real independent assessments, independent methodological review, complete applicable manual-gate evidence, human editorial acceptance and a separate owner release decision remain absent or pending. Existing manual comparisons are AI self-review, not completed independent acceptance. Any full-candidate validation claim is unsupported by this pilot.

All five pilot claims remain UNRESOLVED / REVIEW_REQUIRED; assessments and comparison results remain empty. The trust registry's reviewer_attestations and source_inspections remain empty. accepted_edges=[] and supports_models=[]. Truth, evidence, rights, privacy, cultural_authority, public_synthesis, website and bq_resolution promotion remain false. No merge, deployment, publication authorization, scientific promotion or release is supplied by this record.

## Public specification implementation map · 8 October 2026 UTC

Assessment scope: the engineering files at `3ec6369f4025204924ec79cc233bf159a3eb40c4`,
compared with the [public manual specification](https://akashicnet.org/akashicomni/v0-5-0)
as retrieved on 8 October UTC (7 October in Los Angeles). This extends the existing
M01–M12 table above; it does not replace those gates or assert that any gate passed.

The public v0.5.0 manual specification is available for human-reviewed use. It was
published 1 October, clarified 2 October and updated with a researcher starter kit
7 October. [PR #398](https://github.com/tws9stmcbf-web/AkashicNET/pull/398), merged as
`bcfd82b2d4ce6d69ff8384b11477089e0c21afeb`, records that distinction in the website
mirror. The UNRELEASED statements in this engineering slice apply to its software
packet and acceptance process, not to availability of the public manual method.
The dated September/October 2 receipts and historical v0.4.0 baseline remain intact.

### Executable coverage versus remaining work

Paths below are relative to this repository. `S` means
`schemas/akashicomni-claim-review-v0.5.0.schema.json`; `V` means
`scripts/validate_akashicomni_claim_review_v050.py`. Presence of a field is not proof
that its content is adequate, independently reviewed or scientifically supported.

| Public specification area | Existing executable representation at the inspected head | Remaining gap / existing gate |
| --- | --- | --- |
| Claim wording, origin and separated claim kinds (§5) | S: `claims[].wording`, `kind`, `source_ids`, `lineage_source_id`; V checks references and editorial artifact digest | Candidate domain/evidence labels are not equivalent to pilot kinds or reviewer decisions; M02 remains manual |
| Method/record versions and scope (§5) | S fixes `format_version`, historical `framework_baseline` and target; packet/claim IDs and dated revisions exist | No public-method revision binding or reading-scope record; M01 |
| Source access and dependencies (§§4–5) | S has three access states, locations and provenance notes; V checks registered inspection attestations and blocks support without trusted full-text inspection | No typed source-dependency graph, inspection date or full set of public access states; primary source remains NOT_REINSPECTED and rights NOT_ASSESSED; M03 |
| Alternatives and contrary information (§§3–5) | S requires competing explanations and tracks unfinished counter-evidence searches and missing evidence | Adequacy and dependency-aware interpretation are not machine verified; M04 |
| Twelve-perspective coverage and synthesis (§§2–3) | No coverage or synthesis fields in S; EXPAND² is documented but not executed by V | Cannot record APPLIED / NOT_RELEVANT / INSUFFICIENT_INFORMATION for a reading or its synthesis; M05 and M07 |
| Optional lenses and relationships (§6) | No optional-module or relation representation in S | Source-specific mapping remains manual; PRISM compatibility declarations are not executed OMNI readings; M06 and M12 |
| Reviewers and disagreement (§5) | V: `verification_record`, `trusted_verification`, `compare_assessments`; real registry arrays and pilot assessments are empty | Software checks are implemented; actual source/human verification, independent assessments and methodological review are pending; M08–M09 |
| Revision conditions and history (§§3,5) | S stores sequential dated `revision_history`; V checks numbering and dates | No dedicated conditions-for-revision field or cross-snapshot append-only enforcement; M07–M09 |
| Governance and effectiveness (evidence, record and review sections) | S fixes unresolved/draft states, empty edges/model support and eight false promotion flags | Privacy/cultural/rights decisions, equal-input evaluation, human acceptance and release authorization remain separate; M10–M12 |

### Smallest recommended next capability: a separate coverage record

Recommendation, not implemented or accepted: add a narrowly scoped, machine-readable
companion record for M01/M05, with a separate schema and read-only validator. Preserve
the existing claim packet and closed schema unchanged. This would make missing
perspective coverage inspectable without claiming full specification implementation.

- Bind the companion to the exact packet ID and SHA-256 of its file bytes, explicit
  claim IDs and the public method's version/revision reference. Binding must fail if
  the packet changes. Record the actual author type and date; never invent human review.
- Distinguish a full twelve-perspective reading from disclosed narrower scope.
  For full scope require each baseline perspective exactly once, its coverage state,
  nonblank reason and source-access context. For narrow scope identify exclusions and
  reasons explicitly. Missing material is insufficient information, not irrelevance.
- Keep synthesis separate from the perspective list. Require a synthesis with visible
  uncertainty for a record claiming a completed reading, without interpreting its
  presence as correctness, independent validation or permission to publish.
- Keep optional modules, source-dependency modelling and PRISM conversion outside this
  first slice. Unknown fields or mappings must fail, never be silently dropped/coerced.
- Return structural errors and unresolved manual checks only. Do not write to packets,
  trust registries, claim decisions, evidence/rights records, graph edges or websites.
  No coverage state may satisfy a human-verification or release gate.

Before defining new perspective identifiers, reconcile the existing twelve values in
[`compatible_omni_frameworks` on PR #379](https://github.com/tws9stmcbf-web/AkashicNET/blob/570aee1632fc036d8f114c0fa584ad6c198575a2/schemas/akashic-prism-inquiry-module-v0.1.schema.json).
That field describes module compatibility, not which perspectives were applied to an
exact claim packet. Its presence does not supply this missing coverage contract.
PR #379 also has `disconfirming_conditions`; that separate format is not automatically
interchangeable with this pilot. Neither branch is integrated by this recommendation.

Acceptance for that future engineering slice should exercise a complete structural
fixture, disclosed narrow scope, missing/duplicate/unknown perspectives, blank reasons,
unknown source/claim references, packet-digest mismatch and attempted promotion or
registry mutation. Fixtures must be explicitly synthetic and never populate governed
human assessments. Semantic adequacy of reasons, source access and synthesis remains
manual; structural success must not mark M01/M05 or other acceptance gates passed.

### Bounded verification of this map

At the inspected head, Python 3.12 with jsonschema 4.26.0 passed the unchanged pilot
validator and all 24 existing focused tests. Five in-memory extension probes were
rejected as unknown fields: top-level `candidate_revision`, `perspective_coverage`,
`optional_modules`, source `dependencies`, and claim `revision_conditions`. These
probes establish the closed-contract boundary, not an implementation of those features.
The original packet still validates; no probe was written into repository data.

The five claims remain UNRESOLVED / REVIEW_REQUIRED, actual assessments and trusted
verification arrays remain empty, primary-source reinspection remains outstanding,
and all eight promotion flags remain false. This addendum changes documentation only.
The new documentation head requires its own applicable checks and review. No earlier
approval transfers, and PR #367 remains draft, unmerged and unreleased.
