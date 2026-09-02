#!/usr/bin/env python3
"""Fail-closed validation for cross-source qualification Batch 2 v0.1.3."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "references/community/cross-source-qualification-batch-v0.1.3.json"
FALSE_BOUNDARIES = {"automated_truth_inference_allowed", "automated_acceptance_allowed", "rights_promotion_allowed", "scientific_evidence_promotion_allowed", "canonical_identity_promotion_allowed", "circular_confidence_allowed", "private_drive_metadata_allowed"}
DIRECT = {"EXPLICIT_IDENTIFIER", "EXACT_FULL_TITLE", "EXPLICIT_CITATION"}
CORROBORATING = {"DISTINCTIVE_NAMED_ENTITY", "DISTINCTIVE_MULTI_TOKEN_PHRASE", "EXPLICIT_FRAMEWORK_REFERENCE", "EXPLICIT_QUESTION_REFERENCE"}

def qualifies(anchors):
    usable = [a for a in anchors if not a.get("graph_derived") and not a.get("representation_only")]
    if any(a.get("type") in DIRECT for a in usable): return True
    return len({(a.get("type"), a.get("normalized_value")) for a in usable if a.get("type") in CORROBORATING and a.get("normalized_value")}) >= 2

def validate(data):
    errors=[]
    if data.get("schema_version") != "0.1.3" or data.get("policy_version") != "0.1.2": errors.append("version mismatch")
    if data.get("defaults") != {"assertion_class":"INFERRED_CANDIDATE","review_state":"REVIEW_REQUIRED","accepted_edge":False}: errors.append("unsafe defaults")
    if set(data.get("boundaries",{})) != FALSE_BOUNDARIES or any(data["boundaries"].values()): errors.append("all boundaries must exist and remain false")
    qualified=data.get("qualified_candidates",[]); rejected=data.get("rejected_candidates",[])
    if any(not qualifies(x.get("anchors",[])) for x in qualified): errors.append("unqualified record in qualified set")
    if any(qualifies(x.get("anchors",[])) for x in rejected): errors.append("qualified record in rejected set")
    if any(x.get("decision") != "REJECTED_QUALIFICATION" for x in rejected): errors.append("invalid rejection decision")
    ids=[x.get("candidate_id") for x in qualified+rejected]
    if len(ids)!=len(set(ids)) or None in ids: errors.append("candidate IDs must be unique")
    s=data.get("summary",{})
    if s != {"screened":len(qualified)+len(rejected),"qualified":len(qualified),"rejected":len(rejected),"accepted_edges":0}: errors.append("summary mismatch")
    if data.get("rejection_is_not_negative_evidence") is not True: errors.append("rejection disclaimer required")
    text=json.dumps(data)
    if any(k in text for k in ('"drive_id"','"filename"','"private_path"','/My Drive/')): errors.append("private Drive metadata prohibited")
    return sorted(set(errors))

def main():
    data=json.loads(REPORT.read_text())
    errors=validate(data)
    print(json.dumps(data["summary"],sort_keys=True))
    for e in errors: print("ERROR:",e)
    if not errors: print("AKASHICNET CROSS-SOURCE QUALIFICATION BATCH v0.1.3 PASS")
    return bool(errors)
if __name__ == "__main__": raise SystemExit(main())
