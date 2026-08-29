#!/usr/bin/env python3
from __future__ import annotations
import csv,json,re
from pathlib import Path

GRAPH=Path('data/knowledge-graph-v0.7.json')
PILOT=Path('references/community/n2n-pilot-index.csv')
CONCEPTS=Path('references/community/concept-seed-v0.10.csv')
OUT=Path('data/concept-layer-v0.10.json')

ALIASES={
 'CONCEPT-0001':['consciousness','conscious','awareness'],
 'CONCEPT-0002':['selfhood','self','ego'],
 'CONCEPT-0003':['non-duality','nonduality','non-dual','nondual'],
 'CONCEPT-0004':['psychedelic','psychedelics','psilocybin','lsd','dmt','ayahuasca','ibogaine'],
 'CONCEPT-0005':['buddhism','buddhist','buddha','dharma'],
 'CONCEPT-0006':['hinduism','hindu','vedanta','upanishad','ramayana'],
 'CONCEPT-0007':['shamanism','shamanic','shaman'],
 'CONCEPT-0008':['alchemy','alchemical','alchemist'],
 'CONCEPT-0009':['mysticism','mystical','mystic'],
 'CONCEPT-0010':['meditation','contemplative','contemplation','mindfulness']
}

def textmatch(text, terms):
    t=(text or '').lower()
    return sorted({term for term in terms if re.search(r'(?<![a-z0-9])'+re.escape(term)+r'(?![a-z0-9])',t)})

def main():
    concepts=list(csv.DictReader(CONCEPTS.open(encoding='utf-8',newline='')))
    graph=json.load(GRAPH.open(encoding='utf-8'))
    posts=list(csv.DictReader(PILOT.open(encoding='utf-8',newline='')))
    concept_nodes=[{'node_id':c['concept_id'],'node_type':'concept','label':c['label'],'definition':c['definition'],'review_state':c['review_state']} for c in concepts]
    reddit_edges=[]
    for p in posts:
        text=(p.get('title') or '')+' '+(p.get('short_summary') or '')
        for c in concepts:
            hits=textmatch(text,ALIASES[c['concept_id']])
            if hits:
                reddit_edges.append({'source_type':'reddit_record','source_ref':p.get('reddit_url'),'relationship':'ABOUT_CANDIDATE','target_concept':c['concept_id'],'basis':'explicit_reviewed_alias_match','matched_terms':hits,'review_state':'PROVISIONAL','accepted_edge':False,'not_truth_claim':True,'not_scientific_evidence':True})
    library_edges=[]
    for n in graph.get('nodes',[]):
        if n.get('node_type') not in {'canonical_candidate_family','canonical_family'}: continue
        label=n.get('label','')
        for c in concepts:
            hits=textmatch(label,ALIASES[c['concept_id']])
            if hits:
                library_edges.append({'source_type':'canonical_family','source_ref':n.get('family_id') or n.get('node_id'),'relationship':'ABOUT_CANDIDATE','target_concept':c['concept_id'],'basis':'canonical_label_explicit_alias_match','matched_terms':hits,'review_state':'PROVISIONAL','accepted_edge':False,'not_truth_claim':True})
    out={'version':'0.10','scope':'reviewed-concept-seed-with-provisional-explicit-term-links','concept_count':len(concept_nodes),'reddit_records_examined':len(posts),'reddit_concept_candidates':len(reddit_edges),'library_concept_candidates':len(library_edges),'accepted_edge_count':0,'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,'concept_nodes':concept_nodes,'reddit_edges':reddit_edges,'library_edges':library_edges}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in {'concept_nodes','reddit_edges','library_edges'}},sort_keys=True))

if __name__=='__main__': main()
