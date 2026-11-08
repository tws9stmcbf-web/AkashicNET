# Telephone Study Correction Addendum · Figshare v2 and Wavelength Alignment

8 November 2026 · Public-source verification · Independent scientific review pending.

This addendum updates the release and analysis-availability checkpoints in the [22 October correction](IONS-Telephone-Correction-2026-10-22.md). The October note and receipts are preserved as dated provenance. [PR #399](https://github.com/tws9stmcbf-web/AkashicNET/pull/399) is the continuing review record.

## Public Figshare v2

The [Figshare version record](https://api.figshare.com/v2/articles/21521235/versions/2) dates [v2](https://doi.org/10.6084/m9.figshare.21521235.v2) to 30 October 2026. It retains the v1 workbook as a separate file and adds a README and a ZIP containing corrected completion labels, trial-level data, a revised Figure 2 and analysis code. The archive's internal “v3” label is distinct from the repository version, v2. The deposited README describes the three corrected completion-status labels and records that the first-six-trials restriction is already applied. The journal corrigendum DOI is a placeholder in that README. No published journal corrigendum was identified in the public records checked on 8 November.

The public ZIP (Figshare file 70899264) matched its deposited MD5, `917e34e53510e1967532bd5859d7d416`. Running the deposited `scripts/reproduce_accuracy_results.py` with its trial-level CSV, 10,000 simulations and fixed seed 2026 returned these aggregate outputs.

| Endpoint | Completers | Including dropouts |
| --- | --- | --- |
| Pre-selected correct responses | 101/210 (48.1%) | 147/289 (50.9%) |
| Post-selected correct responses | 205/630 (32.5%) | 243/762 (31.9%) |
| Pre-selected randomisation p-value | .169 | .026 |

The script's one-sided post-selected completer binomial test against 0.33 returned p = .6117. There were 630 post-selected completer responses across 210 trials. The pre-selected randomisation holds guesses fixed, treats “no one” as incapable of a hit and uses inclusive ties, whereas the original methods describe strict exceedances. The change from the original completer randomisation (228 responses, p = .054) therefore should not be attributed solely to the corrected labels. The v2 rerun reproduces the deposited model's output. It does not refit the regressions or settle questions about assignment, trial dependence or selection.

## Downstream Citation

[Ali, Azam and Jahangiri](https://doi.org/10.1016/j.explore.2026.103554), available online in *Explore* on 4 November 2026, repeat the [original abstract's](https://pubmed.ncbi.nlm.nih.gov/37709571/) 50.0% pre-selected accuracy and nominal 33.3% comparator in the Introduction (reference 2). The article-in-press [Table 3, p. 6](https://www.sheldrake.org/files/pdfs/papers/Whos-calling-evaluating-the-accuracy-of-guessing-who-is-on-the-phone.pdf#page=6) gives 48.1% for pre-selected completers. The new paper also reports a non-significant post-selected result without quoting 31.9%. That percentage matches the including-dropout rate. Its use with the completer denominator in the older abstract remains unexplained.

The 50.0% figure provides literature context and is not a parameter of the magnetic feasibility calculation or proposed test thresholds. The earlier exploratory distance result informs the new paper's distance-stratified design, while communication frequency motivates the familiarity question. The theoretical proposal remains empirically unresolved. Its approximately 7 μT modelled detector threshold and 0.5 fT estimated field at 0.3 m are calculations. Proposed signature decoding, blinded proximity and calibrated magnetic shielding tests are separate from observations.

## Cross-References

- [Research Atlas · SRC08](https://akashicnet-research-atlas.vocal-crow-3599.chatgpt.site/?record=SRC08)
- [AkashicNET · Public Telephone Study Correction](https://akashicnet.org/noetic-sciences/telephone-study-correction)
- [PR #399 · Cross-Study Appraisal](Telephone-Cross-Study-Appraisal-2026-10-25.md)
- [Schmidt et al. (2009)](https://openpsychologyjournal.com/VOLUME/2/PAGE/12/) is reference 3 in the new paper. [Stedall and Tressoldi (2025)](https://journalofscientificexploration.org/index.php/jse/article/view/3543) is the separate comparator in PR #399's appraisal.

This addendum contains public-source references and aggregate outputs. Claim status remains UNRESOLVED and independent review remains PENDING.
