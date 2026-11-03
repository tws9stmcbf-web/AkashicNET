# Synthetic primary-alternative comparison results

26 October 2026 · Provisional methods assessment · No participant observations

Every entry is a rejection percentage with a pointwise 95% Wilson Monte Carlo interval. Pair t, betting, Bernstein and Hoeffding use 50,000 synthetic datasets/cell; bootstrap-t uses the first 4,000 of those datasets, with 999 resamples. The full CSV also contains every cheap method on that identical 4,000-dataset subset. Rejection frequencies compare the specified procedures and distributions; they are not hypothesis validation.

**Decision for independent review:** prioritize bounded-mean betting as a replacement family; do not adopt the tested bootstrap-t as a generally calibrated repair. The transparent Bernstein bound is a conservative comparator whose assessed power is generally impractical. Primary inference and final sample remain unresolved.

## Joint rejection under weak-null stresses

Every row below has at least one true component null. Joint rejection therefore is a false-positive event for the required two-mean claim. Reversed skew and negative covariance broaden the original challenge; the rare-adverse and sending-boundary stresses expose additional failures.

| Scenario | Pairs | Pair t | Bootstrap-t | Bounded betting | Empirical Bernstein | Hoeffding |
| --- | ---: | --- | --- | --- | --- | --- |
| Original 10% adverse contrast | 20 | 7.66% (7.43–7.89) | 6.33% (5.61–7.12) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Original 10% adverse contrast | 60 | 6.51% (6.30–6.73) | 5.25% (4.60–5.99) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Original 10% adverse contrast | 160 | 5.61% (5.41–5.82) | 4.42% (3.83–5.11) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Reversed contrast skew | 20 | 3.45% (3.30–3.62) | 4.85% (4.23–5.56) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Reversed contrast skew | 60 | 3.99% (3.83–4.17) | 4.72% (4.11–5.43) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Reversed contrast skew | 160 | 4.52% (4.35–4.71) | 5.53% (4.86–6.28) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Rare 2% adverse contrast | 20 | 13.61% (13.32–13.92) | 13.28% (12.26–14.36) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Rare 2% adverse contrast | 60 | 12.51% (12.22–12.80) | 11.97% (11.01–13.02) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Rare 2% adverse contrast | 160 | 8.86% (8.62–9.11) | 6.20% (5.49–6.99) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Skew at sending-chance boundary | 20 | 9.44% (9.19–9.70) | 8.45% (7.63–9.35) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Skew at sending-chance boundary | 60 | 7.12% (6.89–7.34) | 5.03% (4.39–5.75) | 0.20% (0.16–0.24) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Skew at sending-chance boundary | 160 | 6.12% (5.91–6.33) | 4.35% (3.76–5.03) | 0.28% (0.24–0.33) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Both boundaries, symmetric | 20 | 1.75% (1.64–1.87) | 1.85% (1.48–2.32) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Both boundaries, symmetric | 60 | 1.87% (1.76–2.00) | 2.15% (1.74–2.65) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Both boundaries, symmetric | 160 | 1.88% (1.76–2.00) | 2.20% (1.79–2.70) | 0.03% (0.02–0.05) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Delta boundary, negative arm covariance | 20 | 5.23% (5.03–5.42) | 4.47% (3.88–5.16) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Delta boundary, negative arm covariance | 60 | 5.13% (4.94–5.33) | 5.47% (4.81–6.22) | 0.04% (0.03–0.06) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| Delta boundary, negative arm covariance | 160 | 5.11% (4.92–5.30) | 4.60% (3.99–5.29) | 0.31% (0.26–0.36) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |

The fresh original-skew anchor is a new Monte Carlo sample with a new seed tree, not a correction of the upstream 7.44% result. At 20 pairs it gives 7.66% joint rejection. Bootstrap-t reduces this to 6.33% (5.61–7.12%), but the rare-adverse contrast produces 13.28% (12.26–14.36%) at 20 pairs and 6.20% (5.49–6.99%) at 160. The sending-boundary skew gives bootstrap-t 8.45% (7.63–9.35%) at 20. Thus improved performance on the original distribution is insufficient for promotion.

In the rare-adverse mixture, the probability of sampling no adverse pair is .98^D: about 66.8% at 20 pairs, 29.8% at 60 and 3.9% at 160. Resampling observed pairs cannot add an unobserved pair type. This explains the challenge; it is a deliberately extreme bounded weak-null stress, not an empirical prevalence estimate.

Zero observed rejection means no events in this finite run, not zero risk. For 0/50,000 the pointwise Wilson upper limit is about 0.0077%. The bounded guarantees come from the stated mathematics and assumptions, subject to implementation review; they are not established by these simulation zeros.

## Check each true component, not only the conjunction

| Method | Maximum observed true-component rejection across declared null cells | Scenario | Pairs |
| --- | --- | --- | ---: |
| pair_t | 13.61% (13.32–13.92) (reject_D) | delta_rare02 | 20 |
| bootstrap_t | 13.28% (12.26–14.36) (reject_D) | delta_rare02 | 20 |
| betting_mixture | 0.38% (0.33–0.44) (reject_A) | both_null | 60 |
| empirical_bernstein | 0.00% (0.00–0.01) (reject_D) | delta_skew10 | 20 |
| hoeffding | 0.00% (0.00–0.01) (reject_D) | delta_skew10 | 20 |

These are maxima over a small searched grid, with pointwise intervals; they are not simultaneous upper bounds on worst-case size. The bounded methods were conservative for both true components in the declared cells.

## Conditional joint power

All rows below have A>0 and Delta>0 in the declared mathematical model. Uniform latent ICC=.05; 100 scheduled trials/pair. Effect size and cross-arm coupling both differ between some rows, so there is no isolated cross-scenario estimate of an effect-size penalty.

| Scenario | Pairs | Pair t | Bootstrap-t | Bounded betting | Empirical Bernstein | Hoeffding |
| --- | ---: | --- | --- | --- | --- | --- |
| 30%/25%, independent arms | 20 | 31.17% (30.76–31.58) | 31.45% (30.03–32.91) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 30%/25%, independent arms | 60 | 73.60% (73.21–73.98) | 73.55% (72.16–74.89) | 5.77% (5.57–5.97) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 30%/25%, independent arms | 160 | 98.52% (98.41–98.62) | 98.38% (97.93–98.72) | 80.82% (80.47–81.16) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 28%/25%, shared arms | 20 | 16.82% (16.49–17.15) | 16.65% (15.53–17.84) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 28%/25%, shared arms | 60 | 55.63% (55.19–56.06) | 55.83% (54.28–57.36) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 28%/25%, shared arms | 160 | 94.09% (93.88–94.30) | 94.47% (93.72–95.14) | 39.32% (38.89–39.74) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 35%/25%, independent arms | 20 | 81.13% (80.79–81.47) | 78.95% (77.66–80.19) | 0.01% (0.00–0.02) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 35%/25%, independent arms | 60 | 99.83% (99.79–99.86) | 99.90% (99.74–99.96) | 76.16% (75.78–76.53) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| 35%/25%, independent arms | 160 | 100.00% (99.99–100.00) | 100.00% (99.90–100.00) | 100.00% (99.99–100.00) | 0.04% (0.02–0.06) | 0.00% (0.00–0.01) |

In the five-point reference at 160 pairs, betting joint rejection is **80.82% (80.47–81.16%)**, versus 98.52% for the provisional t rule and 98.38% for bootstrap-t. The latter procedures have weak-null calibration failures elsewhere, so their higher rejection rates cannot be treated as an equally valid efficiency advantage. Betting falls to 5.77% at 60 pairs; its finite-sample protection has a large cost at that scale.

At the three-point/shared-arm 160-pair case, betting joint power is 39.32% (38.89–39.74%). Empirical Bernstein has 0/50,000 joint rejections in the five-point reference and only 0.036% in the ten-point/160-pair case; Hoeffding has zero joint rejections throughout these complete-data power examples. Neither is an attractive default at the assessed scale.

**The 80.82% figure is not final sample approval.** It is one hypothetical model/cell under one baseline strategy. Meaningful effects, covariance, completion, generalization, final testing rules and feasibility remain unresolved, with no search for a recommended sample.

## Matched-dataset bootstrap comparisons

Both columns below use the identical first 4,000 synthetic datasets. The disagreement counts are paired decisions, not independent simulation samples. Small apparent differences should not be over-interpreted.

| Scenario | Pairs | Pair t, matched subset | Bootstrap-t | Bootstrap-only / t-only rejections |
| --- | ---: | --- | --- | ---: |
| delta_skew10 | 20 | 7.25% (6.49–8.10) | 6.33% (5.61–7.12) | 10 / 47 |
| delta_rare02 | 20 | 13.43% (12.40–14.52) | 13.28% (12.26–14.36) | 37 / 43 |
| delta_rare02 | 160 | 8.18% (7.37–9.06) | 6.20% (5.49–6.99) | 2 / 81 |
| chance_skew10 | 20 | 9.80% (8.92–10.76) | 8.45% (7.63–9.35) | 11 / 65 |
| alt05_independent | 160 | 98.47% (98.05–98.81) | 98.38% (97.93–98.72) | 2 / 6 |

## Omission and scientific-interpretation stresses

| Scenario | Pairs | Method | Raw joint | Gate passage | Joint AND gate |
| --- | ---: | --- | --- | --- | --- |
| alt05_mcar5 | 60 | pair_t | 64.70% (64.28–65.12) | 51.28% (50.84–51.72) | 33.60% (33.19–34.02) |
| alt05_mcar5 | 60 | bootstrap_t | 65.55% (64.06–67.01) | 50.50% (48.95–52.05) | 33.60% (32.15–35.08) |
| alt05_mcar5 | 60 | betting_mixture | 4.02% (3.85–4.20) | 51.28% (50.84–51.72) | 2.04% (1.92–2.17) |
| alt05_mcar5 | 60 | empirical_bernstein | 0.00% (0.00–0.01) | 51.28% (50.84–51.72) | 0.00% (0.00–0.01) |
| alt05_mcar5 | 60 | hoeffding | 0.00% (0.00–0.01) | 51.28% (50.84–51.72) | 0.00% (0.00–0.01) |
| alt05_mcar5 | 160 | pair_t | 97.29% (97.15–97.43) | 51.26% (50.82–51.69) | 49.94% (49.50–50.37) |
| alt05_mcar5 | 160 | bootstrap_t | 97.20% (96.64–97.67) | 49.25% (47.70–50.80) | 47.88% (46.33–49.42) |
| alt05_mcar5 | 160 | betting_mixture | 73.36% (72.97–73.75) | 51.26% (50.82–51.69) | 37.87% (37.45–38.30) |
| alt05_mcar5 | 160 | empirical_bernstein | 0.00% (0.00–0.01) | 51.26% (50.82–51.69) | 0.00% (0.00–0.01) |
| alt05_mcar5 | 160 | hoeffding | 0.00% (0.00–0.01) | 51.26% (50.82–51.69) | 0.00% (0.00–0.01) |
| selective_omission | 60 | pair_t | 100.00% (99.99–100.00) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 60 | bootstrap_t | 100.00% (99.90–100.00) | 0.00% (0.00–0.10) | 0.00% (0.00–0.10) |
| selective_omission | 60 | betting_mixture | 99.99% (99.98–100.00) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 60 | empirical_bernstein | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 60 | hoeffding | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 160 | pair_t | 100.00% (99.99–100.00) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 160 | bootstrap_t | 100.00% (99.90–100.00) | 0.00% (0.00–0.10) | 0.00% (0.00–0.10) |
| selective_omission | 160 | betting_mixture | 100.00% (99.99–100.00) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 160 | empirical_bernstein | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |
| selective_omission | 160 | hoeffding | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) | 0.00% (0.00–0.01) |

Exactly 5% independent population omissions leave the empirical 5% gate near its threshold, so passage is about one half. Gated success is the conjunction over all datasets, never conditional power after deleting failed-gate datasets.

Selective omission changes scheduled score means to .294/.180 despite equal .30/.30 latent hit rates. Betting can reject that changed score null almost always at larger pair counts, while the proposed integrity gate blocks every run here. This is not weak-null miscalibration for the observed operational means, and the gate is not a universal safeguard: subtler informative omissions, missing logs and consent deletion need prespecified contingencies.

## Scope and remaining limits

The fixed plan, complete component/joint/gate results, seed tree, pinned dependencies, arithmetic/enumeration checks and retained-byte hashes are part of this draft research workflow. There is no empirical participant validation, reviewed protocol, final sample, recruitment or scientific promotion. Private correspondence was not copied and prior messages were not repeated.

Unexplored leads: more efficient independently specified bounded betting, alternative bootstrap families, design-specific studentized randomisation, intermediate covariance, session/carryover and cross-pair dependence, real allocator/software leakage and deletion contingencies. None is assumed resolved by the present grid.
