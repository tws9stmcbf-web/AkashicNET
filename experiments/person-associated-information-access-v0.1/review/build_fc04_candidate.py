#!/usr/bin/env python3
"""Reproduce the bounded FC04-P2 construction, using only public reviewer data.

Prints the proposal JSON to stdout. The audit rules are construction constraints,
not an independent or held-out validation set. Does not modify active materials.
"""

import copy
import hashlib
import itertools
import json
from pathlib import Path

from audit_fc04_candidate import heuristic_diagnostics


ROOT = Path(__file__).resolve().parents[1]
OFFSETS = [0, 3, 7, 11]


def make_items(persons, ranks):
    items = []
    for person, rank in zip(persons, ranks):
        original = person["delayed_recognition"]
        base = int(person["award_year"]) - OFFSETS[rank - 1]
        years = [base + offset for offset in OFFSETS]
        if min(years) < 1901:
            return None
        if person["person_id"] == "F07" and max(years) >= 2011:
            return None
        if person["person_id"] == "F04" and max(years) >= 1992:
            return None
        wrong_ids = iter(["o1", "o3", "o4"])
        options = [{"id": "o2" if index == rank - 1 else next(wrong_ids),
                    "text": str(year)} for index, year in enumerate(years)]
        items.append({"person_id": person["person_id"], "name": person["name"],
                      "source_item_id": original["id"], "prompt": original["prompt"],
                      "options": options, "correct_option_id": original["correct_option_id"],
                      "correct_year": person["award_year"], "correct_chronological_rank": rank,
                      "allow_do_not_know": original["allow_do_not_know"],
                      "rationale": original["rationale"], "historical_source_ids": person["sources"],
                      "distractor_status": "SYNTHETIC_INCORRECT_OPTIONS_NOT_HISTORICAL_ASSERTIONS"})
    return items


def rank_hash(ranks):
    encoded = json.dumps(list(ranks), separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main():
    baseline_path = ROOT / "materials/stimulus-set.json"
    baseline = json.loads(baseline_path.read_text())
    discarded = json.loads((ROOT / "review/fc04-discarded-p1-2026-10-21.json").read_text())
    proposal = copy.deepcopy(discarded["proposal"])
    assert hashlib.sha256(baseline_path.read_bytes()).hexdigest() == proposal["baseline_stimulus_sha256"]
    # Verify that the archived failed attempt is reproducible with the same rules.
    assert heuristic_diagnostics(discarded["proposal"]["items"]) == discarded["diagnostics"]
    assignments = sorted(set(itertools.permutations([1, 1, 2, 2, 3, 3, 4, 4])))
    eligible = []
    passing = []
    for ranks in assignments:
        items = make_items(baseline["persons"], ranks)
        if items is None:
            continue
        eligible.append(ranks)
        diagnostics = heuristic_diagnostics(items)
        if all(result["correct_items_tie_resolution_bounds"][1] <= 2
               for result in diagnostics.values()):
            passing.append(ranks)
    assert passing, "No candidate satisfies the declared finite construction rules"
    selected = min(passing, key=rank_hash)
    proposal["proposal_id"] = "FC04-P2"
    proposal["items"] = make_items(baseline["persons"], selected)
    proposal["rule"]["correct_rank_by_person"] = {
        person["person_id"]: rank for person, rank in zip(baseline["persons"], selected)}
    proposal["rule"]["selection_basis"] = (
        "Enumerated all balanced rank assignments; rejected candidate years before 1901 "
        "and options in or after McClintock's death year 1992 or Maathai's death year 2011; "
        "retained assignments for which every one of nine declared heuristic rules scores "
        "at most 2/8 even under favorable tie resolution. Selected the retained assignment "
        "with the smallest SHA-256 of its compact JSON rank list. This public deterministic "
        "choice is not a hidden-target draw or a participant assignment.")
    proposal["development_record"] = {
        "discarded_draft": "review/fc04-discarded-p1-2026-10-21.json",
        "discard_reason": "Smallest-last-digit rule scored 5/8 in P1",
        "balanced_assignments_enumerated": len(assignments),
        "assignments_meeting_year_boundaries": len(eligible),
        "assignments_meeting_nine_rule_constraint": len(passing),
        "selected_rank_list": list(selected),
        "selected_rank_list_sha256": rank_hash(selected),
        "selection_inputs": "Public years and synthetic option geometry only; no participant data",
        "held_out_validation": False,
        "additional_rejected_constructions": [
            "Before the Maathai life-span guard, rank list [2,3,3,4,2,4,1,1] yielded a 2015 option.",
            "With only the Maathai guard, rank list [3,4,2,1,4,2,3,1] yielded a 1994 McClintock option.",
            "Both were rejected before publication; final candidates exclude both figures' death years and later years."],
    }
    proposal["rule"]["year_boundaries"] = {"all_persons_minimum_year": 1901,
                                            "F07_maximum_year": 2010,
                                            "F04_maximum_year": 1991}
    proposal["boundary_source_record"] = {
        "claims": ["Wangari Maathai died on 25 September 2011", "Barbara McClintock died on 2 September 1992"],
        "date_checked": "2026-10-21",
        "sources": [
            {"url": "https://www.nelsonmandela.org/wangari-maathai-bio",
             "publisher": "Nelson Mandela Foundation",
             "access": "Page-body text retrieved; death date at paragraph following WMI description. Page attributes its biography to the Green Belt Movement.",
             "retrieval_reference": "turn15view1"},
            {"url": "https://www.nobelprize.org/prizes/peace/2004/maathai/facts/",
             "publisher": "NobelPrize.org",
             "access": "Indexed official facts text corroborates death date; full canonical page not newly retrieved.",
             "retrieval_reference": "turn14search0"},
            {"url": "https://www.nobelprize.org/prizes/medicine/1983/mcclintock/facts/",
             "publisher": "NobelPrize.org", "access": "Indexed official facts text gives McClintock's death date; full page not retrieved in this follow-up.",
             "retrieval_reference": "turn17search0"}],
        "blocked_access_attempts": [
            {"url": "https://www.greenbeltmovement.org/wangari-maathai/", "result": "HTTP_429"},
            {"url": "https://www.un.org/en/node/55032", "result": "HTTP_403"}],
        "scope": "Conservative proposed-option boundary only; not a change to the dossier or a general adjudication of posthumous Nobel eligibility.",
        "reuse": "Links and factual paraphrase only; no copied media.",
        "independent_verification": "PENDING", "rights_review": "PENDING"}
    proposal["limits"].insert(0, "The nine tested rules were used to construct P2; passing them is not independent or held-out evidence. Unexamined strategies can still succeed.")
    print(json.dumps(proposal, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
