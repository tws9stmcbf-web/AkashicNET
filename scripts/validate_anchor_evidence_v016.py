#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"references/community/anchor-evidence-fixture-v0.1.6.json"
TYPES={"EXPLICIT_IDENTIFIER","EXACT_FULL_TITLE","EXPLICIT_CITATION","DISTINCTIVE_NAMED_ENTITY","DISTINCTIVE_MULTI_TOKEN_PHRASE","EXPLICIT_FRAMEWORK_REFERENCE","EXPLICIT_QUESTION_REFERENCE"}
FIELDS={"title","identifier","citation","framework_reference","question_reference","summary"}
FALSE={"automated_truth_inference_allowed","automated_acceptance_allowed","rights_promotion_allowed","scientific_evidence_promotion_allowed","canonical_identity_promotion_allowed","circular_confidence_allowed","private_drive_metadata_allowed"}
GENERIC={"sacred","wisdom","tradition","symbolism","interpretation","consciousness","meaning","spiritual","knowledge","magic"}
def validate(d):
 e=[]
 if d.get("schema_version")!="0.1.6": e.append("version")
 if set(d.get("policy",{}))!=FALSE or any(d.get("policy",{}).values()): e.append("unsafe policy")
 if d.get("candidates")!=[] or d.get("edges")!=[]: e.append("production links prohibited")
 a=d.get("anchors")
 if not isinstance(a,list) or not a: return sorted(set(e+["anchors required"]))
 ids=[]
 for x in a:
  required={"anchor_id","anchor_type","normalized_value","source_endpoint_id","target_endpoint_id","provenance","extraction","independence_key","graph_derived","representation_only","review_explanation","input_digest"}
  if set(x)!=required: e.append("anchor shape")
  ids.append(x.get("anchor_id"))
  if not str(x.get("anchor_id","")).startswith("anchor:") or x.get("anchor_type") not in TYPES: e.append("anchor identity/type")
  if not str(x.get("source_endpoint_id","")).startswith("endpoint:") or not str(x.get("target_endpoint_id","")).startswith("endpoint:"): e.append("endpoint")
  if str(x.get("normalized_value","")).strip().lower() in GENERIC: e.append("generic anchor")
  p=x.get("provenance",{})
  if set(p)!={"artifact_id","record_id","public_safe"} or p.get("public_safe") is not True: e.append("provenance")
  z=x.get("extraction",{})
  if set(z)!={"method","extractor_version","public_metadata_field"} or z.get("method") not in {"EXACT_MATCH","EXPLICIT_REFERENCE"} or z.get("public_metadata_field") not in FIELDS: e.append("extraction")
  if not x.get("independence_key"): e.append("independence")
  if x.get("graph_derived") is not False or x.get("representation_only") is not False: e.append("derived signal")
  if len(str(x.get("review_explanation",""))) < 10: e.append("review explanation")
  if not re.fullmatch(r"[a-f0-9]{64}",str(x.get("input_digest",""))): e.append("digest")
 if None in ids or len(ids)!=len(set(ids)): e.append("anchor IDs")
 seen=set()
 for x in a:
  k=(x.get("anchor_type"),x.get("normalized_value"),x.get("independence_key"))
  if k in seen: e.append("duplicate representation")
  seen.add(k)
 s=json.dumps(d)
 if any(k in s for k in ('"drive_id"','"filename"','"private_path"','/My Drive/')): e.append("private metadata")
 return sorted(set(e))
def main():
 d=json.loads(FIXTURE.read_text()); e=validate(d)
 for x in e: print("ERROR:",x)
 if not e: print("AKASHICNET ANCHOR EVIDENCE v0.1.6 PASS")
 return bool(e)
if __name__=="__main__": raise SystemExit(main())
