"""Optional two-dimensional real quantum-probability illustration, not a fitted model."""
import argparse
import json
import math


def joint(state, first, second):
    # Rank-one yes/no projectors: ||P_second P_first psi||^2.
    return [[math.cos(state - (first + i * math.pi / 2)) ** 2 *
             math.cos((first + i * math.pi / 2) - (second + j * math.pi / 2)) ** 2
             for j in range(2)] for i in range(2)]


def compare(state_degrees, a_degrees, b_degrees):
    if any(not math.isfinite(x) for x in (state_degrees, a_degrees, b_degrees)):
        raise ValueError("angles must be finite")
    state, a, b = map(math.radians, (state_degrees, a_degrees, b_degrees))
    ab = joint(state, a, b)
    raw_ba = joint(state, b, a)
    ba = [[raw_ba[j][i] for j in range(2)] for i in range(2)]
    return {"model": "illustrative_2d_projective_quantum_probability",
            "empirically_validated": False, "physical_quantum_claim": False,
            "axes": "Both tables: rows A yes/no; columns B yes/no",
            "AB": ab, "BA_aligned": ba,
            "total_variation": sum(abs(ab[i][j]-ba[i][j]) for i in range(2) for j in range(2))/2,
            "qq_residual": ab[0][1]+ab[1][0]-ba[0][1]-ba[1][0],
            "limitation": "Synthetic angles; no fitted data or classical comparator. Order effects alone do not establish a quantum mechanism."}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", type=float, default=0)
    p.add_argument("--a", type=float, default=0)
    p.add_argument("--b", type=float, default=45)
    args = p.parse_args()
    try:
        result = compare(args.state, args.a, args.b)
    except ValueError as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))
