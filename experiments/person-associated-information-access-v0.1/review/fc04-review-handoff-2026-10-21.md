# FC04 replacement distractors: review-only handoff

**21 October 2026 · FC04-P2 · AI-suggested · NOT ADOPTED · NOT FOR PARTICIPANT USE**

This is a separate proposal for independent stimulus and methods review. It does not replace [materials 0.2-candidate](../materials/stimulus-set.json), change protocol 0.1, close FC04, or complete any approval. The baseline is commit `2ccb4e2a254c3e5ed604e4b8fc5869fbdde695e3`. All existing material hashes remain valid. No reviewers were contacted and no participant or concealed-target data were created.

The [earlier correction record](../materials/fact-check-2026-10-21.md) found that selecting the second-earliest year answers all eight delayed-recognition items correctly. Shuffling screen positions cannot remove that ordering rule. This handoff makes an alternative concrete for the [existing independent-review packet](review-packet.md).

## Proposed options

Every correct year, keyed option ID, prompt, rationale, source mapping and do-not-know permission is retained. Only the three wrong year values and reviewer serialization order would change if a later review adopted the proposal. No timing, scoring, T/U allocation, hidden-symbol procedure, primary outcome or sample size is changed. Reviewer option IDs remain private metadata; existing stage-specific projection and independent display shuffling are still required.

| Figure | Proposed years, sorted for inspection | Correct year | Correct chronological rank |
| --- | --- | --- | --- |
| Marie Curie | 1911, 1914, 1918, 1922 | 1911 | 1 |
| C. V. Raman | 1923, 1926, 1930, 1934 | 1930 | 3 |
| Dorothy Crowfoot Hodgkin | 1957, 1960, 1964, 1968 | 1964 | 3 |
| Barbara McClintock | 1980, 1983, 1987, 1991 | 1983 | 2 |
| Niels Bohr | 1919, 1922, 1926, 1930 | 1922 | 2 |
| Rabindranath Tagore | 1902, 1905, 1909, 1913 | 1913 | 4 |
| Wangari Maathai | 1993, 1996, 2000, 2004 | 2004 | 4 |
| Santiago Ramón y Cajal | 1906, 1909, 1913, 1917 | 1906 | 1 |

These are synthetic wrong options, not historical assertions about awards in those years. The correct years remain grounded in the sources linked in the [assertion/item record](../materials/fact-check-2026-10-21.json). The [machine-readable proposal](fc04-distractor-candidate-2026-10-21.json) contains the full mapping.

## Construction and rejected attempts

The first attempt, [FC04-P1](fc04-discarded-p1-2026-10-21.json), balanced chronological ranks but allowed a smallest-last-digit strategy to score 5/8. It was discarded. Two subsequent intermediate selections introduced a 2015 Maathai option and a 1994 McClintock option; these were also rejected before publication of this proposal.

The final construction uses ascending within-item offsets `[0, 3, 7, 11]`, assigns each correct chronological rank exactly twice, excludes years before 1901, and excludes McClintock options in or after 1992 and Maathai options in or after 2011. The last two limits are conservative proposed-option boundaries, not a general ruling on posthumous prize eligibility.

Maathai's death date, 25 September 2011, is supported by retrieved [Nelson Mandela Foundation biography text](https://www.nelsonmandela.org/wangari-maathai-bio), attributed there to the Green Belt Movement, and indexed [official Nobel facts](https://www.nobelprize.org/prizes/peace/2004/maathai/facts/). McClintock's death date, 2 September 1992, is supported by indexed [official Nobel facts](https://www.nobelprize.org/prizes/medicine/1983/mcclintock/facts/). The new direct GBM request returned HTTP 429 and the UN profile request HTTP 403; source access and rights limitations are recorded in the proposal. These boundaries and new sources remain subject to independent verification and rights review.

The reproducible search enumerates 2520 rank assignments, of which 414 satisfy the year boundaries and 88 satisfy all nine declared rule constraints. A public SHA-256 tie-break selects one assignment. This deterministic selection concerns public review materials only; it is not random target generation. No participant responses were used.

The nine rules were used in construction. Their scores below are **not held-out or independent validation**. The search has no claim to cover all exploitable strategies.

## Static diagnostics

Values are correct items out of eight, with uniform tie-breaking where required. Bounds show the least/most successful possible resolutions of ties on these fixed eight items; they are not confidence intervals.

| Rule | Existing set | Proposed set | Proposed tie-resolution bounds |
| --- | ---: | ---: | --- |
| earliest | 0.0 | 2.0 | [2, 2] |
| second earliest | 8.0 | 2.0 | [2, 2] |
| third earliest | 0.0 | 2.0 | [2, 2] |
| latest | 0.0 | 2.0 | [2, 2] |
| closest to midrange | 8.0 | 2.0 | [2, 2] |
| closest to mean | 8.0 | 2.0 | [2, 2] |
| closest to multiple of ten | 2.5 | 2.0 | [2, 2] |
| smallest last digit | 5.0 | 2.0 | [2, 2] |
| largest last digit | 0.0 | 0.0 | [0, 0] |

Every fixed chronological-rank rule now scores 2/8 in this proposal. All 24 option-display permutations per item were enumerated: each display slot contains the correct option in 6/24 permutations. This is a mathematical enumeration, not a test of an implemented runtime or its random-number generator. The correct answer stays attached to its stable option ID in every permutation.

The audit also confirms the ten existing material-manifest hashes, preserved answers/prompts/source mappings, all source/rights records still pending, and all seven independent-review rows still NOT_STARTED. The [audit output](fc04-candidate-audit-2026-10-21.json) identifies exact proposal and script hashes.

Reproduce with Python's standard library, from the experiment directory; compare stdout with the corresponding committed JSON files:

```bash
python3 review/build_fc04_candidate.py
python3 review/audit_fc04_candidate.py
```

## Required independent disposition

FC04 remains **OPEN**. An appointed reviewer must record identity, conflicts, exact commit/file hashes, reasoning and an accept/revise/reject decision. The following questions are unresolved:

- Are the three wrong years plausible for each figure, with comparable difficulty, cultural familiarity and readability? The span narrows from 21 to 11 years, which may change recognition difficulty.
- Does public knowledge of the balanced ranks enable cross-item elimination when some answers are known? No feedback does not eliminate that possibility. Should exact balance be retained, or a different prespecified construction be used?
- Do era knowledge, repeated years, digit patterns, award-category knowledge or other untested strategies still distort the intended memory measure? The nine construction rules do not settle this.
- Does the actual future interface correctly shuffle options, retain ID-to-answer mapping, separate do-not-know, and withhold keys, metadata and future items? No runtime exists to validate here.
- If adopted, what revised materials version and immutable freeze should supersede the current candidate? Preserve the original set and current audit as history; rerun affected source, scoring, accessibility and methods checks before any sign-off.

The proposal does not resolve the 14 indexed-only assertion records from the earlier fact-check, rights review, proponent specifications, statistical joint-power work, ethics, cultural review, accessibility, security, acquisition/custody, independent reproduction or registration. The experiment remains unauthorized. Use the [proposal manifest](fc04-review-manifest-2026-10-21.json) to identify this review packet; it is not a preregistration or approval.
