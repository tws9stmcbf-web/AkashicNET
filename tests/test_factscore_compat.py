"""Offline checks. Optional installed-package checks run when factscore is present."""
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from factscore_compat import ModelConfig, generate, require_tokenizer
from prepare_factscore_compat import prepare, HASHES


class CompatTests(unittest.TestCase):
    def test_explicit_models_and_endpoint_required(self):
        with patch.dict(os.environ, {}, clear=True):
            for role in ("ChatGPT", "InstructGPT", "unknown"):
                with self.assertRaises(ValueError):
                    ModelConfig.from_role(role)
            os.environ["FACTSCORE_VERIFY_MODEL"] = "verify-test"
            self.assertEqual(ModelConfig.from_role("ChatGPT"), ModelConfig("verify-test", "chat"))
            os.environ["FACTSCORE_ATOMIC_MODEL"] = "atomic-test"
            for endpoint in ("", "responses"):
                os.environ["FACTSCORE_ATOMIC_ENDPOINT"] = endpoint
                with self.assertRaises(ValueError):
                    ModelConfig.from_role("InstructGPT")
            os.environ["FACTSCORE_ATOMIC_ENDPOINT"] = "chat"
            self.assertEqual(ModelConfig.from_role("InstructGPT"), ModelConfig("atomic-test", "chat"))

    def test_cache_separates_model_and_endpoint(self):
        configs = [ModelConfig("a", "chat"), ModelConfig("b", "chat"), ModelConfig("a", "completion")]
        paths = {c.cache_path("legacy.pkl") for c in configs}
        self.assertEqual(len(paths), 3)
        self.assertNotIn("legacy.pkl", paths)
        self.assertEqual(configs[0].cache_path("legacy.pkl"), configs[0].cache_path("legacy.pkl"))

    def test_chat_and_completion_payload_and_text(self):
        api = types.SimpleNamespace(ChatCompletion=Mock(), Completion=Mock())
        api.ChatCompletion.create.return_value = {"choices": [{"message": {"content": "chat answer"}}]}
        api.Completion.create.return_value = {"choices": [{"text": "completion answer"}]}
        with patch.dict(sys.modules, {"openai": api}):
            for endpoint in ("chat", "completion"):
                answer, _ = generate(ModelConfig("selected-model", endpoint), "public synthetic prompt", 37, 0.7)
                self.assertEqual(answer, endpoint + " answer")
            api.ChatCompletion.create.assert_called_once_with(model="selected-model", messages=[{"role": "user", "content": "public synthetic prompt"}], max_tokens=37, temperature=0.7)
            api.Completion.create.assert_called_once_with(model="selected-model", prompt="public synthetic prompt", max_tokens=37, temperature=0.7)

    def test_api_error_propagates_once_without_fallback(self):
        api = types.SimpleNamespace(ChatCompletion=Mock(), Completion=Mock())
        api.ChatCompletion.create.side_effect = RuntimeError("unsupported parameter")
        with patch.dict(sys.modules, {"openai": api}), self.assertRaises(RuntimeError):
            generate(ModelConfig("test-model", "chat"), "synthetic", 1, 0.7)
        api.ChatCompletion.create.assert_called_once()
        api.Completion.create.assert_not_called()

    def test_empty_response_rejected(self):
        api = types.SimpleNamespace(ChatCompletion=Mock())
        api.ChatCompletion.create.return_value = {"choices": [{"message": {"content": None}}]}
        with patch.dict(sys.modules, {"openai": api}), self.assertRaises(ValueError):
            generate(ModelConfig("test-model", "chat"), "synthetic", 1, 0.7)

    def test_tokenizer_missing_and_preprovisioned(self):
        tokenize = types.SimpleNamespace(sent_tokenize=Mock(side_effect=LookupError("punkt_tab")))
        with patch.dict(sys.modules, {"nltk.tokenize": tokenize}):
            with self.assertRaisesRegex(RuntimeError, "Pre-provision"):
                require_tokenizer()
            tokenize.sent_tokenize.side_effect = None
            tokenize.sent_tokenize.return_value = ["Tokenizer readiness probe."]
            require_tokenizer()

    def test_unreviewed_source_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in HASHES:
                (root / name).write_text("changed upstream")
            dist = types.SimpleNamespace(version="0.2.0", locate_file=lambda _: root)
            with patch("prepare_factscore_compat.importlib.metadata.distribution", return_value=dist):
                with self.assertRaisesRegex(ValueError, "Unreviewed"):
                    prepare(root / "output")
            self.assertFalse((root / "output").exists())

    def test_wrong_version_rejected(self):
        with patch("prepare_factscore_compat.importlib.metadata.distribution", return_value=types.SimpleNamespace(version="0.3.0")):
            with self.assertRaisesRegex(ValueError, "0.2.0"):
                prepare("unused")


try:
    INSTALLED = importlib.metadata.version("factscore") == "0.2.0"
except importlib.metadata.PackageNotFoundError:
    INSTALLED = False


@unittest.skipUnless(INSTALLED, "Optional factscore 0.2.0 environment not installed")
class InstalledOverlayTests(unittest.TestCase):
    def test_real_overlay_import_dispatch_and_tokenizer_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            overlay = prepare(Path(tmp) / "overlay")
            with self.assertRaises(ValueError):
                prepare(overlay)
            code = r'''
import os, socket, tempfile
from pathlib import Path
from unittest.mock import Mock, patch
def forbidden(*args, **kwargs):
    raise AssertionError("Network/download forbidden during offline test")
socket.socket.connect = forbidden
socket.create_connection = forbidden
import nltk
nltk.download = forbidden
from factscore.factscorer import FactScorer
from factscore.atomic_facts import AtomicFactGenerator
from factscore.openai_lm import OpenAIModel
from factscore.akashicnet_compat import require_tokenizer
assert 'overlay' in __import__('factscore').__file__
with tempfile.TemporaryDirectory() as tmp:
    nltk.data.path[:] = [tmp]
    # Construction must fail before reading demos, keys, or loading spaCy.
    try:
        AtomicFactGenerator('missing.key', 'missing-demos')
    except RuntimeError as exc:
        assert 'Pre-provision' in str(exc)
    else:
        raise AssertionError('Missing tokenizer accepted')
    # Synthetic tab data exercises the installed NLTK loader, not language accuracy.
    if hasattr(nltk.tokenize, '_get_punkt_tokenizer'):
        nltk.tokenize._get_punkt_tokenizer.cache_clear()
    from nltk.tokenize.punkt import PunktParameters, save_punkt_params
    data = Path(tmp) / 'tokenizers/punkt_tab/english'
    data.mkdir(parents=True)
    save_punkt_params(PunktParameters(), dir=str(data))
    require_tokenizer()
    os.environ.update(FACTSCORE_VERIFY_MODEL='offline-verify', FACTSCORE_ATOMIC_MODEL='offline-atomic', FACTSCORE_ATOMIC_ENDPOINT='chat')
    import openai
    with patch.object(openai.ChatCompletion, 'create', return_value={'choices': [{'message': {'content': 'synthetic result'}}]}) as request:
        for role in ('ChatGPT', 'InstructGPT'):
            lm = OpenAIModel(role, cache_file=str(Path(tmp) / role))
            # Exercise actual dispatch without loading any credential.
            assert lm._generate('synthetic', max_output_length=11)[0] == 'synthetic result'
            assert request.call_args.kwargs['model'] == ('offline-verify' if role == 'ChatGPT' else 'offline-atomic')
            assert request.call_args.kwargs['max_tokens'] == (2048 if role == 'ChatGPT' else 512)
    with patch('logging.warning') as warning:
        FactScorer.print_cost_estimates(None, 100, 'test', 'davinci-003')
        assert 'unavailable' in warning.call_args.args[0]
print('Real overlay offline checks passed')
'''
            env = {**os.environ, "PYTHONPATH": str(overlay), "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
            result = subprocess.run([sys.executable, "-c", code], env=env, cwd=tmp, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
