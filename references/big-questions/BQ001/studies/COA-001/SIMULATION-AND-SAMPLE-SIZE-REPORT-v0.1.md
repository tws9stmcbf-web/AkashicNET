# COA-001 Rank-Test Operating Characteristics and Sample-Size Report

**Module:** SIM-001  
**Version:** 0.1  
**Date:** 2026-09-17  
**Draft amendment:** 2026-09-24 · INT-001 v0.2 alignment; no operational authorisation  
**State:** PROVISIONAL STAGE-0 ANALYSIS / INDEPENDENT REPRODUCTION REQUIRED  
**Parent protocol:** COA-001 v0.1  
**Statistical plan:** SAP-001 v0.1  
**Reproduction code:** [coa001_rank_operating_characteristics_v0_1.py](./analysis/coa001_rank_operating_characteristics_v0_1.py)  
**Governance:** Issue #356 · Draft PR #357

## Executive result

For the SAP-001 six-candidate normalized-rank endpoint and a one-sided exact upper-tail test at `alpha = 0.025`, the more conservative of two stylized alternative families requires:

| True mean advantage `delta` above null 0.5 | Target power | Required independent rank contributions |
|---:|---:|---:|
| 0.050 | 80% | 377 |
| 0.050 | 90% | 513 |
| 0.075 | 80% | 171 |
| 0.075 | 90% | 231 |
| 0.100 | 80% | 97 |
| 0.100 | 90% | 132 |
| 0.150 | 80% | 43 |
| 0.150 | 90% | 59 |

SAP-001 uses **132 unique `TARGET_EXPOSED` participants** as a planning floor, not an event-count stopping boundary. The 90%-power result at `delta = 0.10` applies only to the independent-rank model. Before recruitment, blinded Stage-1 inputs and independent review must freeze a unique-participant target of at least 132 for the actual participant-weighted endpoint.

This result does not establish that `delta = 0.10` is biologically, clinically or philosophically plausible. It quantifies the conditional sample requirement if that design effect is chosen. Independent statistical review must justify the minimum relevant effect and reproduce the calculations before freeze.

## Endpoint represented

Each committed packet contains one true target sequence and five transcript-independent decoy sequences.

For each blinded scorer:

- strongest correspondence receives rank 1;
- weakest correspondence receives rank 6;
- ties receive their midrank;
- normalized rank utility is `U = (6 - rank) / 5`.

Under exchangeability, each candidate position is equally likely to be true and:

- `E(U) = 0.5`;
- `Var(U) = 7/60 ≈ 0.1167` for one untied rank;
- the study effect is `delta = mean(U_participant) - 0.5`.

The exact operational endpoint averages two locked scorer utilities within event and repeated events within participant. The present calculation uses one independent rank contribution per participant-event. Because within-event scorer dependence and repeated-participant clustering are not yet empirically known, the exact design must be rerun with blinded Stage-1 agreement and cluster distributions.

## Method

The reproduction program uses deterministic probability convolution, not Monte Carlo sampling.

For sample size `n`:

1. represent each participant-event by integer score `y ∈ {0,1,2,3,4,5}`, where `U = y/5`;
2. convolve the six-point probability distribution `n` times;
3. find the smallest critical sum whose null upper-tail probability is no greater than 0.025;
4. evaluate the alternative upper-tail probability at that same critical value;
5. return the first `n` reaching 80% or 90% power.

The non-randomized discrete test is conservative: its achieved type-I error is never intentionally inflated to reach exactly 0.025.

## Alternative families

No empirical COA-001 effect distribution exists. Two stylized families with the same mean advantage were evaluated to expose shape sensitivity.

### A. Sparse top-rank mixture

A fraction `2 × delta` of records receives a best true-candidate rank; all remaining records are exchangeable. This represents occasional strong correspondence embedded in predominantly null records.

For `delta = 0.10`, 20% of records use the top-rank component and 80% remain exchangeable.

### B. Soft rank shift

All rank probabilities are exponentially tilted toward stronger true-candidate ranks and calibrated so `E(U) = 0.5 + delta`. This represents a diffuse shift rather than rare strong records.

Neither family is asserted to describe awareness or real participant behaviour. The larger required sample across the two families is used provisionally.

## Exact results

| `delta` | Sparse mixture 80% | Soft shift 80% | Conservative 80% | Sparse mixture 90% | Soft shift 90% | Conservative 90% |
|---:|---:|---:|---:|---:|---:|---:|
| 0.050 | 377 | 368 | **377** | 513 | 492 | **513** |
| 0.075 | 171 | 163 | **171** | 231 | 218 | **231** |
| 0.100 | 97 | 91 | **97** | 132 | 121 | **132** |
| 0.150 | 43 | 40 | **43** | 59 | 55 | **59** |

Selected sparse-mixture power values show the information gradient:

| Independent rank contributions n | Power at `delta=.05` | Power at `delta=.075` | Power at `delta=.10` | Power at `delta=.15` |
|---:|---:|---:|---:|---:|
| 50 | 0.172 | 0.329 | 0.518 | 0.842 |
| 75 | 0.255 | 0.480 | 0.706 | 0.955 |
| 100 | 0.318 | 0.589 | 0.817 | 0.987 |
| 125 | 0.369 | 0.670 | 0.884 | 0.996 |
| 150 | 0.428 | 0.747 | 0.932 | 0.999 |
| 200 | 0.540 | 0.858 | 0.978 | >0.999 |
| 300 | 0.703 | 0.957 | 0.998 | >0.999 |
| 400 | 0.819 | 0.988 | >0.999 | >0.999 |

Values are design calculations, not predicted study outcomes.

## Translation to eligible-event accrual

The information target is conditional on reaching `TARGET_EXPOSED`, not on merely identifying eligible arrests.

Let `q` be the number of unique `TARGET_EXPOSED` participants divided by `ALL_ELIGIBLE_EVENTS`, counting each participant once. The rough expected eligible-event requirement for the planning floor is `132/q` (replace 132 with the frozen participant target when available):

| Stage-1 unique-participant yield per eligible event | Approximate eligible events needed for 132 unique participants |
|---:|---:|
| 2% | 6,600 |
| 5% | 2,640 |
| 10% | 1,320 |
| 20% | 660 |

These are arithmetic scenarios, not final accrual targets. Confidence limits around the Stage-1 yield, site heterogeneity, calendar time, consent and ethical burden must inform the maximum eligible-event cap.

The provisional Stage-1 range of 150–300 eligible events is therefore a feasibility pilot, not a confirmatory sample. Even at a 20% yield it would be expected to provide only 30–60 unique `TARGET_EXPOSED` participants under this unique-participant yield assumption.

## Attrition and integrity stress rules

Events do not disappear when they fail to reach the primary conditional population.

- Every eligible arrest remains in `ALL_ELIGIBLE_EVENTS`.
- Death, no approach, no consent, no interview, failed activation and unknown exposure are distinct flow outcomes.
- `UNKNOWN` and `UNRECOVERABLE` states count against applicable feasibility gates.
- Within `TARGET_EXPOSED`, null and non-scorable reports receive neutral primary utility `0.5`.
- Critical unresolved integrity records receive neutral primary utility plus `0`/ `1` worst/best-case bounds.
- Per-protocol exclusion is supportive only.

If 10% of `TARGET_EXPOSED` records receive neutral utility because scoring cannot be completed, an underlying `delta = 0.10` is diluted toward approximately `0.09`, increasing the needed information. This motivates operational contingency and rerunning simulation with Stage-1 failure rates; it does not justify deleting failed records.

## Type-I error and optional stopping

The exact null is exchangeability of the true label within each committed six-candidate packet.

Type-I error protection depends on:

- target and decoy exchangeability;
- transcript-independent candidate construction;
- locked scorer rankings before truth release;
- a single primary endpoint;
- one-sided `alpha = 0.025`;
- no score-informed accrual or optional stopping;
- fixed analysis code and seed procedure;
- reporting all participant-event and site flow states.

Only safety, ethics, feasibility and integrity rules may pause accrual. There is no efficacy or futility look at correspondence outcomes.

## Sensitivity work required before freeze

SIM-001 v0.2 must incorporate, using blinded Stage-1 or external design inputs:

1. two-scorer correlation and disagreement;
2. tie and null-report frequency;
3. repeated participant-events and participant clustering;
4. site heterogeneity;
5. target-class and decoy-stratum imbalance;
6. non-scorable and integrity-state rates;
7. contamination-state mixtures;
8. incomplete candidate exchangeability;
9. alternative effect distributions with equal means;
10. exact versus seeded-randomization computation;
11. confidence-interval coverage;
12. negative-control decision rules;
13. yield uncertainty and maximum eligible-event cap;
14. sensitivity to four, five, seven or more decoys if operationally justified.

A design is not frozen merely because one scenario reaches nominal power.

## Reproducibility record

The supplied Python program:

- uses only the Python standard library;
- contains no participant data;
- uses deterministic convolution;
- prints the alternative family, effect, target power, minimum sample size, achieved power, achieved alpha and critical sum;
- supports independent line-by-line reimplementation.

Before SAP freeze:

- a second implementation in another language must reproduce all table entries;
- code and output digests must be recorded;
- test fixtures must be added;
- an independent statistician must sign the operating-characteristics decision;
- discrepancies must be resolved without selecting the result that favours feasibility.

## Decision

SIM-001 supports continued Stage-0 development with a planning floor of 132 unique `TARGET_EXPOSED` participants. It establishes 90% power at `delta = 0.10` only for the independent-rank model, not the final participant-weighted design.

It does **not** establish:

- a final eligible-event sample size;
- feasibility of obtaining the frozen number of unique target-exposed participants;
- the truth of the alternative;
- awareness during resuscitation;
- continuity, personal survival or an afterlife.

Stage 1 must first estimate yield, agreement, ties, clustering, missingness and integrity performance.

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

SIM-001 is a planning analysis, not scientific evidence or a BQ001 update.


