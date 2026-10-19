"""Offline checks. Optional installed-package checks run when factscore is present."""
import importlib.metadata
import errno
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
from prepare_factscore_compat import prepare, publish_noreplace, HASHES


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


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        # Synthetic source exercises preparation without installing/importing upstream.
        fixtures = {
            'openai_lm.py': 'import logging\nclass LM:\n    def run(self, model_name, cache_file):\n        self.model_name = model_name\n        if self.model_name == "ChatGPT":\n            pass\n',
            'atomic_facts.py': 'import nltk\nnltk.download("punkt")\nclass Atomic:\n    def __init__(self):\n        self.nlp = spacy.load("test")\n',
            'factscorer.py': 'class Scorer:\n    def print_cost_estimates(self):\n        pass\n    def get_score(self):\n        pass\n',
        }
        import hashlib
        digests = {}
        for name, content in fixtures.items():
            (self.source / name).write_text(content)
            digests[name] = hashlib.sha256(content.encode()).hexdigest()
        self.original = {p.name: p.read_bytes() for p in self.source.iterdir()}
        dist = types.SimpleNamespace(version='0.2.0', locate_file=lambda _: self.source)
        for mocker in (patch('prepare_factscore_compat.importlib.metadata.distribution', return_value=dist),
                       patch('prepare_factscore_compat.HASHES', digests)):
            mocker.start()
            self.addCleanup(mocker.stop)
        self.destination = self.root / 'result'

    def assert_unpublished_and_clean(self):
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.root.iterdir()), [self.source])
        self.assertEqual({p.name: p.read_bytes() for p in self.source.iterdir()}, self.original)

    def test_partial_copy_failure_is_cleaned(self):
        def fail_copy(source, target, **kwargs):
            self.assertFalse(self.destination.exists())
            target.mkdir(parents=True)
            (target / 'atomic_facts.py').write_bytes(self.original['atomic_facts.py'])
            raise OSError('copy failed')
        with patch('prepare_factscore_compat.shutil.copytree', side_effect=fail_copy):
            with self.assertRaisesRegex(OSError, 'copy failed'):
                prepare(self.destination)
        self.assert_unpublished_and_clean()

    def test_each_write_failure_or_interrupt_is_cleaned(self):
        original_write = Path.write_bytes
        for name in (*HASHES, 'akashicnet_compat.py'):
            for error in (OSError('write failed'), KeyboardInterrupt()):
                with self.subTest(name=name, error=type(error).__name__):
                    def fail_write(path, data):
                        self.assertFalse(self.destination.exists())
                        if path.name == name:
                            original_write(path, data[:10])
                            raise error
                        return original_write(path, data)
                    with patch.object(Path, 'write_bytes', fail_write):
                        with self.assertRaises(type(error)):
                            prepare(self.destination)
                    self.assert_unpublished_and_clean()

    def test_silent_incomplete_write_rejected(self):
        original_write = Path.write_bytes
        def truncate(path, data):
            return original_write(path, data[:10] if path.name == 'atomic_facts.py' else data)
        with patch.object(Path, 'write_bytes', truncate):
            with self.assertRaisesRegex(ValueError, 'Incomplete transformed overlay'):
                prepare(self.destination)
        self.assert_unpublished_and_clean()

    def test_rename_failure_is_cleaned(self):
        with patch('prepare_factscore_compat.publish_noreplace', side_effect=OSError('rename failed')):
            with self.assertRaisesRegex(OSError, 'rename failed'):
                prepare(self.destination)
        self.assert_unpublished_and_clean()

    def test_success_visible_only_at_rename(self):
        original_rename = publish_noreplace
        def inspect(staged, destination):
            self.assertFalse(destination.exists())
            self.assertEqual(staged.parent.parent, destination.parent)
            target = staged / 'factscore'
            self.assertNotIn('nltk.download', (target / 'atomic_facts.py').read_text())
            self.assertIn('require_tokenizer()', (target / 'atomic_facts.py').read_text())
            for name in (*HASHES, 'akashicnet_compat.py'):
                compile((target / name).read_bytes(), name, 'exec')
            return original_rename(staged, destination)
        with patch('prepare_factscore_compat.publish_noreplace', side_effect=inspect):
            self.assertEqual(prepare(self.destination), self.destination)
        self.assertEqual(set(self.root.iterdir()), {self.source, self.destination})

    def test_concurrent_empty_destination_is_preserved(self):
        claimed = None
        def claim_then_publish(staged, destination):
            nonlocal claimed
            destination.mkdir()
            claimed = destination.stat()
            return publish_noreplace(staged, destination)
        with patch('prepare_factscore_compat.publish_noreplace', side_effect=claim_then_publish):
            with self.assertRaises(FileExistsError):
                prepare(self.destination)
        current = self.destination.stat()
        self.assertEqual((current.st_dev, current.st_ino), (claimed.st_dev, claimed.st_ino))
        self.assertEqual(list(self.destination.iterdir()), [])
        self.assertEqual(set(self.root.iterdir()), {self.source, self.destination})
        self.assertEqual({p.name: p.read_bytes() for p in self.source.iterdir()}, self.original)

    def test_unsupported_publication_is_cleaned_without_fallback(self):
        for failure in ('platform', 'libc', 'kernel'):
            with self.subTest(failure=failure):
                libc = types.SimpleNamespace()
                if failure == 'kernel':
                    libc.renameat2 = Mock(return_value=-1)
                with patch('prepare_factscore_compat.sys.platform', 'other' if failure == 'platform' else 'linux'), \
                     patch('prepare_factscore_compat.ctypes.CDLL', return_value=libc), \
                     patch('prepare_factscore_compat.ctypes.get_errno', return_value=errno.ENOSYS), \
                     patch.object(Path, 'rename') as unsafe_rename:
                    with self.assertRaises(OSError) as error:
                        prepare(self.destination)
                    self.assertEqual(error.exception.errno, errno.ENOSYS)
                    unsafe_rename.assert_not_called()
                self.assert_unpublished_and_clean()

    def test_existing_destination_rejected_without_changes(self):
        for kind in ('directory', 'file', 'dangling_symlink'):
            with self.subTest(kind=kind):
                if kind == 'directory':
                    self.destination.mkdir()
                elif kind == 'file':
                    self.destination.write_text('keep')
                else:
                    self.destination.symlink_to(self.root / 'missing')
                with patch('prepare_factscore_compat.shutil.copytree') as copy:
                    with self.assertRaisesRegex(ValueError, 'new overlay directory'):
                        prepare(self.destination)
                    copy.assert_not_called()
                if kind == 'directory':
                    self.assertEqual(list(self.destination.iterdir()), [])
                    self.destination.rmdir()
                else:
                    if kind == 'file':
                        self.assertEqual(self.destination.read_text(), 'keep')
                    else:
                        self.assertTrue(self.destination.is_symlink())
                    self.destination.unlink()
                self.assert_unpublished_and_clean()


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

