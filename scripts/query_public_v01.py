#!/usr/bin/env python3
"""Opt-in public metadata CLI. The v0.25 private-local interface is unchanged."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from public_retrieval_snapshot_v01 import load_snapshot
from retrieval_evidence_v01 import EVIDENCE_STATUSES
from query_multihop_v022 import retrieve as multihop
from query_ranked_v023 import retrieve as ranked
from query_unified_v024 import retrieve as unified


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse normally quotes arbitrary caller values and local filenames.
        self.exit(2, "Invalid public retrieval request\n")


def main():
    parser = SafeParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--domain", choices=["all", "reddit", "library"], default="all")
    parser.add_argument("--state", choices=["all", "accepted", "hold"], default="all")
    parser.add_argument("--evidence", choices=sorted(EVIDENCE_STATUSES), default=None)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("invalid limit")
    try:
        graph, concept, dedup = load_snapshot(args.snapshot)
        response = unified(args.query, ranked(args.query, multihop(args.query, graph, concept, dedup), dedup),
                           args.domain, args.state, args.limit, args.evidence)
        response.update(contract="AKASHICNET_PUBLIC_RETRIEVAL", version="0.1")
        response["policy"]["public_projection"] = "explicit_eligible_metadata_allowlist_v0.1"
        response["policy"]["private_local_interface"] = False
        # These aggregates describe approved public units, not public object
        # identities. Digest values, object links and files are never returned.
        response["policy"]["manifestation_details_exposed"] = False
        rendered = json.dumps(response, ensure_ascii=False, indent=2, allow_nan=False)
    except Exception:
        # This public process must not relay implementation exceptions containing
        # rejected labels, IDs, paths or JSON parser snippets. No fallback.
        print("Public retrieval unavailable: invalid snapshot", file=sys.stderr)
        return 1
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
