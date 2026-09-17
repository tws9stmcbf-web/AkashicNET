# COA-001 Estimands, Analysis Populations and Stage-1 Feasibility Gates

**Module:** EAP-001  
**Version:** 0.1  
**Date:** 2026-09-17  
**State:** DRAFT / STAGE-0 METHOD DEVELOPMENT  
**Parent protocol:** COA-001 v0.1  
**Governance:** Issue #356 · Draft PR #357

## Purpose

This module defines what COA-001 will estimate, which records contribute to each estimate, and how every provisional Stage-1 feasibility gate is calculated.

It prevents:

- device or data failures from disappearing through eligibility rules;
- selective restriction to survivors, interviewed participants or visually striking reports;
- pooled results from hiding a failing site;
- unknown states from being treated as successes;
- protocol feasibility from being confused with evidence for awareness, anomalous perception or continuity.

All rules remain provisional until clinical, statistical, ethics/data-protection and adversarial review is complete. No participant recruitment is authorized.

## Core units

| Unit | Definition | Repeated observations |
|---|---|---|
| Eligible event | One in-hospital cardiac-arrest event meeting the frozen clinical/location criteria | A person with two eligible arrests contributes two events |
| Participant | One surviving person linked to one or more eligible events | Participant-level uncertainty must account for repeated events |
| Interview | One protocol-governed interview after an eligible event | The first eligible locked interview is primary; later interviews are secondary |
| Claim | One independently codable report element | Multiple claims from one interview are not independent participants |
| Target epoch | One prespecified displayed time interval | Epochs are nested within events and participants |
| Site | One separately governed hospital deployment | Site effects and failures are always reported |

The eligible event is the denominator unit for Stage-1 device, timing, safety and event-accounting gates. The interview is the denominator unit only for interview-process gates. Claims and target epochs may contribute to descriptive or Stage-2 scoring analyses but never inflate the participant or event count.

## Eligibility and flow states

Event eligibility is determined solely by:

1. adult patient aged 18 years or older;
2. in-hospital cardiac arrest in a participating area during a prespecified study-active period;
3. initiation of chest compressions.

The following are outcomes or flow states, never eligibility conditions:

- clinical-timing availability;
- device status;
- activation or target-exposure status;
- target-package or log recoverability;
- survival;
- interview eligibility;
- consent;
- interview completion;
- transcript lock;
- integrity-breach status.

Every eligible event receives explicit machine-readable values, including `UNKNOWN` or `UNRECOVERABLE` when appropriate. Unknown and unrecoverable values remain in the complete eligible-event denominator and count as failures for the applicable completeness gate.

## Population map

| Population | Entry rule | Primary use | Excluded from |
|---|---|---|---|
| ALL-ELIGIBLE-EVENTS | Every eligible event | Denominator, device, timing, safety and attrition feasibility | Nothing |
| ALL-SURVIVORS | Eligible event followed by hospital survival | Survivor flow and approach feasibility | No event-level feasibility analysis |
| ALL-APPROACH-ELIGIBLE | Survivor meeting the frozen clinical/ethical approach rule | Approach and consent feasibility | No target-effect claim |
| ALL-INTERVIEWED | At least one completed protocol interview after an eligible event | Interview feasibility and broad report sensitivity analyses | No automatic target-effect inclusion |
| TARGET-EXPOSED | ALL-INTERVIEWED participant-event with an auditable target sequence displayed during the prespecified event interval | Stage-2 target-correspondence estimand and sensitivity analyses | Interviews with absent or uncertain valid exposure |
| VISUAL-CLAIM | Interview contains a prespecified visual-perception claim for the relevant interval | Secondary/exploratory subgroup only | Confirmatory primary population unless independently justified before Stage 2 |
| PER-PROTOCOL TARGET-EXPOSED | TARGET-EXPOSED record without a frozen critical integrity breach | Secondary supportive analysis | Primary intention-to-observe sensitivity analysis |

`PER-PROTOCOL` is not a free-standing population. It is always named as a subset of an underlying population and accompanied by the corresponding unrestricted analysis.

## Repeated events, interviews, claims and epochs

- A new cardiac arrest is a new eligible event even when it occurs in the same person.
- The first completed, transcript-locked interview within the frozen window is the primary interview.
- Later interviews are retained and labelled secondary; they cannot replace or overwrite the primary interview.
- Each eligible event remains a distinct participant-event scoring unit; analyses account for repeated events through participant clustering.
- Multiple claims or target epochs are aggregated by the frozen scoring rule before participant-level inference.
- The analysis may not select the most accurate claim, epoch or interview after unblinding.
- Cross-site transfers and duplicate records are reconciled through a pseudonymous linkage process before database lock.

## Estimands

### E1 — Stage-1 protocol-feasibility profile

**Question:** Can the complete protocol operate across participating sites while retaining all eligible events and meeting every mandatory process, integrity and safety gate?

**Population:** ALL-ELIGIBLE-EVENTS, with interview-process components evaluated in their independently defined interview denominators.

**Measure:** The complete vector of prespecified gate estimates; it is not collapsed into a single score.

**Intercurrent events:** Death, no interview, device failure, failed activation, timing uncertainty, missing logs and integrity breaches remain observable flow states. They are not imputed as successful target exposures or silently removed.

**Decision:** Stage 1 progresses only when every mandatory gate passes its frozen rule. An interesting report or target correspondence cannot compensate for a failed gate.

### E2 — Stage-2 target-correspondence estimand

**Question:** Among events with a valid auditable target exposure, do locked reports correspond more strongly to their true time-aligned sequence than to exchangeable blinded decoy sequences under the frozen scoring rule?

**Population:** TARGET-EXPOSED.

**Unit of analysis:** Participant-event, with prespecified aggregation across epochs; inference accounts for participant and site clustering.

**Contrast:** True sequence score versus the frozen randomization/decoy distribution.

**Interpretation:** This estimates information correspondence under controlled conditions. It does not directly observe awareness and cannot by itself establish continuity, personal survival or an afterlife.

The score, decoy construction, number of decoys, aggregation, clustering, tie rule, multiplicity family, missing-data rule, meaningful-effect threshold and one-/two-sided decision boundary must be frozen before Stage 2.

### E3 — All-interviewed sensitivity estimand

**Question:** How do report and correspondence outcomes appear when all completed primary interviews are retained, including absent, failed, uncertain or unrecoverable target exposure?

**Population:** ALL-INTERVIEWED.

**Measure:** Full flow and outcome distribution, with target status explicit. Records without valid exposure are not assigned a target-match success.

**Purpose:** Detect selection created by restricting analysis to successful device operation.

### E4 — Per-protocol supportive estimand

**Question:** What is the Stage-2 target-correspondence estimate after applying only the frozen critical-breach exclusions?

**Population:** PER-PROTOCOL TARGET-EXPOSED.

**Purpose:** Supportive only. It must be reported beside E2 with every exclusion and reason disclosed.

### E5 — Visual-claim exploratory estimand

**Question:** Among interviews containing a prespecified visual-perception claim, what is the distribution of blinded true-versus-decoy scores?

**Population:** VISUAL-CLAIM intersected with TARGET-EXPOSED.

**Purpose:** Secondary/exploratory. It cannot become the primary analysis after outcome inspection.

## Common gate rules

Unless a gate states otherwise:

1. **Thresholds are provisional.** Their final rationale and operating characteristics require simulation and independent statistical review.
2. **Unknown handling:** `UNKNOWN`, `UNRECOVERABLE` and missing applicable status count in the denominator and not the numerator.
3. **Uncertainty:** Report the estimate and a two-sided 95% interval. Binomial proportions use an exact or Wilson interval selected before database lock.
4. **Zero denominators:** A mandatory gate with a zero denominator is `NOT_EVALUABLE`, never `PASS`.
5. **Site rule:** Report pooled and site-specific estimates. A site failure cannot be hidden through pooling.
6. **Programme rule:** Any zero-tolerance safety, unauthorized-access or premature-unblinding event at any site pauses programme progression. For other mandatory gates, a failing site pauses that site and programme progression until the cause is remediated and an independent review determines whether the remaining evidence is interpretable.
7. **No discretionary exclusions:** Denominator changes after recruitment require a versioned deviation record and independent adjudication.
8. **Confidence intervals do not prove absence:** Zero observed events are accompanied by a one-sided 95% upper confidence bound.
9. **Freeze rule:** Numerator, denominator, threshold, uncertainty method and site rule are frozen before the first Stage-1 event.

## Operational Stage-1 gates

### Event, device and target-system gates

| Gate | Numerator | Denominator | Provisional pass rule | Unknown/failure handling |
|---|---|---|---|---|
| Complete event denominator | Eligible events with a complete minimum event-flow record | Independently audited count of all eligible events | ≥98% | Missing/unlinked eligible events fail |
| Recoverable device status | Eligible events with recoverable device status, including explicit not-installed/not-active states | ALL-ELIGIBLE-EVENTS | ≥98% | `UNKNOWN`/`UNRECOVERABLE` fail |
| Valid target activation | Equipped eligible events with a valid activation in the frozen interval | All equipped eligible events | ≥85% | No, late, partial or unknown activation fails |
| Complete tamper-evident target logs | Activations with complete valid signed/hash-chained logs | All activations | ≥95% | Invalid, missing or unrecoverable logs fail |
| Asset-manifest match | Valid exposures whose rendered assets match the frozen manifest | All valid exposures | 100% | Mismatch or unknown fails |
| Encrypted package recovery | Activations with authenticated recoverable evidence package | All activations | ≥98% | Missing/unrecoverable fails |
| Clock synchronization | Valid activations aligned within ±1 second with measured uncertainty | All valid activations | ≥95% | Outside tolerance or unknown fails |
| Independent display verification | Activations with independent evidence that intended pixels were displayed for the logged interval | All claimed valid exposures | Threshold to be frozen after commissioning | Render acknowledgement alone is insufficient |

### Interview, contamination and blinding gates

| Gate | Numerator | Denominator | Provisional pass rule | Unknown/failure handling |
|---|---|---|---|---|
| Transcript locked before any target/event unblinding | Completed primary interviews locked before unblinding | All completed primary interviews | 100% | Premature or uncertain unblinding fails |
| Critical interviewer unblinding | Completed primary interviews with critical interviewer unblinding | All completed primary interviews | ≤2%; every case disclosed and excluded only from supportive per-protocol analysis | Unknown blindness status counts as breach pending adjudication |
| Completed contamination/exposure audit | Completed primary interviews with frozen contamination audit completed before unblinding | All completed primary interviews | ≥95% | Missing audit fails |
| Dual-coder coverage | Scorable primary reports coded independently by two qualified coders | All scorable primary reports defined before viewing scores | 100% | Missing second code fails |
| Blinding assessment | Relevant staff completing the frozen blinding-assessment instrument | All staff/cases for whom it is required | Threshold to be frozen | Missing assessment fails completeness |
| Primary-interview timeliness | Primary interviews completed inside the frozen clinically appropriate window | All survivors eligible for approach | Threshold to be derived from Stage-0 simulation/clinical review | Death, instability, refusal and non-approach remain separate flow states |

### Reliability gates

| Gate | Estimate | Denominator/sample | Provisional pass rule | Uncertainty |
|---|---|---|---|---|
| Categorical coding agreement | Cohen’s κ or prespecified multi-rater equivalent | All dual-coded primary reports with applicable categorical fields | Point estimate ≥0.80 | 95% interval and prevalence/bias diagnostics |
| Continuous score agreement | Prespecified ICC form | All dual-coded primary reports with applicable continuous scores | Point estimate ≥0.90 | 95% interval and model specification |
| Decoy-score reproducibility | Agreement of independently executed frozen scoring pipeline | Prespecified synthetic and blinded rehearsal packets | 100% computational reproduction; human-score tolerance frozen before Stage 1 | Every discrepancy retained |

Reliability gates remain `NOT_EVALUABLE` if the minimum sample required by the simulation report is not reached.

### Safety, rights and operational gates

| Gate | Event counted | Denominator | Provisional pass rule | Required reporting |
|---|---|---|---|---|
| Serious device-related adverse event | Any serious adverse event judged at least possibly device-related | ALL-ELIGIBLE-EVENTS and installed-device exposure time | 0 observed; any event pauses programme | One-sided 95% upper bound; adjudication |
| Research interference with resuscitation | Any documented delay, obstruction, distraction or alteration of care attributable to research | ALL-ELIGIBLE-EVENTS | 0 observed; any event pauses programme | Incident narrative and independent clinical review |
| Unauthorized plaintext target access | Confirmed access before permitted unblinding | All activations plus access-log audit period | 0 confirmed; any event pauses programme | Scope, affected cases and incident response |
| Premature unblinding | Target/event identity released before the complete frozen lock sequence | All completed primary interviews and all unblinding requests | 0 analysed cases; any occurrence pauses programme | All occurrences, including prevented attempts |
| Unresolved viewing route | Installed site/device configuration with an unresolved ordinary visual/reflection route | All commissioned configurations | 0 before activation | Optical survey and remediation record |
| Interview withdrawal due to burden | Approached survivors withdrawing because of study burden | All approached eligible survivors | ≤10%; review gate rather than efficacy gate | Estimate, 95% interval and reasons |
| Interpreter confidentiality compliance | Interpreted interviews satisfying the frozen confidentiality and role-separation procedure | All interpreted interviews | 100% | Deviations and affected scope |

## Attrition and missingness ledger

Every site reports, without collapsing categories:

1. all arrests in participating areas during study-active periods;
2. eligible events;
3. device installed/equipped status;
4. successful, failed, late, partial and unknown activations;
5. valid, invalid, absent and unknown target exposure;
6. recoverable, unrecoverable and invalid evidence packages;
7. return of spontaneous circulation;
8. hospital survival;
9. approach eligibility;
10. approached/not approached and reason;
11. consented/declined/unavailable and authority;
12. completed and incomplete primary interviews;
13. transcript lock status;
14. memories reported or not reported;
15. interval-linked perception reported or not reported;
16. visual claim present or absent;
17. scorable/not scorable and frozen reason;
18. integrity and contamination states;
19. inclusion in each estimand and sensitivity analysis.

No downstream subgroup count substitutes for the complete eligible-event denominator.

## Decision states

Each mandatory gate is assigned exactly one state:

- `PASS`
- `FAIL`
- `NOT_EVALUABLE`
- `PAUSED_PENDING_ADJUDICATION`

Only `PASS` permits progression. `NOT_EVALUABLE` is not evidence of feasibility. A gate may not be waived because an efficacy or correspondence result is interesting.

## Required next artifacts

Before a v0.2 freeze candidate:

- simulation-based operating-characteristics and sample-size report;
- frozen interview and contamination-audit manual;
- frozen blinded-scoring and decoy-construction manual;
- complete statistical analysis plan;
- ethics and data-protection outline;
- data-flow and role-access matrix;
- independent clinical, statistical, ethics/data-protection and adversarial-security reviews.

## Governance lock

- COA-001: **DRAFT / STAGE 0**
- This module: **PROVISIONAL, NOT PREREGISTERED**
- Recruitment: **NOT AUTHORIZED**
- Protocol feasibility: **NOT ESTABLISHED**
- BQ001: **UNRESOLVED · Level 8/10**
- Accepted canonical edges: **0**
- `supports_models`: **[]**
- Truth inference: **OFF**
- Scientific-evidence promotion: **OFF**
- Rights/public synthesis: **OFF**
- Website promotion: **OFF**

This module defines method-development rules only. It is not a result, trial registration, ethics approval, accepted edge or evidence for awareness or continuity.
