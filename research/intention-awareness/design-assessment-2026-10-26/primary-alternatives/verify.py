#!/usr/bin/env python3
"""Retained-byte and result consistency checks; never statistical validation."""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'sha256.json').read_text())
for name,digest in manifest.items():
    p=(ROOT/name).resolve()
    if ROOT.resolve() not in p.parents: raise ValueError('Out-of-package manifest path')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest: raise ValueError('Hash mismatch: '+name)
plan=json.loads((ROOT/'plan.json').read_text())
run=json.loads((ROOT/'results/run.json').read_text())
assert run['plan_sha256']==hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
assert run['framework_sha256']==hashlib.sha256((ROOT.parent/'assessment.py').read_bytes()).hexdigest()
assert (run['analytic_reps'],run['bootstrap_reps'],run['draws'])==(plan['analytic_reps'],plan['bootstrap_reps'],plan['bootstrap_draws'])
rows=list(csv.DictReader((ROOT/'results/comparison.csv').open()))
assert len(rows)==len(plan['scenarios'])*len(plan['pairs'])*9
keys={(r['scenario'],int(r['pairs']),r['method'],r['sample']) for r in rows}
assert len(keys)==len(rows)
for r in rows:
    n=int(r['reps'])
    for field in ['reject_A','reject_D','joint','gate_pass','joint_gated']:
        p=float(r[field]);lo=float(r[field+'_lo']);hi=float(r[field+'_hi'])
        assert -1e-12<=lo<=p+1e-12 and p-1e-12<=hi<=1+1e-12
        assert abs(p*n-round(p*n))<1e-7
    assert float(r['joint'])<=min(float(r['reject_A']),float(r['reject_D']))+1e-12
    assert float(r['joint_gated'])<=min(float(r['joint']),float(r['gate_pass']))+1e-12
    expected=run['analytic_reps'] if r['sample']=='full' else run['bootstrap_reps']
    assert n==expected
paired=list(csv.DictReader((ROOT/'results/bootstrap-vs-t-paired.csv').open()))
assert len(paired)==run['cells']==33
status=json.loads((ROOT/'review-status.json').read_text())
assert status['replacement_adopted'] is False and status['final_sample_size'] is None
assert status['primary_test']=='UNRESOLVED_AFTER_CALIBRATION_STRESS'
assert status['independent_statistical_review']=='PENDING'
subprocess.run([sys.executable,str(ROOT.parent/'verify_package.py')],check=True)
print(f'{len(manifest)} follow-up hashes and {len(rows)} result rows consistent; 33 cells; original package intact; no scientific validation')
