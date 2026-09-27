# COA-001 Stage-2 Statistical Analysis Plan

**Module:** SAP-001  
**Version:** 0.1  
**Date:** 2026-09-17  
**Draft amendment:** 2026-09-24 · INT-001 v0.2 alignment; no operational authorisation  
**State:** DRAFT FREEZE CANDIDATE / INDEPENDENT STATISTICAL REVIEW REQUIRED  
**Parent protocol:** COA-001 v0.1  
**Related modules:** EAP-001 v0.1 · INT-001 v0.2 · SDC-001 v0.1 · TS-001 v0.1  
**Governance:** Issue #356 · Draft PR #357

## Status and purpose

SAP-001 specifies a candidate confirmatory endpoint and analysis contract for Stage 2. It is designed to make target correspondence testable without treating correspondence as direct observation of awareness.

This document is not yet a preregistration or operational authorization. It becomes frozen only after independent statistical review, successful reproduction of SIM-001, Stage-1 feasibility, ethics/IRB approval, prospective registration and a versioned protocol amendment. No real participant data may be inspected to tune this plan.

The plan follows the principle that the population, variable, intercurrent-event strategy, summary measure and sensitivity analyses must be aligned before data interpretation. It is informed by [ICH E9(R1)](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf).

## Confirmatory question

Among participant-events with an auditable target sequence displayed during the prespecified resuscitation interval and a primary locked interview, does the true sequence rank higher for correspondence with the locked free-recall claim set than it would under exchangeable assignment among one true and five transcript-independent decoy sequences?

This is a correspondence question. A positive result cannot by itself establish awareness during resuscitation, continuity, personal survival or an afterlife.

## Primary estimand EF-2R

| Attribute | Frozen candidate definition |
|---|---|
| Population | `TARGET_EXPOSED`: `ALL_INTERVIEWED` participant-events with an independently auditable target sequence displayed during the prespecified interval |
| Unit | Participant, giving equal participant weight after within-participant aggregation of repeated eligible events |
| Variable | Mean pre-adjudication normalized rank utility of the true candidate across two independent blinded scorers |
| Candidate set | Six candidates: one true sequence and five transcript-independent decoys |
| Intercurrent-event strategy | Treatment-policy-like retention of scoring failures and critical integrity states inside `TARGET_EXPOSED`; flow and bounds analyses for events outside it |
| Summary | `delta = mean(U_participant) - 0.5` |
| Null | Candidate truth labels are exchangeable within each committed six-candidate packet |
| Alternative | True candidates have higher normalized rank utility |
| Interpretation | Conditional correspondence estimand only; no prevalence or continuity inference |

`TARGET_EXPOSED` is a post-event operational stratum and may be selected by device performance. Therefore every report must also show the full `ALL_ELIGIBLE_EVENTS` and `ALL_INTERVIEWED` flow, target-exposure yield and unresolved-state bounds. The conditional primary estimand cannot be generalized to all arrests or survivors.

## Primary outcome construction

### Candidate ranking

Each independent scorer ranks all six masked candidates using the locked SDC-001 rubric and transcript-only claim table.

- Rank 1 is the strongest correspondence.
- Rank 6 is the weakest correspondence.
- Ties receive their midrank.
- Free-narrative and prompted free-recall claims contribute to the primary ranking.
- Forced-choice recognition is excluded from the primary ranking and analysed separately.
- Scorers complete and lock rankings without truth-position access.
- Primary inference uses the two original independent scorer rankings, not the adjudicated ranking.

For candidate rank `R`, normalized utility is:

`U = (6 - R) / 5`

Thus `U = 1` for an untied best rank, `U = 0` for an untied worst rank and the exchangeable null expectation is `0.5`.

For each participant-event, the primary value is the mean of the two scorers’ true-candidate utilities. Repeated participant-events are averaged within participant before the study mean is calculated. Each participant therefore has total weight one.

### Primary-source compatibility with INT-001 v0.2

The candidate endpoint retains one true plus five decoy sequences, two original blinded scorer rankings, normalized rank utility, equal participant weighting and one-sided alpha 0.025. Recognition remains excluded from primary ranking.

INT-001 v0.2 moves structured phenomenology and target-directed prompted recall into L2. Therefore the phrase “prompted free-recall claims” cannot automatically include all material available in the earlier interview sequence.

Before prospective freeze, independent statistical/methods review MUST:

1. enumerate eligible L1 elicitation classes and excluded L2/recognition classes;
2. define the rule for audit-elicited and closing-addition content;
3. review the effects of the revised source set on scorability, ties, missingness and anticipated information yield;
4. assess the applicability of SIM-001 assumptions and reproduce or revise simulations if required;
5. align population membership and failed-lock treatment with EAP-001 and the machine-readable contract;
6. freeze rules without inspecting real participant outcomes.

Until then, primary-source compatibility is HOLD. The historical calculation of 132 independent rank contributions is not validated for the revised source workflow. The participant-level stopping rule below supersedes the former participant-event boundary.

If a designated interview lacks a valid L1, do not reconstruct claims. Apply existing unresolved/critical-integrity handling only inside an already established and lawfully usable TARGET_EXPOSED record. If exposure or data-use authority cannot be established without prohibited access, keep that status unresolved and processing blocked; do not assume exposure to force the record into a scoring population.

### Null and non-scorable reports

- A locked null report gives every candidate a tie and `U = 0.5`.
- A report declared non-scorable under a frozen reason remains in the flow ledger and receives `U = 0.5` in the primary `TARGET_EXPOSED` analysis.
- A missing scorer record receives the available scorer value if one valid blind score exists; if neither exists, `U = 0.5`.
- A critical integrity breach inside `TARGET_EXPOSED` receives `U = 0.5` for the primary analysis and `U = 0` and `U = 1` in worst/best-case bounds.
- No missing, failed or breached record may be silently deleted.

The neutral assignment prevents scoring failure from manufacturing positive correspondence. Bounds expose how conclusions depend on unresolved records.

## Primary test

The primary test is a conditional randomization test at one-sided `alpha = 0.025`.

1. Keep every locked scorer ranking, participant cluster, site, packet and candidate set fixed.
2. Under the null, enumerate or reproducibly sample each of the six candidate positions as the truth position within every packet.
3. Recalculate within-participant aggregation and the study mean for each assignment.
4. The p-value is the proportion of null assignments with a statistic at least as large as observed.
5. When complete enumeration is computationally impractical, use at least 1,000,000 seeded draws plus the observed assignment, with the Monte Carlo error and seed commitment reported.
6. The analysis code, seed derivation and synthetic test vectors must be locked before unblinding.

The randomization distribution is generated from candidate labels inside each committed packet; it does not assume normally distributed scores. Sites remain fixed, and participant-event labels are permuted jointly through the participant-level aggregation.

## Effect estimate and uncertainty

Report:

- observed mean normalized utility;
- `delta = mean(U) - 0.5`;
- a two-sided 95% randomization-compatible confidence interval obtained by inversion where computationally feasible;
- participant-cluster bootstrap interval as a labelled secondary uncertainty analysis;
- site-specific estimates and intervals;
- empirical truth-rank distribution;
- number of ties, null reports, non-scorable reports and integrity states.

The minimum effect worth carrying forward for scientific review is provisionally `delta = 0.05`. The design target used for planning is `delta = 0.10`. These values require independent justification before freeze and are not awareness thresholds.

## Confirmatory success rule

Stage-2 confirmatory success requires all of the following:

1. one-sided randomization p-value `<= 0.025`;
2. observed `delta >= 0.05`;
3. the primary conclusion remains directionally positive under the prespecified neutral-missing and participant-cluster analyses;
4. no unresolved systemic leakage, truth-position exposure or decoy-exchangeability failure;
5. every prerequisite validity gate was passed before unblinding;
6. the complete flow, negative controls and all prespecified sensitivity analyses are reported.

Failure of any condition means the confirmatory criterion is not met. It does not automatically falsify awareness; the result must be classified as valid null/negative, underpowered, infeasible, compromised or not evaluable under the frozen rules.

A successful single study is only a review candidate. Independent preregistered replication is required before any comparative-model review, and BQ001 cannot update automatically.

## Sample-size rule

SIM-001 evaluates a six-candidate rank test under two stylized alternative families. For a planning effect of `delta = 0.10`, the more conservative model requires:

- **97 independent rank contributions for at least 80% power in that model**;
- **132 independent rank contributions for at least 90% power in that model**.

The Stage-2 planning floor is **132 unique `TARGET_EXPOSED` participants**, counted once each regardless of repeated events. Before recruitment, independent reproduction and a blinded Stage-1 simulation update must determine and freeze the required unique-participant target (at least 132) for the participant-weighted endpoint, including scorer dependence, repeated events, ties, missingness and site effects. The simple rank calculation alone does not establish 90% power for that endpoint; recruitment remains blocked until this review and freeze are complete.

This is not 132 eligible arrests. The number of `ALL_ELIGIBLE_EVENTS` required depends on survival, approach, consent, interview, activation and valid-exposure yields. Stage 1 must estimate those yields with uncertainty before an ethical maximum accrual cap and duration can be set.

Stage 2 must use a dual stopping boundary fixed before recruitment:

- stop accrual when the frozen unique-participant information target (at least 132 unique `TARGET_EXPOSED` participants) is reached; repeated events never increment this count; or
- stop at the earlier maximum eligible-event count or calendar date derived from Stage-1 yield and ethics review.

Reaching the ethical count/date cap below the information target is an underpowered/infeasible stop, not information-target attainment. All eligible events accrued before stopping remain in the ledger. Accrual staff and oversight bodies must remain blinded to correspondence outcomes. There is no early stopping for efficacy or futility based on correspondence scores.

## Repeated events, sites and clustering

- The participant is the primary weighting unit.
- Multiple eligible arrests for one participant are retained and averaged within participant.
- The event-level result is a sensitivity analysis.
- Pooled and by-site results are mandatory.
- Leave-one-site-out analyses assess site dominance.
- A site with a critical unresolved leakage route is paused; affected records remain visible and enter prespecified bounds.
- No site may be removed because its observed correspondence is inconvenient.

If repeated events are more common than assumed, SIM-001 must be rerun using the observed blinded cluster-size distribution before unblinding to assess achieved information; this does not authorize an outcome-informed target change or accrual extension.

## Multiplicity

There is one confirmatory endpoint, EF-2R, tested at one-sided `alpha = 0.025`.

The following are secondary or exploratory and do not create additional confirmatory claims:

- adjudicated-rank analysis;
- recognition-only correspondence;
- auditory-channel correspondence;
- exact/partial atomic-claim scores;
- visual-claim subgroup;
- phenomenology scales;
- target-epoch or content-class analyses;
- site and demographic subgroups;
- post-lock amendments.

If any secondary outcome is promoted to confirmatory status, a new SAP version must define a closed testing or other justified family-wise-error procedure before unblinding.

## Validity gates and negative controls

Before primary unblinding, an independent committee confirms:

- candidate sets and manifests verify;
- claim and score locks precede truth release;
- decoy-generation test vectors reproduce;
- no unresolved unauthorized plaintext access exists;
- metadata and presentation symmetry tests pass;
- scorer-blinding assessments are complete;
- the analysis implementation reproduces synthetic expected results.

Prespecified negative controls include non-displayed sequences, non-overlapping windows, shuffled claim-to-packet assignments and recognition-only contrasts. Control results are reported with effect estimates and Holm-adjusted p-values within the control family.

A negative-control effect at least as large as the primary effect, or any Holm-adjusted control p-value `<= 0.05`, triggers `PAUSED_PENDING_ADJUDICATION`. Confirmatory interpretation is withheld until a blinded independent review determines whether the primary result remains identifiable.

## Sensitivity and supplementary analyses

Mandatory sensitivity analyses:

1. neutral assignment for unresolved primary values;
2. worst/best-case unresolved-state bounds;
3. per-protocol target-exposed records, labelled supportive only;
4. single-scorer analyses;
5. adjudicated-rank analysis;
6. event-weighted rather than participant-weighted analysis;
7. leave-one-site-out analysis;
8. free-narrative-only claims;
9. exclusion of recognition-derived content;
10. exclusion and stratification by contamination state;
11. alternative tie conventions fixed before unblinding;
12. exact enumeration versus seeded Monte Carlo where both are feasible.

Mandatory flow analyses:

- `ALL_ELIGIBLE_EVENTS` through every denominator state;
- `ALL_SURVIVORS`;
- `ALL_APPROACH_ELIGIBLE`;
- `ALL_INTERVIEWED`;
- exposure, interview and scoring yields with uncertainty;
- explicit `UNKNOWN` and `UNRECOVERABLE` counts.

Death, no interview, failed activation and unknown exposure are not ordinary missing primary scores; they are distinct flow outcomes that delimit the conditional estimand.

## Falsification and interpretation classes

| Outcome | Classification |
|---|---|
| Valid study, confirmatory rule met, controls clean | Correspondence signal; replication required |
| Valid study, rule not met with adequate information | Failure to detect the prespecified effect |
| Confidence interval excludes effects at or above the frozen minimum | Evidence against effects of that magnitude under this design |
| Excess negative-control correspondence or leakage association | Evidence against anomalous-correspondence interpretation |
| Severe attrition, inadequate exposure yield or scoring failure | Protocol infeasible or under-informative |
| Critical unresolved unblinding or decoy failure | Compromised / not evaluable |
| Independent preregistered replication fails | Counts against a robust replicable correspondence effect |

None of these classes directly proves or disproves awareness, continuity, personal survival or an afterlife.

## Analysis-lock and change control

Before any truth-position release:

- protocol, SAP, SDC-001 and simulation versions are fixed;
- code and dependency manifests are hashed;
- synthetic test outputs are independently reproduced;
- population membership is locked without scores;
- deviations and integrity states are locked;
- database snapshot and analysis decision log are signed;
- the independent statistician confirms readiness;
- prospective registration timestamp precedes unblinding.

Any later change is versioned, justified and labelled post hoc. Primary results under the frozen plan remain reported.

## Required independent review

SAP-001 requires review by:

- an independent statistician experienced in randomization inference;
- a psychometric or blinded-assessment specialist;
- a clinical-trial methodologist;
- an information-security reviewer;
- the ethics/data-protection pathway for data use and stopping implications.

## Governance lock

- BQ001 status: **UNRESOLVED**
- BQ001 depth: **Level 6/10**
- Accepted canonical edges: **0**
- `supports_models`: **[]**
- Truth inference: **OFF**
- Scientific-evidence promotion: **OFF**
- Rights/public synthesis: **OFF**
- Website promotion: **OFF**
- Recruitment: **NOT AUTHORIZED**
- COA-001 state: **DRAFT / PROTOCOL-FEASIBLE NOT YET ESTABLISHED**

SAP-001 is a method-development artifact, not a result or evidence of continuity.


