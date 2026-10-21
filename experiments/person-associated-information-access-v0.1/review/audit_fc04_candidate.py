#!/usr/bin/env python3
"""Static reviewer audit of the FC04 proposal; no participant/hidden-target data."""

import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "review/fc04-distractor-candidate-2026-10-21.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(item):
    years = sorted(int(option["text"]) for option in item["options"])
    keyed = next(int(option["text"]) for option in item["options"]
                 if option["id"] == item["correct_option_id"])
    return years.index(keyed) + 1


def heuristic_diagnostics(items):
    """Ties use equal weight; also report bounds over all tie resolutions."""
    rules = {
        "earliest": lambda years: [min(years)],
        "second_earliest": lambda years: [sorted(years)[1]],
        "third_earliest": lambda years: [sorted(years)[2]],
        "latest": lambda years: [max(years)],
        "closest_to_midrange": lambda years: minimizers(
            years, lambda y: abs(2 * y - min(years) - max(years))),
        "closest_to_mean": lambda years: minimizers(
            years, lambda y: abs(4 * y - sum(years))),
        "closest_to_multiple_of_ten": lambda years: minimizers(
            years, lambda y: min(y % 10, 10 - y % 10)),
        "smallest_last_digit": lambda years: minimizers(years, lambda y: y % 10),
        "largest_last_digit": lambda years: minimizers(years, lambda y: -(y % 10)),
    }
    results = {}
    for name, select in rules.items():
        expected = Fraction(0)
        lower = upper = tied = 0
        for item in items:
            years = [int(option["text"]) for option in item["options"]]
            key = next(int(option["text"]) for option in item["options"]
                       if option["id"] == item["correct_option_id"])
            choices = select(years)
            tied += len(choices) > 1
            if key in choices:
                expected += Fraction(1, len(choices))
                upper += 1
                lower += len(choices) == 1
        results[name] = {
            "correct_items_with_uniform_tie_breaking": float(expected),
            "exact_fraction_of_items_correct": str(expected / len(items)),
            "correct_items_tie_resolution_bounds": [lower, upper],
            "tied_items": tied,
            "total_items": len(items),
        }
    return results


def minimizers(values, score):
    best = min(map(score, values))
    return [value for value in values if score(value) == best]


def main():
    baseline_path = ROOT / "materials/stimulus-set.json"
    baseline = json.loads(baseline_path.read_text())
    proposal = json.loads(PROPOSAL.read_text())
    assert digest(baseline_path) == proposal["baseline_stimulus_sha256"]
    assert proposal["status"] == "REVIEW_ONLY_NOT_ADOPTED_NOT_FOR_PARTICIPANT_USE"
    assert proposal["finding_status"] == "FC04_OPEN_PENDING_INDEPENDENT_DISPOSITION"
    assert not proposal["adoption_gates"]["participant_use_authorized"]
    assert not proposal["adoption_gates"]["active_materials_replaced"]
    assert not baseline["approved_for_collection"]
    assert baseline["materials_version"] == "0.2-candidate"
    assert baseline["protocol_version"] == "0.1"
    assert len(proposal["items"]) == len(baseline["persons"]) == 8

    original_items = []
    rows = []
    for person, proposed in zip(baseline["persons"], proposal["items"]):
        original = person["delayed_recognition"]
        original_items.append(original)
        assert proposed["person_id"] == person["person_id"]
        assert proposed["name"] == person["name"]
        assert proposed["source_item_id"] == original["id"]
        for field in ["prompt", "correct_option_id", "allow_do_not_know", "rationale"]:
            assert proposed[field] == original[field], field
        assert proposed["historical_source_ids"] == person["sources"]
        assert len(proposed["options"]) == 4
        assert {option["id"] for option in proposed["options"]} == {"o1", "o2", "o3", "o4"}
        assert all(len(option["text"]) == 4 and option["text"].isdigit()
                   for option in proposed["options"])
        years = sorted(int(option["text"]) for option in proposed["options"])
        assert len(set(years)) == 4
        assert [y - years[0] for y in years] == [0, 3, 7, 11]
        assert years[0] >= 1901
        if person["person_id"] == "F07":
            assert max(years) < 2011
        if person["person_id"] == "F04":
            assert max(years) < 1992
        key = next(option["text"] for option in proposed["options"]
                   if option["id"] == proposed["correct_option_id"])
        assert key == person["award_year"] == proposed["correct_year"]
        assert rank(proposed) == proposed["correct_chronological_rank"]

        # All 24 possible display permutations; this is not a runtime test.
        hits_by_slot = [0] * 4
        for permutation in itertools.permutations(proposed["options"]):
            for slot, option in enumerate(permutation):
                hits_by_slot[slot] += option["id"] == proposed["correct_option_id"]
        assert hits_by_slot == [6, 6, 6, 6]
        rows.append({"person_id": person["person_id"], "key": key,
                     "original_rank": rank(original), "proposed_rank": rank(proposed),
                     "sorted_years": years, "permutations_enumerated": 24,
                     "correct_counts_by_display_slot": hits_by_slot})

    old_ranks = Counter(rank(item) for item in original_items)
    new_ranks = Counter(rank(item) for item in proposal["items"])
    assert old_ranks == {2: 8}, old_ranks
    assert new_ranks == {1: 2, 2: 2, 3: 2, 4: 2}, new_ranks
    diagnostics = heuristic_diagnostics(proposal["items"])
    assert proposal["proposal_id"] == "FC04-P2"
    assert all(result["correct_items_tie_resolution_bounds"][1] <= 2
               for result in diagnostics.values())

    manifest = json.loads((ROOT / "materials/manifest.json").read_text())
    checked_hashes = {name: digest(ROOT / name) for name in manifest["sha256"]}
    assert checked_hashes == manifest["sha256"]
    assert not manifest["independent_review_completed"]
    assert all(source["independent_verification"] == "PENDING" and
               source["rights_review"] == "PENDING" for source in baseline["sources"])
    assert (ROOT / "review/review-packet.md").read_text().count("| NOT_STARTED |") == 7

    report = {
        "status": "PASS_STATIC_PROPOSAL_CHECKS_NOT_APPROVAL",
        "proposal_id": proposal["proposal_id"],
        "baseline_commit": proposal["baseline_commit"],
        "proposal_sha256": digest(PROPOSAL),
        "audit_script_sha256": digest(Path(__file__)),
        "baseline_manifest_sha256": digest(ROOT / "materials/manifest.json"),
        "baseline_manifest_file_hashes_match": checked_hashes,
        "unchanged_correct_years_key_ids_prompts_and_source_mappings": True,
        "all_independent_source_and_rights_records_pending": True,
        "independent_review_rows_not_started": 7,
        "original_rank_counts": dict(sorted(old_ranks.items())),
        "proposed_rank_counts": dict(sorted(new_ranks.items())),
        "items": rows,
        "heuristics": {"baseline": heuristic_diagnostics(original_items),
                       "proposal": diagnostics},
        "interpretation": "The tested universal second-earliest shortcut is absent in this proposal. This does not establish psychometric validity, equal difficulty, chance-level performance or absence of other shortcuts.",
        "runtime_randomization_tested": False,
        "participant_data_used": False,
        "independent_human_review": False,
        "participant_use_authorized": False,
        "fc04_closed": False,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
