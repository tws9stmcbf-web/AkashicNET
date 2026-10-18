# Future Data Dictionary and Lock Contract

Draft specification; no real dataset exists. Public files in this candidate contain no participant information or secret targets. The descriptive study slug is not a canonical PSI claim identifier.

## Separation of stores

| Store | Minimum fields | Access and release |
| --- | --- | --- |
| Consent/contact | consent version, legal retention/withdrawal permissions, private linkage | Independent controller; never public GitHub |
| Enrollment ledger | pseudonymous participant ID, screening/eligibility/disposition, allocation receipt, scheduled 16 slots | Custodian and auditor; approved aggregates |
| Person-material manifest | fixed person ID, exact cues/dossier versions, fact/inference keys, sources and rights | Frozen before enrollment; no hidden assignment |
| Familiarization | participant ID, four T/four U assignment, exposure duration, baseline and delayed scores, timing deviations | Masked analysts; de-identification review |
| Secret target store | trial/person/participant IDs, target code, secret salt, canonical record hash, encryption and signing metadata, trusted commitment receipt, clock uncertainty | Independent custodian; no response-system access |
| Response store | trial ID, original text lock, choice code or null, confidence, attribution, felt connection, times, independent response receipt | Facilitator cannot join to target truth |
| Integrity ledger | statuses, exact fault reason, extent and time, reviewer identity, original and amended decision receipts | Freeze before outcome join; preserve all versions |
| Authorized analysis export | all planned rows, blinded arm, T/U, verified result/status, permitted targets after locks, software/protocol hashes | Independent analysts; raw release only after privacy/ethics review |

Identity deduplication is performed by an authorized custodian before randomization, with minimum necessary data. No browser fingerprinting or undeclared tracking is prescribed. Eight person IDs appear twice each per participant; four remain T and four U throughout. Trial IDs cannot encode the selected symbol. Every retry remains linked to the first attempt. Never overwrite raw text with a cleaned or AI-assisted version.

## Planned-slot status vocabulary

- observed: one timely locked choice and a verified concealed pre-response target.
- abstain: explicit no-choice response.
- timeout: no choice before the frozen deadline.
- not_started: planned trial not begun.
- technical_failure: acquisition, receipt, device or join failure.
- integrity_failure: confirmed or unresolved concealment/ordering/custody issue.
- withdrawn: no usable outcome retained under the approved policy.

A status is not an exclusion. All statuses stay in lawful aggregate counts. Primary scoring gives 1 only to a verified observed exact match, otherwise 0; valid-observation and uncertainty bounds are separate. Withdrawal can make the fixed-denominator test not evaluable if legal retention is insufficient. Never create a fictitious individual row to circumvent erasure rights.

The early-stop ledger includes trials that had no target generated. Those receive no invented target value. Any systemic integrity issue blocks interpretation; a clean-looking subset is not substituted.

## Synthetic reference format

reference_analysis.py deliberately accepts only a document with data_kind = SYNTHETIC and study_version = 0.1. This marker is a guard, not a privacy detector. Do not relabel real data to bypass it. A production export/parser requires separate approval and implementation.

The synthetic fixture contains:

- participants: 48 unique IDs and arm M or R; 24 each.
- trials: 768 unique participant_id/trial_index pairs; index 0–15.
- person_id: F01–F08, each twice, with familiarity T or U fixed within person.
- choice and target: integer 0–3 or null; booleans are invalid.
- status: one of the seven declared values.
- target_committed_at, response_locked_at, target_opened_at: numerical toy times for observed rows, with strict order commitment < response < opening.

The toy order check does not verify cryptography, trusted clocks, real device access, valid consent or sensory isolation. Those require the independent audit and full receipt verification specified in the protocol. Synthetic fixtures are deterministic software examples, never concealed targets or participant data.

## Output contract

Reference output labels every table SYNTHETIC_ONLY and includes:

- planned and valid denominators for all MT/MU/RT/RU cells;
- hits, zero-scored dispositions and best/worst bounds;
- H1 exact target-null p-value;
- H2 participant-allocation permutation p-value, draws, seed and Monte Carlo error;
- participant bootstrap intervals for all four cells, the trained contrast and interaction;
- unresolved integrity count and participant resampling unit.

No output labels a mechanism established, opens a gate or grants publication rights. The future report must add the full screening flow, withdrawal-policy audit, independent reproduction, receipt verification and all outcome deviations.

