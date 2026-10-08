# FSC-001 — Falsification, Stopping and Outcome-Classification Rules

**Version:** 0.1  
**Date:** 2026-09-17  
**Draft amendment:** 2026-09-24 · canonical maturity wording per issue #363; all gates remain closed  
**State:** DRAFT / STAGE-0 / NOT PREREGISTERED  
**Parent protocol:** COA-001  
**Normative scope:** decision rules for feasibility, validity, stopping and interpretation  
**Operational use:** NOT AUTHORIZED

## Purpose

FSC-001 prevents an interesting narrative, a nominally significant result, a null result or an operational failure from being described more strongly than the design permits. It separates:

1. protocol infeasibility;
2. data that are invalid or not evaluable for the confirmatory question;
3. failure to detect the prespecified effect;
4. evidence that effects at or above the minimum meaningful bound are incompatible with the data under the frozen model;
5. a statistical correspondence signal;
6. a signal that remains blocked by leakage, timing, negative-control or robustness failures;
7. an anomalous-perception review candidate;
8. an independently replicated review candidate.

No COA-001 outcome directly falsifies or establishes awareness, consciousness, continuity, personal survival or an afterlife. The observable remains a later locked report and its correspondence with independently timed information.

## Non-negotiable boundaries

- Clinical eligibility is defined independently of device status, survival, consent, interview completion and data recoverability.
- Unknown, unrecoverable, failed and breached states remain in every applicable denominator.
- Safety, ethics, privacy and critical-integrity failures cannot be offset by a target match.
- No outcome-informed change to eligibility, target exposure, scoring, decoys, analysis populations, minimum effect, alpha, missingness rules or stopping rules is permitted.
- No unblinded efficacy or futility monitoring is permitted.
- A single case, striking narrative, subgroup or secondary endpoint cannot replace the confirmatory result.
- Positive, null, infeasible, contradictory and invalid results must all be reported.
- BQ001 and every AkashicNET promotion gate remain outside this protocol's automatic control.

## Ordered decision process

The classification authority applies the following order. A later step cannot cure a failure at an earlier step.

1. **Authority and participant protection:** confirm approvals, consent/data-use authority, safety oversight and permitted processing.
2. **Denominator integrity:** reconcile the independent eligible-event source with the protocol ledger.
3. **Operational feasibility:** apply every mandatory Stage-1 gate using EAP-001.
4. **Confirmatory validity:** verify exposure, locks, blinding, exchangeability, leakage, negative controls and analysis reproducibility.
5. **Statistical result:** apply the frozen SAP without outcome-informed amendment.
6. **Robustness:** evaluate prespecified neutral, bounded, participant-cluster, site and unresolved-state analyses.
7. **Interpretation:** assign exactly one primary outcome class and all applicable secondary flags.
8. **Replication status:** evaluate only after a valid primary interpretation exists.
9. **Governance:** submit any eligible review candidate to independent governance; never update BQ001 automatically.

## Readiness and validity states

### Pre-recruitment states

| State | Meaning | Required action |
|---|---|---|
| `STAGE_0_DRAFT` | Design artifact only | Continue bounded development |
| `RECRUITMENT_NOT_AUTHORIZED` | One or more approvals or commissioning gates absent | No recruitment |
| `SITE_NOT_AUTHORIZED` | Site annex, ethics, regulatory, DPIA, clinical or security gate incomplete | Site may not activate |
| `READY_FOR_PREREGISTRATION_REVIEW` | Frozen candidate package complete, independently reviewed | Governance review only; not recruitment |
| `RECRUITMENT_AUTHORIZED` | Competent external authorities and all frozen gates approve | May be assigned only outside AkashicNET governance |

This document cannot assign `RECRUITMENT_AUTHORIZED`.

### Event/study validity states

| State | Meaning | Confirmatory use |
|---|---|---|
| `VALID_FOR_FROZEN_ANALYSIS` | All applicable locks, exposure, integrity and analysis prerequisites pass | Include under frozen SAP |
| `VALID_WITH_PRESPECIFIED_SENSITIVITY_FLAG` | Noncritical uncertainty handled by a frozen sensitivity/bound | Primary handling follows SAP; flag retained |
| `HELD_PENDING_ADJUDICATION` | Material fact unresolved without authorized resolution | No release or interpretation |
| `NOT_EVALUABLE` | Required denominator, information or endpoint condition is absent without a critical breach | Report flow; do not call positive or negative |
| `INVALID_FOR_CONFIRMATORY_INTERPRETATION` | Critical leakage, exchangeability, premature-unblinding or analysis-integrity failure | Retain and report; no confirmatory claim |
| `SAFETY_PRIVACY_OR_AUTHORITY_STOP` | Participant protection or legal/ethical authority failed | Stop affected activity immediately |

Invalidation concerns the confirmatory interpretation; it never deletes an eligible event from the flow ledger.

## Primary outcome classes

Assign exactly one class to the study's primary visual-target result after the ordered decision process.

| Code | Class | Decision rule | Permitted statement |
|---|---|---|---|
| `C0_NOT_STARTED` | No operational study | Recruitment never began | No result exists |
| `C1_PROTOCOL_INFEASIBLE` | Feasibility failed | One or more mandatory Stage-1 gates fail or remain not evaluable at the frozen decision point | The protocol was not shown feasible; no efficacy inference |
| `C2_CONFIRMATORY_INVALID` | Critical validity failure | Systemic leakage, exchangeability failure, premature truth access, irreproducible scoring/analysis or another frozen critical condition | The confirmatory question cannot be interpreted |
| `C3_VALID_NULL_IMPRECISE` | No detected effect, insufficient precision | Frozen test does not reject and the prespecified upper bound does not exclude the minimum meaningful effect | No prespecified effect was detected; meaningful effects remain unresolved |
| `C4_VALID_BOUND_BELOW_MINIMUM` | Adequately precise negative result | Frozen test does not reject; required information and validity gates pass; and the prespecified one-sided upper confidence/compatibility bound is below delta 0.05 | Under this protocol, effects at or above the frozen minimum were not supported |
| `C5_STATISTICAL_SIGNAL_ONLY` | Confirmatory statistical criteria pass | SAP significance and minimum-effect criteria pass, but anomaly-level interpretation prerequisites are incomplete | A preregistered correspondence signal was observed; interpretation remains open |
| `C6_SIGNAL_INTERPRETATION_BLOCKED` | Signal plus rival-pathway/control failure | Statistical criteria pass but a frozen leakage, timing, negative-control, site-dominance, missingness or robustness rule fails | The signal cannot support an anomalous-perception interpretation |
| `C7_ANOMALY_REVIEW_CANDIDATE` | Valid single-study anomaly candidate | Statistical criteria, minimum effect, validity gates, negative controls and all mandatory robustness analyses pass with no unresolved critical route | The result is eligible for independent anomaly review; it does not establish continuity |
| `C8_INDEPENDENTLY_REPLICATED_REVIEW_CANDIDATE` | Independent replication criterion met | At least one qualifying independent preregistered replication reaches C7 under the rule below | Eligible for comparative-model governance review; no automatic BQ001 update |

C4 is a statement about effects at or above the frozen bound under this design. It is not evidence that awareness was absent, because survival, encoding, memory and reportability remain necessary selection mechanisms.

C5 cannot be reported as C7 while any anomaly-level prerequisite is incomplete. C6 takes precedence over C7 whenever a blocking failure is present.

## Feasibility failure rules

Classify the programme as `C1_PROTOCOL_INFEASIBLE` at the frozen Stage-1 decision point when:

- any mandatory EAP-001 gate is `FAIL`;
- a mandatory gate remains `NOT_EVALUABLE`;
- any site has an unresolved critical safety, care-interference, privacy, authority, denominator, leakage or premature-unblinding event;
- the minimum evaluable counts approved after simulation are not reached within the ethics-approved event/calendar cap;
- the target-exposed yield makes the confirmatory information target infeasible within the approved burden cap; or
- required clinical, statistical, ethics/privacy or security reviewers do not authorize progression.

The team may redesign a later protocol version. It may not relabel the failed version feasible.

## Negative-control and rival-pathway rules

Before recruitment, the SAP and commissioning package must freeze tests, units, thresholds and multiplicity handling for:

- non-displayed decoy sequences;
- off-interval target windows;
- sham/non-activation records where ethically and technically valid;
- metadata-only truth-position distinguishability;
- blinded scorer truth-position guessing;
- interviewer, scorer and analyst blinding assessments;
- site and device configuration effects;
- access-log, contamination and timing indicators;
- auditory results interpreted through ordinary auditory processing;
- post-lock information and recognition-only effects;
- outcome dependence on one site, scorer, participant or event.

The following always block C7:

- truth or candidate identity is distinguishable above the frozen tolerance from metadata or interface behaviour;
- a negative-control family shows a prespecified systematic correspondence pattern;
- target correspondence is materially concentrated in records with contamination, ordinary access, timing uncertainty or critical access-log anomalies;
- the primary direction disappears under a mandatory prespecified neutral-missing, participant-cluster or leave-one-site-out analysis;
- decoy exchangeability or transcript-independent generation cannot be reproduced;
- a critical leakage route remains unresolved.

A control failure may produce C2 or C6 depending on whether the confirmatory statistic itself remains valid. The distinction must be made by blinded independent adjudication using the frozen rule.

## Pause and stopping rules

### Immediate stop

The affected activity stops immediately for:

- research interference with resuscitation or a serious device-related safety event;
- ethics, regulatory or institutional authority withdrawal;
- unauthorized identifiable-data disclosure or an uncontained high-risk privacy breach;
- unauthorized target/truth access, premature unblinding or key-custody compromise;
- evidence of fabricated, forged, substituted or replayed exposure/audit records;
- systematic denominator suppression;
- a device, room or software configuration outside the commissioned baseline.

Clinical care always takes priority. The stop decision does not await an outcome analysis.

### Site pause

A site pauses activation and recruitment when:

- a critical event is suspected but not yet adjudicated;
- denominator reconciliation, access-log review or display verification falls outside a mandatory gate;
- an unreviewed production change requires recommissioning;
- staffing, consent, interview, security or incident-response certification lapses;
- an external monitor requires corrective action.

Reactivation requires documented corrective/preventive action, independent retest and the same authority that approved commissioning. Prior affected events remain in the ledger.

### Study-wide pause or termination

Study-wide activation pauses when a systemic route may affect more than one site, the common software/build/decoy pipeline is compromised, central custody or unblinding controls fail, or the independent safety/ethics authority directs it.

Permanent termination is required when competent authority withdraws approval, acceptable participant risk cannot be restored, the ethics-approved burden cap is reached without the frozen information requirement, or a critical systemic validity failure cannot be bounded.

### Prohibited stopping

- no unblinded efficacy stopping;
- no outcome-based sample-size extension;
- no futility stopping based on target correspondence;
- no stopping after a striking case;
- no selective site closure because its results are weak;
- no reopening accrual after seeing the primary result.

Accrual may end only at the prospectively approved information/event/calendar cap or for safety, ethics, feasibility, privacy, security or integrity reasons independent of the effect direction.

## Missingness, attrition and severe selection

Death, incapacity, no consent pathway, no interview, null report, failed activation, unknown exposure and unrecoverable package are distinct observed flow states. They cannot be imputed into awareness outcomes or removed from the complete event denominator.

A null result with severe attrition is `C1`, `C2` or `C3` according to the frozen rules; it is never described as falsification of awareness. C4 requires all prespecified information, attrition, unresolved-state and selection-bias conditions to pass.

## Replication rule

A replication qualifies toward C8 only when it:

1. is led by a team and institutional sponsor independent of the original study's operational and analytic leadership;
2. is prospectively registered before recruitment;
3. uses separately recruited participants and independently commissioned sites;
4. freezes the same primary construct, endpoint direction, minimum effect and critical validity boundaries, or prospectively declares a stricter compatible test;
5. uses independently generated target assets, commitments and analysis implementation;
6. meets C7 without unresolved critical leakage, safety, privacy, denominator, negative-control or robustness failures;
7. reports the complete denominator and all null, contradictory and invalid records; and
8. passes independent statistical, clinical, ethics/privacy and adversarial-security review.

A multi-site result under one sponsor/protocol is one study, not an independent replication. Reanalysis, subgroup discovery, alternative scoring of the same data and conceptual similarity do not count.

A failed or contradictory qualifying replication changes the status to `REPLICATION_CONFLICT` and requires comparative review; it cannot be hidden by pooling only favourable studies.

## Classification authority and audit record

Classification requires at least:

- independent clinical/safety representative;
- statistician not responsible for the primary analysis;
- ethics/privacy representative;
- independent security/leakage reviewer;
- protocol governance representative without unilateral authority.

The signed record includes protocol/SAP/build versions, frozen thresholds, denominator reconciliation, all gate states, incidents, negative controls, robustness results, dissent, primary class and prohibited claims. Machine-readable classification is committed before public narrative drafting.

## Publication language

Every report must state:

- the primary class and all secondary flags;
- the full eligible-event flow and target-exposed yield;
- deviations, pauses, breaches and invalid records;
- negative controls and mandatory robustness analyses;
- that target correspondence measures a later report proxy;
- that one study cannot establish awareness, continuity, survival or afterlife;
- that BQ001 remains governed separately.

Terms such as “proved consciousness,” “proved survival,” “falsified consciousness,” “evidence of afterlife,” “verified NDE” and equivalent causal or ontological claims are prohibited.

## Machine-readable states

- `STAGE_0_DRAFT`
- `RECRUITMENT_NOT_AUTHORIZED`
- `SITE_NOT_AUTHORIZED`
- `HELD_PENDING_ADJUDICATION`
- `NOT_EVALUABLE`
- `INVALID_FOR_CONFIRMATORY_INTERPRETATION`
- `SAFETY_PRIVACY_OR_AUTHORITY_STOP`
- `C0_NOT_STARTED`
- `C1_PROTOCOL_INFEASIBLE`
- `C2_CONFIRMATORY_INVALID`
- `C3_VALID_NULL_IMPRECISE`
- `C4_VALID_BOUND_BELOW_MINIMUM`
- `C5_STATISTICAL_SIGNAL_ONLY`
- `C6_SIGNAL_INTERPRETATION_BLOCKED`
- `C7_ANOMALY_REVIEW_CANDIDATE`
- `C8_INDEPENDENTLY_REPLICATED_REVIEW_CANDIDATE`
- `REPLICATION_PENDING`
- `REPLICATION_CONFLICT`
- `PUBLICATION_GATE_CLOSED`

## Unresolved items before freeze

- independent statistical review of the C4 compatibility-bound method;
- simulation of classification error and stopping behaviour;
- frozen quantitative negative-control tolerances;
- ethics-approved eligible-event and calendar burden cap;
- adjudication charter, conflict-of-interest rules and appeal path;
- executable validation of prose/JSON coverage and controlled vocabularies;
- prospective registration and external domain sign-off.

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
- Live participant-data processing: **NOT AUTHORIZED**
- COA-001 state: **DRAFT / PROTOCOL-FEASIBLE NOT YET ESTABLISHED**

FSC-001 is a Stage-0 decision contract. It does not preregister, authorize, classify a result that does not exist, change BQ001 or open any promotion gate.

