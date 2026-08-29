#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

GRAPH=Path('data/knowledge-graph-v0.7.json')
CONCEPT=Path('data/concept-layer-v0.11.json')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('query')
    p.add_argument('--accepted-only',action='store_true')
    a=p.parse_args()

    graph=json.load(GRAPH.open(encoding='utf-8'))
    concept=json.load(CONCEPT.open(encoding='utf-8'))
    nodes={n['node_id']:n for n in graph['nodes']}
    concepts={c['node_id']:c for c in concept['concept_nodes']}
    q=a.query.lower()
    matched={cid for cid,c in concepts.items() if q in c['label'].lower() or q in c['definition'].lower() or q==cid.lower()}

    family_by_ref={}
    for n in graph['nodes']:
        if n.get('node_type') in {'canonical_family','canonical_candidate_family'}:
            family_by_ref[n.get('family_id') or n.get('node_id')]=n
            family_by_ref[n.get('node_id')]=n

    incoming={}
    for e in graph['edges']:
        incoming.setdefault(e['target'],[]).append(e)

    paths=[]
    for domain,key in [('reddit','reddit_edges'),('library','library_edges')]:
        for e in concept[key]:
            if e['target_concept'] not in matched: continue
            if a.accepted_only and not e.get('accepted_edge'): continue
            concept_hop={
                'from':e['source_ref'],'relationship':e['relationship'],'to':e['target_concept'],
                'review_state':e.get('review_state'),'decision':e.get('v011_decision'),
                'basis':e.get('basis'),'not_truth_claim':True
            }
            path={'domain':domain,'concept':concepts[e['target_concept']]['label'],'hops':[concept_hop]}
            if domain=='reddit':
                path['source']={'type':'reddit_record','ref':e['source_ref'],'rights_status':'LINK_ONLY_METADATA','scientific_evidence_default':False}
            else:
                fam=family_by_ref.get(e['source_ref'])
                path['source']={'type':'canonical_family','ref':e['source_ref'],'label':fam.get('label') if fam else None}
                if fam:
                    for ce in incoming.get(fam['node_id'],[]):
                        drive=nodes.get(ce['source'])
                        if not drive: continue
                        path['hops'].append({
                            'from':fam['node_id'],'relationship':'HAS_PROVENANCE_MEMBER', 'to':drive['node_id'],
                            'inverse_of':ce['relationship'],'confidence':ce.get('confidence'),'review_state':ce.get('review_state'),
                            'basis':ce.get('basis'),'not_truth_claim':True
                        })
                        path['drive_provenance']={
                            'drive_node_id':drive['node_id'],'collection_path':drive.get('collection_path'),
                            'drive_object_kind':drive.get('drive_object_kind','folder'),
                            'rights_status':drive.get('rights_status','UNKNOWN_UNVERIFIED')
                        }
                        break
            paths.append(path)

    print(json.dumps({
        'version':'0.12','query':a.query,'matched_concepts':sorted(matched),'path_count':len(paths),
        'accepted_only':a.accepted_only,'truth_inference_allowed':False,'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,'paths':paths
    },ensure_ascii=False,indent=2))

if __name__=='__main__': main()
