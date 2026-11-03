#!/usr/bin/env python3
"""Optional standalone scientific figure: requires matplotlib==3.10.8."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parent
with (ROOT/'results/power.csv').open() as f:power=list(csv.DictReader(f))
with (ROOT/'results/skew-calibration.csv').open() as f:skew=list(csv.DictReader(f))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
for rho,coupling,label,color in [(0.,'independent','ICC 0','#64748b'),(.05,'shared','ICC .05, shared pair effect','#007f86'),(.05,'independent','ICC .05, separate arm effects','#b55d20')]:
    rows=[r for r in power if float(r['p_s'])==.3 and int(r['trials_per_pair'])==100 and float(r['rho'])==rho and r['coupling']==coupling]
    x=np.array([int(r['pairs']) for r in rows]);y=np.array([float(r['joint']) for r in rows])
    axs[0].plot(x,100*y,'o-',color=color,label=label)
    axs[0].fill_between(x,[100*float(r['joint_lo']) for r in rows],[100*float(r['joint_hi']) for r in rows],color=color,alpha=.15)
axs[0].axhline(80,color='#888',ls=':',lw=1)
axs[0].set(xlabel='Independent participant pairs',ylabel='Joint rejection probability (%)',ylim=(0,103),title='Power depends on cross-condition covariance\nHypothetical 30% / 25%, 100 trials per pair')
axs[0].legend(loc='lower right',frameon=False,fontsize=9)
x=np.array([int(r['pairs']) for r in skew]);y=np.array([float(r['joint']) for r in skew])*100
lo=np.array([float(r['joint_lo']) for r in skew])*100;hi=np.array([float(r['joint_hi']) for r in skew])*100
axs[1].errorbar(x,y,yerr=[y-lo,hi-y],fmt='o-',color='#ae3445',capsize=4,label='Candidate pair t tests')
axs[1].axhline(5,color='#444',ls='--',lw=1,label='Nominal 5%')
axs[1].set(xlabel='Independent participant pairs',ylabel='Joint false-positive probability (%)',ylim=(0,9),title='A skewed weak-null stress fails calibration\nTrue population sending − control = 0')
axs[1].legend(frameon=False,loc='lower right')
fig.suptitle('Intention Awareness · Synthetic design assessment · Review draft',fontsize=14)
fig.supxlabel('Shading/bars: pointwise 95% Monte Carlo intervals. Power uses provisional tests; no participant data.',fontsize=9)
fig.savefig(ROOT/'design-assessment.png',dpi=180)
print('Wrote design-assessment.png')
