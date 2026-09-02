import copy,json,unittest
from pathlib import Path
from scripts.validate_cross_source_qualification_batch_v015 import validate
D=json.loads((Path(__file__).parents[1]/"references/community/cross-source-qualification-batch-v0.1.5.json").read_text())
class TestBatch3(unittest.TestCase):
 def test_baseline(self): self.assertEqual(validate(D),[])
 def m(self,f): d=copy.deepcopy(D); f(d); self.assertTrue(validate(d))
 def test_truth(self): self.m(lambda d:d["boundaries"].__setitem__("automated_truth_inference_allowed",True))
 def test_accept(self): self.m(lambda d:d["defaults"].__setitem__("accepted_edge",True))
 def test_boundary(self): self.m(lambda d:d["boundaries"].pop("circular_confidence_allowed"))
 def test_type(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"].__setitem__("endpoint_type","UNKNOWN"))
 def test_id(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"].__setitem__("endpoint_id","bad"))
 def test_public(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"]["provenance"].__setitem__("public_safe",False))
 def test_provenance(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].pop("record_id"))
 def test_direct_rejected(self): self.m(lambda d:d["rejected_candidates"][0]["anchors"].append({"type":"EXACT_FULL_TITLE","normalized_value":"x"}))
 def test_two_rejected(self): self.m(lambda d:d["rejected_candidates"][0]["anchors"].extend([{"type":"DISTINCTIVE_NAMED_ENTITY","normalized_value":"a"},{"type":"DISTINCTIVE_MULTI_TOKEN_PHRASE","normalized_value":"b"}]))
 def test_summary(self): self.m(lambda d:d["summary"].__setitem__("qualified",1))
 def test_duplicate(self): self.m(lambda d:d["rejected_candidates"][1].__setitem__("candidate_id","qual-batch3-0001"))
 def test_decision(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("decision","ACCEPTED"))
 def test_disclaimer(self): self.m(lambda d:d.__setitem__("rejection_is_not_negative_evidence",False))
 def test_private(self): self.m(lambda d:d.__setitem__("drive_id","secret"))
if __name__=="__main__": unittest.main()
