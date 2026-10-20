#!/usr/bin/env python3
import ast, json, os, re, sys
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
GATES=("truth_inference_allowed","scientific_evidence_promotion_allowed","rights_promotion_allowed","public_synthesis_updated","website_promotion_allowed","privacy_posture_changed","canonical_promotion_applied","website_updated")
def fail(msg): raise ValueError(msg)
def json_assertions(value,qid=None,path_qid=None):
    found=[]
    if isinstance(value,dict):
        if "question_id" in value:
            identity=value["question_id"]
            if not isinstance(identity,str) or not BQ.fullmatch(identity):fail("invalid structured question identity")
            qid=identity.upper()
            if path_qid and qid!=path_qid:fail("structured question identity conflicts with path")
        if "asserted_level" in value and value["asserted_level"] is not None:
            if type(value["asserted_level"]) is not int:fail("asserted_level must be an integer or null")
            if qid is None:fail("structured maturity assertion lacks question identity")
            found.append((qid,value["asserted_level"]))
        if value.get("maximum")==10 and type(value.get("level")) is int:
            if qid is None:fail("structured maturity assertion lacks question identity")
            found.append((qid,value["level"]))
        for child in value.values():found.extend(json_assertions(child,qid,path_qid))
    elif isinstance(value,list):
        for child in value:found.extend(json_assertions(child,qid,path_qid))
    return found
def text_assertions(text,qid=None):
    found=[]
    matches=list(BQ.finditer(text))
    if qid:
        end=matches[0].start() if matches else len(text)
        found.extend((qid,int(x)) for x in LEVEL.findall(text[:end]))
    for index,match in enumerate(matches):
        end=matches[index+1].start() if index+1<len(matches) else len(text)
        found.extend((match.group(1).upper(),int(x)) for x in LEVEL.findall(text[match.end():end]))
    return found

def script_assertions(source,text,path_qid=None):
    """Read literal maturity objects with a syntax tree; never execute source.

    Identity is inherited only within an object subtree, not between siblings.
    Maturity values must be static integer literals. Ambiguous overrides and
    malformed source fail closed instead of silently omitting an assertion.
    Install scripts/big-question-maturity-requirements.txt before running.
    """
    try:
        from tree_sitter import Language, Parser
        import tree_sitter_javascript as javascript
        import tree_sitter_typescript as typescript
    except ImportError:
        fail("install scripts/big-question-maturity-requirements.txt to scan scripts")
    suffix=Path(source).suffix.lower()
    grammar=(typescript.language_tsx() if suffix==".tsx" else
             typescript.language_typescript() if suffix==".ts" else javascript.language())
    root=Parser(Language(grammar)).parse(text.encode("utf-8")).root_node
    if root.has_error:fail(f"{source}: invalid script syntax")
    unknown=object()
    def literal(node):
        if node is None:return unknown
        if node.type in ("parenthesized_expression","as_expression","satisfies_expression"):
            return literal(node.named_children[0])
        if node.type=="null":return None
        if node.type not in ("number","string"):return unknown
        try:return ast.literal_eval(node.text.decode("utf-8"))
        except (ValueError,SyntaxError):return unknown
    def key_name(node):
        if node is None:return unknown
        if node.type in ("property_identifier","identifier"):
            return node.text.decode("utf-8")
        if node.type=="computed_property_name":
            return literal(node.named_children[0])
        return literal(node)
    def walk(node,qid):
        found=[]
        ambiguous=False
        # A link mentioning another BQ must not change the identity of later
        # JSX text or another string. Object identities supply local context.
        if node.type=="template_string":
            found.extend(text_assertions(node.text.decode("utf-8")[1:-1],qid))
        if node.type in ("string","jsx_text","comment"):
            value=literal(node) if node.type=="string" else node.text.decode("utf-8")
            return text_assertions(value,qid) if isinstance(value,str) else []
        if node.type=="object":
            fields={}
            for child in node.named_children:
                if child.type=="comment":continue
                if child.type=="pair":
                    key=key_name(child.child_by_field_name("key"))
                    value=child.child_by_field_name("value")
                elif child.type=="shorthand_property_identifier":
                    key=child.text.decode("utf-8");value=None
                elif child.type=="method_definition":
                    key=key_name(child.child_by_field_name("name"));value=None
                else:
                    ambiguous=True
                    continue
                if key is unknown:
                    ambiguous=True
                elif key in ("question_id","id","level","maximum","asserted_level"):
                    if key in fields:fail(f"{source}: duplicate maturity/identity field {key}")
                    fields[key]=literal(value)
            if "question_id" in fields:
                identity=fields["question_id"]
                if not isinstance(identity,str) or not BQ.fullmatch(identity):
                    fail(f"{source}: invalid structured question identity")
                qid=identity.upper()
            # The existing website index uses id rather than question_id.
            identity=fields.get("id")
            if isinstance(identity,str) and BQ.fullmatch(identity):
                if "question_id" in fields and identity.upper()!=qid:
                    fail(f"{source}: conflicting structured question identities")
                qid=identity.upper()
            if ("question_id" in fields or isinstance(identity,str) and BQ.fullmatch(identity)) and path_qid and qid!=path_qid:
                fail(f"{source}: structured question identity conflicts with path")
            if "asserted_level" in fields and fields["asserted_level"] is not None:
                if type(fields["asserted_level"]) is not int:
                    fail(f"{source}: asserted_level needs a literal integer or null")
                if qid is None:fail(f"{source}: structured maturity assertion lacks question identity")
                found.append((qid,fields["asserted_level"]))
            if "level" in fields or "maximum" in fields:
                if type(fields.get("level")) is not int or type(fields.get("maximum")) is not int or fields["maximum"]!=10:
                    fail(f"{source}: maturity needs literal integer level and maximum: 10")
                if qid is None:fail(f"{source}: structured maturity assertion lacks question identity")
                found.append((qid,fields["level"]))
        for child in node.named_children:
            found.extend(walk(child,qid))
        if found and ambiguous:
            fail(f"{source}: dynamic keys or spreads can override maturity data")
        return found
    return walk(root,path_qid)

def assertions(source,text):
    match=PATH_Q.search(source.replace("\\","/"))
    found=[]
    qid=f"BQ{match.group(1)}" if match else None
    suffix=Path(source).suffix.lower()
    if suffix==".json":
        found.extend(json_assertions(json.loads(text),qid,qid))
    elif suffix in (".ts",".tsx",".js",".jsx"):
        return script_assertions(source,text,qid)
    return found+text_assertions(text,qid)
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
    for key in GATES:
        if gov.get(key) is not False:fail(f"{qid} execution gate opened: {key}")
def validate(ladder,registry,texts=(),pr_body="",artifacts=None):
    actual=[(x.get("level"),x.get("id"),x.get("label")) for x in ladder.get("stages",[])]
    if (ladder.get("status")!="CANONICAL" or ladder.get("meaning")!=MEANING or actual!=STAGES
        or type(ladder.get("maximum_level")) is not int or ladder["maximum_level"]!=10):fail("canonical ladder semantics changed")
    for key in RULES:
        if ladder.get("fail_closed_rules",{}).get(key) is not True:fail(f"rule weakened: {key}")
    if registry.get("status")!="REVIEW_CANDIDATE":fail("registry must remain review-candidate")
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
