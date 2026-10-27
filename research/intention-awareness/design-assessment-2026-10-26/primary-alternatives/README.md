# Provisional primary-test alternatives for Intention Awareness

26 October 2026 · Follow-up to draft PR #415 · Synthetic observations only

This bounded extension evaluates replacements for the provisional pair t tests. It reuses `../assessment.py` and adds 33 declared cells rather than rerunning the completed factorial assessment. [plan.json](plan.json) was written before the numerical run. It is an analysis plan for synthetic comparisons, not a preregistered participant protocol. Original assessment files and the published October addenda are preserved.

**No primary method or final sample is adopted.** The scientific hypothesis remains UNTESTED; independent statistical review is PENDING. [review-status.json](review-status.json) preserves these gates alongside the [upstream status](../review-status.json). No emails are sent by this follow-up.

## Preserve the two required successes

For independent participant pairs, let S_i and C_i be hits divided by scheduled trials in each arm, with ordinary omissions scored zero. Retain equal pair weights and the same two weak population-mean nulls:

- H_A: E(S_i) <= .25, with S_i in [0,1].
- H_D: E(S_i-C_i) <= 0, with S_i-C_i in [-1,1].

Require **both** one-sided component tests to reject at .05 using one prespecified method per component. This intersection-union rule needs no Bonferroni division between these two mandatory criteria: under the union null at least one component is true, and joint rejection is a subset of that component's rejection. It does require a valid test of every true component. Report each component, their conjunction, the proposed integrity gate, and conjunction with that gate. Gate passage is not a data-selection step for the reported rejection rate.

Do not select whichever candidate gives the most favorable observed result, or use one method to rescue another. Choosing among these methods belongs before participant outcomes and requires independent review. Adding an OR across methods or sensitivities would be a different, multiplicity-sensitive rule.

## Candidate definitions and inferential assumptions

| Method | Target and assumptions | Finite-sample control | Skew and power considerations |
| --- | --- | --- | --- |
| Fixed-mixture bounded betting | Same weak means; independent IID pair vectors from the target population, known bounds, fixed weights and bets | A nonnegative terminal e-value with null expectation <=1 gives a level-.05 component rule at E>=20. Mathematical argument below; implementation not independently reviewed | No normality or symmetry assumption; can tolerate rare extremes in its theorem. Known full ranges limit permissible bets and can cost substantial power |
| Empirical Bernstein | Same weak means; bounded independent IID pair vectors, fixed analysis size | One-sided lower confidence bound from Maurer-Pontil Theorem 4, reflected and rescaled | Variance-sensitive but its range-dependent finite-n penalty is substantial; skew does not defeat the stated bound |
| Pair-vector bootstrap-t | Same weak means; IID representative pairs, nonzero variance and a reliable empirical approximation to the pair distribution | Approximate/asymptotic only; no distribution-free finite-sample claim | Studentization can improve ordinary skew behavior; resampling cannot recover a rare adverse type absent from the sample. Discrete/degenerate pivots need conventions |
| Pair t test, reference | Same weak means; exact normal model or sufficient asymptotic approximation across pairs | Exact normal-model test, not general finite-sample weak-null control | Already fails upstream skew stress; retained to measure gains/costs on identical datasets |
| Hoeffding, reference | Same weak means; bounded independent pairs | Range-based one-sided finite-sample bound | Retains the previously assessed conservative benchmark; not adopted |

The paired contrast always uses each pair's S_i-C_i. No trial independence is assumed for these pair-summary methods. Independence **between** pairs, trustworthy assignment/response logs, the scheduled scoring definition and the intended population remain substantive assumptions. Shared people, cross-pair communication, selective enrollment or post-outcome exclusions are not repaired by a bounded test. A convenience sample does not automatically represent a broader population.

### Fixed mixture and a short control argument

For X_i=S_i, use m0=.25, a=0, b=1; for X_i=S_i-C_i, use m0=0, a=-1, b=1. Predefine q=(.10,.25,.50,.75,.99), lambda_j=q_j/(m0-a), and equal weights 1/5. The implemented statistic is

`E_n = (1/5) sum_j product_i [1 + lambda_j (X_i-m0)]`.

Each factor is nonnegative throughout the **known** score support. Under the IID composite null E(X_i)<=m0, its expectation is <=1; independence makes the product expectation <=1. The fixed mixture also has expectation <=1. Markov's inequality gives P(E_n>=20)<=.05. This is a direct specialization of bounded-mean betting, not an implementation of the cited authors' optimized strategy. Computation uses logs and log-sum-exp.

The final-time argument also extends to independent nonidentically distributed pairs when their **average expected score** is <=m0: for each constant lambda, the product of nonnegative expected factors is at most their arithmetic average to the n-th power. That extension concerns a fixed-size average and does not itself justify optional stopping or population generalization. The simulation targets IID pairs. No sequential stopping protocol is proposed.

The fixed mixture is not the maximum over bets. Observed minima/maxima do not replace the known bounds, and full-data estimates do not select a favorable lambda. Optimized predictable betting or fixed-time constructions could warrant further review, but optimizing on this grid and calling the same grid validation would be circular. Terminal E>=20 is used for each criterion; no minimum over times, favorable subset or repeated analysis is evaluated.

### Empirical Bernstein implementation

For score support [a,b], n pairs and sample variance v using divisor n-1, the lower bound is

`L = mean(X) - sqrt[2 v log(2/.05)/n] - 7 (b-a) log(2/.05) / [3(n-1)]`.

Apply Theorem 4 to `(b-X)/(b-a)` to obtain the required upper-tail protection for the observed mean and hence this lower bound on the true mean. Reject if L>m0. The contrast's known width is **2**, the sending score's **1**. These are separate marginal bounds used in the mandatory AND rule, not simultaneous confidence intervals.

### Bootstrap implementation

Resample complete pair vectors with replacement, using identical pair indices for A and Delta. For each endpoint compute `t_observed=mean(X)/SE(X)` and centered `t*=[mean(X*)-mean(X)]/SE(X*)`, where X is S-.25 or S-C. Estimate the upper-tail probability with inclusive ties and `(1 + number(t*>=t_observed))/(B+1)`. The plus-one convention avoids zero estimates; bootstrap draws are not an exact null randomisation distribution and this convention does **not** make the test exact.

Observed zero variance gives no rejection, matching the upstream convention. Zero-variance bootstrap resamples count as upper-tail exceedances, a deliberately conservative numerical rule. All such choices require review. These are ordinary multinomial resamples, not Owen's proposed beta-weight variant or a BCa interval.

## Bounded follow-up design

The 11 scenarios in [plan.json](plan.json) use 20, 60 and 160 pairs. This is 33 cells, with 50,000 synthetic datasets per cell for the four cheap methods, and 4,000 datasets with 999 resamples each for bootstrap-t. Every cheap method is additionally reported on those same 4,000 datasets for fair paired comparisons; [bootstrap-vs-t-paired.csv](results/bootstrap-vs-t-paired.csv) records discordant decisions. More repetitions of a smaller grid quantify Monte Carlo uncertainty; they do not certify robustness across all distributions.

New stress directions are reversed contrast skew, a rarer 2% adverse-pair component, skew in the sending-chance boundary, opposite cross-arm latent effects, and the impact of existing omission mechanisms on each replacement. The upstream skew distribution is reused only as an anchor at three sizes. No prior power factorial, 30/100-pair skew cells or trial-level randomisation study is repeated.

The rare adverse mixture uses sending=.30; control=.288 for 98% of pairs or .888 for 2%. Its control mean is exactly .30, so Delta=0. The sending-boundary mixture uses .27 for 90% or .07 for 10%, mean .25, against .20 control. These are deliberate mathematical weak-null challenges, not psychological models or blinded target-independence nulls.

Power examples retain the inherited uniform random effects: .30/.25 with independent arms, .28/.25 with shared arms, and .35/.25 with independent arms, rho=.05 and 100 trials/pair. The three-point case also changes cross-arm coupling; do not attribute differences from the five-point case solely to effect size. There is no sample-size search, interpolation or approval.

The selective-omission case has equal .30/.30 latent hit probabilities but scheduled observed means .294/.180. Its positive score contrast is **not** a false positive for the operational mean null. It challenges the interpretation of score success as information transfer. The proposed gate and completion assumptions need independent scientific and statistical review.

## Numerical results

The strongest review lead is bounded betting, with an explicit efficiency tradeoff. In the five-point, independent-arm, rho=.05 example at 160 pairs it gave 80.82% joint rejection (95% Monte Carlo interval 80.47–81.16%). In the rarer adverse-pair null, bootstrap-t rejected jointly in 13.28% of 20-pair simulations and 6.20% at 160, so it is not a generally calibrated repair. These are provisional synthetic findings, not sample approval.

See [RESULTS.md](RESULTS.md), the complete [comparison.csv](results/comparison.csv) and [run metadata](results/run.json). All intervals are pointwise 95% Wilson **Monte Carlo** intervals. They are neither participant effect intervals nor simultaneous coverage statements. Bootstrap intervals include variability of the stated finite-resample decision rule; at B=999 its per-dataset tail-probability Monte Carlo SE near .05 is about .0069. For 4,000 outer repeats, SE near 5% is about .34 percentage points; for 50,000 it is about .10 points.

## Independent-review priorities

1. **Bounded betting merits first review as a replacement family.** Audit the two mean targets, known score bounds, component and joint control argument, eligibility/omission mapping, actual fixed-mixture code and power costs. Consider a separately specified, more efficient fixed-time or predictable strategy only with new checks; the current mixture is a baseline, not a selected protocol.
2. **Bootstrap-t merits conditional review, not automatic promotion.** Determine whether pair sampling and heterogeneity assumptions make it credible at a feasible design scale; inspect the rare-adverse-pair and sending-boundary failures, discreteness, degeneracy rules and simulation uncertainty. A finite grid that looks calibrated does not prove uniform control.
3. **Empirical Bernstein is a transparent finite-sample fallback/comparator.** Review its exact theorem direction, score range and penalty. Its power may make it impractical; retaining a guarantee alone does not solve feasibility.
4. **A design-specific studentized randomisation analysis is a separate review lead.** Wu-Ding and Chung-Romano explain how studentization can yield asymptotic weak-null validity under stated experimental designs. Their results do not automatically validate the existing condition shuffle, the target shuffle, a pair sign-flip test or this proposed design. Derive its exact allocator, potential-outcome target, cluster variance, omission/carryover assumptions and both success criteria before implementation. No new randomisation method is promoted here.

A sign test or signed-rank test changes the target toward signs/medians or a symmetry-based location parameter; neither generally establishes these two population means under heterogeneous skew. A standard mixed-model likelihood test or small-sample cluster correction can be useful under its model but does not by itself remove misspecification or guarantee 5% control here. These options were screened conceptually, not implemented as extra rescue paths.

Reviewers must settle meaningful effects, representativeness and independent-pair structure, missing/deleted data contingencies, a single method for each criterion, stopping/reporting rules and design feasibility before fresh final-test power planning. Neither this follow-up nor passing software checks validates the hypothesis or approves recruitment.

## Reproduce

Use Python 3.12 and the parent's pinned NumPy/SciPy requirements. No participant-input or network interface is provided by the simulation.

```sh
cd research/intention-awareness/design-assessment-2026-10-26/primary-alternatives
python -m pip install -r ../requirements.txt
python -m unittest discover -s . -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python alternatives.py --out reproduced
python verify.py
```

Compare reproduced CSV and metadata hashes with the retained run before replacing any reviewed files. Exact bytes depend on recorded versions, seed tree, scenario order, data chunk size and bootstrap batch size. The small GitHub smoke run is a software check only. [sources.json](sources.json) identifies primary methods and access limits. No cited author or institution endorses this proposal.
