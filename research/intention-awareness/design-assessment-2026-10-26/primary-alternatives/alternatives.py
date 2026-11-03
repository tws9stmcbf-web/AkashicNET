#!/usr/bin/env python3
"""Bounded synthetic follow-up. Reuses PR #415 generators and reporting utilities."""
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy import special

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from assessment import ALPHA, latent_rates, metric, t_pvalue, write_csv

PLAN = json.loads((ROOT/'plan.json').read_text())
FRACTIONS = np.array(PLAN['bet_fractions'])
METHODS = ['pair_t', 'betting_mixture', 'empirical_bernstein', 'hoeffding']


def validate_values(x, low, high):
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or x.shape[1] < 2 or not np.isfinite(x).all():
        raise ValueError('Expected finite rows of at least two independent pair scores')
    if np.any(x < low-1e-12) or np.any(x > high+1e-12):
        raise ValueError('Scores outside declared pre-data bounds')
    return x


def betting_log_e(x, null, low, high):
    """Fixed equal mixture of nonnegative constant-bet product e-values.

    With independent identically distributed pairs E(X)<=null, each factor
    1+lambda*(X-null) is nonnegative and has expectation <=1.
    Mixture weights are fixed, not the post-data maximizing bet.
    """
    x = validate_values(x, low, high)
    if not low < null < high:
        raise ValueError('Interior null required')
    lam = FRACTIONS/(null-low)
    log_capital = np.stack([np.log1p(l*(x-null)).sum(axis=1) for l in lam], axis=1)
    return special.logsumexp(log_capital, axis=1)-np.log(len(lam))


def bernstein_lower(x, low, high, alpha=ALPHA):
    """Maurer-Pontil Thm 4, applied to reflected/rescaled bounded observations."""
    x = validate_values(x, low, high)
    n = x.shape[1]
    log = np.log(2/alpha)
    radius = np.sqrt(2*x.var(axis=1, ddof=1)*log/n)+(high-low)*7*log/(3*(n-1))
    return x.mean(axis=1)-radius


def hoeffding_lower(x, low, high, alpha=ALPHA):
    x = validate_values(x, low, high)
    return x.mean(axis=1)-(high-low)*np.sqrt(np.log(1/alpha)/(2*x.shape[1]))


def analytic_flags(s, c):
    delta = s-c
    return {
        'pair_t': (t_pvalue(s-.25)<=ALPHA, t_pvalue(delta)<=ALPHA),
        'betting_mixture': (betting_log_e(s,.25,0,1)>=np.log(1/ALPHA),
                           betting_log_e(delta,0,-1,1)>=np.log(1/ALPHA)),
        'empirical_bernstein': (bernstein_lower(s,0,1)>.25, bernstein_lower(delta,-1,1)>0),
        'hoeffding': (hoeffding_lower(s,0,1)>.25, hoeffding_lower(delta,-1,1)>0),
    }


def bootstrap_from_indices(x, indices):
    """Centered bootstrap-t pivots for both endpoints with identical pair resamples.

    x shape = (2, outer_batch, pairs); indices=(outer_batch, draws, pairs).
    Resample original pair vectors, never individual trials/arms independently.
    Zero resample variance is counted as an upper-tail exceedance (conservative).
    Zero observed variance yields p=1, matching inherited no-rejection convention.
    Plus-one regularizes finite-draw estimates; it confers no exact bootstrap validity.
    """
    n = x.shape[-1]
    mean = x.mean(axis=-1)
    se = x.std(axis=-1, ddof=1)/np.sqrt(n)
    observed = np.divide(mean, se, out=np.zeros_like(mean), where=se>1e-14)
    pvals = []
    for k in range(2):
        sample = np.take_along_axis(x[k,:,None,:], indices, axis=2)
        boot_mean = sample.mean(axis=2)
        boot_se = sample.std(axis=2, ddof=1)/np.sqrt(n)
        numerator = boot_mean-mean[k,:,None]
        pivot = np.divide(numerator, boot_se, out=np.full_like(numerator,np.inf), where=boot_se>1e-14)
        # Floating-point ties are inclusive with small explicit tolerance.
        exceed = pivot >= observed[k,:,None]-1e-12
        p = (1+exceed.sum(axis=1))/(indices.shape[1]+1)
        pvals.append(np.where(se[k]>1e-14,p,1.))
    return tuple(pvals)


def bootstrap_flags(rng, s, c, draws, batch=8):
    out_a, out_d = [], []
    for start in range(0,len(s),batch):
        ss, cc = s[start:start+batch], c[start:start+batch]
        ix = rng.integers(0,s.shape[1],size=(len(ss),draws,s.shape[1]))
        pa,pd = bootstrap_from_indices(np.stack([ss-.25,ss-cc]),ix)
        out_a.append(pa<=ALPHA); out_d.append(pd<=ALPHA)
    return np.concatenate(out_a),np.concatenate(out_d)


def generate(rng, r, d, scenario):
    """Inherited conditional-binomial pair framework, explicit new rate mixtures."""
    name,m = scenario['id'],scenario['m']
    shape=(r,d); ns=nc=m//2
    if name in ['delta_skew10','delta_reverse10','delta_rare02']:
        rare, common, exceptional = {
            'delta_skew10':(.1,.28,.48),
            'delta_reverse10':(.1,.32,.12),
            'delta_rare02':(.02,.288,.888),
        }[name]
        ps=np.full(shape,.30)
        pc=np.where(rng.random(shape)<rare,exceptional,common)
    elif name=='chance_skew10':
        ps=np.where(rng.random(shape)<.1,.07,.27); pc=np.full(shape,.20)
    elif name=='selective_omission':
        ps=pc=np.full(shape,.30)
    else:
        means={'both_null':(.25,.25),'delta_negative_cov':(.30,.30),
               'alt05_independent':(.30,.25),'alt03_shared':(.28,.25),
               'alt10_independent':(.35,.25),'alt05_mcar5':(.30,.25)}
        sm,cm=means[name]
        coupling='shared' if name in ['alt03_shared','delta_negative_cov'] else 'independent'
        ps,pc=latent_rates(rng,shape,sm,cm,.05,coupling)
        if name=='delta_negative_cov': pc=2*cm-pc
    hs,hc=rng.binomial(ns,ps),rng.binomial(nc,pc)
    # Reuse the scheduled-denominator omission construction from summary_run.
    hs_omit=hc_omit=ms_omit=mc_omit=0.
    if name=='alt05_mcar5': hs_omit=hc_omit=ms_omit=mc_omit=.05
    if name=='selective_omission': hs_omit=ms_omit=mc_omit=.02;hc_omit=.40
    os=rng.binomial(hs,1-hs_omit); oc=rng.binomial(hc,1-hc_omit)
    ons=os+rng.binomial(ns-hs,1-ms_omit)
    onc=oc+rng.binomial(nc-hc,1-mc_omit)
    missing_s=1-ons.sum(axis=1)/(d*ns);missing_c=1-onc.sum(axis=1)/(d*nc)
    missing=1-(ons+onc).sum(axis=1)/(d*m)
    gate=(missing<=.05+1e-12)&(np.abs(missing_s-missing_c)<=.02+1e-12)
    return os/ns,oc/nc,gate


def summarize(name, flags, gate, info):
    a,d=flags
    out=dict(info,method=name)
    for label,flag in [('reject_A',a),('reject_D',d),('joint',a&d),
                       ('gate_pass',gate),('joint_gated',a&d&gate)]:
        metric(out,label,flag)
    return out


def run(reps, boot_reps, draws, out):
    out.mkdir(parents=True,exist_ok=True)
    children=np.random.SeedSequence(PLAN['seed']).spawn(len(PLAN['scenarios'])*len(PLAN['pairs']))
    rows=[]; paired_rows=[]; index=0
    for scenario in PLAN['scenarios']:
        for d in PLAN['pairs']:
            data_seed,boot_seed=children[index].spawn(2)
            rng=np.random.default_rng(data_seed);brng=np.random.default_rng(boot_seed)
            index+=1; all_s=[];all_c=[];all_g=[]
            # Chunk only data generation; deterministic for fixed versions and chunk size.
            for start in range(0,reps,2048):
                s,c,g=generate(rng,min(2048,reps-start),d,scenario)
                all_s.append(s);all_c.append(c);all_g.append(g)
            s=np.concatenate(all_s);c=np.concatenate(all_c);g=np.concatenate(all_g)
            info=dict(scenario=scenario['id'],role=scenario['role'],pairs=d,
                      trials_per_pair=scenario['m'],A=scenario['A'],Delta=scenario['Delta'],
                      observed_mean_s=float(s.mean()),observed_mean_c=float(c.mean()))
            flags=analytic_flags(s,c)
            for method in METHODS:
                rows.append(summarize(method,flags[method],g,dict(info,sample='full',reps=reps,draws=0)))
                rows.append(summarize(method,tuple(x[:boot_reps] for x in flags[method]),g[:boot_reps],
                                      dict(info,sample='bootstrap_subset',reps=boot_reps,draws=0)))
            bf=bootstrap_flags(brng,s[:boot_reps],c[:boot_reps],draws)
            rows.append(summarize('bootstrap_t',bf,g[:boot_reps],dict(info,sample='bootstrap_subset',reps=boot_reps,draws=draws)))
            # Paired differences in rejection rates use the same datasets; retain disagreement counts.
            base=np.stack(flags['pair_t'])[:,:boot_reps].all(axis=0)
            bj=bf[0]&bf[1]
            paired=dict(scenario=scenario['id'],pairs=d,reps=boot_reps,
                        bootstrap_only=int(np.sum(bj&~base)),t_only=int(np.sum(base&~bj)))
            paired_rows.append(paired)
            print(f"{scenario['id']} D={d} done",flush=True)
    write_csv(out/'comparison.csv',rows)
    write_csv(out/'bootstrap-vs-t-paired.csv',paired_rows)
    metadata=dict(status='PROVISIONAL_SYNTHETIC_ONLY',plan_sha256=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest(),
                  seed=PLAN['seed'],analytic_reps=reps,bootstrap_reps=boot_reps,draws=draws,
                  python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                  bit_generator='PCG64',data_chunk=2048,bootstrap_batch=8,
                  source_commit=PLAN['source_commit'],cells=index,
                  stream_order='scenario then pairs; two children per cell: data, bootstrap',
                  framework_sha256=hashlib.sha256((ROOT.parent/'assessment.py').read_bytes()).hexdigest())
    (out/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=ROOT/'results')
    parser.add_argument('--reps',type=int,default=PLAN['analytic_reps'])
    parser.add_argument('--bootstrap-reps',type=int,default=PLAN['bootstrap_reps'])
    parser.add_argument('--draws',type=int,default=PLAN['bootstrap_draws'])
    args=parser.parse_args()
    if not 1<=args.bootstrap_reps<=args.reps or args.draws<1: parser.error('1 <= bootstrap reps <= reps; draws positive')
    run(args.reps,args.bootstrap_reps,args.draws,args.out)
