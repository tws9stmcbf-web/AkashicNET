#!/usr/bin/env python3
"""Synthetic design assessment only. No network, recruitment or participant input."""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

SEED = 20261026
ALPHA = .05


def latent_rates(rng, shape, ps, pc, rho, coupling):
    """Exact within-arm Bernoulli ICC=rho before omissions; uniform random effects."""
    us = rng.uniform(-1, 1, shape)
    uc = us if coupling == 'shared' else rng.uniform(-1, 1, shape)
    s = ps + np.sqrt(3*rho*ps*(1-ps))*us
    c = pc + np.sqrt(3*rho*pc*(1-pc))*uc
    if np.any((s < 0) | (s > 1) | (c < 0) | (c > 1)):
        raise ValueError('Uniform random effect extends beyond [0,1]')
    return s, c


def t_pvalue(x):
    """Rows=replicates, columns=independent pairs. Degenerate variance: no rejection."""
    mean = x.mean(axis=-1)
    se = x.std(axis=-1, ddof=1)/np.sqrt(x.shape[-1])
    t = np.divide(mean, se, out=np.zeros_like(mean), where=se > 1e-14)
    return np.where(se > 1e-14, stats.t.sf(t, x.shape[-1]-1), 1.)


def wilson(k, n):
    z = stats.norm.ppf(.975)
    p = k/n
    center = (p+z*z/(2*n))/(1+z*z/n)
    half = z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return [float(center-half), float(center+half)]


def metric(out, name, flag):
    k, n = int(np.count_nonzero(flag)), int(flag.size)
    out[name] = k/n
    lo, hi = wilson(k, n)
    out[name+'_lo'], out[name+'_hi'] = lo, hi


def summary_run(rng, r, d, m, ps, pc, rho, coupling, missing='none', allocation=.5):
    # m=all scheduled trials per pair, two sessions. Counts sufficient for pair tests.
    if m % 2 or int(m/2*allocation) != m/2*allocation:
        raise ValueError('Integer allocation required in each session')
    ns = int(m*allocation)
    nc = m-ns
    s, c = latent_rates(rng, (r,d), ps, pc, rho, coupling)
    hs, hc = rng.binomial(ns, s), rng.binomial(nc, c)
    # Split hits and misses to allow explicitly outcome-dependent omission stress.
    ms, mc, hit_ms, hit_mc = 0., 0., 0., 0.
    if missing == 'mcar5': ms = mc = hit_ms = hit_mc = .05
    if missing == 'differential': ms = hit_ms = .01; mc = hit_mc = .10
    if missing == 'selective': hit_ms = .02; ms = .02; hit_mc = .40; mc = .02
    obs_hs = rng.binomial(hs, 1-hit_ms)
    obs_hc = rng.binomial(hc, 1-hit_mc)
    obs_ns = obs_hs+rng.binomial(ns-hs, 1-ms)
    obs_nc = obs_hc+rng.binomial(nc-hc, 1-mc)
    if missing == 'pair_dropout10':
        # Entire pair drops before any scored response; retains schedule, scores zero.
        keep = rng.random((r,d)) >= .10
        obs_hs *= keep; obs_hc *= keep; obs_ns *= keep; obs_nc *= keep
    ss, cc = obs_hs/ns, obs_hc/nc
    pa, pd = t_pvalue(ss-.25), t_pvalue(ss-cc)
    missing_s = 1-obs_ns.sum(axis=1)/(d*ns)
    missing_c = 1-obs_nc.sum(axis=1)/(d*nc)
    overall_missing = 1-(obs_ns+obs_nc).sum(axis=1)/(d*m)
    gate = (overall_missing <= .05+1e-12) & (np.abs(missing_s-missing_c) <= .02+1e-12)
    completed_s = np.divide(obs_hs,obs_ns,out=np.zeros_like(ss),where=obs_ns>0)
    completed_c = np.divide(obs_hc,obs_nc,out=np.zeros_like(cc),where=obs_nc>0)
    complete_valid = ((obs_ns>0) & (obs_nc>0)).all(axis=1)
    cp = (t_pvalue(completed_s-.25)<=ALPHA) & (t_pvalue(completed_s-completed_c)<=ALPHA) & complete_valid
    # Intentionally naive independent-trial z comparison: diagnostic, never candidate primary.
    pooled = (obs_hs+obs_hc).sum(axis=1)/(d*m)
    se = np.sqrt(pooled*(1-pooled)*(1/(d*ns)+1/(d*nc)))
    z = np.divide((ss-cc).mean(axis=1),se,out=np.zeros(r),where=se>0)
    out = dict(pairs=d,trials_per_pair=m,send_fraction=allocation,p_s=ps,p_c=pc,rho=rho,
               coupling=coupling,missing=missing,reps=r,mean_s=float(ss.mean()),mean_c=float(cc.mean()))
    for name, flag in [('reject_A',pa<=ALPHA),('reject_D',pd<=ALPHA),
                       ('joint',(pa<=ALPHA)&(pd<=ALPHA)),('gate_pass',gate),
                       ('joint_gated',(pa<=ALPHA)&(pd<=ALPHA)&gate),('completed_joint',cp),
                       ('naive_D',stats.norm.sf(z)<=ALPHA)]:
        metric(out,name,flag)
    out['degenerate_A'] = int(np.count_nonzero(ss.std(axis=1)==0))
    out['degenerate_D'] = int(np.count_nonzero((ss-cc).std(axis=1)==0))
    return out


def biased_responses(rng, d, m, constant=False):
    # Markov guesses independent of targets/conditions under sharp null.
    if constant: return np.zeros((d,2,m//2),dtype=np.int8)
    response = rng.choice(4,size=(d,2,m//2),p=[.7,.1,.1,.1]).astype(np.int8)
    persist = rng.random(response.shape) < .65
    for t in range(1,m//2):
        response[:,:,t] = np.where(persist[:,:,t],response[:,:,t-1],response[:,:,t])
    return response


def trial_data(rng,d,m,ps,pc,rho,coupling,missing='none',constant=False):
    n=m//2
    condition = np.zeros((d,2,n),dtype=bool)
    condition[:,:,:n//2] = True
    condition = rng.permuted(condition,axis=2)
    targets = rng.integers(0,4,condition.shape,dtype=np.int8)
    responses = biased_responses(rng,d,m,constant)
    rates_s,rates_c = latent_rates(rng,(d,1,1),ps,pc,rho,coupling)
    p = np.where(condition,rates_s,rates_c)
    # A transparent synthetic information injection; not a psychological mechanism.
    up = (p-.25)/.75
    down = (.25-p)/.25
    force_match = rng.random(p.shape) < np.maximum(up,0)
    force_miss = rng.random(p.shape) < np.maximum(down,0)
    responses = np.where(force_match,targets,responses)
    responses = np.where(force_miss,(targets+rng.integers(1,4,p.shape))%4,responses)
    hit = responses == targets
    prob = np.zeros(p.shape)
    if missing == 'mcar5': prob[:] = .05
    if missing == 'differential': prob = np.where(condition,.01,.10)
    if missing == 'selective': prob = np.where((~condition)&hit,.40,.02)
    eligible = rng.random(p.shape) >= prob
    return targets,responses,condition,eligible


def conditional_hits(rng,targets,responses,eligible,b):
    """Uniform target permutations, compressed by response counts in each stratum.

    Each row is one pair/session/condition stratum. Sequential multivariate
    hypergeometric allocations preserve the EXACT observed target margins.
    Ineligible rows are the final unscored response group, never removed.
    """
    nstrata=len(targets)
    counts=np.array([[np.count_nonzero(t==k) for k in range(4)] for t in targets])
    rcounts=np.array([[np.count_nonzero((r==k)&e) for k in range(4)] for r,e in zip(responses,eligible)])
    remaining=np.broadcast_to(counts,(b,nstrata,4)).copy()
    hits=np.zeros((b,nstrata),dtype=int)
    for response in range(4):
        need=np.broadcast_to(rcounts[:,response],(b,nstrata)).copy()
        allocated=[]
        for k in range(3):
            good=remaining[:,:,k]
            bad=remaining[:,:,k+1:].sum(axis=2)
            draw=rng.hypergeometric(good,bad,need)
            allocated.append(draw)
            need=need-draw
        allocated.append(need)
        for k,a in enumerate(allocated): remaining[:,:,k]-=a
        hits+=allocated[response]
    return hits.sum(axis=1)


def randomization_pvalues(rng,targets,responses,condition,eligible,b):
    hits=(targets==responses)&eligible
    obs_s=int(hits[condition].sum())
    obs_c=int(hits[~condition].sum())
    # All pairs have same schedule => pooled count has identical ordering to equal pair mean.
    ts=[t[c] for t,c in zip(targets.reshape(-1,targets.shape[-1]),condition.reshape(-1,condition.shape[-1]))]
    rs=[r[c] for r,c in zip(responses.reshape(-1,responses.shape[-1]),condition.reshape(-1,condition.shape[-1]))]
    es=[e[c] for e,c in zip(eligible.reshape(-1,eligible.shape[-1]),condition.reshape(-1,condition.shape[-1]))]
    perm_s=conditional_hits(rng,ts,rs,es,b)
    # Uniform condition permutation within pair/session: number of fixed hits assigned S
    # is hypergeometric, exactly the sufficient-statistic distribution for fixed arm sizes.
    total=hits.sum(axis=2).reshape(-1)
    n=targets.shape[-1]; ns=n//2
    cond_s=rng.hypergeometric(total,n-total,ns,size=(b,len(total))).sum(axis=1)
    # Balance makes ordering of Delta equivalent to S hits, total hits fixed.
    p_target=(1+np.count_nonzero(perm_s>=obs_s))/(b+1)
    p_cond=(1+np.count_nonzero(cond_s>=obs_s))/(b+1)
    redraw=rng.binomial(int(eligible[condition].sum()),.25,size=b)
    p_redraw=(1+np.count_nonzero(redraw>=obs_s))/(b+1)
    expected=sum(sum(np.count_nonzero(t==k)*np.count_nonzero((r==k)&e) for k in range(4))/len(t) for t,r,e in zip(ts,rs,es))
    return p_target,p_cond,p_redraw,expected,obs_s,obs_c


def randomization_run(rng,r,b,d,m,name,ps,pc,rho,coupling,missing='none',constant=False):
    values=[]; pair=[]; expectations=[]
    for _ in range(r):
        t,y,c,e=trial_data(rng,d,m,ps,pc,rho,coupling,missing,constant)
        pt,pd,pr,ex,hs,hc=randomization_pvalues(rng,t,y,c,e,b)
        values.append((pt,pd,pr))
        s=(((t==y)&e)&c).sum(axis=(1,2))/(m//2)
        co=(((t==y)&e)&(~c)).sum(axis=(1,2))/(m//2)
        pair.append((float(t_pvalue(s[None,:]-.25)[0]),float(t_pvalue((s-co)[None,:])[0])))
        expectations.append(ex/(d*m/2))
    v=np.array(values); p=np.array(pair)
    out=dict(scenario=name,pairs=d,trials_per_pair=m,p_s=ps,p_c=pc,rho=rho,coupling=coupling,
             missing=missing,constant=constant,reps=r,draws=b,conditional_mean=float(np.mean(expectations)))
    for label,flag in [('target',v[:,0]<=ALPHA),('condition',v[:,1]<=ALPHA),('redraw',v[:,2]<=ALPHA),
                       ('sensitivity_both',(v[:,0]<=ALPHA)&(v[:,1]<=ALPHA)),
                       ('primary_joint',(p[:,0]<=ALPHA)&(p[:,1]<=ALPHA))]: metric(out,label,flag)
    return out


def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path('results'))
    parser.add_argument('--reps',type=int,default=20000)
    parser.add_argument('--perm-reps',type=int,default=1000)
    parser.add_argument('--draws',type=int,default=999)
    args=parser.parse_args()
    if min(args.reps,args.perm_reps,args.draws)<1: parser.error('Positive counts required')
    args.out.mkdir(parents=True,exist_ok=True)
    streams=np.random.SeedSequence(SEED).spawn(4)
    rng=np.random.default_rng(streams[0]); rows=[]
    for d in [30,60,100,160]:
        for m in [40,100,200]:
            for ps in [.28,.30,.35]:
                for rho in [0.,.02,.05]:
                    for coupling in (['independent'] if rho==0 else ['independent','shared']):
                        rows.append(summary_run(rng,args.reps,d,m,ps,.25,rho,coupling))
    write_csv(args.out/'power.csv',rows);print('power scenarios',len(rows),flush=True)
    rng=np.random.default_rng(streams[1]);rows=[]
    for d in [20,30,60,100]:
        for ps,pc in [(.25,.25),(.30,.30),(.25,.20),(.23,.25)]:
            for rho in [0.,.02,.05]:
                for coupling in (['independent'] if rho==0 else ['independent','shared']):
                    for alloc in [.5,.75]:
                        rows.append(summary_run(rng,args.reps,d,200,ps,pc,rho,coupling,allocation=alloc))
    write_csv(args.out/'calibration.csv',rows);print('calibration scenarios',len(rows),flush=True)
    rng=np.random.default_rng(streams[2]);rows=[]
    for d in [60,100,160]:
        for ps,pc in [(.30,.25),(.30,.30),(.25,.25)]:
            for coupling in ['independent','shared']:
                for missing in ['none','mcar5','differential','selective','pair_dropout10']:
                    rows.append(summary_run(rng,args.reps,d,100,ps,pc,.05,coupling,missing))
        for alloc in [.25,.5,.75]:
            rows.append(summary_run(rng,args.reps,d,200,.30,.25,.05,'independent',allocation=alloc))
    write_csv(args.out/'missing-allocation.csv',rows);print('missing/allocation scenarios',len(rows),flush=True)
    rng=np.random.default_rng(streams[3]);rows=[]
    scenarios=[('sharp_biased',.25,.25,0.,'independent','none',False),
               ('sharp_constant',.25,.25,0.,'independent','none',True),
               ('sharp_mcar',.25,.25,0.,'independent','mcar5',False),
               ('alternative',.30,.25,.05,'independent','none',False),
               ('weak_delta_boundary',.30,.30,.05,'independent','none',False),
               ('differential_missing',.30,.30,.05,'independent','differential',False),
               ('target_dependent_missing',.25,.25,0.,'independent','selective',False)]
    for name,ps,pc,rho,coupling,missing,constant in scenarios:
        rows.append(randomization_run(rng,args.perm_reps,args.draws,30,40,name,ps,pc,rho,coupling,missing,constant))
        print('randomization',name,flush=True)
    write_csv(args.out/'randomization.csv',rows)
    meta=dict(seed=SEED,numpy=np.__version__,scipy=scipy.__version__,python=platform.python_version(),
              bit_generator='PCG64',stream_order=['power','calibration','missing-allocation','randomization'],
              reps=args.reps,perm_reps=args.perm_reps,draws=args.draws,
              status='SYNTHETIC_ONLY_REVIEW_REQUIRED',alpha=ALPHA)
    (args.out/'run.json').write_text(json.dumps(meta,indent=2)+'\n')
    names=['power.csv','calibration.csv','missing-allocation.csv','randomization.csv','run.json']
    checks={name:hashlib.sha256((args.out/name).read_bytes()).hexdigest() for name in names}
    checks['../assessment.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (args.out/'sha256.json').write_text(json.dumps(checks,indent=2)+'\n')

if __name__=='__main__': main()
