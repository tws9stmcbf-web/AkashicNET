# Example N-of-1 Reproducible Scaffold

This folder demonstrates a minimal reproducible scaffold for an illustrative N-of-1 experiment based on `experiments/mappings/example-hieratic-001.md`.

Contents

- `data/n-of-1-example.csv`: small synthetic dataset (timestamped daily records)
- `analysis/analysis.py`: simple analysis script that computes baseline vs intervention summaries
- `requirements.txt`: Python dependencies for the analysis

How to run

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the analysis script:

```bash
python analysis/analysis.py data/n-of-1-example.csv
```

This scaffold is intentionally minimal. For full reproducibility include a `Dockerfile` or `environment.yml`, a notebook with plots, and a `data-dictionary.yaml` as described in `experiments/n-of-1-methodology.md`.
