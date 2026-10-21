# Independent review packet and decision register

**Date:** 18 October 2026  
**Candidate:** protocol 0.1 plus materials 0.2-candidate  
**Status:** DRAFT / STAGE 0 / REVIEW_REQUIRED

This packet gives reviewers concrete materials and questions. No reviewer has been appointed or contacted by this change. No independent sign-off, ethics determination, registration or experiment has occurred. GitHub documents and synthetic calculations remain the only authorized work.

## Decisions the proponent must specify

Acceptance of the random person-associated hidden-symbol bridge is recorded in protocol.json. The following decisions are still **UNRESOLVED**; drafting scripts does not supply the proponent's assent.

| Decision | Concrete proposal for review | Required record |
| --- | --- | --- |
| Instruction fidelity | Use the exact five-minute M track and one-minute reminders in materials/session-scripts.md, with no extra ritual or neural claim. | Accept, revise or reject the wording and duration; give reasons before data. |
| Necessary conditions | Present hidden targets, no living sender, a one-day dossier delay, four trained and four minimally cued people, no special-state requirement. | State whether these conditions are sufficient for the proposed prediction. If not, specify observable conditions and redesign before registration. |
| Meaningful effect | Keep H1 and H2 as written; separately define the smallest practically meaningful MT advantage over 0.25 and MT–RT difference. | Two numerical effect thresholds with a rationale. No numerical value has been approved. |
| Representation claim | Keep the T/U interaction exploratory in this feasibility pilot. | Confirm whether the main theory requires the interaction; if it does, a later powered confirmatory test is necessary. |
| A constraining null | A precise result can constrain only the signed operational effect under agreed conditions. | Specify in advance what interval would count against the numerical prediction; prohibit post hoc “wrong state” explanations that change eligibility. |

The proposed scripts and timings are AI-suggested implementation choices. They do not turn the original neural-representation hypothesis into an established construct. Source identity and physical 7D storage have no success criteria here.

## Required roles and independence

A responsible institution/investigator must appoint people and disclose conflicts. At minimum, the stimulus/key reviewer, statistician and security reviewer must be independent of the proponent and original implementation author. Two analysts must reproduce the approved export. A skeptical reviewer and a contemplative-practice reviewer can assess different concerns; neither replaces ethics review. Remote target custody must remain separate from participant contact and selective exclusions.

| Review | Exact inputs | Questions and required deliverable | Current state |
| --- | --- | --- | --- |
| Stimuli and ordinary scoring | materials/stimulus-set.json; materials/README.md | Verify every factual assertion, source access, key and distractor. Check that final recall is distinct from award-year recognition. Record errors and signed disposition. | NOT_STARTED |
| Methods and cultural fidelity | session-scripts.md; README sections 2–5 | Are instructions interpretable and acceptable? Are duration, expectancy and workload differences adequately described? Does U exposure undermine the intended manipulation? | NOT_STARTED |
| Statistics | protocol.json; reference code/tests; validation.json | Review estimands, null assumptions, fixed denominators, withdrawal policy, randomization test and intervals; independently simulate joint decisions. | NOT_STARTED |
| Acquisition and custody | data-dictionary.md; future deployed system | Inspect an actual isolated implementation, commitment receipts, response locks, clocks, recovery paths and access logs. No implementation exists yet. | NOT_STARTED |
| Ethics and data governance | future consent/debrief and management plan | Obtain institutional determination, eligibility rules, risk/withdrawal response, retention/deletion, compensation and controlled-release decisions. | NOT_STARTED |
| Accessibility | text, future audio and actual interface | Check screen reader/keyboard equivalence, names, response timing, translations and accommodations without target leakage. | NOT_STARTED |
| Independent reproduction | immutable code/materials and synthetic authorized export | Recompute every planned score and demonstrate failure handling. Same-assistant checks do not count. | NOT_STARTED |

Reviewers record identity/role, conflict statement, exact commit and file hashes, issues, response to each issue, decision and date. Changes after a sign-off invalidate that sign-off for affected files. Leave all boxes open until an actual signed review exists; no auto-approval by passing software tests.

## AI-assisted stimulus preparation update, 21 October 2026

The [source-linked fact-check](../materials/fact-check-2026-10-21.md) and [assertion/item record](../materials/fact-check-2026-10-21.json) are available for the appointed independent reviewer. They do not change any NOT_STARTED independent-review state above. Historical assertions are classified by retrieved-page versus indexed-only support; pending rights reviews remain pending.

**FC04 requires disposition before use:** all eight recognition items use the same year offsets (-9, 0, +6, +12), so choosing the second-earliest year yields 8/8 without recall. Screen-position randomization does not fix this. The current correction leaves options unchanged to preserve the proposed design; an independent stimulus/methods review must approve a replacement distractor scheme and new material freeze. This concern applies to ordinary recognition, not the independently concealed symbol task.

Other human-review work remains: original-source access/attribution, frozen field/synonym codebook, distractor plausibility, cultural/readability/accessibility checks and inference ceiling effects. No newly completed scientific, statistical, ethics or security review is claimed.

## Statistical review specification

The existing calculation covers H1 alone under an ideal homogeneous model. It does not establish adequate power for the joint rule or the representation interaction. Do not describe the 48-person pilot as adequately powered from the 61/192 threshold.

An independently written simulator should reproduce the actual 24-of-48 arm randomization, four-of-eight T assignment per participant, eight fixed people, two hidden trials per person, recorded target generation, scoring and missing-data rules. Preserve participant clustering and paired T/U structure. Compare the existing reference implementation with an independently implemented analysis.

The following are **proposed simulation inputs**, not observations or approved minimum effects:

| Scenario | MT | MU | RT | RU | Purpose |
| --- | ---: | ---: | ---: | ---: | --- |
| Clean target null | .25 | .25 | .25 | .25 | Joint false-positive calibration under independent concealed assignments |
| Small trained M advantage | .30 | .25 | .25 | .25 | Sensitivity to a five-point MT excess |
| Larger trained M advantage | .35 | .25 | .25 | .25 | Sensitivity to a ten-point MT excess |
| M advantage in both familiarity conditions | .35 | .35 | .25 | .25 | Show that a primary signal need not imply a T/U interaction |
| Shared trained advantage | .35 | .25 | .35 | .25 | Show that H1 alone need not imply an M-versus-R effect |
| Equal elevation in every cell | .35 | .35 | .35 | .35 | Show that general target correspondence need not support M specificity |

These are abstract performance distributions, not mechanisms. Ordinary learning cannot by itself make independently concealed targets predictable under the documented null.

Include:
- Homogeneous participants and heterogeneous alternatives with prespecified between-participant and within-person dependence. Under the clean target null, independent fresh target labels imply conditionally independent .25 matches; do not introduce a beta-binomial target null merely because human responses are correlated.
- Missing opportunities at 0%, 5% and 10%, both independent and arm-related; all lawful fixed denominators remain. These percentages are stress-test settings only.
- Learning failure, timing deviations, noncompletion and a failure to enroll all 48. Incomplete enrollment has descriptive outcomes only under version 0.1.
- Deliberate leakage, swapped IDs, nonuniform/target-balanced draws and premature opening as invalid-integrity scenarios. Successful detection/blocked interpretation, not a “corrected significant result,” is the expected system response.
- H1-only and H2-only rejection, both-primary rejection, interaction estimates, interval coverage, Monte Carlo error and the proportion rendered not evaluable.
- A reproducible seed/configuration manifest and enough simulated replicates for a stated Monte Carlo precision target; the statistician chooses and justifies the run count before inspecting favorable power curves.
- A separate evaluation of the proposed 20,000-resample percentile intervals in this small pilot. If uncertainty coverage is poor, revise the analysis before registration rather than claim that the bootstrap is exact.

Do not promote a simulation outcome to empirical evidence. Do not tune thresholds or sample size using participant outcomes.

## Security acceptance exercises using synthetic data only

The security reviewer must evaluate the eventual implementation, not just assertions in this packet:

1. Search participant-facing HTML, JavaScript bundles, JSON, accessibility labels, caches, error messages, telemetry, filenames and network traffic for truth or salts. Verify stage-specific stimulus projection so answer keys and future items are not preloaded.
2. Attempt four-code brute-force recovery from published commitments; secret random salts must prevent this shortcut. Validate canonical serialization and trusted pre-response receipts.
3. Inject late commitments, ambiguous clock ordering, target openings before full locks, altered records and incorrect participant/person/trial joins. Each must preserve a fault record and block a clean scientific interpretation.
4. Exercise reconnects, retries, clipboard, downloads, crash recovery and backups. Confirm no redraw, overwrite, silent exclusion or target-dependent timing.
5. Verify staff role separation and target-invariant audio, reflections and display behavior. Audit the actual test environment and permitted accessibility aids.
6. Demonstrate no live study data or real targets are sent to public GitHub, AI tools or unauthorized analytics. Use obviously synthetic fixtures during engineering.
7. Independently replay all planned slots and reconcile every disposition. Withdrawal behavior must match the institution-approved policy; erasure rights cannot be bypassed to satisfy an analysis.

The present change implements none of the acquisition or custody system. It contains no credentials, participants or hidden assignments.

## Ethics and release preparation

Prepare, for institutional review, an information sheet, consent form, neutral debrief, contact/support route, compensation schedule, accessibility plan and data-management/withdrawal policy. Name the responsible institution before claiming any exemption or approval. The draft debrief in session-scripts.md is only a starting text.

No deception about authentic contact, spiritual attainment or diagnosis. No drug intervention, sleep manipulation, brain stimulation or clinical recruitment. Optional subjective reports remain Lived Experience-Testimony; they cannot authenticate the source.

After reviews, reconcile all comments into a new version. Freeze the approved protocol, complete materials, actual audio/interface, custody code, analysis code, exclusion/deviation rules and report template with immutable timestamps before real data. Record a registration URI and independent sign-offs explicitly. Prospective registration does not itself grant ethics approval.

Maintain the existing issue #354 classification:
- Candidate hypothesis: Hypothesis / working hypothesis.
- Hidden present targets without sender: RV; CHN/MED only separate attributed-source reports.
- TEL, PRE/PRE-PHY, PK/BIO-PK not tested.
- Big Questions UNRESOLVED; accepted canonical edges 0; supports_models empty.
- Truth inference, evidence/model/rights/public/website promotion and experimental execution remain closed.

## Next handoff

The concrete next handoff is this commit plus its material hashes to an appointed independent methods/statistics reviewer and stimulus reviewer. No request has been sent. In parallel, the proponent can resolve the three outstanding specifications: script fidelity, necessary conditions and meaningful effect. Recruitment begins only after all required reviews, implementation audit and prospective registration.

