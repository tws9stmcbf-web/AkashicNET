"""Synthetic-only reference analysis. No recruitment, acquisition or target generation.

Run --planning for exact H1 operating characteristics, --demo for a deterministic
synthetic analysis, or unittest for malformed-fixture and numerical checks.
Python 3.10+ standard library only. This is not an approved production pipeline.
"""
import argparse
import itertools
import json
import math
import random
from collections import Counter, defaultdict

STATUSES = {"observed", "abstain", "timeout", "not_started",
            "technical_failure", "integrity_failure", "withdrawn"}
CELLS = ("MT", "MU", "RT", "RU")
PERSONS = {f"F{i:02d}" for i in range(1, 9)}


def binomial_tail(n, k, p=0.25):
    """P[X >= k], with no normal approximation."""
    if type(n) is not int or type(k) is not int or n < 0:
        raise ValueError("n and k must be integers; n must be nonnegative")
    if not 0 <= p <= 1:
        raise ValueError("p outside [0,1]")
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return min(1.0, math.fsum(math.comb(n, j) * p**j * (1-p)**(n-j)
                              for j in range(k, n+1)))


def planning():
    n = 192
    critical = next(k for k in range(n+1) if binomial_tail(n, k) <= .025)
    return {
        "kind": "MODEL_CALCULATION_NOT_STUDY_DATA",
        "n": n, "alpha": .025, "critical_hits": critical,
        "null_tail": binomial_tail(n, critical),
        "h1_only_power_at_0_30": binomial_tail(n, critical, .30),
        "h1_only_power_at_0_35": binomial_tail(n, critical, .35),
        "scope": "Homogeneous independent-hit model; not joint or interaction power."
    }


def validate_synthetic(data):
    if data.get("data_kind") != "SYNTHETIC" or data.get("study_version") != "0.1":
        raise ValueError("Only explicitly synthetic v0.1 fixtures are supported")
    people = data.get("participants", [])
    if len(people) != 48:
        raise ValueError("Exactly 48 planned participants required")
    ids = [p.get("id") for p in people]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != 48:
        raise ValueError("Participant IDs must be unique nonempty strings")
    if Counter(p.get("arm") for p in people) != {"M": 24, "R": 24}:
        raise ValueError("Allocation must contain 24 M and 24 R")
    rows = data.get("trials", [])
    if len(rows) != 768:
        raise ValueError("All 768 planned slots required, including missing outcomes")
    arm = {p["id"]: p["arm"] for p in people}
    seen, by_person, by_participant = set(), defaultdict(list), defaultdict(list)
    for r in rows:
        pid, idx = r.get("participant_id"), r.get("trial_index")
        if pid not in arm or type(idx) is not int or not 0 <= idx < 16:
            raise ValueError("Invalid participant/slot identity")
        key = (pid, idx)
        if key in seen:
            raise ValueError("Duplicate/retry cannot replace a planned slot")
        seen.add(key)
        if r.get("person_id") not in PERSONS or r.get("familiarity") not in {"T", "U"}:
            raise ValueError("Invalid person/familiarity")
        if r.get("status") not in STATUSES:
            raise ValueError("Unknown status; no implicit exclusions")
        for field in ("choice", "target"):
            v = r.get(field)
            if v is not None and (type(v) is not int or not 0 <= v <= 3):
                raise ValueError("Canonical code must be null or integer 0..3")
        if r["status"] == "observed":
            if r.get("choice") is None or r.get("target") is None:
                raise ValueError("Observed row requires one choice and one target")
            times = [r.get(k) for k in ("target_committed_at",
                                       "response_locked_at", "target_opened_at")]
            if any(type(t) not in (int, float) or not math.isfinite(t) for t in times):
                raise ValueError("Observed row requires finite toy receipt times")
            if not times[0] < times[1] < times[2]:
                raise ValueError("Observed row has invalid commitment/lock/open order")
        by_participant[pid].append(r)
        by_person[(pid, r["person_id"])].append(r)
    for pid in ids:
        pr = by_participant[pid]
        if Counter(r["familiarity"] for r in pr) != {"T": 8, "U": 8}:
            raise ValueError("Every participant needs eight T and eight U slots")
        for figure in PERSONS:
            pair = by_person[(pid, figure)]
            if len(pair) != 2 or len({r["familiarity"] for r in pair}) != 1:
                raise ValueError("Each of eight people must appear twice in a fixed condition")
    return arm


def score(row):
    return int(row["status"] == "observed" and row["choice"] == row["target"])


def arm_randomization(counts, arm, draws=100000, seed=20261018):
    """Sharp-null Fisher test; reassign whole people, never individual trials."""
    if type(draws) is not int or draws < 1:
        raise ValueError("At least one permutation draw required")
    ids = sorted(counts)
    if len(ids) != 48 or Counter(arm[p] for p in ids) != {"M": 24, "R": 24}:
        raise ValueError("Expected 48 complete participant clusters")
    values = [counts[p]["T"] for p in ids]
    total = sum(values)
    observed = 2 * sum(counts[p]["T"] for p in ids if arm[p] == "M") - total
    rng, ge = random.Random(seed), 0
    for _ in range(draws):
        chosen = rng.sample(range(48), 24)
        null_stat = 2 * sum(values[i] for i in chosen) - total
        ge += null_stat >= observed
    p = (1+ge)/(1+draws)
    return {"p_value": p, "draws": draws, "seed": seed,
            "monte_carlo_se": math.sqrt(p*(1-p)/(draws+1)),
            "difference": observed/192,
            "unit": "participant", "clusters": 48,
            "null": "sharp no-instruction-effect; uniform 24-of-48 allocation"}


def quantile(values, probability):
    values = sorted(values)
    x = (len(values)-1)*probability
    lo, hi = math.floor(x), math.ceil(x)
    return values[lo] + (x-lo)*(values[hi]-values[lo])


def bootstrap(counts, arm, draws=20000, seed=20261019):
    if type(draws) is not int or draws < 2:
        raise ValueError("At least two bootstrap draws required")
    groups = {a: [p for p in sorted(counts) if arm[p] == a] for a in ("M", "R")}
    rng = random.Random(seed)
    estimates = {k: [] for k in (*CELLS, "trained_difference", "interaction")}
    for _ in range(draws):
        cells = {}
        for a in ("M", "R"):
            sample = rng.choices(groups[a], k=24)
            for f in ("T", "U"):
                cells[a+f] = sum(counts[p][f] for p in sample)/192
                estimates[a+f].append(cells[a+f])
        estimates["trained_difference"].append(cells["MT"]-cells["RT"])
        estimates["interaction"].append(cells["MT"]-cells["MU"]-cells["RT"]+cells["RU"])
    return {"draws": draws, "seed": seed, "unit": "participant within arm",
            "interval_type": "two-sided 95% percentile; small-pilot approximation",
            "intervals": {k: [quantile(v, .025), quantile(v, .975)]
                          for k, v in estimates.items()}}


def analyze_synthetic(data, permutation_draws=100000, bootstrap_draws=20000):
    arm = validate_synthetic(data)
    counts = {p: {"T": 0, "U": 0} for p in arm}
    cells = {c: {"planned": 0, "observed": 0, "hits": 0, "zero_scored_statuses": {}}
             for c in CELLS}
    statuses = {c: Counter() for c in CELLS}
    for r in data["trials"]:
        pid, f = r["participant_id"], r["familiarity"]
        c = arm[pid]+f
        y = score(r)
        counts[pid][f] += y
        cells[c]["planned"] += 1
        cells[c]["observed"] += r["status"] == "observed"
        cells[c]["hits"] += y
        if r["status"] != "observed":
            statuses[c][r["status"]] += 1
    for c, obj in cells.items():
        missing = obj["planned"]-obj["observed"]
        obj["rate"] = obj["hits"]/obj["planned"]
        obj["valid_observation_rate"] = (obj["hits"]/obj["observed"]
                                          if obj["observed"] else None)
        obj["missing_bounds"] = [obj["rate"], (obj["hits"]+missing)/obj["planned"]]
        obj["zero_scored_statuses"] = dict(statuses[c])
    return {
        "kind": "SYNTHETIC_ONLY_NOT_STUDY_RESULTS",
        "participants": 48, "planned_trials": 768, "cells": cells,
        "h1": {"n": 192, "hits": cells["MT"]["hits"],
               "p_value": binomial_tail(192, cells["MT"]["hits"]),
               "null": "iid concealed uniform targets; .25 conditional match probability"},
        "h2": arm_randomization(counts, arm, permutation_draws),
        "participant_intervals": bootstrap(counts, arm, bootstrap_draws),
        "trained_difference_missing_bounds": [
            cells["MT"]["missing_bounds"][0]-cells["RT"]["missing_bounds"][1],
            cells["MT"]["missing_bounds"][1]-cells["RT"]["missing_bounds"][0]],
        "integrity_failure_slots": sum(r["status"] == "integrity_failure"
                                       for r in data["trials"]),
        "scientific_interpretation": "NONE: synthetic software check only",
        "independent_review": "NOT_COMPLETED"
    }


def synthetic_fixture():
    """Deterministic, obvious toy data, not a target-generation algorithm."""
    people = [{"id": f"P{i:03d}", "arm": "M" if i < 24 else "R"} for i in range(48)]
    rows = []
    for p in people:
        for i in range(16):
            figure = i//2+1
            rows.append({
                "participant_id": p["id"], "trial_index": i,
                "person_id": f"F{figure:02d}", "familiarity": "T" if i < 8 else "U",
                "choice": 0 if i % 4 == 0 else 1, "target": 0,
                "status": "observed",
                "target_committed_at": 0, "response_locked_at": i+1,
                "target_opened_at": 100
            })
    return {"data_kind": "SYNTHETIC", "study_version": "0.1",
            "participants": people, "trials": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--planning", action="store_true")
    action.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    print(json.dumps(planning() if args.planning else analyze_synthetic(synthetic_fixture()),
                     indent=2))

