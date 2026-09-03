#!/usr/bin/env python3
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_semantic_link_adjudication_v021 import ARTIFACT, validate

def load():
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))

class SemanticLinkAdjudicationV021Tests(unittest.TestCase):
    def test_baseline_passes(self):
        self.assertEqual(validate(load()), [])

    def test_accepted_edge_requires_parent(self):
        data = load()
        data["edges"][1]["parent_edge_ids"] = []
        self.assertTrue(validate(data))

    def test_relationship_cannot_broaden(self):
        data = load()
        data["edges"][1]["relationship"] = "ABOUT"
        self.assertTrue(any("broadened" in e for e in validate(data)))

    def test_truth_inference_stays_off(self):
        data = load()
        data["policy"]["truth_inference_allowed"] = True
        self.assertTrue(validate(data))

    def test_original_candidate_cannot_be_promoted(self):
        data = load()
        data["edges"][0]["accepted_edge"] = True
        self.assertTrue(validate(data))

if __name__ == "__main__":
    unittest.main()
