#!/usr/bin/env python3
"""Adversarial weak-null calibration: deliberately skewed pair contrasts."""
import argparse
import numpy as np
from scipy import stats
from assessment import metric, t_pvalue, write_csv

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=str,default='results/skew-calibration.csv')
    parser.add_argument('--reps',type=int,default=50000)
    args=parser.parse_args()
    rng=np.random.default_rng(20261027)
    rows=[]
    for d in [20,30,60,100,160]:
        # Sending .30; controls .28 with probability .9 or .48 with probability .1.
        # Both marginal means .30. Condition effects vary between pairs: +.02 or -.18.
        # This is a WEAK population null; NOT a blinded uniform-target sharp null.
        p_c=np.where(rng.random((args.reps,d))<.1,.48,.28)
        s=rng.binomial(100,.30,(args.reps,d))/100
        c=rng.binomial(100,p_c)/100
        pa=t_pvalue(s-.25);pd=t_pvalue(s-c)
        delta=(s-c).mean(axis=1)
        # A bounded independent-pair Hoeffding comparator, not proposed as new primary.
        # Differences lie in [-1,1], so P(mean >= x) <= exp(-D*x^2/2) under E(mean)<=0.
        bound=np.exp(-d*np.maximum(delta,0)**2/2)
        row=dict(pairs=d,trials_per_pair=200,p_s=.30,p_c=.30,reps=args.reps,
                 scenario='skewed_weak_Delta_null',control_within_arm_rho=.0036/(.30*.70),
                 seed=20261027)
        for name,flag in [('reject_D',pd<=.05),('joint',(pa<=.05)&(pd<=.05)),('bounded_D',bound<=.05)]:metric(row,name,flag)
        rows.append(row)
    from pathlib import Path
    write_csv(Path(args.out),rows)
    print(rows)

if __name__=='__main__':main()
