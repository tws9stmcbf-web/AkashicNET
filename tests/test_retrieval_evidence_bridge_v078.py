import importlib.util
from pathlib import Path


def test_retrieval_evidence_bridge_executes():
    path = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_retrieval_evidence_bridge_v078.py'
    spec = importlib.util.spec_from_file_location('validate_retrieval_evidence_bridge_v078', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
