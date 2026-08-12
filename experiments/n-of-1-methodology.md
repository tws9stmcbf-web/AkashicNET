# N-of-1 Methodology Guidance

This document provides practical guidance for designing, running and analysing N-of-1 (single-participant) experiments for the Noetic Sciences Toolkit.

## Recommended designs

- AB (baseline → intervention)
- ABAB / withdrawal designs when ethically and practically feasible
- Multiple-baseline designs across behaviours or contexts
- Randomised block or alternating schedules (when blinding/randomisation is possible)

Choose a design that balances participant burden, safety and the ability to detect within-person change.

## Measurement and baseline

- Record a baseline long enough to establish stability (common default: 7–14 days; adapt to outcome variability).
- Define measurement frequency (daily, multiple times per day) and keep it consistent.
- Use validated measures where available; if using self-report, include clear instructions and anchors.

## Analysis recommendations

- Visual inspection of time-series plots is the first step.
- Consider time-series / interrupted-time-series methods (ARIMA, segmented regression) or GLS to account for autocorrelation.
- For pooled inference across multiple N-of-1s, use mixed-effects models with participant-level random effects.
- Report effect sizes with confidence intervals, and include temporal plots and raw data tables.

## Handling autocorrelation and missing data

- Check and report autocorrelation (e.g., ACF/PACF plots) and adjust models accordingly.
- Pre-specify rules for missing data (exclude, interpolate, or model-based imputation) and document them in the protocol.

## Data schema example

Store observations under `data/experiments/<id>/` with a `README.md` and `data-dictionary.yaml`.

Example CSV columns (timestamped rows):

- `timestamp` (ISO 8601)
- `measure_name` (e.g., mood_rating)
- `value` (numeric or categorical)
- `unit` (if applicable)
- `context` (optional tag describing context)
- `participant_id` (pseudonymised id)

## Reporting and reproducibility

- Include analysis code in a repository with a commit hash or release tag.
- Provide `requirements.txt` / `environment.yml` or a `Dockerfile` for reproducibility.
- Share anonymised or aggregated data where ethics permit and cite a DOI for the dataset when possible.

## Example preregistration frontmatter (for N-of-1)

---
id: experiment-2026-001
title: Example N-of-1: sleep intervention
authors:
  - Name (participant/researcher)
year: 2026
status: exploratory
preregistered: true
preregistration_uri: https://example.org/prereg/12345
primary_outcome: sleep_duration_minutes
primary_timepoint: daily morning
analysis_plan: segmented regression with AR(1) errors; code: https://github.com/.../commit/abcd1234
data_path: data/experiments/experiment-2026-001/
---

Include this example in the protocol template as a copyable example.
