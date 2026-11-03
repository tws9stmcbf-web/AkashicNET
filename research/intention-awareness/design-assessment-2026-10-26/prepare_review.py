#!/usr/bin/env python3
"""Prepare human-readable tables and one inspectable synthetic observation ledger."""
import csv
from pathlib import Path
import numpy as np
from assessment import trial_data

ROOT=Path(__file__).resolve().parent

def read(name):
    with (ROOT/'results'/name).open() as f:return list(csv.DictReader(f))

def matches(row, **kw):return all(row[k]==str(v) for k,v in kw.items())

def select(rows, **kw):return next(x for x in rows if matches(x,**kw))

def rate(row,k):
    def pct(v):
        v=float(v)
        return f"{100*v:.3f}" if v<.001 or v>.999 else f"{100*v:.1f}"
    return f"{pct(row[k])}% ({pct(row[k+'_lo'])}–{pct(row[k+'_hi'])})"

def table(head, rows):
    return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)

def main():
    power=read('power.csv');missing=read('missing-allocation.csv');skew=read('skew-calibration.csv');perm=read('randomization.csv')
    text='# Generated synthetic-result tables\n\nAll intervals are pointwise 95% Wilson Monte Carlo intervals, not effect intervals. Power is for provisional tests. No participant data.\n\n'
    text+='## 30% versus 25%, 100 scheduled trials per pair\n\n'
    rows=[]
    for d in [30,60,100,160]:
        rows.append([d]+[rate(select(power,pairs=d,trials_per_pair=100,p_s=.3,rho=r,coupling=c),'joint') for r,c in [(0.,'independent'),(.05,'independent'),(.05,'shared')]])
    text+=table(['Pairs','ICC 0','ICC .05, separate arm effects','ICC .05, shared pair effect'],rows)
    text+='\n## Equal total trial budgets, 30% versus 25%, ICC .05, separate effects\n\n'
    rows=[]
    for d,m in [(30,200),(60,100),(60,200),(120,100),(100,40),(100,100),(100,200),(160,100)]:
        if d==120:continue  # Outside declared grid; do not interpolate an unrun cell.
        x=select(power,pairs=d,trials_per_pair=m,p_s=.3,rho=.05,coupling='independent')
        rows.append([d,m,d*m,rate(x,'joint')])
    text+=table(['Pairs','Trials/pair','All trials','Joint rejection'],rows)
    text+='\n## Smaller effect: 28% versus 25%, ICC .05, separate effects\n\n'
    text+=table(['Pairs','Trials/pair','Joint rejection'],[[d,m,rate(select(power,pairs=d,trials_per_pair=m,p_s=.28,rho=.05,coupling='independent'),'joint')] for d,m in [(60,100),(100,100),(160,100),(160,200)]])
    text+='\n## Omissions, 100 pairs × 100 trials, ICC .05, separate effects\n\n'
    rows=[]
    for ps,pc in [(.3,.25),(.3,.3),(.25,.25)]:
        for mis in ['none','mcar5','differential','selective','pair_dropout10']:
            x=select(missing,pairs=100,p_s=ps,p_c=pc,coupling='independent',missing=mis)
            rows.append([f'{ps:.2f}/{pc:.2f}',mis,f"{100*float(x['mean_s']):.2f}/{100*float(x['mean_c']):.2f}",rate(x,'joint'),rate(x,'gate_pass'),rate(x,'joint_gated'),rate(x,'completed_joint')])
    text+=table(['Completed rates S/C','Omissions','Scheduled means S/C %','Raw joint','Integrity gate pass','Joint AND gate','Completed joint'],rows)
    text+='\n## Allocation, 100 pairs × 200 trials, 30%/25%, ICC .05, separate effects\n\n'
    text+=table(['Send fraction','Joint rejection'],[[f,rate(select(missing,pairs=100,trials_per_pair=200,send_fraction=f),'joint')] for f in [.25,.5,.75]])
    text+='\n## Skewed weak-null stress; true population Delta = 0\n\n'
    text+=table(['Pairs','Reject Delta','Joint rejection','Bounded comparator'],[[x['pairs'],rate(x,'reject_D'),rate(x,'joint'),rate(x,'bounded_D')] for x in skew])
    text+='\n## Randomisation sensitivities; 30 pairs × 40 trials, 1,000 replicates, 999 draws\n\n'
    text+=table(['Scenario','Target shuffle','Condition shuffle','Target redraw','Both sensitivities','Candidate primary joint'],[[x['scenario']]+[rate(x,k) for k in ['target','condition','redraw','sensitivity_both','primary_joint']] for x in perm])
    (ROOT/'RESULTS.md').write_text(text)
    t,y,c,e=trial_data(np.random.default_rng(20261028),4,40,.30,.25,.05,'independent','mcar5')
    with (ROOT/'synthetic-example.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['synthetic_pair','session','trial','condition','target','locked_response','eligible','scored_hit'])
        for pair,session,trial in np.ndindex(t.shape):
            idx=(pair,session,trial)
            w.writerow([pair+1,session+1,trial+1,'S' if c[idx] else 'C',int(t[idx]),int(y[idx]),int(e[idx]),int((t[idx]==y[idx])&e[idx])])
    print('Wrote RESULTS.md and synthetic-example.csv')

if __name__=='__main__':main()
