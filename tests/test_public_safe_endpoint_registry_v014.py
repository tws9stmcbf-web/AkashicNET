import copy,json,unittest
from pathlib import Path
from scripts.validate_public_safe_endpoint_registry_v014 import validate
D=json.loads((Path(__file__).parents[1]/"references/community/public-safe-endpoint-registry-fixture-v0.1.4.json").read_text())
class TestEndpoints(unittest.TestCase):
 def test_baseline(self): self.assertEqual(validate(D),[])
 def m(self,f): d=copy.deepcopy(D); f(d); self.assertTrue(validate(d))
 def test_truth(self): self.m(lambda d:d["policy"].__setitem__("automated_truth_inference_allowed",True))
 def test_accept(self): self.m(lambda d:d["policy"].__setitem__("automated_acceptance_allowed",True))
 def test_missing_type(self): self.m(lambda d:d["endpoints"].pop())
 def test_duplicate_id(self): self.m(lambda d:d["endpoints"][1].__setitem__("endpoint_id",d["endpoints"][0]["endpoint_id"]))
 def test_bad_id(self): self.m(lambda d:d["endpoints"][0].__setitem__("endpoint_id","BAD"))
 def test_edge(self): self.m(lambda d:d["edges"].append({"x":1}))
 def test_private_key(self): self.m(lambda d:d.__setitem__("drive_id","secret"))
 def test_private_value(self): self.m(lambda d:d["endpoints"][0].__setitem__("label","/My Drive/private"))
 def test_public_safe(self): self.m(lambda d:d["endpoints"][0]["provenance"].__setitem__("public_safe",False))
 def test_assertion(self): self.m(lambda d:d["endpoints"][0].__setitem__("assertion_class","INFERRED_TRUTH"))
 def test_identity(self): self.m(lambda d:d["endpoints"][0].__setitem__("identity_state","CANONICAL"))
 def test_evidence(self): self.m(lambda d:d["endpoints"][0].__setitem__("evidence_status","PROVEN"))
if __name__=="__main__": unittest.main()
