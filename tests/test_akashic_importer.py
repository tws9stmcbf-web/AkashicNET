import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools/akashic-library" / "drive_importer.py"

spec = importlib.util.spec_from_file_location("akashic_importer_module", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AkashicImporterLocalMockTests(unittest.TestCase):
    def test_mock_dataset_traversal_and_index_generation(self):
        mock_data = {
            "root": {
                "id": "root",
                "name": "Books",
                "kind": "drive#file",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [],
                "modifiedTime": "2024-01-10T12:00:00Z",
                "owners": [{"displayName": "Archive Owner"}],
            },
            "children": {
                "root": [
                    {
                        "id": "folder_1",
                        "name": "Philosophy",
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": ["root"],
                        "modifiedTime": "2024-01-11T12:00:00Z",
                    },
                    {
                        "id": "file_1",
                        "name": "Intro to Consciousness.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["root"],
                        "size": "153200",
                        "modifiedTime": "2024-01-12T12:30:00Z",
                        "owners": [{"displayName": "Archive Owner"}],
                    },
                ],
                "folder_1": [
                    {
                        "id": "file_2",
                        "name": "Consciousness Essay.pdf",
                        "mimeType": "application/pdf",
                        "parents": ["folder_1"],
                        "size": "245000",
                        "modifiedTime": "2024-01-13T13:00:00Z",
                        "owners": [{"displayName": "Archive Curator"}],
                    }
                ],
            },
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            local_path = os.path.join(tmpdir, "mock_drive.json")
            with open(local_path, "w", encoding="utf-8") as handle:
                json.dump(mock_data, handle)

            session = module.DriveImportSession(
                root_folder_id="root",
                auth_mode="mock",
                mock_data_path=local_path,
                batch_size=10,
                dry_run=True,
                checkpoint_path=os.path.join(tmpdir, "checkpoint.json"),
                audit_log_path=os.path.join(tmpdir, "audit.jsonl"),
                error_log_path=os.path.join(tmpdir, "errors.jsonl"),
                output_csv_path=os.path.join(tmpdir, "index.csv"),
                output_md_path=os.path.join(tmpdir, "index.md"),
            )

            result = session.run()
            self.assertEqual(result["discovered_count"], 3)
            self.assertEqual(result["index_only_count"], 3)
            self.assertTrue(os.path.exists(result["output_csv"]))
            self.assertTrue(os.path.exists(result["output_md"]))
            self.assertTrue(any("Consciousness" in line for line in open(result["output_csv"], encoding="utf-8")))


class AkashicImporterRemoteOAuthTests(unittest.TestCase):
    def _make_client_secret(self, tmpdir):
        path = os.path.join(tmpdir, "client_secrets.json")
        payload = {
            "installed": {
                "client_id": "test-client-id",
                "client_secret": "test-client-secret",
                "redirect_uris": ["http://localhost"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        return path

    def test_build_codespaces_redirect_uri_uses_codespace_port_when_port_missing(self):
        with patch.dict(os.environ, {
            "CODESPACE_NAME": "example-space",
            "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN": "app.github.dev",
            "PORT": "8128",
        }, clear=False):
            redirect_uri = module.build_codespaces_redirect_uri(0)
        self.assertEqual(redirect_uri, "https://8128-example-space.app.github.dev/")

    def test_remote_oauth_state_preserved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            client_path = self._make_client_secret(tmpdir)
            token_path = os.path.join(tmpdir, "token.json")

            class FakeFlow:
                def __init__(self):
                    self.redirect_uri = None
                    self.credentials = None

                def authorization_url(self, **kwargs):
                    return "https://example.com/auth?state=abc123", "abc123"

            with patch.object(module.Flow, "from_client_config", return_value=FakeFlow()):
                session = module.RemoteCodespacesOAuthSession(client_path, token_path, module.SCOPES)
                auth_url, state, redirect_uri = session.build_authorization_url(port=8128)

            parsed = urlparse(auth_url)
            params = parse_qs(parsed.query)
            self.assertIn("state", params)
            self.assertEqual(params["state"][0], state)
            self.assertIn("8128", redirect_uri)
            self.assertIn("state=" + state, auth_url)

    def test_remote_oauth_callback_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            client_path = self._make_client_secret(tmpdir)
            token_path = os.path.join(tmpdir, "token.json")

            class FakeFlow:
                def __init__(self):
                    self.redirect_uri = None
                    self.credentials = type('Creds', (), {"to_json": lambda self: json.dumps({"access_token": "abc", "refresh_token": "def", "token_uri": "https://oauth2.googleapis.com/token", "expiry": "2026-01-01T00:00:00Z"})})()
                    self._state = "abc123"

                def authorization_url(self, **kwargs):
                    return "https://example.com/auth?state=abc123", "abc123"

                def fetch_token(self, **kwargs):
                    return {"access_token": "abc"}

            with patch.object(module.Flow, "from_client_config", return_value=FakeFlow()):
                session = module.RemoteCodespacesOAuthSession(client_path, token_path, module.SCOPES)
                auth_url, state, redirect_uri = session.build_authorization_url(port=8128)
                result = session.consume_callback(f"{redirect_uri}?code=test-code&state={state}")

            self.assertTrue(result["token_written"])
            self.assertTrue(os.path.exists(token_path))
            payload = json.loads(open(token_path, "r", encoding="utf-8").read())
            self.assertIn("access_token", payload)
            self.assertIn("refresh_token", payload)

    def test_remote_oauth_prefers_web_client_config_for_codespaces(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            client_path = os.path.join(tmpdir, "client_secrets.json")
            payload = {
                "installed": {
                    "client_id": "desktop-client",
                    "client_secret": "desktop-secret",
                    "redirect_uris": ["http://localhost"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                },
                "web": {
                    "client_id": "web-client",
                    "client_secret": "web-secret",
                    "redirect_uris": ["https://8128-example-space.app.github.dev/"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                },
            }
            with open(client_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)

            class FakeFlow:
                def __init__(self):
                    self.redirect_uri = None
                    self.credentials = None

                def authorization_url(self, **kwargs):
                    return "https://example.com/auth?state=abc123", "abc123"

            with patch.object(module.Flow, "from_client_config", return_value=FakeFlow()) as mock_from_config:
                module.RemoteCodespacesOAuthSession(client_path, os.path.join(tmpdir, "token.json"), module.SCOPES)

            selected = mock_from_config.call_args[0][0]
            self.assertIn("web", selected)
            self.assertNotIn("installed", selected)
            self.assertEqual(selected["web"]["client_id"], "web-client")

    def test_remote_oauth_callback_state_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            client_path = self._make_client_secret(tmpdir)
            token_path = os.path.join(tmpdir, "token.json")

            class FakeFlow:
                def __init__(self):
                    self.redirect_uri = None
                    self.credentials = None

                def authorization_url(self, **kwargs):
                    return "https://example.com/auth?state=abc123", "abc123"

            with patch.object(module.Flow, "from_client_config", return_value=FakeFlow()):
                session = module.RemoteCodespacesOAuthSession(client_path, token_path, module.SCOPES)
                auth_url, state, redirect_uri = session.build_authorization_url(port=8128)

                with self.assertRaises(ValueError):
                    session.consume_callback(f"{redirect_uri}?code=test-code&state=wrong-state")

    def test_remote_oauth_token_file_write_does_not_print_contents(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            client_path = self._make_client_secret(tmpdir)
            token_path = os.path.join(tmpdir, "token.json")

            class FakeFlow:
                def __init__(self):
                    self.redirect_uri = None
                    self.credentials = None

                def authorization_url(self, **kwargs):
                    return "https://example.com/auth?state=abc123", "abc123"

            with patch.object(module.Flow, "from_client_config", return_value=FakeFlow()):
                session = module.RemoteCodespacesOAuthSession(client_path, token_path, module.SCOPES)
                with patch("builtins.print") as mock_print:
                    session.write_token_file({"access_token": "very-secret-token", "refresh_token": "very-secret-refresh", "token_uri": "https://oauth2.googleapis.com/token", "expiry": "2026-01-01T00:00:00Z"})
                self.assertFalse(mock_print.called)
                self.assertTrue(os.path.exists(token_path))


if __name__ == "__main__":
    unittest.main()
