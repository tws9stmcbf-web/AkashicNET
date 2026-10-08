# COA-001 Blinded Scoring and Decoy-Construction Manual

**Module:** SDC-001  
**Version:** 0.1  
**Date:** 2026-09-17  
**Draft amendment:** 2026-09-24 · INT-001 v0.2 alignment; no operational authorisation  
**State:** DRAFT / STAGE-0 METHOD DEVELOPMENT  
**Parent protocol:** COA-001 v0.1  
**Governance:** Issue #356 · Draft PR #357  
**Related modules:** EAP-001 v0.1 · INT-001 v0.2 · TS-001 v0.1

## Purpose and boundary

SDC-001 defines how locked later reports are converted into reproducible claims, compared symmetrically with true and decoy target sequences, and released for analysis without revealing the true assignment to claim coders or scorers.

The directly scored object is correspondence between a locked later report and candidate information. It is not awareness itself. A high score, rank, apparent hit or true-over-decoy difference cannot by itself establish awareness during resuscitation, continuity, personal survival or an afterlife.

This manual is a Stage-0 design artifact. It does not authorize recruitment, scoring of real participant data, preregistration, Stage-1 progression or a confirmatory claim. The exact confirmatory endpoint, decoy count, score weights, minimum meaningful effect, multiplicity family and decision boundary remain to be frozen in the Stage-2 statistical analysis plan after simulation and independent statistical review.

## Non-negotiable rules

1. The primary source is the chronologically first completed primary interview within the frozen window, designated independently of lock success or outcome. Only a verified L1 source is eligible for ordinary primary claim extraction. A failed lock stays attached to the designated interview; a later interview cannot replace it.
2. Source recording and final transcript digests must be verified before scoring preparation.
3. Claim extraction is completed and locked without access to any candidate target.
4. Decoy eligibility, sampling and replacement rules are frozen independently of transcript content.
5. The candidate-set manifest is cryptographically committed before any scorer receives a packet.
6. True and decoy candidates are rendered in the same format and presented in randomized, masked order.
7. Claim coders, primary scorers and adjudicators remain blind to truth position.
8. Null, contradictory, uncertain, contaminated and non-scorable reports remain in the flow ledger.
9. Disagreement is resolved without revealing which candidate is true.
10. Every access, transformation, exclusion, replacement, score, amendment and unblinding is auditable.
11. Scoring rules cannot be changed after examining true-versus-decoy results.
12. No individual narrative can replace the prespecified participant-event analysis.
13. Post-lock information cannot alter the primary transcript, claim set or score; it is append-only and sensitivity-only.
14. Recognition is secondary under SAP-001 and remains separately identifiable. Its data-collection pathway is NOT AUTHORISED; it never enters the primary ranking or claim packet.
15. Visual and auditory channels are scored and analysed separately.

## Unit and packet hierarchy

The provisional Stage-2 unit is one **participant-event** with one primary locked interview.

A scoring package contains:

- one pseudonymous participant-event ID;
- the verified locked transcript and permitted structured fields;
- a frozen atomic-claim table;
- one masked candidate set containing the true sequence and prespecified decoys;
- candidate timing and modality metadata at the permitted blinded resolution;
- contamination, deviation and integrity flags that do not reveal truth position;
- manifest, software and rule-set identifiers;
- cryptographic digests and timestamps.

Multiple arrests for one participant remain separate participant-events and are linked for cluster-aware analysis. Later interviews, repeated claims and multiple target epochs cannot create additional independent primary units. Their aggregation rules must be frozen in the SAP.

## Roles and access separation

| Role | Transcript access | Target/decoy access | Truth-position access before score lock |
|---|---:|---:|---:|
| Transcript custodian | Yes | No | No |
| Claim coder | Redacted locked transcript | No | No |
| Decoy-pool custodian | No | Frozen target library | Custodial only |
| Candidate-set generator | No transcript content | Target library and committed algorithm | System-only; no discretionary selection |
| Packet assembler | Claim table and masked candidates | Masked candidates | No |
| Primary scorer | Claim table and masked candidates | Masked candidates | No |
| Adjudicator | Claim table, masked candidates and disputed fields | Masked candidates | No |
| Statistical analyst | Locked scores and masked assignment until analysis lock | Masked IDs | No |
| Independent unblinding custodian | No narrative content unless authorized | Linkage table | Yes, dual-control release only |
| Public/AkashicNET team | No case-level source data | No | No |

No person may combine claim coding, discretionary decoy selection and truth-position access for the same participant-event. The target custodian must not communicate candidate identity, target status or room-event details to participant-facing staff.

## Required preconditions

A participant-event may enter scoring preparation only when:

- the primary interview status is resolved;
- source recording and transcript digests verify;
- the transcript is marked `FINAL_PRIMARY_LOCKED`;
- transcript lock precedes every target or event-record release;
- the contamination audit is complete or explicitly marked incomplete;
- critical blinding and integrity states are recorded;
- the applicable target asset and activation manifests exist;
- protocol, manual, rubric, pool and software versions are fixed for the packet.

Failure of a precondition does not erase the event. It produces an explicit scoring state and remains in the applicable denominator or sensitivity analysis.

## Phase A — transcript-only claim extraction

Under the proposed INT-001 v0.2 sequence, primary coders receive L1 only. Preserve each claim's first source span and elicitation class: spontaneous narrative, participant-led clarification, open environmental recall, audit-elicited or closing addition. Keep L2 and recognition records out of the primary claim/scoring packet. A claim with no frozen source-eligibility rule remains unresolved; the coder cannot decide eligibility by inspecting candidate correspondence.
>
The statistical reviewers must freeze which L1 prompted classes contribute to the primary rank endpoint. New content first supplied in L2 or after candidate exposure cannot enter the primary claim set. Any audit-elicited or closing-addition rule must address the possibility that the audit itself supplied a cue.
>
Failed source integrity triggers the existing held/breached-record pathway, not reconstruction from later retellings. Later-discovered contamination may change validity or interpretation through an append-only adjudication; original primary bytes and score provenance remain preserved subject to authorised rights handling.

Two qualified coders independently review the same redacted locked transcript without targets, decoys, activation status, room-event logs or the study’s true assignment.

Each potentially scorable statement is decomposed into the smallest defensible atomic claim. The claim table records:

- verbatim source span and transcript location;
- claim ID and parent narrative ID;
- modality: visual, auditory, tactile, spatial, semantic or other;
- content class using the frozen ontology;
- specific attributes stated by the participant;
- claimed temporal interval and basis for that placement;
- viewpoint/location claim;
- spontaneity: free narrative, prompted free recall, structured prompt or recognition;
- participant confidence using the frozen scale;
- negation, contradiction and uncertainty;
- possible post-event source or contamination flag;
- coder scorable/non-scorable decision and reason.

Coders must not infer missing colour, orientation, wording, order, location, timing or meaning. Synonyms, partial matches, superordinate categories and contradictions are handled only by the frozen rubric.

Before candidate access, the two claim tables are compared. Disagreements are resolved by a blind adjudicator or retained as parallel prespecified variants. The final claim table receives a digest and immutable lock timestamp.

## Claim exclusions and non-scorable states

A claim may be non-scorable only for a frozen reason, including:

- no content capable of mapping to the frozen target ontology;
- content introduced only after candidate presentation;
- unintelligible or irrecoverably ambiguous source material;
- missing modality required by the scoring rule;
- claimed timing wholly outside the prespecified interval;
- withdrawal from the applicable data use;
- critical source-integrity failure.

A null report is not missing and is not excluded. Contamination, uncertain timing and contradictions normally remain scoreable with flags unless the SAP prespecifies otherwise. Counts and reasons are reported against `ALL_INTERVIEWED`; the scorable denominator may not be defined after seeing candidate matches.

## Target-library and decoy-pool freeze

Before any real transcript is opened for scoring:

1. define the target universe and modality-specific asset classes;
2. record each asset’s content attributes, provenance, rights status and technical properties;
3. define permissible sequences, timing structure and repetition constraints;
4. define candidate similarity strata such as modality, duration, information density, visual complexity and base-rate content;
5. define exclusions independently of participant reports;
6. version and hash every asset and metadata record;
7. create an ordered pool manifest and commit its digest with an authenticated timestamp;
8. freeze the decoy count or mark it pending simulation before recruitment;
9. publish the algorithm specification and test vectors without exposing operational secrets;
10. preserve superseded manifests and reasons for change.

Assets requiring unavailable rights or carrying unintended clinical, cultural or accessibility risks cannot enter the operational pool. Rights clearance for study use is not scientific-evidence or website-publication promotion.

## Transcript-independent decoy generation

For each eligible true sequence, decoys are selected by a deterministic, reproducible procedure using only precommitted inputs:

- frozen pool and stratum identifiers;
- target sequence technical metadata permitted by the rule;
- participant-event pseudonymous ID or a committed derivation;
- an independently generated secret seed committed before scoring;
- frozen sampling, exclusion and collision rules.

Transcript words, participant characteristics, reported imagery, scorer preferences and observed matches are prohibited inputs.

Decoys must be exchangeable with the true candidate under the scoring task as far as practical. They must match the frozen design on modality, presentation duration, number of elements, timing granularity, technical quality and prespecified complexity strata. The true candidate receives no distinctive label, file order, resolution, metadata, compression artefact or interface treatment.

A decoy may be replaced only for a frozen technical reason discovered without reference to transcript content. The original draw, replacement reason, replacement draw and both digests remain in the audit record. Human selection for an apparently “plausible” or “hard” foil is prohibited.

## Candidate-set commitment and masking

Before scorer access, the generator produces:

- unordered source candidate IDs;
- randomized masked labels;
- candidate renderings;
- pool, algorithm, seed-commitment and software versions;
- truth-linkage ciphertext held outside the scoring environment;
- candidate-set manifest and digest;
- creation timestamp and signer identity.

At least two independent checks must confirm that the masked files match the committed source assets and that no truth-revealing metadata remain. The packet assembler receives masked candidates only.

Candidate order is independently randomized per packet under the frozen rule. Screen layout, navigation, exposure time and response collection are identical for every candidate.

## Phase B — blinded correspondence scoring

At least two qualified scorers independently score every primary packet using the same locked claim table and masked candidate set.

The provisional rubric must distinguish:

- exact prespecified correspondence;
- partial correspondence;
- generic or high-base-rate overlap;
- contradiction;
- absent/unspecified attribute;
- timing consistency;
- modality consistency;
- recognition-only correspondence, reserved for a separately approved secondary packet and excluded from primary ranking;
- contamination-sensitive correspondence.

Every assigned value requires claim IDs, candidate IDs and rubric-rule IDs. Free-recall, prompted free-recall and recognition contributions remain separable. Scorers cannot add new claims, reinterpret the participant’s intended timing or consult outside event information.

The exact numerical scale and weights are not frozen by v0.1. They must be selected using synthetic or training data isolated from the confirmatory set, justified before unblinding, and evaluated by simulation for calibration, power and false-positive behaviour.

## Ties, disagreement and adjudication

- Candidate-score ties remain ties; no informal tie-break is allowed.
- Scorer disagreement is measured before adjudication.
- A scorer cannot revise a score after learning another scorer’s score.
- Adjudication uses masked labels and the same frozen rubric.
- The adjudicator may correct rule application but cannot invent transcript content or change decoys.
- Original scores, reasons and adjudicated values are all retained.
- Unresolved disagreement follows a prespecified aggregation or sensitivity rule.
- Inter-rater agreement is reported overall, by site, modality, content class and elicitation source where counts permit.

A truth-position reveal during disagreement handling is a critical breach and triggers `PAUSED_PENDING_ADJUDICATION`.

## Primary score and ranking contract

Before Stage 2, the SAP must freeze:

- primary score formula and direction;
- treatment of generic overlaps, contradictions and missing attributes;
- claim weighting and within-candidate aggregation;
- participant-event and target-epoch aggregation;
- decoy count and strata;
- handling of ties;
- scorer aggregation and adjudication;
- site and participant clustering;
- minimum meaningful effect;
- randomization distribution and exact test statistic;
- one- or two-sided decision rule;
- multiplicity family and adjustment;
- missingness and unresolved-state bounds;
- sensitivity analyses and negative controls;
- stopping, progression and rejection boundaries.

The primary null remains that true and decoy assignments are exchangeable under the frozen procedure. Stage-1 outcomes cannot tune the confirmatory score unless a training/validation split, version change and independent approval were prospectively specified.

## Negative controls and falsification diagnostics

The scoring pipeline must include prespecified controls such as:

- non-displayed candidate sequences;
- candidates from non-overlapping time windows;
- synthetic null transcripts;
- shuffled claim-to-packet assignments;
- metadata-blinded duplicate packets for reproducibility;
- leakage-positive rehearsal cases kept outside analysis;
- recognition-only versus free-recall contrasts;
- pre-lock versus append-only post-lock information contrasts.

Results count against the scoring or anomalous-correspondence interpretation when:

- masked true candidates do not outperform decoys under the frozen test;
- apparent effects depend on post-hoc categories or weights;
- performance tracks contamination, ordinary access or truth-position leakage;
- effects occur equally in negative-control windows or shuffled assignments;
- findings disappear with independent scoring or prespecified sensitivity analyses;
- the decoy procedure is not reproducible or exchangeable;
- independent preregistered replication fails.

Pipeline failure, severe attrition or insufficient information is not automatically evidence against awareness. It is classified separately as infeasible, not evaluable, or failure to detect the prespecified minimum effect.

## Leakage and security controls

The scoring environment must:

- use least-privilege role accounts and multifactor authentication;
- separate transcript, candidate and truth-linkage stores;
- encrypt data in transit and at rest;
- prohibit personal devices, screenshots, uncontrolled export and shared credentials;
- log reads, writes, downloads, transforms and releases;
- remove filenames, EXIF data, thumbnails, cache entries and ordering cues;
- verify reproducible software builds or record measured build digests;
- review access logs before unblinding;
- revoke access promptly after role changes;
- define incident classification, containment, key rotation and recovery;
- require dual control for linkage-table and seed-secret release.

Suspected access or metadata leakage is never silently repaired. The affected packet is held, the event retained, and the consequence independently adjudicated before any analytic inclusion decision.

## Score lock and unblinding sequence

Unblinding may begin only after all required objects are independently verified and locked:

1. source recording and final transcript;
2. atomic-claim table;
3. candidate-set manifest;
4. independent scorer records;
5. disagreement/adjudication record;
6. contamination and breach states;
7. analysis-code version and synthetic-data checks;
8. packet and score digests;
9. database snapshot and authorized release request.

Two authorized custodians approve release. The system records who released what, when, why and under which protocol version. Truth position is joined only inside the approved analysis environment. Scorers and interviewers receive no case-level correctness feedback during active collection.

Any post-unblinding correction is append-only, cannot replace the primary score, and requires a documented sensitivity analysis.

## Required scoring states

Every participant-event receives all applicable controlled states:

- `CLAIM_SET_LOCKED`
- `CLAIM_SET_DISAGREEMENT`
- `REPORT_NULL`
- `REPORT_NONSCORABLE`
- `SCORABILITY_UNKNOWN`
- `CANDIDATE_SET_COMMITTED`
- `DECOY_GENERATION_REPRODUCED`
- `DECOY_GENERATION_FAILED`
- `CANDIDATE_METADATA_LEAK`
- `DUAL_SCORING_COMPLETE`
- `SCORER_DISAGREEMENT`
- `ADJUDICATION_COMPLETE`
- `SCORE_LOCKED_BEFORE_UNBLINDING`
- `PREMATURE_TRUTH_REVEAL`
- `UNBLINDED_FOR_AUTHORIZED_ANALYSIS`
- `PACKET_HELD_PENDING_ADJUDICATION`

Unknown and unrecoverable states remain explicit and are never converted to clean records.

## Minimum machine-readable scoring record

The locked record includes:

- pseudonymous participant-event and packet IDs;
- protocol, INT-001 and SDC-001 versions;
- source recording, transcript and claim-table digests;
- target-pool, decoy-pool and candidate-set manifest digests;
- algorithm, seed-commitment and software-build identifiers;
- masked candidate IDs and randomized order;
- claim-level values, rule IDs and scorer rationales;
- scorer, adjudicator and certification pseudonyms;
- independent and adjudicated scores;
- tie and disagreement states;
- contamination, integrity and breach states;
- all exclusion/non-scorable reasons;
- score-lock and authorized-unblinding timestamps;
- access-log audit outcome;
- append-only amendments;
- analysis-population and sensitivity-analysis flags.

No public artifact may contain raw participant data, operational secrets or re-identifying linkage.

## Training, calibration and reproducibility

Certification requires:

- training on the frozen ontology and rubric;
- synthetic positive, null, ambiguous and contradictory cases;
- practice with masked true/decoy packets;
- prespecified agreement thresholds;
- successful reproduction of deterministic decoy test vectors;
- security and breach-reporting training.

Calibration data must be separate from confirmatory data. Recalibration during a confirmatory phase requires a prospective version boundary; it cannot use observed truth-position performance.

An independent implementation must reproduce candidate-set generation and numerical scoring from the same committed inputs before recruitment. Any tolerated numerical difference must be frozen and justified.

## Stage-1 scoring gates

At minimum, Stage 1 must report:

- claim-coder coverage and agreement;
- proportion of `ALL_INTERVIEWED` assigned each scorability state;
- dual-scorer coverage;
- categorical and continuous agreement under the frozen statistics;
- deterministic decoy-generation reproduction;
- candidate-set manifest verification;
- score-lock-before-unblinding compliance;
- unauthorized truth-access and metadata-leak incidents;
- packet production time and unresolved adjudication burden;
- pooled and by-site results with uncertainty;
- zero-denominator and insufficient-variance states as `NOT_EVALUABLE`.

Mandatory gates cannot offset one another. Critical leakage or premature unblinding pauses the affected analysis and triggers independent adjudication.

## Required before operational use

SDC-001 cannot be operational until all are complete:

- independent statistical and psychometric review;
- simulation of null calibration, power, tie frequency and false-positive behaviour;
- frozen target ontology, rubric, weights and decoy count;
- frozen SAP and randomization-test implementation;
- independent implementation and test-vector reproduction;
- security threat-model and access-control validation;
- clinical, ethics/IRB and data-protection approval;
- staff certification and multisite rehearsal;
- prospective registration and versioned publication policy.

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

SDC-001 is not evidence of continuity and cannot change BQ001 or any promotion gate.

