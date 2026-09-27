import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v",ROOT/"scripts/validate_big_question_maturity_v01.py");v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Tests(unittest.TestCase):
 def test_explicit_text_identity_overrides_directory(s):
  path="references/big-questions/BQ001/x.md"
  with s.assertRaises(ValueError):v.validate(s.l,s.r,[(path,"BQ002 Level 6/10")])
  s.assertEqual(v.assertions(path,"Level 6/10\nBQ002 Level 4/10\nBQ003 Level 4/10"),
                [("BQ001",6),("BQ002",4),("BQ003",4)])
  v.validate(s.l,s.r,[(path,"BQ002 Level 4/10")])
 def test_structured_script_overstatement(s):
  for ext in ("ts","tsx","js","jsx"):
   path=f"website/app/big-questions/bq001/x.{ext}"
   with s.subTest(ext=ext),s.assertRaises(ValueError):
    v.validate(s.l,s.r,[(path,"const progress = { level: 8, maximum: 10 };")])
 def test_registry_privacy_gate(s):
  for value in (True,None,0,"false","missing"):
   c=copy.deepcopy(s.r);c["governance"]["privacy_posture_changed"]=value
   if value=="missing":del c["governance"]["privacy_posture_changed"]
   with s.subTest(value=value),s.assertRaises(ValueError):v.validate(s.l,c)
 def test_script_identity_scopes(s):
  path="website/app/big-questions/index.ts"
  text="""const records = [
   { question_id: 'BQ001', progress: { maximum: 10, level: 6 } },
   { id: 'BQ002', progress: { level: 4, maximum: 10 } }
  ];"""
  s.assertEqual(v.assertions(path,text),[("BQ001",6),("BQ002",4)])
  v.validate(s.l,s.r,[(path,text)])
  with s.assertRaises(ValueError):
   v.validate(s.l,s.r,[(path,text.replace("level: 4","level: 6"))])
  with s.assertRaisesRegex(ValueError,"lacks question identity"):
   v.assertions(path,"const x = [{question_id:'BQ001'}, {level:6, maximum:10}];")
 def test_script_literals_and_syntax(s):
  for ext in ("ts","tsx","js","jsx"):
   path=f"website/app/big-questions/bq001/x.{ext}"
   text='const p = { "maximum": /* comment */ 10, ["level"]: 6 };'
   with s.subTest(ext=ext):
    s.assertEqual(v.assertions(path,text),[("BQ001",6)])
    with s.assertRaisesRegex(ValueError,"invalid script syntax"):
     v.assertions(path,"const p = { level: 6, maximum: 10;")
  v.validate(s.l,s.r,[("website/app/big-questions/bq001/x.ts",
   "const p = {level: (6 as const), maximum: 10} satisfies Progress;")])
 def test_script_dynamic_maturity_fails_closed(s):
  cases=(
   "{level: nextLevel, maximum: 10}",
   "{level: 6 + 2, maximum: 10}",
   "{level: 6, maximum: limit}",
   "{level, maximum: 10}",
   "{get level() { return 8; }, maximum: 10}",
   "{level: 6, maximum: 10, ...override}",
   "{level: 6, maximum: 10, [key]: 8}",
   "{level: 6, level: 8, maximum: 10}",
   "{level: 6}",
   "{level: '6', maximum: 10}",
   "{level: 6, maximum: 9}",
   "{question_id: identity, progress: {level:6, maximum:10}}",
   "{question_id: 'BQ001', progress: {level:6, maximum:10}, ...override}",
  )
  for value in cases:
   with s.subTest(value=value),s.assertRaises(ValueError):
    v.assertions("website/app/big-questions/bq001/x.ts","const p = "+value+";")
 def test_script_identity_conflicts(s):
  for value in (
   "{question_id:'BQ002', level:6, maximum:10}",
   "{question_id:'BQ001', id:'BQ002', level:6, maximum:10}",
  ):
   with s.subTest(value=value),s.assertRaises(ValueError):
    v.assertions("website/app/big-questions/bq001/x.ts","const p = "+value+";")
 def test_script_comments_and_strings_are_not_objects(s):
  path="website/app/big-questions/bq001/x.ts"
  text='// {level:8, maximum:10}\nconst example = "{level:8, maximum:10}";'
  s.assertEqual(v.assertions(path,text),[])
 def test_script_text_is_locally_scoped(s):
  path="website/app/big-questions/bq001/x.tsx"
  text='const link = "BQ002"; const page = <p>Level 6/10</p>;'
  s.assertEqual(v.assertions(path,text),[("BQ001",6)])
  v.validate(s.l,s.r,[(path,text)])
  for text in ('const p = <p>BQ002 Level 6/10</p>;',
               'const p = "BQ002 Level 6/10";',
               'const p = `BQ002 Level 6/10`;'):
   with s.subTest(text=text),s.assertRaises(ValueError):v.validate(s.l,s.r,[(path,text)])
  text='const p = [{id:"BQ001",status:"Level 6/10"}, {id:"BQ002",status:"Level 4/10"}];'
  v.validate(s.l,s.r,[("website/app/big-questions/x.ts",text)])
 def test_managed_files_and_pr_body(s):
  texts=[(str(p.relative_to(ROOT)),p.read_text()) for p in v.managed_files()]
  v.validate(s.l,s.r,texts,pr_body="BQ001 Level 6/10; BQ002 Level 4/10; BQ003 Level 4/10")
 def test_execution_privacy_gate(s):
  for value in (True,None,0,"false","missing"):
   artifact=s.execution_artifact();artifact["governance"]["privacy_posture_changed"]=value
   if value=="missing":del artifact["governance"]["privacy_posture_changed"]
   with s.subTest(value=value),s.assertRaises(ValueError):
    v.check_execution("BQ001","references/big-questions/BQ001/tests/run.json",artifact)
 def test_root_json_question_identity(s):
  for value in ({"question_id":"BQ001","overall_progress":{"level":8,"maximum":10}},
                [{"question_id":"BQ001","overall_progress":{"level":8,"maximum":10}}],
                {"records":[{"question_id":"BQ001","overall_progress":{"level":8,"maximum":10}}]}):
   with s.subTest(value=value),s.assertRaises(ValueError):
    v.validate(s.l,s.r,[("references/big-questions/new.json",json.dumps(value))])
  good={"records":[{"question_id":"BQ001","overall_progress":{"level":6,"maximum":10}},
                   {"question_id":"BQ002","overall_progress":{"level":4,"maximum":10}}]}
  v.validate(s.l,s.r,[("references/big-questions/new.json",json.dumps(good))])
 def test_canonical_maximum_level(s):
  for value in (9,None,"10",10.0):
   c=copy.deepcopy(s.l);c["maximum_level"]=value
   with s.subTest(value=value),s.assertRaises(ValueError):v.validate(c,s.r)
 def test_execution_website_updated_gate(s):
  ref="references/big-questions/BQ001/tests/run.json"
  for value in (True,None,0):
   artifact=s.execution_artifact();artifact["governance"]["website_updated"]=value
   with s.subTest(value=value),s.assertRaises(ValueError):v.check_execution("BQ001",ref,artifact)
  artifact=s.execution_artifact();artifact["governance"]["website_updated"]=False
  v.check_execution("BQ001",ref,artifact)
 @classmethod
 def setUpClass(c):
  c.l=json.loads((ROOT/"references/big-questions/research-maturity-ladder-v0.1.json").read_text());c.r=json.loads((ROOT/"references/big-questions/maturity-assessments-v0.1.json").read_text())
 def test_ok(s):v.validate(s.l,s.r,[("index","BQ001 · Level 6/10\nBQ002 · Level 4/10")])
 def test_ladder_pinned(s):
  c=copy.deepcopy(s.l);c["stages"][7]["label"]="Other"
  with s.assertRaises(ValueError):v.validate(c,s.r)
 def test_score_pinned(s):
  c=copy.deepcopy(s.r);c["assessments"][0].update(asserted_level=7,completed_stages=list(range(1,8)))
  with s.assertRaises(ValueError):v.validate(s.l,c)
 def test_classification_pinned(s):
  c=copy.deepcopy(s.r);c["assessments"][-1]["scoring_status"]="UNSCORED_EXPLORATORY_NONCANONICAL"
  with s.assertRaises(ValueError):v.validate(s.l,c)
 def test_nonconsecutive(s):
  c=copy.deepcopy(s.r);c["assessments"][0]["completed_stages"]=[1,2,3,4,6]
  with s.assertRaises(ValueError):v.validate(s.l,c)
 def test_level8_binding(s):
  c=copy.deepcopy(s.r);old=v.EXPECTED["BQ001"];v.EXPECTED["BQ001"]=(8,None)
  try:
   c["assessments"][0].update(asserted_level=8,completed_stages=list(range(1,9)))
   with s.assertRaises(ValueError):v.validate(s.l,c)
  finally:v.EXPECTED["BQ001"]=old
 def test_multiline_file(s):
  with s.assertRaises(ValueError):v.validate(s.l,s.r,[("x.md","BQ001:\nLevel 8/10")])
 def test_path_binding(s):
  with s.assertRaises(ValueError):v.validate(s.l,s.r,[("references/big-questions/BQ001/x.md","Level 8/10")])
 def test_multiline_pr(s):
  with s.assertRaises(ValueError):v.validate(s.l,s.r,pr_body="BQ001:\nLevel 8/10")
 def test_recursive_scan(s):
  paths={str(p.relative_to(ROOT)) for p in v.managed_files()};s.assertIn("references/big-questions/BQ003/progress-assessment-v0.1.json",paths);s.assertIn("website/app/big-questions/bq001/page.tsx",paths)
 def test_gate(s):
  c=copy.deepcopy(s.r);c["governance"]["website_promotion_allowed"]=True
  with s.assertRaises(ValueError):v.validate(s.l,c)
 def execution_artifact(s):
  return {"question_id":"BQ001","execution_status":"COMPLETED","test_results_recorded":True,"governance":{"review_state":"REVIEW_REQUIRED","canonical_promotion_applied":False,"website_updated":False,**{key:False for key in v.GATES}}}
 def test_long_multiline_assertions(s):
  overstatement="BQ001:\n"+("x"*1000)+"\nLevel 8/10"
  with s.assertRaises(ValueError):v.validate(s.l,s.r,[("x.md",overstatement)])
  with s.assertRaises(ValueError):v.validate(s.l,s.r,pr_body=overstatement)
 def test_structured_json_level(s):
  text=json.dumps({"overall_progress":{"level":8,"maximum":10}})
  with s.assertRaises(ValueError):v.validate(s.l,s.r,[("references/big-questions/BQ001/new.json",text)])
 def test_execution_path_traversal(s):
  c=copy.deepcopy(s.r);old=v.EXPECTED["BQ001"];v.EXPECTED["BQ001"]=(8,None)
  ref="references/big-questions/BQ001/tests/../../BQ002/not-a-test.json"
  try:
   c["assessments"][0].update(asserted_level=8,completed_stages=list(range(1,9)),governed_test_execution_refs=[ref])
   with s.assertRaises(ValueError):v.validate(s.l,c,artifacts={ref:s.execution_artifact()})
  finally:v.EXPECTED["BQ001"]=old
 def test_execution_promotion_gates(s):
  c=copy.deepcopy(s.r);old=v.EXPECTED["BQ001"];v.EXPECTED["BQ001"]=(8,None)
  ref="references/big-questions/BQ001/tests/run.json"
  try:
   c["assessments"][0].update(asserted_level=8,completed_stages=list(range(1,9)),governed_test_execution_refs=[ref])
   for key in v.GATES:
    with s.subTest(key=key):
     artifact=s.execution_artifact();artifact["governance"][key]=True
     with s.assertRaises(ValueError):v.validate(s.l,c,artifacts={ref:artifact})
  finally:v.EXPECTED["BQ001"]=old
if __name__=="__main__":unittest.main()
