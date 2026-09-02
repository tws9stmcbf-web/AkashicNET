#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"references/community/cross-source-qualification-batch-v0.1.7.json"
TYPES={"TOPIC","PUBLICATION","FRAMEWORK","QUESTION","SOURCE_RECORD","EVIDENCE_RECORD"}
FALSE={"automated_truth_inference_allowed","automated_acceptance_allowed","rights_promotion_allowed","scientific_evidence_promotion_allowed","canonical_identity_promotion_allowed","circular_confidence_allowed","private_drive_metadata_allowed"}
OLD={"https://www.reddit.com/r/NeuronsToNirvana/comments/1t4mza9/wisdom_traditions_as_cognitive_maps/","https://www.reddit.com/r/NeuronsToNirvana/comments/1udv3su/visual_symbolism_and_the_sacred/","https://www.reddit.com/r/NeuronsToNirvana/comments/1u6dq0s/hieratic_as_interpretive_scaffolding/"}
def validate(d):
 e=[]
 if (d.get("schema_version"),d.get("policy_version"),d.get("endpoint_registry_version"),d.get("anchor_evidence_version"))!=("0.1.7","0.1.2","0.1.4","0.1.6"): e.append("version")
 if d.get("defaults")!={"assertion_class":"INFERRED_CANDIDATE","review_state":"REVIEW_REQUIRED","accepted_edge":False}: e.append("defaults")
 if set(d.get("boundaries",{}))!=FALSE or any(d.get("boundaries",{}).values()): e.append("boundaries")
 q=d.get("qualified_candidates",[]); r=d.get("rejected_candidates",[]); allc=q+r
 if q: e.append("unaudited qualification")
 for c in allc:
  if c.get("source_endpoint",{}).get("provenance",{}).get("record_id") in OLD: e.append("reused Batch 3 pair")
  for n in ("source_endpoint","target_endpoint"):
   x=c.get(n,{})
   if x.get("endpoint_type") not in TYPES or not str(x.get("endpoint_id","")).startswith("endpoint:"): e.append("endpoint")
   p=x.get("provenance",{})
   if set(p)!={"artifact_id","record_id","independence_key","public_safe"} or p.get("public_safe") is not True: e.append("provenance")
  if c.get("anchor_evidence")!=[]: e.append("unvalidated anchor")
  if not c.get("observed_nonqualifying_signals"): e.append("signal explanation")
  if c.get("decision")!="REJECTED_QUALIFICATION": e.append("decision")
 ids=[x.get("candidate_id") for x in allc]
 if None in ids or len(ids)!=len(set(ids)): e.append("IDs")
 if d.get("summary")!={"screened":len(allc),"qualified":len(q),"rejected":len(r),"accepted_edges":0}: e.append("summary")
 if d.get("rejection_is_not_negative_evidence") is not True: e.append("disclaimer")
 s=json.dumps(d)
 if any(k in s for k in ('"drive_id"','"filename"','"private_path"','/My Drive/')): e.append("private metadata")
 return sorted(set(e))
def main():
 d=json.loads(REPORT.read_text()); e=validate(d); print(json.dumps(d["summary"],sort_keys=True))
 for x in e: print("ERROR:",x)
 if not e: print("AKASHICNET AUDITED CROSS-SOURCE BATCH v0.1.7 PASS")
 return bool(e)
if __name__=="__main__": raise SystemExit(main())
