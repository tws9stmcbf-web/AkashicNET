#!/usr/bin/env python3
import json, os, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LADDER=ROOT/"references/big-questions/research-maturity-ladder-v0.1.json"
ASSESSMENTS=ROOT/"references/big-questions/maturity-assessments-v0.1.json"
ROOTS=(ROOT/"references/big-questions",ROOT/"website/app/big-questions")
SUFFIXES={".json",".md",".mdx",".tsx",".ts",".jsx",".js"}
BQ=re.compile(r"\b(BQ\d{3})\b",re.I)
LEVEL=re.compile(r"\bLevel\s+(\d{1,2})/10\b",re.I)
PATH_Q=re.compile(r"(?:^|/)(?:BQ|bq)(\d{3})(?:/|$)")
MEANING="A level records completed governed research work. It is not a truth probability, evidence-strength grade, confidence score or promotion decision."
STAGES=[(1,"QUESTION_FRAMED","Frame the question"),(2,"SOURCES_MAPPED","Map sources"),(3,"REVIEW_CANDIDATE_REACHED","Reach review-candidate status"),(4,"MODELS_SEPARATED","Separate models"),(5,"EVIDENCE_MAPPED","Map evidence"),(6,"METHODS_STRESS_TESTED","Stress-test methods"),(7,"PREDICTIONS_DEFINED","Define predictions"),(8,"GOVERNED_TESTS_RUN","Run tests"),(9,"FINDINGS_TRIANGULATED","Triangulate findings"),(10,"RESOLUTION_REVIEW_ENTERED","Enter resolution review")]
EXPECTED={"BQ001":(6,None),"BQ002":(4,None),"BQ003":(4,None),**{f"BQ{i:03d}":(None,"UNSCORED_EXPLORATORY_NONCANONICAL") for i in range(4,9)},"BQ009":(None,"UNASSIGNED")}
RULES=("levels_are_cumulative","asserted_level_must_equal_highest_completed_stage","missing_or_unvalidated_stage_blocks_higher_assertions","level_8_requires_governed_test_execution","unresolved_is_allowed_at_every_level","level_change_does_not_promote_truth_evidence_rights_public_synthesis_or_website")
GATES=("truth_inference_allowed","scientific_evidence_promotion_allowed","rights_promotion_allowed","public_synthesis_updated","website_promotion_allowed")
def fail(msg): raise ValueError(msg)
def json_levels(value):
    found=[]
    if isinstance(value,dict):
        if value.get("maximum")==10 and isinstance(value.get("level"),int):found.append(value["level"])
        for child in value.values():found.extend(json_levels(child))
    elif isinstance(value,list):
        for child in value:found.extend(json_levels(child))
    return found
def assertions(source,text):
    match=PATH_Q.search(source.replace("\\","/"))
    if match:
        levels=LEVEL.findall(text)
        if Path(source).suffix.lower()==".json":
            try:levels.extend(json_levels(json.loads(text)))
            except json.JSONDecodeError:pass
        return [(f"BQ{match.group(1)}",int(x)) for x in levels]
    matches=list(BQ.finditer(text)); found=[]
    for index,match in enumerate(matches):
        end=matches[index+1].start() if index+1<len(matches) else len(text)
        found.extend((match.group(1).upper(),int(x)) for x in LEVEL.findall(text[match.end():end]))
    return found
def managed_files():
    return sorted(p for root in ROOTS for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUFFIXES)
def execution_path(qid,ref):
    if not isinstance(ref,str) or not ref.endswith(".json"):fail(f"{qid} invalid execution ref")
    governed=(ROOT/f"references/big-questions/{qid}/tests").resolve()
    candidate=(ROOT/ref).resolve()
    try:candidate.relative_to(governed)
    except ValueError:fail(f"{qid} invalid execution ref")
    return candidate
def check_execution(qid,ref,artifact):
    execution_path(qid,ref)
    if artifact.get("question_id")!=qid or artifact.get("execution_status")!="COMPLETED" or artifact.get("test_results_recorded") is not True:fail(f"{qid} governed execution not completed")
    gov=artifact.get("governance",{})
    if gov.get("review_state")!="REVIEW_REQUIRED":fail(f"{qid} execution not review-required")
    for key in ("canonical_promotion_applied",)+GATES:
        if gov.get(key) is not False:fail(f"{qid} execution gate opened: {key}")
def validate(ladder,registry,texts=(),pr_body="",artifacts=None):
    actual=[(x.get("level"),x.get("id"),x.get("label")) for x in ladder.get("stages",[])]
    if ladder.get("status")!="CANONICAL" or ladder.get("meaning")!=MEANING or actual!=STAGES:fail("canonical ladder semantics changed")
    for key in RULES:
        if ladder.get("fail_closed_rules",{}).get(key) is not True:fail(f"rule weakened: {key}")
    if registry.get("ladder_ref")!="references/big-questions/research-maturity-ladder-v0.1.json":fail("wrong ladder ref")
    items=registry.get("assessments",[]); by_id={x.get("question_id"):x for x in items}
    if set(by_id)!=set(EXPECTED) or len(by_id)!=len(items):fail("BQ001-BQ009 required exactly once")
    artifacts=artifacts or {}
    for qid,(expected,classification) in EXPECTED.items():
        item=by_id[qid]; level=item.get("asserted_level"); done=item.get("completed_stages",[])
        if item.get("question_status")!="UNRESOLVED":fail(f"{qid} resolved")
        if level!=expected:fail(f"{qid} governed score changed")
        if level is None:
            if done or item.get("scoring_status")!=classification:fail(f"{qid} classification changed")
            continue
        if done!=list(range(1,level+1)):fail(f"{qid} nonconsecutive stages")
        refs=item.get("governed_test_execution_refs",[])
        if not isinstance(refs,list):fail(f"{qid} execution refs invalid")
        if level<8 and refs:fail(f"{qid} execution binding below Level 8")
        if level>=8:
            if not refs:fail(f"{qid} Level 8 lacks execution binding")
            for ref in refs:
                if ref not in artifacts:fail(f"{qid} missing execution artifact {ref}")
                check_execution(qid,ref,artifacts[ref])
    gov=registry.get("governance",{})
    if gov.get("supports_models")!=[] or gov.get("accepted_canonical_edges")!=0:fail("model/edge promotion")
    for key in GATES:
        if gov.get(key) is not False:fail(f"gate opened: {key}")
    for source,text in texts:
        for qid,level in assertions(source,text):
            if qid not in by_id or by_id[qid].get("asserted_level")!=level:fail(f"{source}: {qid} Level {level}/10 conflicts")
    for qid,level in assertions("pull-request body",pr_body):
        if qid not in by_id or by_id[qid].get("asserted_level")!=level:fail(f"PR body: {qid} Level {level}/10 conflicts")
def main():
    ladder=json.loads(LADDER.read_text()); registry=json.loads(ASSESSMENTS.read_text()); paths=managed_files()
    texts=[(str(p.relative_to(ROOT)),p.read_text()) for p in paths]
    artifacts={}
    for item in registry["assessments"]:
        for ref in item.get("governed_test_execution_refs",[]):
            path=execution_path(item["question_id"],ref)
            if path.is_file():artifacts[ref]=json.loads(path.read_text())
    body=""
    if os.environ.get("GITHUB_EVENT_PATH"):body=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text()).get("pull_request",{}).get("body") or ""
    validate(ladder,registry,texts,body,artifacts);print(f"Big Question maturity valid; scanned {len(paths)} files")
if __name__=="__main__":
    try:main()
    except (OSError,json.JSONDecodeError,ValueError) as exc:print(f"ERROR: {exc}",file=sys.stderr);raise SystemExit(1)
