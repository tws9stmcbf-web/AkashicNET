#!/usr/bin/env python3
"""Generate review tables from retained synthetic outputs, never rerun simulations."""
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
rows=list(csv.DictReader((ROOT/'results/comparison.csv').open()))
lookup={(r['scenario'],int(r['pairs']),r['method'],r['sample']):r for r in rows}


def get(sc,n,method,sample=None):
    sample=sample or ('bootstrap_subset' if method=='bootstrap_t' else 'full')
    return lookup[sc,n,method,sample]


def fmt(r,key='joint'):
    return f"{100*float(r[key]):.2f}% ({100*float(r[key+'_lo']):.2f}–{100*float(r[key+'_hi']):.2f})"


def table(out,names,key='joint'):
    out.extend(['| Scenario | Pairs | Pair t | Bootstrap-t | Bounded betting | Empirical Bernstein | Hoeffding |',
                '| --- | ---: | --- | --- | --- | --- | --- |'])
    for sc,label in names:
        for n in [20,60,160]:
            values=[fmt(get(sc,n,m),key) for m in ['pair_t','bootstrap_t','betting_mixture','empirical_bernstein','hoeffding']]
            out.append('| '+' | '.join([label,str(n)]+values)+' |')
    out.append('')


out=['# Synthetic primary-alternative comparison results','',
     '26 October 2026 · Provisional methods assessment · No participant observations','',
     'Every entry is a rejection percentage with a pointwise 95% Wilson Monte Carlo interval. Pair t, betting, Bernstein and Hoeffding use 50,000 synthetic datasets/cell; bootstrap-t uses the first 4,000 of those datasets, with 999 resamples. The full CSV also contains every cheap method on that identical 4,000-dataset subset. Rejection frequencies compare the specified procedures and distributions; they are not hypothesis validation.','',
     '**Decision for independent review:** prioritize bounded-mean betting as a replacement family; do not adopt the tested bootstrap-t as a generally calibrated repair. The transparent Bernstein bound is a conservative comparator whose assessed power is generally impractical. Primary inference and final sample remain unresolved.','',
     '## Joint rejection under weak-null stresses','',
     'Every row below has at least one true component null. Joint rejection therefore is a false-positive event for the required two-mean claim. Reversed skew and negative covariance broaden the original challenge; the rare-adverse and sending-boundary stresses expose additional failures.','']
table(out,[('delta_skew10','Original 10% adverse contrast'),('delta_reverse10','Reversed contrast skew'),('delta_rare02','Rare 2% adverse contrast'),('chance_skew10','Skew at sending-chance boundary'),('both_null','Both boundaries, symmetric'),('delta_negative_cov','Delta boundary, negative arm covariance')])
out += ['The fresh original-skew anchor is a new Monte Carlo sample with a new seed tree, not a correction of the upstream 7.44% result. At 20 pairs it gives 7.66% joint rejection. Bootstrap-t reduces this to 6.33% (5.61–7.12%), but the rare-adverse contrast produces 13.28% (12.26–14.36%) at 20 pairs and 6.20% (5.49–6.99%) at 160. The sending-boundary skew gives bootstrap-t 8.45% (7.63–9.35%) at 20. Thus improved performance on the original distribution is insufficient for promotion.','',
        'In the rare-adverse mixture, the probability of sampling no adverse pair is .98^D: about 66.8% at 20 pairs, 29.8% at 60 and 3.9% at 160. Resampling observed pairs cannot add an unobserved pair type. This explains the challenge; it is a deliberately extreme bounded weak-null stress, not an empirical prevalence estimate.','',
        'Zero observed rejection means no events in this finite run, not zero risk. For 0/50,000 the pointwise Wilson upper limit is about 0.0077%. The bounded guarantees come from the stated mathematics and assumptions, subject to implementation review; they are not established by these simulation zeros.','',
        '## Check each true component, not only the conjunction','',
        '| Method | Maximum observed true-component rejection across declared null cells | Scenario | Pairs |',
        '| --- | --- | --- | ---: |']
for method in ['pair_t','bootstrap_t','betting_mixture','empirical_bernstein','hoeffding']:
    options=[]
    for sc in ['delta_skew10','delta_reverse10','delta_rare02','chance_skew10','both_null','delta_negative_cov']:
        for n in [20,60,160]:
            r=get(sc,n,method)
            for key in (['reject_A','reject_D'] if sc=='both_null' else ['reject_A'] if sc=='chance_skew10' else ['reject_D']):
                options.append((float(r[key]),r,key))
    _,r,key=max(options,key=lambda z:z[0])
    out.append(f"| {method} | {fmt(r,key)} ({key}) | {r['scenario']} | {r['pairs']} |")
out += ['', 'These are maxima over a small searched grid, with pointwise intervals; they are not simultaneous upper bounds on worst-case size. The bounded methods were conservative for both true components in the declared cells.','',
        '## Conditional joint power','',
        'All rows below have A>0 and Delta>0 in the declared mathematical model. Uniform latent ICC=.05; 100 scheduled trials/pair. Effect size and cross-arm coupling both differ between some rows, so there is no isolated cross-scenario estimate of an effect-size penalty.','']
table(out,[('alt05_independent','30%/25%, independent arms'),('alt03_shared','28%/25%, shared arms'),('alt10_independent','35%/25%, independent arms')])
out += ['In the five-point reference at 160 pairs, betting joint rejection is **80.82% (80.47–81.16%)**, versus 98.52% for the provisional t rule and 98.38% for bootstrap-t. The latter procedures have weak-null calibration failures elsewhere, so their higher rejection rates cannot be treated as an equally valid efficiency advantage. Betting falls to 5.77% at 60 pairs; its finite-sample protection has a large cost at that scale.','',
        'At the three-point/shared-arm 160-pair case, betting joint power is 39.32% (38.89–39.74%). Empirical Bernstein has 0/50,000 joint rejections in the five-point reference and only 0.036% in the ten-point/160-pair case; Hoeffding has zero joint rejections throughout these complete-data power examples. Neither is an attractive default at the assessed scale.','',
        '**The 80.82% figure is not final sample approval.** It is one hypothetical model/cell under one baseline strategy. Meaningful effects, covariance, completion, generalization, final testing rules and feasibility remain unresolved, with no search for a recommended sample.','',
        '## Matched-dataset bootstrap comparisons','',
        'Both columns below use the identical first 4,000 synthetic datasets. The disagreement counts are paired decisions, not independent simulation samples. Small apparent differences should not be over-interpreted.','',
        '| Scenario | Pairs | Pair t, matched subset | Bootstrap-t | Bootstrap-only / t-only rejections |',
        '| --- | ---: | --- | --- | ---: |']
paired={(r['scenario'],int(r['pairs'])):r for r in csv.DictReader((ROOT/'results/bootstrap-vs-t-paired.csv').open())}
for sc,n in [('delta_skew10',20),('delta_rare02',20),('delta_rare02',160),('chance_skew10',20),('alt05_independent',160)]:
    pr=paired[sc,n]
    out.append(f"| {sc} | {n} | {fmt(get(sc,n,'pair_t','bootstrap_subset'))} | {fmt(get(sc,n,'bootstrap_t'))} | {pr['bootstrap_only']} / {pr['t_only']} |")
out += ['', '## Omission and scientific-interpretation stresses','',
        '| Scenario | Pairs | Method | Raw joint | Gate passage | Joint AND gate |',
        '| --- | ---: | --- | --- | --- | --- |']
for sc in ['alt05_mcar5','selective_omission']:
    for n in [60,160]:
        for method in ['pair_t','bootstrap_t','betting_mixture','empirical_bernstein','hoeffding']:
            r=get(sc,n,method)
            out.append('| '+' | '.join([sc,str(n),method,fmt(r),fmt(r,'gate_pass'),fmt(r,'joint_gated')])+' |')
out += ['', 'Exactly 5% independent population omissions leave the empirical 5% gate near its threshold, so passage is about one half. Gated success is the conjunction over all datasets, never conditional power after deleting failed-gate datasets.','',
        'Selective omission changes scheduled score means to .294/.180 despite equal .30/.30 latent hit rates. Betting can reject that changed score null almost always at larger pair counts, while the proposed integrity gate blocks every run here. This is not weak-null miscalibration for the observed operational means, and the gate is not a universal safeguard: subtler informative omissions, missing logs and consent deletion need prespecified contingencies.','',
        '## Scope and remaining limits','',
        'The fixed plan, complete component/joint/gate results, seed tree, pinned dependencies, arithmetic/enumeration checks and retained-byte hashes are part of this draft research workflow. There is no empirical participant validation, reviewed protocol, final sample, recruitment or scientific promotion. Private correspondence was not copied and prior messages were not repeated.','',
        'Unexplored leads: more efficient independently specified bounded betting, alternative bootstrap families, design-specific studentized randomisation, intermediate covariance, session/carryover and cross-pair dependence, real allocator/software leakage and deletion contingencies. None is assumed resolved by the present grid.']
(ROOT/'RESULTS.md').write_text('\n'.join(out)+'\n')
print('Wrote RESULTS.md from retained CSVs')
