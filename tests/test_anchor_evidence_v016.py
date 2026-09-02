import copy,json,unittest
from pathlib import Path
from scripts.validate_anchor_evidence_v016 import validate
D=json.loads((Path(__file__).parents[1]/"references/community/anchor-evidence-fixture-v0.1.6.json").read_text())
class TestAnchorEvidence(unittest.TestCase):
 def test_baseline(self): self.assertEqual(validate(D),[])
 def m(self,f): d=copy.deepcopy(D); f(d); self.assertTrue(validate(d))
 def test_truth(self): self.m(lambda d:d["policy"].__setitem__("automated_truth_inference_allowed",True))
 def test_missing_policy(self): self.m(lambda d:d["policy"].pop("circular_confidence_allowed"))
 def test_candidate(self): self.m(lambda d:d["candidates"].append({"candidate_id":"x"}))
 def test_edge(self): self.m(lambda d:d["edges"].append({"edge_id":"x"}))
 def test_type(self): self.m(lambda d:d["anchors"][0].__setitem__("anchor_type","GENERIC_TERM"))
 def test_endpoint(self): self.m(lambda d:d["anchors"][0].__setitem__("target_endpoint_id","bad"))
 def test_public(self): self.m(lambda d:d["anchors"][0]["provenance"].__setitem__("public_safe",False))
 def test_field(self): self.m(lambda d:d["anchors"][0]["extraction"].__setitem__("public_metadata_field","graph"))
 def test_graph(self): self.m(lambda d:d["anchors"][0].__setitem__("graph_derived",True))
 def test_representation(self): self.m(lambda d:d["anchors"][0].__setitem__("representation_only",True))
 def test_digest(self): self.m(lambda d:d["anchors"][0].__setitem__("input_digest","bad"))
 def test_generic(self): self.m(lambda d:d["anchors"][0].__setitem__("normalized_value","wisdom"))
 def test_duplicate_id(self): self.m(lambda d:d["anchors"][1].__setitem__("anchor_id","anchor:fixture:exact-title:001"))
 def test_duplicate_basis(self): self.m(lambda d:d["anchors"][1].update({"anchor_type":d["anchors"][0]["anchor_type"],"normalized_value":d["anchors"][0]["normalized_value"],"independence_key":d["anchors"][0]["independence_key"]}))
 def test_private(self): self.m(lambda d:d.__setitem__("drive_id","secret"))
if __name__=="__main__": unittest.main()
