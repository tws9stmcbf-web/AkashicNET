#!/usr/bin/env python3
"""Simple N-of-1 analysis: compare baseline vs intervention means.

Usage: python analysis.py path/to/n-of-1-example.csv
"""
import sys
import pandas as pd


def main(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    # assume first 7 rows baseline, next 7 intervention for this example
    baseline = df.iloc[:7]
    intervention = df.iloc[7:14]

    def summarize(name, series):
        return {
            "n": int(series.count()),
            "mean": float(series.mean()),
            "sd": float(series.std()),
        }

    ba = summarize("baseline_alertness", baseline["morning_alertness_rating"])
    ia = summarize("interv_alertness", intervention["morning_alertness_rating"])

    print("Baseline (first 7 days):", ba)
    print("Intervention (next 7 days):", ia)
    diff = ia["mean"] - ba["mean"]
    print(f"Mean difference (intervention - baseline): {diff:.3f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analysis.py data/n-of-1-example.csv")
        sys.exit(1)
    main(sys.argv[1])
