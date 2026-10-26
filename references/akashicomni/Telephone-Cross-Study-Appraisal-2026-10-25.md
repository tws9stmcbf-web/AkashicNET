# Telephone caller-identification studies: focused cross-study appraisal

25 October 2026 (America/Los_Angeles). AI-assisted documentary appraisal; **INDEPENDENT_SCIENTIFIC_REVIEW_PENDING / REVIEW_REQUIRED**. This is an addition to draft PR #399, not an inferential reanalysis, formal peer review or release.

## Assessment

**Related experiments with substantially different methods.** A source-labelled descriptive comparison is useful; a pooled accuracy estimate, combined significance claim, or direct replication-success verdict is not currently justified. Different alternatives alone need not prohibit a future meta-analysis, but the null-generating mechanisms, selection, dependence and estimands must first be reconciled.

Stedall and Tressoldi's 2025 experiment tests the fourth Sheldrake–Stedall protocol [S1, p203], not a direct replication of Wahbeh's two-condition design. Independence should be described by component: KPU1048 names Tressoldi and Sheldrake as leads [S2, p1], and Stedall also coauthored the predecessor. This does not invalidate replication, but “independent” should not imply independent platform development or a fully separate research lineage.

The [22 October correction](IONS-Telephone-Correction-2026-10-22.md) remains authoritative for the completed descriptive reconciliation [S8]. It is not repeated or modified here. Corrected Wahbeh inference remains pending.

## Design and analysis map

| Dimension | Stedall–Tressoldi | Wahbeh and colleagues |
|---|---|---|
| Participant selection | Adults recruited personally by an assistant, mainly Padova students [S1, p204]. KPU1048 requires mutual bonding at least 3/5 [S2, p3]. | Adults with smartphones and English competency; health-related exclusions [S4, pp3–4]. IONS recruitment networks; family-relatedness design later admits friends [S7, pp3–4]. Neither is a population-probability sample. |
| Roles and conditions | One designated receiver, two nominated callers; caller chosen before guessing. No post-selected condition [S2, p3]. | Triad roles allocated by the system; pre-selected intention condition and post-selected connection condition [S4, pp4–5]. |
| Response alternatives | Two caller identities, nominal chance 1/2 [S2, pp1–3]. | Two other people or “no one,” nominal chance 1/3 [S4, pp4–6]. “No one” is a possible outcome after post-selection, but not the destination of the pre-selected guessing receiver [S3, pp3–4]. |
| Units and denominators | 117 receivers; 294 hits/604 completed trials (48.6%) [S1, pp204–205]. | Corrected completers: 35 triads/105 people; 210 pre-selected response records and 630 post-selected records. Each completed post-selected call event supplies three responses [S8]. |
| Planned selection/stopping | Six trials per receiver; recruit replacements to reach 600; retain valid partial sessions, exclude technical failures [S2, p2]. Reported total slightly exceeds target [S1, p204]. | Main completer and separate incomplete-session analyses; original target 100 triads and funding deadline [S4, p5]. Later target 30, broader eligibility and higher compensation [S7, p3]. |
| Caller randomisation | Registered PHP Mersenne Twister [S2, p3]; paper specifies mt_rand and time/location/system seeding [S1, p204]. | Registration specifies random.org [S5, p4]; publication describes PHP pseudorandom generation [S3, p3]. Adaptive path assignment documented during collection [S6, pp4–5]. |
| Concealment and leakage controls | Generic caller ID and guess recorded before voice connection [S2, p3]; assistant reportedly present with receiver [S1, p205]. | Guesser intended to be blind to condition; automated prompts and randomised response-key mapping [S3, pp3–4]. No contemporaneous receiver supervision reported; paper acknowledges possible pre-selected co-location communication [S3, p7]. |
| Confirmatory analysis | KPU1048: exact one-sided binomial against .50, alpha .05; approximately five-percentage-point anticipated excess [S2, pp1–2]. | Above-chance accuracy for each path; exact binomial, Agresti–Coull intervals; fixed-response, simulated-target randomisation for post-selection dependence [S4, pp5–6]. |
| Exploratory analysis | Retrospective reported strategy groups [S1, pp205–206]; absent from KPU1048 [S2]. | Between-path difference, genetic relatedness and relational moderators designated exploratory [S7, pp2–3]; publication also contains post-hoc response-bias and protocol checks [S3, p8]. |

## What the registered results do and do not say

The 2025 paper reports an overall one-tailed p=.76 and does not confirm its anticipated above-chance performance [S1, p205]. This is a failure to demonstrate the registered effect in that sample/protocol. Failure to reject a chance null is not an equivalence test, a bound excluding every small effect, or disproof of anomalous information transfer.

KPU1048 specifies testing against 50%, not using 55% as the statistical null [S2, pp1–2]. The paper's “at least 55%” language therefore concerns the anticipated effect. It reports a z statistic alongside a binomial result [S1, p205]; exact-versus-approximate implementation should be checked against syntax rather than assumed from that presentation. No p-values are independently recalculated here.

For Wahbeh, reuse the completed correction and its pending corrected randomisation requirement [S8]. Historical binomial significance cannot stand in for that requirement. Do not repeat the first-six-trials restriction or alter completion labels again.

## Why the numerical scales are not interchangeable

The following is methodological reasoning, not a new empirical result.

A response menu does not by itself determine the chance distribution. Conditional on being the pre-selected guessing receiver, “no one” cannot be the actual connection. Under fair assignment of the two real callers, if the receiver chooses “no one” with probability q, expected accuracy is (1-q)/2. One-third follows only at q=1/3. Guesser blinding to condition does not make an impossible target possible. Wahbeh's discussion itself recognises response-frequency sensitivity [S3, p8].

The binary design has a .50 null if caller allocation remains fair and independent of guesses among included trials. Unequal answering/completion probabilities could change that distribution; target-assignment and failed-attempt logs are needed to assess this possibility. This is an audit question, not an allegation that imbalance occurred.

The strongest apparent bridge is the restricted Wahbeh analysis discussed by Stedall–Tressoldi: excluding “no one” guesses makes a caller-only comparison possible [S1, p204]. However, Wahbeh explicitly presents this as post hoc and uses the including-dropout population [S3, p8]. It is not the corrected completer endpoint, and exclusion after observing response behaviour does not recreate a prospectively binary task. Its null still requires checking target allocation, missingness and selection.

Repeated observations within receivers/triads require attention. Repetition alone does not invalidate a binomial test if targets are independent, correctly calibrated and completion is non-informative. Those assumptions require evidence. Three responses sharing one post-selected connection are additionally coupled, explicitly recognised in KPU1062 [S4, p6]. Neither 604 nor 630 is a participant count. A significant finding in one study and a non-significant finding in another is not itself a significant between-study difference.

## Exploratory strategy observations

The reported groups are 220/395 intuitive-strategy hits and 74/209 rational-strategy hits [S1, p205]. Strategy was reported after feedback-bearing trials; it was not randomly assigned. These groups cannot demonstrate that intuitive instructions cause better performance, nor establish a telepathic mechanism.

The preregistration contains no strategy analysis [S2]. Classification rules, coder blinding, reliability, unreported candidate partitions and multiplicity are unresolved. Post-performance self-description permits reverse explanation and confounding. The paper's separate within-group tests do not replace a prespecified direct strategy contrast. The striking lower-performing group warrants the same scrutiny as the higher-performing group. A future test could randomise strategy instructions prospectively, use blind coding and registered contrasts, and retain full completion logs.

## Registration fidelity and unresolved questions

- **KPU1048:** Verify whether the bonding threshold was implemented; it is not documented in the publication. Clarify why the registry permits role switching [S2, p3] while the paper describes a fixed receiver [S1, p204]. Establish recruitment dates, stopping/overshoot accounting, all attempted versus completed calls, repeated participation and overlapping friend groups. These are reporting gaps, not proven deviations.
- **KPU1062:** Reconcile random.org in the registrations with PHP generation in the paper. The amendments document consent/compensation changes (23 February), adaptive path balance and more attempts (14 March), then reduced recruitment target and friend eligibility (20 July) [S5–S7]. Changes occurred during collection; preserve version chronology and inspect outcomes without fitting exclusions. The final registration's attempt cap and publication also differ; this is already adjacent to the historical methods follow-up.
- **Blinding:** Distinguish caller concealment, receiver condition concealment, assistant target access, researcher access to running outcomes, and blinded analysis. Wahbeh reports investigators blind to hit totals until collection stopped [S3, p3]. The 2025 system offers password-protected running totals [S1, p205]; availability does not establish investigator access or optional stopping. Neither automation nor a non-cryptographic RNG proves leakage or proves its absence.
- **Reproduction:** The 2025 paper's Figshare DOI did not resolve through the inspected retrieval paths. Do not infer that data are absent or relabel a different deposit as its raw data. Wahbeh's publisher-final supplement/corrigendum and corrected v2 were not newly retrieved. No participant-level files, caller logs or production code were independently audited.

## Independent critique and scope

Schmidt, Erath, Ivanova and Walach (2009) [S9, pp12–13] provide a primary, independent methodological critique of earlier telephone experiments: guesses recorded after answering permit auditory cues; familiar-caller comparisons require response-bias correction; selection and flexible protocols affect interpretation. They also acknowledge improved videotaped controls and report Sheldrake's competing randomisation response. This is a specific methodological dispute, not a blanket dismissal.

Their older four-caller experiments are not direct audits of these automated systems. The relevant transferable questions are secure pre-connection guess recording, target/response-frequency calibration, observation and registered selection. Bounded searches did not locate a dedicated independent critique of the 2025 report; this does not establish none exists. The 2025 field meta-analysis [S10] shares authors with the binary experiment and is not independent adjudication of either study.

## Next independent-review packet

Before quantitative synthesis, obtain: (1) corrected Wahbeh targets, labels and analysis scripts; (2) verified 2025 data/syntax and attempt-level accounting; (3) actual RNG implementation and assignment logs; (4) eligibility, concealment and strategy-coding documentation. Predefine a common caller-identification estimand and valid null, account for clustering/overlap and protocol versions, then assess whether a restricted sensitivity comparison is defensible. Raw-rate pooling, pooling p-values and mechanistic promotion are premature.

**Boundary unchanged:** claims UNRESOLVED; independent review PENDING; engineering UNRELEASED / REVIEW_REQUIRED; promotion flags false; no accepted model support. No merge, site deployment or private-correspondence publication.

[Source-access and preservation receipt](telephone-cross-study-appraisal-2026-10-25.json).

## Sources

Locations are printed page numbers unless noted. Public sources inspected 25 October 2026 PDT / 26 October UTC.

- **S1:** Stedall & Tressoldi (2025), *Who is calling? An Independent Replication of a Telephone Telepathy Test*, JSE 39(2), 203–206. [Publication](https://journalofscientificexploration.org/index.php/jse/article/view/3543), DOI [10.31275/20253543](https://doi.org/10.31275/20253543), [full text](https://journalofscientificexploration.org/index.php/jse/article/view/3543/2345).
- **S2:** [KPU1048](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1048.pdf), submitted 3 November 2018, pp1–3; linked to S1 by the [official register](https://koestlerunit.wordpress.com/study-registry/registered-studies/). No revision listed for 1048 at inspection.
- **S3:** Wahbeh, Cannard, Radin & Delorme (2024; online 2023), EXPLORE 20(2), 239–247, DOI [10.1016/j.explore.2023.08.008](https://doi.org/10.1016/j.explore.2023.08.008). [Article-in-press full text](https://www.sheldrake.org/files/pdfs/papers/Whos-calling-evaluating-the-accuracy-of-guessing-who-is-on-the-phone.pdf), local PDF pagination 1–9, not a corrected publisher edition.
- **S4:** [KPU1062 original](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062.pdf), 28 July 2021.
- **S5:** [KPU1062 revision 2](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062_2.pdf), 23 February 2022.
- **S6:** [KPU1062 revision 3](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062_3.pdf), 14 March 2022.
- **S7:** [KPU1062 revision 4](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062_4.pdf), 20 July 2022.
- **S8:** [Existing 22 October correction](IONS-Telephone-Correction-2026-10-22.md), reused without reopening correspondence or redoing arithmetic; [public correction](https://akashicnet.org/noetic-sciences/telephone-study-correction).
- **S9:** Schmidt et al. (2009), *Do You Know Who is Calling? Experiments on Anomalous Cognition in Phone Call Receivers*, Open Psychology Journal 2, 12–18. [Primary full text](https://openpsychologyjournal.com/contents/volumes/V2/TOPSYJ-2-12/TOPSYJ-2-12.pdf), DOI [10.2174/1874350100902010012](https://doi.org/10.2174/1874350100902010012).
- **S10:** Sheldrake, Stedall & Tressoldi (2025), [Telecommunication Telepathy: A Meta-Analysis](https://journals.lub.lu.se/jaex/article/view/25934). Used only for research-lineage context, not adopted as an independent review.
