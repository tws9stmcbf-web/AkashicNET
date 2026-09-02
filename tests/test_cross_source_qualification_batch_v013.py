import copy, json, unittest
from pathlib import Path
from scripts.validate_cross_source_qualification_batch_v013 import validate

DATA=json.loads((Path(__file__).parents[1]/"references/community/cross-source-qualification-batch-v0.1.3.json").read_text())
class TestBatch2(unittest.TestCase):
    def test_baseline(self): self.assertEqual(validate(DATA),[])
    def mutated(self,fn):
        d=copy.deepcopy(DATA); fn(d); self.assertTrue(validate(d))
    def test_truth_switch(self): self.mutated(lambda d:d["boundaries"].__setitem__("automated_truth_inference_allowed",True))
    def test_acceptance_switch(self): self.mutated(lambda d:d["boundaries"].__setitem__("automated_acceptance_allowed",True))
    def test_missing_boundary(self): self.mutated(lambda d:d["boundaries"].pop("private_drive_metadata_allowed"))
    def test_unsafe_defaults(self): self.mutated(lambda d:d["defaults"].__setitem__("accepted_edge",True))
    def test_summary(self): self.mutated(lambda d:d["summary"].__setitem__("qualified",1))
    def test_duplicate_id(self): self.mutated(lambda d:d["rejected_candidates"][1].__setitem__("candidate_id","qual-batch2-0001"))
    def test_direct_anchor_rejected(self): self.mutated(lambda d:d["rejected_candidates"][0]["anchors"].append({"type":"EXACT_FULL_TITLE","normalized_value":"x"}))
    def test_two_anchors_rejected(self): self.mutated(lambda d:d["rejected_candidates"][0]["anchors"].extend([{"type":"DISTINCTIVE_NAMED_ENTITY","normalized_value":"a"},{"type":"DISTINCTIVE_MULTI_TOKEN_PHRASE","normalized_value":"b"}]))
    def test_bad_decision(self): self.mutated(lambda d:d["rejected_candidates"][0].__setitem__("decision","ACCEPTED"))
    def test_disclaimer(self): self.mutated(lambda d:d.__setitem__("rejection_is_not_negative_evidence",False))
    def test_private_key(self): self.mutated(lambda d:d.__setitem__("drive_id","secret"))
if __name__ == "__main__": unittest.main()
