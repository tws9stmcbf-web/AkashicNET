import copy,json,unittest
from pathlib import Path
from scripts.validate_cross_source_qualification_batch_v017 import validate
D=json.loads((Path(__file__).parents[1]/"references/community/cross-source-qualification-batch-v0.1.7.json").read_text())
class TestBatch4(unittest.TestCase):
 def test_baseline(self): self.assertEqual(validate(D),[])
 def m(self,f): d=copy.deepcopy(D); f(d); self.assertTrue(validate(d))
 def test_truth(self): self.m(lambda d:d["boundaries"].__setitem__("automated_truth_inference_allowed",True))
 def test_accept(self): self.m(lambda d:d["defaults"].__setitem__("accepted_edge",True))
 def test_boundary(self): self.m(lambda d:d["boundaries"].pop("private_drive_metadata_allowed"))
 def test_qualified(self): self.m(lambda d:d["qualified_candidates"].append(d["rejected_candidates"].pop()))
 def test_anchor(self): self.m(lambda d:d["rejected_candidates"][0]["anchor_evidence"].append({"anchor_id":"unreviewed"}))
 def test_type(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"].__setitem__("endpoint_type","UNKNOWN"))
 def test_public(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"]["provenance"].__setitem__("public_safe",False))
 def test_provenance(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].pop("record_id"))
 def test_signal(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("observed_nonqualifying_signals",[]))
 def test_decision(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("decision","ACCEPTED"))
 def test_old_pair(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"]["provenance"].__setitem__("record_id","https://www.reddit.com/r/NeuronsToNirvana/comments/1t4mza9/wisdom_traditions_as_cognitive_maps/"))
 def test_duplicate(self): self.m(lambda d:d["rejected_candidates"][1].__setitem__("candidate_id","qual-batch4-0001"))
 def test_summary(self): self.m(lambda d:d["summary"].__setitem__("qualified",1))
 def test_disclaimer(self): self.m(lambda d:d.__setitem__("rejection_is_not_negative_evidence",False))
 def test_private(self): self.m(lambda d:d.__setitem__("drive_id","secret"))
if __name__=="__main__": unittest.main()
