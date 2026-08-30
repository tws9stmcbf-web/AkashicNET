import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_bq001_scientific_baseline_batch1.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("bq001_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bq001_scientific_baseline_batch1_passes():
    assert load_validator().main() == 0
