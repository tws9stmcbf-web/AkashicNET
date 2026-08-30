#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_bq001_batch4_v01 import validate

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "references" / "big-questions" / "BQ001" / "evidence-batch4-v0.1.json"


class Batch4ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(BATCH.read_text(encoding="utf-8"))

    def test_fixture_valid(self):
        validate(copy.deepcopy(self.payload))

    def test_rejects_resolved_conclusion(self):
        bad = copy.deepcopy(self.payload)
        bad["question_status"] = "RESOLVED"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_rejects_philosophy_as_established_evidence(self):
        bad = copy.deepcopy(self.payload)
        claim = next(c for c in bad["claims"] if c["claim_id"] == "CLAIM-BQ001-PHYSICALISM-HYP-01")
        claim["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_rejects_metaphysical_promotion_guard(self):
        bad = copy.deepcopy(self.payload)
        bad["promotion_guards"]["self_transcendence_proves_nonlocal_consciousness"] = True
        with self.assertRaises(ValueError):
            validate(bad)

    def test_rejects_missing_uncertainty(self):
        bad = copy.deepcopy(self.payload)
        bad["claims"][0]["uncertainty"] = ""
        with self.assertRaises(ValueError):
            validate(bad)


if __name__ == "__main__":
    unittest.main()
