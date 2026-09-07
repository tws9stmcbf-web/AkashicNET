import copy,hashlib,json,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.validate_cross_source_qualification_batch_v017 import validate
D=json.loads((Path(__file__).parents[1]/"references/community/cross-source-qualification-batch-v0.1.7.json").read_text())
class TestBatch4(unittest.TestCase):
 def test_baseline(self): self.assertEqual(validate(D),[])
 def m(self,f): d=copy.deepcopy(D); f(d); self.assertTrue(validate(d))
 def test_truth(self): self.m(lambda d:d["boundaries"].__setitem__("automated_truth_inference_allowed",True))
 def test_accept(self): self.m(lambda d:d["defaults"].__setitem__("accepted_edge",True))
 def test_embedded_accept(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("accepted_edge",True))
 def test_top_level_edges(self): self.m(lambda d:d.__setitem__("edges",[{"edge_id":"forbidden"}]))
 def test_boundary(self): self.m(lambda d:d["boundaries"].pop("private_drive_metadata_allowed"))
 def test_qualified(self): self.m(lambda d:d["qualified_candidates"].append(d["rejected_candidates"].pop()))
 def test_anchor(self): self.m(lambda d:d["rejected_candidates"][0]["anchor_evidence"].append({"anchor_id":"unreviewed"}))
 def test_type(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"].__setitem__("endpoint_type","UNKNOWN"))
 def test_endpoint_syntax(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"].__setitem__("endpoint_id","endpoint:Bad Unicode"))
 def test_public(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"]["provenance"].__setitem__("public_safe",False))
 def test_provenance(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].pop("record_id"))
 def test_blank_provenance(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].__setitem__("record_id",""))
 def test_unknown_artifact(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].__setitem__("artifact_id","artifact:unknown"))
 def test_independence_mismatch(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].__setitem__("independence_key","source:other"))
 def test_unknown_source_record(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"]["provenance"].__setitem__("record_id","https://www.reddit.com/r/NeuronsToNirvana/comments/fabricated/"))
 def test_unknown_target_record(self): self.m(lambda d:d["rejected_candidates"][0]["target_endpoint"]["provenance"].__setitem__("record_id","FABRICATED-001"))
 def test_same_artifact_pair(self):
  def mutate(d):
   target=d["rejected_candidates"][0]["target_endpoint"]
   target["provenance"]["artifact_id"]=d["source_artifacts"][0]["artifact_id"]
   target["provenance"]["independence_key"]=d["source_artifacts"][0]["independence_key"]
  self.m(mutate)
 def test_empty_sources(self): self.m(lambda d:d.__setitem__("source_artifacts",[]))
 def test_source_hash(self): self.m(lambda d:d["source_artifacts"][0].__setitem__("sha256","0"*64))
 def test_actual_source_hash(self):
  with patch.object(Path,"read_bytes",return_value=b"tampered source"):
   self.assertTrue(validate(copy.deepcopy(D)))
 def test_source_hash_and_bytes_cannot_move_together(self):
  d=copy.deepcopy(D); tampered=b"tampered source"
  d["source_artifacts"][0]["sha256"]=hashlib.sha256(tampered).hexdigest()
  with patch.object(Path,"read_bytes",return_value=tampered):
   self.assertTrue(validate(d))
 def test_duplicate_source(self): self.m(lambda d:d["source_artifacts"].append(copy.deepcopy(d["source_artifacts"][0])))
 def test_signal(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("observed_nonqualifying_signals",[]))
 def test_decision(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("decision","ACCEPTED"))
 def test_old_pair(self): self.m(lambda d:d["rejected_candidates"][0]["source_endpoint"]["provenance"].__setitem__("record_id","https://www.reddit.com/r/NeuronsToNirvana/comments/1t4mza9/wisdom_traditions_as_cognitive_maps/"))
 def test_duplicate(self): self.m(lambda d:d["rejected_candidates"][1].__setitem__("candidate_id","qual-batch4-0001"))
 def test_summary(self): self.m(lambda d:d["summary"].__setitem__("qualified",1))
 def test_disclaimer(self): self.m(lambda d:d.__setitem__("rejection_is_not_negative_evidence",False))
 def test_private_key_variants(self):
  for key in ("drive_id","drive_file_id","drive_object_id","file_id","filename","file_name","path","parent_id","parent_path","parents","private_path","object_hash"):
   with self.subTest(key=key): self.m(lambda d,k=key:d["rejected_candidates"][0].__setitem__(k,"secret"))
 def test_private_value(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("note","/My Drive/private.pdf"))
 def test_private_manifestation_id(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("note","AKM-001234"))
 def test_private_manifestation_embedded(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("note","copy_AKM-001234.pdf"))
 def test_private_manifestation_key(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("AKM-001234","private"))
 def test_private_manifestation_in_array(self): self.m(lambda d:d["rejected_candidates"][0]["observed_nonqualifying_signals"].append("copy_AKM-001234.pdf"))
 def test_private_path_in_array(self): self.m(lambda d:d["rejected_candidates"][0]["observed_nonqualifying_signals"].append("/My Drive/private.pdf"))
 def test_private_path_key(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("/My Drive/private.pdf","private"))
 def test_private_link_key(self): self.m(lambda d:d["rejected_candidates"][0].__setitem__("drive.google.com/open?id=private","private"))
if __name__=="__main__": unittest.main()
