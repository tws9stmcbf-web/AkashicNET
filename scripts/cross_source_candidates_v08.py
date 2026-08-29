#!/usr/bin/env python3
from __future__ import annotations
import csv,json,re
from pathlib import Path

G=Path('data/knowledge-graph-v0.7.json')
P=Path('references/community/n2n-pilot-index.csv')
O=Path('data/cross-source-candidates-v0.8.json')
STOP=set('the a an and or of to in for on with by from is are as at into about this that volume vol book books complete works'.split())

def toks(s):
    return [x for x in re.findall(r'[a-z0-9]+',(s or '').lower()) if len(x)>2 and x not in STOP]

def main():
    graph=json.load(G.open(encoding='utf-8'))
    fam=[]
    for n in graph.get('nodes',[]):
        if n.get('node_type') in {'canonical_candidate_family','canonical_family'} and n.get('family_id'):
            fam.append((n['family_id'],n.get('label',''),toks(n.get('label',''))))
    with P.open(encoding='utf-8',newline='') as f:
        posts=list(csv.DictReader(f))
    cand=[]
    for p in posts:
        pt=set(toks((p.get('title') or '')+' '+(p.get('short_summary') or '')))
        for fid,label,ft0 in fam:
            ft=set(ft0)
            if not ft or not pt: continue
            overlap=len(ft & pt)
            containment=overlap/len(ft)
            union=len(ft | pt)
            jaccard=overlap/union if union else 0
            score=round((0.7*containment+0.3*jaccard)*100,2)
            if score < 35: continue
            cand.append({
                'reddit_url':p.get('reddit_url'),'reddit_title':p.get('title'),
                'family_id':fid,'family_label':label,'candidate_score':score,
                'review_state':'REVIEW_REQUIRED','accepted_edge':False,
                'basis':{'family_token_containment':round(containment,4),'token_jaccard':round(jaccard,4)},
                'not_truth_claim':True,'not_scientific_evidence':True,'not_rights_clearance':True
            })
    cand.sort(key=lambda x:(-x['candidate_score'],x['family_id'],x['reddit_url'] or ''))
    for i,c in enumerate(cand,1): c['candidate_id']=f'XSR-{i:06d}'
    out={'version':'0.8','scope':'review-candidates-only','reddit_records_examined':len(posts),
         'canonical_families_examined':len(fam),'candidate_count':len(cand),
         'accepted_edge_count':0,'review_required_count':len(cand),
         'truth_inference_allowed':False,'rights_promotion_allowed':False,
         'scientific_evidence_promotion_allowed':False,'candidates':cand}
    O.parent.mkdir(parents=True,exist_ok=True)
    json.dump(out,O.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='candidates'},sort_keys=True))

if __name__=='__main__': main()
