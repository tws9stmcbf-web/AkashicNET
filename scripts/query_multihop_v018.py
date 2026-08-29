#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

GRAPH=Path('data/knowledge-graph-v0.16.json')
CONCEPT=Path('data/concept-layer-v0.11.json')
DEDUP=Path('data/dedup-retrieval-view-v0.17.json')


def unit_payload(u):
    return {
        'retrieval_unit_id':u['retrieval_unit_id'],
        'collapse_basis':u['collapse_basis'],
        'deduplicated':u['deduplicated'],
        'physical_manifestation_count':u['physical_manifestation_count'],
        'labels':u['labels'],
        'sha256':u.get('sha256'),
        'manifestations':u['manifestations'],
        'rights_states':u['rights_states'],
        'not_truth_claim':True,
        'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('query')
    p.add_argument('--accepted-only',action='store_true')
    a=p.parse_args()

    graph=json.load(GRAPH.open(encoding='utf-8'))
    concept=json.load(CONCEPT.open(encoding='utf-8'))
    dedup=json.load(DEDUP.open(encoding='utf-8'))

    q=a.query.lower().strip()
    concepts={c['node_id']:c for c in concept['concept_nodes']}
    matched={cid for cid,c in concepts.items() if q in c['label'].lower() or q in c['definition'].lower() or q==cid.lower()}

    family_by_ref={}
    unique_families={}
    for n in graph['nodes']:
        if n.get('node_type') in {'canonical_family','canonical_candidate_family'}:
            fid=n.get('family_id') or n.get('node_id')
            family_by_ref[fid]=n
            family_by_ref[n.get('node_id')]=n
            unique_families[n.get('node_id')]=n

    units_by_family={}
    for u in dedup['retrieval_units']:
        for fid in u.get('family_ids',[]):
            units_by_family.setdefault(fid,[]).append(u)

    results=[]
    seen=set()

    # Reviewed concept paths first. Dedup units are attached only when the
    # reviewed concept edge lands on a family that has a manifestation view.
    for domain,key in [('reddit','reddit_edges'),('library','library_edges')]:
        for e in concept[key]:
            if e['target_concept'] not in matched:
                continue
            if a.accepted_only and not e.get('accepted_edge'):
                continue

            base={
                'domain':domain,
                'query_path':'reviewed_concept',
                'concept':concepts[e['target_concept']]['label'],
                'concept_hop':{
                    'from':e['source_ref'],'relationship':e['relationship'],'to':e['target_concept'],
                    'review_state':e.get('review_state'),'decision':e.get('v011_decision'),
                    'basis':e.get('basis'),'not_truth_claim':True
                }
            }
            if domain=='reddit':
                base['source']={'type':'reddit_record','ref':e['source_ref'],'rights_status':'LINK_ONLY_METADATA','scientific_evidence_default':False}
                base['retrieval_resolution']='REDDIT_CANONICAL_URL'
                keyid=('reddit',e['source_ref'],e['target_concept'])
                if keyid not in seen:
                    seen.add(keyid); results.append(base)
                continue

            fam=family_by_ref.get(e['source_ref'])
            base['source']={'type':'canonical_family','ref':e['source_ref'],'label':fam.get('label') if fam else None}
            fid=(fam or {}).get('family_id')
            units=units_by_family.get(fid,[]) if fid else []
            if units:
                base['retrieval_resolution']='DEDUP_LOGICAL_UNITS_RESOLVED'
                base['logical_retrieval_units']=[unit_payload(u) for u in units]
            else:
                base['retrieval_resolution']='NO_MANIFESTATION_VIEW_FOR_FAMILY'
            keyid=('library',e['source_ref'],e['target_concept'])
            if keyid not in seen:
                seen.add(keyid); results.append(base)

    # Canonical-family fallback within the same query engine. This does not
    # create semantic edges; it only matches existing family labels/IDs.
    for fam in unique_families.values():
        label=(fam.get('label') or fam.get('canonical_label') or '')
        fid=fam.get('family_id') or ''
        if not q or (q not in label.lower() and q not in fid.lower() and q not in fam.get('node_id','').lower()):
            continue
        units=units_by_family.get(fid,[])
        base={
            'domain':'library',
            'query_path':'canonical_family_label',
            'source':{'type':'canonical_family','ref':fam.get('node_id'),'family_id':fid,'label':label},
            'retrieval_resolution':'DEDUP_LOGICAL_UNITS_RESOLVED' if units else 'NO_MANIFESTATION_VIEW_FOR_FAMILY',
            'not_semantic_inference':True,
        }
        if units:
            base['logical_retrieval_units']=[unit_payload(u) for u in units]
        keyid=('canonical',fam.get('node_id'))
        if keyid not in seen:
            seen.add(keyid); results.append(base)

    summary={
        'version':'0.18','query':a.query,'matched_concepts':sorted(matched),'accepted_only':a.accepted_only,
        'result_count':len(results),
        'logical_units_returned':sum(len(r.get('logical_retrieval_units',[])) for r in results),
        'physical_manifestations_returned':sum(sum(u['physical_manifestation_count'] for u in r.get('logical_retrieval_units',[])) for r in results),
        'deduplicated_units_returned':sum(sum(1 for u in r.get('logical_retrieval_units',[]) if u['deduplicated']) for r in results),
        'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
        'results':results
    }
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
