"""Offline regression checks for the N2N ledger's current continuation."""

import csv
import json
import re
import unittest
from pathlib import Path

from scripts.reddit_corpus_census import canonicalise

ROOT = Path(__file__).resolve().parents[1]


class N2NAnalysisLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(
            (ROOT / "references/community/n2n-analysis-ledger.json").read_text()
        )

    def test_checkpoint_is_smallest_pending_archive_id(self):
        ledger = self.ledger
        ids = set()
        with (ROOT / ledger["queue"]["source_path"]).open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            reader = csv.reader(handle)
            next(reader)
            for row in reader:
                if not row:
                    continue
                record = canonicalise(row[0])
                if (record.get("subreddit", "").casefold() == "neuronstonirvana"
                        and record["status"] in {"candidate", "annotation_derived"}):
                    ids.add(record["post_id"])
        statuses = {r["post_id"]: r["status"] for r in ledger["records"]}
        pending = sorted(i for i in ids if statuses.get(i, "PENDING") == "PENDING")
        self.assertEqual(len(ids), ledger["queue"]["unique_n2n_post_ids"])
        self.assertEqual(
            ledger["checkpoint"]["next_pending_post_id"],
            pending[0] if pending else None,
        )

    def test_investigation_continuation_uses_checkpoint_not_copied_id(self):
        items = self.ledger["investigation_register"]["items"]
        matches = [i for i in items if i["issue_id"] == "N2N-INV-001"]
        self.assertEqual(len(matches), 1)
        action = matches[0]["next_action"]
        self.assertIn("resume repository-only assessment at checkpoint.next_pending_post_id", action)
        self.assertIn("smallest PENDING ID under queue.resume_rule", action)
        self.assertIn("If no pending ID remains, stop queue continuation.", action)
        # Reject reintroduced literal pointers, including a currently correct ID
        # which would become stale on the next batch. Historical follow-ups stay intact.
        self.assertIsNone(re.search(r"\bpost ID\s+[0-9a-z]+\b", action))
        for post_id in {r["post_id"] for r in self.ledger["records"]} | {
            self.ledger["checkpoint"]["next_pending_post_id"]
        }:
            if post_id is not None:
                self.assertNotRegex(action, rf"\b{re.escape(post_id)}\b")


if __name__ == "__main__":
    unittest.main()
