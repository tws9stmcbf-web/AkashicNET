# IONS Mind2Mind And AkashicNET: Evidence And Methods Comparison

3 November 2026 · Approved documentation update · **No participant results**

The user approved adding this dated comparison and the R1–R6 clarification checklist to draft PR #415, together with a short linked note on the public companion. This approval covers documentation only. It does not adopt a primary test, approve a final sample, preregister a participant study or authorise recruitment, a pilot or participant testing.

## Research Status

- Hypothesis: **UNTESTED**.
- Primary test: **UNRESOLVED_AFTER_CALIBRATION_STRESS**.
- Independent statistical review: **PENDING**.
- Both required population-mean criteria are retained.
- No empirical validation or IONS endorsement is claimed.
- Existing assessment files, numerical results, October addenda and simulation plans are preserved.

The comparison inspected PR #415 at commit [ef135589386c11196c199c3ee4defe7eb705c908](https://github.com/tws9stmcbf-web/AkashicNET/commit/ef135589386c11196c199c3ee4defe7eb705c908). The implementation is a synthetic methods assessment, not an audited participant-testing platform.

## Public Evidence And Publication Check

A search on 3 November 2026 did not locate an identifiable full methods-and-results paper or DOI for the 100-dyad Mind2Mind study described at TSC2026. Searches covered the programme name, remote intention discrimination, paired talent search and investigators, including official, publisher and preprint searches. The IONS publications page did not expose a browsable publication list in retrieval. **Non-discovery does not establish that the paper is unpublished.** Full Part 1 methods and results remain unavailable to this comparison.

The [official TSC2026 programme](https://tsc2026.org/workshops.html) reports remote testing in 100 screened dyads and an excess of receivers satisfying an above-chance criterion relative to a binomial reference. It does not provide the hit counts, effect estimate, uncertainty interval, precise decision rule or enough detail to reproduce that finding. This is preliminary conference reporting.

[IONS recruitment information](https://noetic.org/mind2mind/) describes adult bonded pairs or twins, mutually confirmed reported experiences and staged participation. Its recruitment goal and the conference report are separate statements; they do not supply an analysed-sample flowchart.

### Distinct Exploratory Follow-Up

[KPU registration 1107, version 1.3](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1107.pdf), submitted 30 September 2026, describes a separate exploratory Part 2 study. Its seven pages were inspected. It is not the full Part 1 results paper and explicitly disclaims confirmatory above-chance inference.

The planned follow-up selects about 20 high-performing Part 1 dyads. Two 10-trial blocks switch roles. Receivers give binary intention/not-intention responses while senders either direct positive intention or count backwards aloud by threes. Five labels of each type are shuffled per block, with private sender cues and separated partners. Unlogged responses are omitted from descriptive accuracy. These planned procedures and retrospective descriptions cannot substitute for the missing full methods of the conference study.

## Comparison And Transferability

| Dimension | Available IONS Reporting | AkashicNET Proposal And Consequence |
| --- | --- | --- |
| Selection | Screened experiential dyads; full flow, thresholds and selection timing unavailable for the conference result. | Define the population and eligibility before outcomes. Performance screening, if used, needs independent confirmatory trials. A selected population does not supply a general-population effect estimate. |
| Intended-action categories | The conference description does not list categories. | Retain up/down/left/right token-move targets. Binary detection of sending status would be a different endpoint. |
| Controls | A matched no-sending arm is not specified in the conference description. | Retain targets generated and sealed in both arms, shown only in sending trials, with a neutral sender prompt in control. An active cognitive task is a different contrast. |
| Randomisation | Target generator, probabilities, concealment and support unavailable for the conference finding. | Distinguish independently uniform four-category targets from exact within-session condition counts randomly interleaved. Audit the actual allocator. |
| Response distributions | Frequencies, confusion matrices and sequence data unavailable. | Report arm-specific target/response frequencies, exact matches, omissions and response runs. No post-outcome recoding or preferred-response exclusions. |
| Dependence | Trial/session dependence, reused people and the aggregation model unavailable. | Use the pair vector across all sessions as the independent unit. Prevent reused people across pairs. Specify session structure and carryover. |
| Above-chance meaning | An excess of threshold-crossing receivers is reported; aggregation details are unavailable. | Retain both equal-pair scheduled means. A count of individually significant receivers cannot establish both criteria. |
| Missingness | Conference-study rules unavailable. | Keep ordinary omissions distinct from technical aborts, lost logs, withdrawals and consent-required deletion. Complete-case scoring changes the estimand. |

Unavailable details are reporting gaps, not findings that IONS omitted the safeguards. Staged screening, explicit task definition, concealed allocation, audit trails and separately labelled subjective reports are transferable design principles. Their implementation and effects are not validated by the conference description.

## Statistical Meaning

For pair i, S_i and C_i are exact hits divided by all scheduled sending and control trials. Ordinary omissions score zero. The retained weak population-mean nulls are:

- H_A: E(S_i) <= .25.
- H_Delta: E(S_i - C_i) <= 0.

Both one-sided components must reject at .05 using prespecified methods. The intersection–union rule does not require a .025/.025 split for this single conjunctive claim, but it requires each true component to be valid. No favourable-method or sensitivity substitution is permitted.

A binomial reference for the count of successful receivers requires a defined analysis unit, calibrated individual rejection probabilities and appropriate independence. Unequal probabilities can require a Poisson-binomial or design-based reference. Illustratively, a one-sided exact .05 test on 10 independent fair binary trials rejects first at nine hits; its actual size is 11/1024, about 1.07%, not 5%. This is a mathematical illustration, not reconstructed IONS data.

With target–response independence, P(match) = sum(q_k r_k). Independent uniform four-category targets give .25 for complete responses regardless of response preference. Nonuniform targets, selective completion or information about restricted sequences require separate treatment. Balance alone does not establish an independent-trial binomial distribution.

Pair-summary methods need not assume independent trials within a pair. The bounded approach still requires independent pair vectors, trustworthy logs and an appropriate population target. Extra trials or switched roles do not create extra independent pairs. Target- and condition-shuffle sensitivities retain their distinct invariance/sharp-null roles; they are not automatic tests of weak population means.

The [retained alternative-method results](../design-assessment-2026-10-26/primary-alternatives/RESULTS.md) remain unchanged. Bootstrap-t has documented calibration failures. Fixed-mixture bounded-mean betting remains a provisional candidate with substantial power costs under specified assumptions. Conference reporting and synthetic performance are not independent validation. [Methods and review priorities](../design-assessment-2026-10-26/primary-alternatives/README.md) remain the source of the candidate definitions.

## R1–R6 Clarification Checklist

Approval adds this checklist to the research record. It does not resolve the open choices or certify that the audits have been performed.

| ID | Status | Clarification Or Required Work |
| --- | --- | --- |
| R1 | Existing design retained; comparison documented | Retain the four targets, sealed no-sending targets, scheduled equal-pair means and both criteria. The IONS receiver-count report cannot replace them. |
| R2 | OPEN before preregistration | Define eligibility, population, roles, prior experience, unique-pair rule and any screening. Separate performance selection from confirmation and retain the recruitment flow. |
| R3 | Existing safeguards retained; implementation/audit OPEN | Specify independent uniform targets separately from condition allocation. Document server concealment, receiver/staff blinding, timing, response lock, feedback embargo and leakage/abort rules. |
| R4 | Reporting requirements documented; operational rules OPEN | Add arm-specific target/response tables, omissions and sequence diagnostics. Freeze invalidation rules before outcomes. Confidence and subjective reports remain exploratory. |
| R5 | Independent-pair requirement retained; schedule/carryover OPEN | Keep the dyad as the independent unit across its sessions and prevent shared participants across pairs. Specify carryover/washout and session schedules. Any feasibility pilot requires separate approval. |
| R6 | Scheduled scoring retained; contingencies/gate OPEN | Distinguish omissions, aborts, lost logs, noncompliance, withdrawal and required deletion. Finalise the proposed integrity gate; report raw success, gate passage and their conjunction. |

Substituting binary state discrimination, selecting successful receivers, replacing scheduled denominators with completed-only scores, pooling all trials as independent or promoting a sharp-null shuffle would change the question or assumptions. Such redesigns are not adopted here.

Sending versus a neutral prompt does not isolate motor intention from target perception, imagery or other sender states. Positive intention versus mental arithmetic similarly bundles affective, attentional and cognitive differences. Mechanistic controls belong in a separately justified later design.

## Outstanding Review And Evidence

R7–R8 remain subsequent work: independent statistical review of the primary method, bounds, assumptions, implementation and uncertainty intervals, followed by final-test power/precision planning after effects and design choices are settled. No final test or sample has been adopted.

Still needed from the full IONS report:

1. Title/DOI, supplement, registration, task materials, code and data where consent permits.
2. Recruitment/exclusion flow, selection timing, analysis units and repeated participants.
3. Response categories, sender actions, controls, allocator, concealment, timing and feedback.
4. Response distributions, missingness rules, individual tests, aggregation, effect sizes and uncertainty.
5. Which procedures belong to Part 1 versus the distinct exploratory follow-up.

## Sources And Preserved Records

- [TSC2026 workshop programme](https://tsc2026.org/workshops.html).
- [IONS Mind2Mind recruitment](https://noetic.org/mind2mind/).
- [KPU registry](https://koestlerunit.wordpress.com/study-registry/registered-studies/) and [KPU1107](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1107.pdf).
- [Original 26 October assessment](../design-assessment-2026-10-26/README.md).
- [Primary alternatives and review boundaries](../design-assessment-2026-10-26/primary-alternatives/README.md).
- [Waudby-Smith and Ramdas: bounded-mean betting](https://arxiv.org/html/2010.09686v7).
- [Wu and Ding: randomisation tests for weak nulls](https://arxiv.org/abs/1809.07419).
- [Chung and Romano: robust permutation tests](https://arxiv.org/abs/1304.5939).
- [Public research companion](https://akashicnet.org/intention-awareness).

No private correspondence is reproduced. No additional messages were sent. This documentation update does not change existing numerical results, code, simulation plans, status files or promotion gates.
