"""Build a bounded proposal queue from explicitly nominated claim pairs. Stdlib only."""
import argparse
import json
from pathlib import Path

SCOPE = ("population", "conditions", "definition", "time")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def build_queue(data, budget=5):
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if not isinstance(data, dict) or not all(isinstance(data.get(k), list) for k in ("claims", "pairs")):
        raise ValueError("input requires claims and pairs arrays")
    claims = {}
    for claim in data["claims"]:
        if not isinstance(claim, dict):
            raise ValueError("each claim must be an object")
        cid = claim.get("id")
        if not nonempty(cid) or cid in claims:
            raise ValueError("claim IDs must be unique nonempty strings")
        if not nonempty(claim.get("text")):
            raise ValueError("each claim requires text")
        scope = claim.get("scope", {})
        if not isinstance(scope, dict):
            raise ValueError("scope must be an object")
        sources = claim.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(s, dict) for s in sources):
            raise ValueError("sources must be a list of objects")
        claims[cid] = claim
    rows, seen = [], set()
    for candidate in data["pairs"]:
        if not isinstance(candidate, dict):
            raise ValueError("each pair must be an object")
        pair = candidate.get("claims")
        if not isinstance(pair, list) or len(pair) != 2 or not all(nonempty(x) for x in pair):
            raise ValueError("each pair requires two claim IDs")
        a, b = sorted(pair)
        if a == b or a not in claims or b not in claims:
            raise ValueError("pair must reference two distinct known claims")
        if (a, b) in seen:
            raise ValueError("duplicate pair")
        seen.add((a, b))
        left, right = claims[a], claims[b]
        anchored = all(any(nonempty(s.get("ref")) and nonempty(s.get("passage"))
                           for s in c.get("sources", [])) for c in (left, right))
        unknown = [k for k in SCOPE if not all(nonempty(c.get("scope", {}).get(k))
                                               for c in (left, right))]
        different = [k for k in SCOPE if k not in unknown and
                     left["scope"][k] != right["scope"][k]]
        test = candidate.get("next_test", "")
        if not isinstance(test, str):
            raise ValueError("next_test must be a string")
        if not anchored:
            state, rank, action = "needs_source", 0, "Locate original passages for both claims."
        elif different:
            state, rank, action = "scope_difference", 1, "Check whether differing scope explains the apparent conflict."
        elif unknown:
            state, rank, action = "needs_context", 2, "Recover missing scope before judging contradiction."
        else:
            state, rank, action = "candidate_conflict", 3, "Review semantic incompatibility; matching scope alone is not proof."
        rows.append({"claims": [a, b], "state": state, "unknown_scope": unknown,
                     "different_scope": different, "next_action": action,
                     "proposed_test": test.strip() or None, "priority_rank": rank,
                     "status": "unresolved", "provenance": "ai-suggested",
                     "automatic_adjudication": False})
    # Resolve provenance/context prerequisites before investigating substantive conflicts.
    rows.sort(key=lambda row: (row["priority_rank"], row["claims"]))
    return {"schema_version": "0.1", "mode": "REVIEW_PACKET_ONLY",
            "publication_allowed": False,
            "automated_acceptance_allowed": False,
            "rights_promotion_allowed": False,
            "scientific_evidence_promotion_allowed": False,
            "claims": [claims[cid] for cid in sorted(claims)],
            "queue": rows[:budget], "deferred": len(rows[budget:]),
            "stop_condition": "budget_exhausted" if len(rows) > budget else "queue_exhausted",
            "requires_researcher_adjudication": True,
            "truth_promotion": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--budget", type=int, default=5)
    args = parser.parse_args()
    try:
        result = build_queue(json.loads(args.input.read_text()), args.budget)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
