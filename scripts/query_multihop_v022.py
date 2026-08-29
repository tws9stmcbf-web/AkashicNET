#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

GRAPH=Path('data/knowledge-graph-v0.16.json')
CONCEPT=Path('data/concept-layer-v0.22.json')
DEDUP=Path('data/dedup-retrieval-view-v0.17.json')


def unit_payload(u):
    return {
        'retrieval_unit_id':u['retrieval_unit_id'],'collapse_basis':u['collapse_basis'],
        'deduplicated':u['deduplicated'],'physical_manifestation_count':u['physical_manifestation_count'],
        'labels':u['labels'],'sha256':u.get('sha256'),'manifestations':u['manifestations'],
        'rights_states':u['rights_states'],'not_truth_claim':True,
        'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
    }


def main():
    p=argparse.ArgumentParser(); p.add_argument('query'); p.add_argument('--accepted-only',action='store_true'); a=p.parse_args()
    graph=json.load(GRAPH.open(encoding='utf-8'))
    concept=json.load(CONCEPT.open(encoding='utf-8'))
    dedup=json.load(DEDUP.open(encoding='utf-8'))
    q=a.query.lower().strip()
    concepts={c['node_id']:c for c in concept['concept_nodes']}
    matched={cid for cid,c in concepts.items() if q in c['label'].lower() or q in c['definition'].lower() or q==cid.lower()}

    family_labels={}
    for n in graph['nodes']:
        if n.get('node_type') in {'canonical_family','canonical_candidate_family'}:
            fid=n.get('family_id') or n.get('node_id')
            family_labels.setdefault(fid,n.get('label') or n.get('canonical_label'))

    units_by_family={}
    for u in dedup['retrieval_units']:
        for fid in u.get('family_ids',[]): units_by_family.setdefault(fid,[]).append(u)

    results=[]
    for e in concept['reddit_edges']:
        if e['target_concept'] not in matched: continue
        if a.accepted_only and not e.get('accepted_edge'): continue
        results.append({
            'domain':'reddit','query_path':'reviewed_concept','concept':concepts[e['target_concept']]['label'],
            'source':{'type':'reddit_record','ref':e['source_ref'],'rights_status':'LINK_ONLY_METADATA','scientific_evidence_default':False},
            'concept_hop':{'from':e['source_ref'],'relationship':e['relationship'],'to':e['target_concept'],'review_state':e.get('review_state'),'decision':e.get('v021_decision') or e.get('v020_decision') or e.get('v011_decision'),'basis':e.get('basis'),'not_truth_claim':True},
            'retrieval_resolution':'REDDIT_CANONICAL_URL'
        })

    for e in concept['library_edges']:
        if e['target_concept'] not in matched: continue
        if a.accepted_only and not e.get('accepted_edge'): continue
        fid=e['logical_family_id']
        units=units_by_family.get(fid,[])
        r={
            'domain':'library','query_path':'normalised_reviewed_concept','concept':concepts[e['target_concept']]['label'],
            'source':{'type':'canonical_family','family_id':fid,'label':family_labels.get(fid)},
            'concept_hop':{'from':fid,'relationship':e['relationship'],'to':e['target_concept'],'review_state':e.get('review_state'),'basis_set':e.get('basis_set',[]),'matched_terms':e.get('matched_terms',[]),'representation_count':e.get('representation_count',1),'representation_sources':e.get('representation_sources',[]),'representation_multiplicity_not_semantic_strength':True,'not_truth_claim':True},
            'retrieval_resolution':'DEDUP_LOGICAL_UNITS_RESOLVED' if units else 'NO_MANIFESTATION_VIEW_FOR_FAMILY'
        }
        if units: r['logical_retrieval_units']=[unit_payload(u) for u in units]
        results.append(r)

    print(json.dumps({
        'version':'0.22','query':a.query,'matched_concepts':sorted(matched),'accepted_only':a.accepted_only,
        'result_count':len(results),'logical_units_returned':sum(len(r.get('logical_retrieval_units',[])) for r in results),
        'physical_manifestations_returned':sum(sum(u['physical_manifestation_count'] for u in r.get('logical_retrieval_units',[])) for r in results),
        'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
        'semantic_strength_from_representation_count':False,'results':results
    },ensure_ascii=False,indent=2))

if __name__=='__main__': main()
