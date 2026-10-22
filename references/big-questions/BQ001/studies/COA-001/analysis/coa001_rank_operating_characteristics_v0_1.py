#!/usr/bin/env python3
"""Exact operating characteristics for COA-001 SAP-001 v0.1.

No participant data are used. The program enumerates the distribution of the
sum of six-candidate normalized rank utilities. It evaluates a conservative
non-randomized upper-tail test at one-sided alpha 0.025 under two stylized
alternative families.

Rank utility is U = y / 5, where y is 5 for best rank and 0 for worst rank.
Under exchangeability y is discrete uniform on {0,1,2,3,4,5}.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Iterable


ALPHA = 0.025
MAX_N = 600
DELTAS = (0.05, 0.075, 0.10, 0.15)
POWERS = (0.80, 0.90)


@dataclass(frozen=True)
class Result:
    n: int
    achieved_power: float
    achieved_alpha: float
    critical_sum: int


def convolve(distribution: list[float], probabilities: Iterable[float]) -> list[float]:
    probabilities = list(probabilities)
    output = [0.0] * (len(distribution) + 5)
    for total, mass in enumerate(distribution):
        if mass == 0.0:
            continue
        for score, probability in enumerate(probabilities):
            output[total + score] += mass * probability
    return output


def upper_tail(distribution: list[float], threshold: int) -> float:
    return sum(distribution[threshold:])


def critical_value(null_distribution: list[float]) -> tuple[int, float]:
    for threshold in range(len(null_distribution)):
        tail = upper_tail(null_distribution, threshold)
        if tail <= ALPHA:
            return threshold, tail
    return len(null_distribution), 0.0


def sparse_top_rank(delta: float) -> list[float]:
    """A fraction 2*delta has best rank; the remainder is exchangeable."""
    signal_fraction = 2.0 * delta
    probabilities = [(1.0 - signal_fraction) / 6.0] * 6
    probabilities[5] += signal_fraction
    return probabilities


def mean_score(probabilities: Iterable[float]) -> float:
    return sum(score * probability for score, probability in enumerate(probabilities))


def soft_rank_shift(delta: float) -> list[float]:
    """Exponential tilt calibrated so E[U] = 0.5 + delta."""
    target_mean_score = 2.5 + 5.0 * delta
    low, high = 0.0, 3.0
    for _ in range(80):
        theta = (low + high) / 2.0
        weights = [exp(theta * score) for score in range(6)]
        normalizer = sum(weights)
        probabilities = [weight / normalizer for weight in weights]
        if mean_score(probabilities) < target_mean_score:
            low = theta
        else:
            high = theta
    theta = (low + high) / 2.0
    weights = [exp(theta * score) for score in range(6)]
    normalizer = sum(weights)
    return [weight / normalizer for weight in weights]


def minimum_sample_sizes(alternative_factory) -> dict[float, dict[float, Result]]:
    null_probabilities = [1.0 / 6.0] * 6
    null_distribution = [1.0]
    alternative_distributions = {delta: [1.0] for delta in DELTAS}
    results: dict[float, dict[float, Result]] = {delta: {} for delta in DELTAS}

    for n in range(1, MAX_N + 1):
        null_distribution = convolve(null_distribution, null_probabilities)
        for delta in DELTAS:
            alternative_distributions[delta] = convolve(
                alternative_distributions[delta], alternative_factory(delta)
            )

        threshold, achieved_alpha = critical_value(null_distribution)
        for delta in DELTAS:
            achieved_power = upper_tail(alternative_distributions[delta], threshold)
            for target_power in POWERS:
                if target_power not in results[delta] and achieved_power >= target_power:
                    results[delta][target_power] = Result(
                        n=n,
                        achieved_power=achieved_power,
                        achieved_alpha=achieved_alpha,
                        critical_sum=threshold,
                    )
    return results


def main() -> None:
    families = {
        "sparse_top_rank": sparse_top_rank,
        "soft_rank_shift": soft_rank_shift,
    }
    print("family,delta,target_power,n,achieved_power,achieved_alpha,critical_sum")
    for family_name, factory in families.items():
        results = minimum_sample_sizes(factory)
        for delta in DELTAS:
            for target_power in POWERS:
                result = results[delta][target_power]
                print(
                    f"{family_name},{delta:.3f},{target_power:.2f},{result.n},"
                    f"{result.achieved_power:.9f},{result.achieved_alpha:.9f},"
                    f"{result.critical_sum}"
                )


if __name__ == "__main__":
    main()
