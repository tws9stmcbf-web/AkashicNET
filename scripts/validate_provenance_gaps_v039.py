#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from pathlib import Path

REG=Path('references/community/provenance-gap-registry-v0.39.csv')
RECON=Path('references/community/drive-canonicalisation-reconciliation-v0.1.csv')


def load(path):
    with path.open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))


def main():
    gaps=load(REG)
    assert {g['family_id'] for g in gaps}=={'CANON-0010','CANON-0029'}
    assert all(g['status']=='OPEN' for g in gaps)
    assert all(g['resolution_condition'].strip() for g in gaps)
    assert all(g['forbid_inference_from'].strip() for g in gaps)
    recon=load(RECON)
    by={r.get('family_id'):r for r in recon}
    # Historical reconciliation must not be silently promoted by this registry.
    for family in ('CANON-0010','CANON-0029'):
        assert family in by
    out={
      'registry':'AKASHICNET_PROVENANCE_GAPS','version':'0.39','open_gaps':len(gaps),
      'families':[g['family_id'] for g in gaps],
      'fabricated_identifiers_allowed':False,
      'lexical_inference_can_close_gap':False,
      'semantic_inference_can_close_gap':False,
      'rights_promotion_allowed':False,
      'truth_inference_allowed':False,
    }
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__': main()
