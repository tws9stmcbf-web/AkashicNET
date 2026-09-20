import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v",ROOT/"scripts/validate_big_question_maturity_v01.py");v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Tests(unittest.TestCase):
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
  return {"question_id":"BQ001","execution_status":"COMPLETED","test_results_recorded":True,"governance":{"review_state":"REVIEW_REQUIRED","canonical_promotion_applied":False,**{key:False for key in v.GATES}}}
 def test_long_multiline_assertions(s):
  overstatement="BQ001:\\n"+("x"*1000)+"\\nLevel 8/10"
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
