#!/usr/bin/env python3
"""Akashic Library batch importer scaffold.

This tool is designed for resumable, rights-safe processing of a public Google
Drive archive. It keeps the archive in a provenance-first mode and never claims
full import validation when the public metadata does not expose sufficient
licence or item-level detail.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

try:  # pragma: no cover - optional dependency
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow, InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except Exception:  # pragma: no cover
    Request = None
    service_account = None
    Credentials = None
    Flow = None
    InstalledAppFlow = None
    build = None
    HttpError = None

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from audit import AuditLogger
    from checkpoint import CheckpointStore
    from classifiers import classify_licence_status, classify_reuse_decision, classify_source_type, classify_subject
    from models import CheckpointState
else:
    from .audit import AuditLogger
    from .checkpoint import CheckpointStore
    from .classifiers import classify_licence_status, classify_reuse_decision, classify_source_type, classify_subject
    from .models import CheckpointState

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


def paginate_items(items: List[Dict[str, Any]], page_size: int) -> List[List[Dict[str, Any]]]:
    if page_size <= 0:
        return [items]
    return [items[index : index + page_size] for index in range(0, len(items), page_size)]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_runtime_auth_paths() -> Tuple[str, str]:
    home_dir = Path.home()
    config_dir = home_dir / ".config" / "akashic"
    token_file = str(config_dir / "drive-token.json")
    credentials_candidates: List[str] = []

    env_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.environ.get("AKASHIC_DRIVE_CLIENT_SECRETS_JSON")
    if env_credentials:
        credentials_candidates.append(env_credentials)

    if config_dir.exists():
        for item in sorted(config_dir.iterdir()):
            if item.is_file() and item.suffix.lower() == ".json" and item.name != "drive-token.json":
                credentials_candidates.append(str(item))

    if not credentials_candidates:
        return "", token_file

    for candidate in credentials_candidates:
        try:
            if os.path.isfile(candidate):
                return candidate, token_file
        except OSError:
            continue

    return credentials_candidates[0], token_file


def select_oauth_client_config(client_config: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(client_config, dict):
        return client_config
    if "web" in client_config:
        return {"web": client_config["web"]}
    if "installed" in client_config:
        return {"installed": client_config["installed"]}
    return client_config


def build_codespaces_redirect_uri(port: int, base_domain: Optional[str] = None) -> str:
    codespace_name = os.environ.get("CODESPACE_NAME")
    domain = base_domain or os.environ.get("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN") or "app.github.dev"
    forwarded_port = int(port or os.environ.get("PORT") or 0)
    if codespace_name and forwarded_port:
        return f"https://{forwarded_port}-{codespace_name}.{domain}/"
    if codespace_name:
        return f"https://{codespace_name}.{domain}/"
    if forwarded_port:
        return f"http://localhost:{forwarded_port}/"
    return "http://localhost:8080/"


class RemoteCodespacesOAuthSession:
    """Minimal OAuth flow for remote GitHub Codespaces browser callbacks.

    This keeps the normal local `run_local_server()` behavior unchanged while adding
    an explicit remote/Codespaces path that preserves the OAuth state and completes
    the authorization code exchange in the same flow/session.
    """

    def __init__(self, client_secrets_path: str, token_file: Optional[str], scopes: Iterable[str], callback_port: Optional[int] = None):
        self.client_secrets_path = client_secrets_path
        self.token_file = token_file or str(Path.home() / ".config" / "akashic" / "drive-token.json")
        self.scopes = list(scopes)
        self.callback_port = callback_port
        self.flow = None
        self.state = None
        self.redirect_uri = None
        self._load_flow()

    def _load_flow(self) -> None:
        if Flow is None:
            raise RuntimeError("google-auth-oauthlib is not installed.")
        with open(self.client_secrets_path, "r", encoding="utf-8") as handle:
            client_config = json.load(handle)

        self.flow = Flow.from_client_config(select_oauth_client_config(client_config), self.scopes)

    def build_authorization_url(self, port: Optional[int] = None) -> Tuple[str, str, str]:
        target_port = int(port or self.callback_port or os.environ.get("PORT") or 0)
        self.redirect_uri = build_codespaces_redirect_uri(target_port)
        self.flow.redirect_uri = self.redirect_uri
        auth_url, self.state = self.flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return auth_url, self.state, self.redirect_uri

    def consume_callback(self, callback_url: str) -> Dict[str, Any]:
        if not callback_url:
            raise ValueError("OAuth callback URL is required.")
        parsed = __import__("urllib.parse").parse.urlsplit(callback_url)
        query = __import__("urllib.parse").parse.parse_qs(parsed.query)
        received_state = query.get("state", [None])[0]
        code = query.get("code", [None])[0]
        if query.get("error"):
            raise ValueError("OAuth callback returned an error.")
        if not received_state:
            raise ValueError("OAuth callback did not include a state.")
        if not self.state:
            raise ValueError("OAuth authorization state was not initialized.")
        if received_state != self.state:
            raise ValueError("OAuth state mismatch: callback state did not match the authenticated request.")
        if not code:
            raise ValueError("OAuth callback did not include a code.")
        self.flow.fetch_token(code=code, redirect_uri=self.redirect_uri)
        credentials = getattr(self.flow, "credentials", None)
        payload = credentials.to_json() if credentials is not None else {}
        self.write_token_file(payload)
        return {"token_written": True, "token_path": self.token_file}

    def write_token_file(self, token_payload: Any) -> None:
        token_path = Path(self.token_file)
        token_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(token_payload, dict):
            token_contents = token_payload
        elif isinstance(token_payload, str):
            token_contents = json.loads(token_payload)
        else:
            raise TypeError("Token payload must be a dict or JSON string.")

        token_path.write_text(json.dumps(token_contents, ensure_ascii=True, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    default_credentials, default_token = resolve_runtime_auth_paths()
    parser = argparse.ArgumentParser(description="Akashic Library batch importer")
    parser.add_argument("--source-url", default="https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ", help="Canonical source URL for the archive.")
    parser.add_argument("--root-folder-id", default=os.environ.get("AKASHIC_DRIVE_FOLDER_ID", ""), help="Google Drive folder ID to traverse. Required for authenticated API mode.")
    parser.add_argument("--auth-mode", choices=["mock", "service-account", "oauth", "oauth-remote"], default=os.environ.get("AKASHIC_AUTH_MODE", "mock"), help="Authentication mode for the Drive API.")
    parser.add_argument("--credentials-file", default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or default_credentials, help="Path to a service-account JSON file or OAuth client secrets file.")
    parser.add_argument("--token-file", default=os.environ.get("AKASHIC_DRIVE_TOKEN_FILE") or default_token, help="Path to the authorized OAuth token JSON file.")
    parser.add_argument("--items-csv", default="", help="Optional pre-discovered CSV of known items for a dry-run import or test run.")
    parser.add_argument("--batch-size", type=int, default=50, help="Maximum number of items processed in a batch.")
    parser.add_argument("--dry-run", action="store_true", help="Default safe mode: classify and log without copying any files.")
    parser.add_argument("--resume", action="store_true", help="Resume from the last checkpoint when available.")
    parser.add_argument("--checkpoint", default="tools/akashic-library/state/checkpoint.json", help="Checkpoint file for batch state.")
    parser.add_argument("--audit-log", default="tools/akashic-library/state/audit.jsonl", help="Append-only audit log for processing decisions.")
    parser.add_argument("--error-log", default="tools/akashic-library/state/errors.jsonl", help="Log file for failed or unavailable items.")
    parser.add_argument("--limit", type=int, default=0, help="Optional number of items to process in a dry-run subset.")
    parser.add_argument("--out-csv", default="references/akashic-library/AKASHIC_LIBRARY_INDEX.csv", help="Output CSV for the current discovered batch index.")
    parser.add_argument("--out-md", default="references/akashic-library/AKASHIC_LIBRARY_INDEX.md", help="Output Markdown index generated from the current discovered batch.")
    parser.add_argument("--mock-data-path", default="", help="Local JSON mock dataset for testing without live Drive access.")
    parser.add_argument("--report", action="store_true", help="Print a dry-run summary without downloading or importing any collection files.")
    return parser.parse_args()


def read_mock_dataset(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Mock data file not found: {path}")
    with p.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload


class DriveImportSession:
    """Session for authenticated Drive enumeration with a mock fallback.

    This scaffold intentionally defaults to a dry-run, metadata-only model. It does
    not download the collection and keeps rights decisions conservative.
    """

    def __init__(
        self,
        root_folder_id: str,
        auth_mode: str = "mock",
        credentials_file: str = "",
        token_file: str = "",
        batch_size: int = 50,
        dry_run: bool = True,
        checkpoint_path: str = "tools/akashic-library/state/checkpoint.json",
        audit_log_path: str = "tools/akashic-library/state/audit.jsonl",
        error_log_path: str = "tools/akashic-library/state/errors.jsonl",
        output_csv_path: str = "references/akashic-library/AKASHIC_LIBRARY_INDEX.csv",
        output_md_path: str = "references/akashic-library/AKASHIC_LIBRARY_INDEX.md",
        source_url: str = "",
        mock_data_path: str = "",
        resume: bool = False,
        limit: int = 0,
    ) -> None:
        self.root_folder_id = root_folder_id
        self.auth_mode = auth_mode
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.batch_size = batch_size
        self.dry_run = dry_run
        self.source_url = source_url or "https://drive.google.com/drive/folders/"
        self.checkpoint_store = CheckpointStore(checkpoint_path)
        self.audit_logger = AuditLogger(audit_log_path)
        self.error_log_path = Path(error_log_path)
        self.output_csv_path = Path(output_csv_path)
        self.output_md_path = Path(output_md_path)
        self.resume = resume
        self.limit = limit
        self.service = None
        if mock_data_path:
            try:
                self.mock_data = read_mock_dataset(mock_data_path)
            except FileNotFoundError:
                if resume:
                    self.mock_data = {}
                else:
                    raise
        else:
            self.mock_data = {}
        self.seen_ids: set[str] = set()
        self.seen_signatures: set[str] = set()
        self.records: List[Dict[str, Any]] = []
        self.last_error: Optional[str] = None
        self._load_checkpoint_state()

    def _load_checkpoint_state(self) -> None:
        if not self.resume:
            return
        state = self.checkpoint_store.load()
        if state is not None:
            self.root_folder_id = state.last_folder_id or self.root_folder_id
            self.records = []
            self.seen_ids = set()
            self.seen_signatures = set()

    def _log_error(self, item_id: str, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        entry = {
            "timestamp_utc": utc_now(),
            "item_id": item_id,
            "message": message,
            "event": "error",
        }
        if extra:
            entry.update(extra)
        self.error_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.error_log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=True) + "\n")
        self.audit_logger.log_event(event="error", item_id=item_id, message=message, extra=json.dumps(extra or {}))

    def _handle_rate_limit(self, retry_after_seconds: Optional[int] = None) -> None:
        delay = retry_after_seconds or 2
        if delay > 0:
            time.sleep(delay)
        self.audit_logger.log_event(event="rate_limit_backoff", delay_seconds=delay, timestamp_utc=utc_now())

    def _safe_int(self, value: Any) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _normalise_item(self, item: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        title = str(item.get("name") or item.get("title") or "unknown").strip() or "unknown"
        drive_id = str(item.get("id") or "unknown")
        mime = str(item.get("mimeType") or "application/octet-stream")
        size = self._safe_int(item.get("size"))
        modified = str(item.get("modifiedTime") or "unknown")
        owners = item.get("owners") or []
        author = "unknown"
        if owners:
            author = str(owners[0].get("displayName") or owners[0].get("emailAddress") or "unknown")
        source_name = str(item.get("source_name") or author or "unknown")
        licence_note = str(item.get("description") or item.get("license") or item.get("licence_status") or "unknown").strip()
        licence_status = classify_licence_status(licence_note)
        if licence_status in {"unknown", "unclear"}:
            licence_status = "unknown"
        subject = classify_subject(title, folder_path)
        source_type = classify_source_type(title, mime)
        reuse_decision = classify_reuse_decision(licence_status, title)
        item_signature = hashlib.sha1(f"{title}|{folder_path}|{size or 0}|{modified}".encode("utf-8")).hexdigest()
        return {
            "drive_id": drive_id,
            "title": title,
            "parent_folder_id": str(item.get("parents", [""])[0] if item.get("parents") else "root"),
            "drive_path": folder_path,
            "file_type": "folder" if mime == "application/vnd.google-apps.folder" else "file",
            "mime_type": mime,
            "size_bytes": size,
            "modified_time": modified,
            "author": author,
            "source_name": source_name,
            "licence_status": licence_status,
            "reuse_decision": reuse_decision,
            "source_type": source_type,
            "subject_category": subject,
            "original_source_url": self.source_url,
            "drive_url": str(item.get("webViewLink") or f"https://drive.google.com/file/d/{drive_id}/view"),
            "provenance_status": "metadata_only",
            "notes": f"Google Drive item discovered via authenticated traversal. Licence value defaulted to {licence_status} unless explicit metadata stated otherwise.",
            "signature": item_signature,
        }

    def _get_service(self):
        if self.service is not None:
            return self.service
        if self.auth_mode == "mock":
            self.service = None
            return None
        if build is None:
            raise RuntimeError("The google-api-python-client package is not installed. Install it with `pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib`.")
        if self.auth_mode == "service-account":
            if not self.credentials_file:
                raise ValueError("Service-account mode requires GOOGLE_APPLICATION_CREDENTIALS or --credentials-file.")
            creds = service_account.Credentials.from_service_account_file(self.credentials_file, scopes=SCOPES)
            self.service = build("drive", "v3", credentials=creds, cache_discovery=False)
            return self.service
        if self.auth_mode == "oauth":
            if not self.credentials_file:
                raise ValueError("OAuth mode requires a client secret JSON file via --credentials-file or AKASHIC_DRIVE_CLIENT_SECRETS_JSON.")
            if self.token_file and os.path.exists(self.token_file):
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
                if creds and creds.valid:
                    self.service = build("drive", "v3", credentials=creds, cache_discovery=False)
                    return self.service
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    self.service = build("drive", "v3", credentials=creds, cache_discovery=False)
                    return self.service

            with open(self.credentials_file, "r", encoding="utf-8") as handle:
                client_config = select_oauth_client_config(json.load(handle))
            flow = Flow.from_client_config(client_config, SCOPES)
            if os.environ.get("CODESPACE_NAME"):
                flow.redirect_uri = build_codespaces_redirect_uri(int(os.environ.get("PORT") or 0))
            else:
                flow.redirect_uri = "http://localhost"
            creds = flow.run_local_server(port=0)
            if self.token_file:
                with open(self.token_file, "w", encoding="utf-8") as handle:
                    handle.write(creds.to_json())
            self.service = build("drive", "v3", credentials=creds, cache_discovery=False)
            return self.service
        raise ValueError(f"Unsupported auth mode: {self.auth_mode}")

    def _mock_children(self, parent_id: str) -> List[Dict[str, Any]]:
        if not self.mock_data:
            return []
        return list(self.mock_data.get("children", {}).get(parent_id, []))

    def _iter_drive_children(self, parent_id: str, current_path: str) -> Iterator[Dict[str, Any]]:
        if self.auth_mode == "mock":
            for item in self._mock_children(parent_id):
                yield item
            return
        service = self._get_service()
        query = f"'{parent_id}' in parents and trashed = false"
        page_token = None
        while True:
            try:
                response = service.files().list(
                    q=query,
                    pageSize=self.batch_size,
                    pageToken=page_token,
                    fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, owners, parents, webViewLink, description)",
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                ).execute()
            except HttpError as exc:  # pragma: no cover - network/auth path
                if exc.resp.status == 429:
                    retry_after = int(exc.headers.get("Retry-After", 2))
                    self._handle_rate_limit(retry_after)
                    continue
                self._log_error(parent_id, "Drive listing failed", {"error": str(exc)})
                break
            for item in response.get("files", []):
                yield item
            page_token = response.get("nextPageToken")
            if page_token is None:
                break

    def _walk_folder(self, folder_id: str, folder_path: str = "root") -> None:
        if self.limit and len(self.records) >= self.limit:
            return
        self.audit_logger.log_event(event="folder_visit", folder_id=folder_id, folder_path=folder_path)
        for item in self._iter_drive_children(folder_id, folder_path):
            if not isinstance(item, dict):
                self._log_error("unknown", "Encountered non-dictionary item in Drive listing", {"item": item})
                continue
            if item.get("available") is False:
                self._log_error(str(item.get("id") or "unknown"), "Drive file unavailable", {"detail": item})
                continue
            item_id = str(item.get("id") or "unknown")
            if not item_id or item_id in self.seen_ids:
                continue
            item_path = f"{folder_path}/{item.get('name', 'unknown')}" if folder_path != "root" else item.get("name", "unknown")
            record = self._normalise_item(item, item_path)
            self.seen_ids.add(item_id)
            signature = record["signature"]
            if signature in self.seen_signatures:
                self.audit_logger.log_event(event="duplicate_detected", drive_id=item_id, signature=signature)
                continue
            self.seen_signatures.add(signature)
            self.records.append(record)
            if self.limit and len(self.records) >= self.limit:
                break
            if item.get("mimeType") == "application/vnd.google-apps.folder":
                child_path = f"{item_path}"
                self._walk_folder(item_id, child_path)

    def _write_csv(self) -> str:
        self.output_csv_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "drive_id",
            "title",
            "parent_folder_id",
            "drive_path",
            "file_type",
            "mime_type",
            "size_bytes",
            "modified_time",
            "author",
            "source_name",
            "licence_status",
            "reuse_decision",
            "source_type",
            "subject_category",
            "original_source_url",
            "drive_url",
            "provenance_status",
            "notes",
            "signature",
        ]
        with self.output_csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.records:
                writer.writerow({field: row.get(field, "") for field in fieldnames})
        return str(self.output_csv_path)

    def _write_markdown(self) -> str:
        self.output_md_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Akashic Library index",
            "",
            "This index is generated by the authenticated Google Drive importer scaffold and remains metadata-only unless a licence or permissions evaluation explicitly approves import.",
            "",
            "| Title | Path | Type | MIME | Size | Modified | Author | Licence | Decision |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for row in self.records:
            title = row.get("title", "unknown")
            path = row.get("drive_path", "root")
            file_type = row.get("file_type", "unknown")
            mime_type = row.get("mime_type", "unknown")
            size = row.get("size_bytes")
            modified = row.get("modified_time", "unknown")
            author = row.get("author", "unknown")
            licence = row.get("licence_status", "unknown")
            decision = row.get("reuse_decision", "INDEX_ONLY")
            lines.append(f"| {title} | {path} | {file_type} | {mime_type} | {size if size is not None else 'unknown'} | {modified} | {author} | {licence} | {decision} |")
        self.output_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(self.output_md_path)

    def _write_checkpoint(self, processed_count: int, completed: bool = False) -> None:
        state = CheckpointState(
            run_id=f"akashic-import-{utc_now().replace(':', '').replace('-', '')}",
            source_url=self.source_url,
            last_folder_id=self.root_folder_id,
            batch_index=0,
            processed_count=processed_count,
            discovered_count=len(self.records),
            index_only_count=sum(1 for item in self.records if item["reuse_decision"] == "INDEX_ONLY"),
            link_plus_metadata_count=sum(1 for item in self.records if item["reuse_decision"] == "LINK_PLUS_METADATA"),
            import_count=sum(1 for item in self.records if item["reuse_decision"] == "IMPORT"),
            updated_at_utc=utc_now(),
            completed=completed,
        )
        self.checkpoint_store.save(state)

    def build_dry_run_summary(self) -> Dict[str, Any]:
        folders_discovered = sum(1 for item in self.records if item.get("file_type") == "folder")
        files_discovered = sum(1 for item in self.records if item.get("file_type") != "folder")
        files_eligible_for_import = sum(1 for item in self.records if item.get("reuse_decision") == "IMPORT")
        index_only_files = sum(1 for item in self.records if item.get("reuse_decision") == "INDEX_ONLY")
        licence_review_files = sum(1 for item in self.records if item.get("reuse_decision") == "LINK_PLUS_METADATA")
        errors = 0
        if self.error_log_path.exists():
            errors = sum(1 for line in self.error_log_path.read_text(encoding="utf-8").splitlines() if line.strip())
        return {
            "folders_discovered": folders_discovered,
            "files_discovered": files_discovered,
            "files_eligible_for_import": files_eligible_for_import,
            "index_only_files": index_only_files,
            "licence_review_files": licence_review_files,
            "errors": errors,
            "dry_run": True,
        }

    def run(self) -> Dict[str, Any]:
        if self.auth_mode == "mock" and not self.mock_data:
            raise ValueError("Mock mode requires --mock-data-path or a local mock dataset.")
        if self.auth_mode != "mock":
            try:
                self._get_service()
            except Exception as exc:  # pragma: no cover - runtime auth path
                self.last_error = str(exc)
                self._log_error(self.root_folder_id or "unknown", "Authentication setup failed", {"detail": str(exc)})
                raise

        self._walk_folder(self.root_folder_id, "root")
        if self.limit and self.limit > 0:
            self.records = self.records[: self.limit]

        csv_path = self._write_csv()
        md_path = self._write_markdown()
        self._write_checkpoint(len(self.records), completed=True)
        self.audit_logger.log_event(event="run_complete", count=len(self.records), dry_run=self.dry_run, root_folder_id=self.root_folder_id)

        summary = {
            "root_folder_id": self.root_folder_id,
            "source_url": self.source_url,
            "auth_mode": self.auth_mode,
            "dry_run": self.dry_run,
            "discovered_count": len(self.records),
            "folders_discovered": sum(1 for item in self.records if item.get("file_type") == "folder"),
            "files_discovered": sum(1 for item in self.records if item.get("file_type") != "folder"),
            "index_only_count": sum(1 for item in self.records if item["reuse_decision"] == "INDEX_ONLY"),
            "link_plus_metadata_count": sum(1 for item in self.records if item["reuse_decision"] == "LINK_PLUS_METADATA"),
            "import_count": sum(1 for item in self.records if item["reuse_decision"] == "IMPORT"),
            "files_eligible_for_import": sum(1 for item in self.records if item["reuse_decision"] == "IMPORT"),
            "index_only_files": sum(1 for item in self.records if item["reuse_decision"] == "INDEX_ONLY"),
            "licence_review_files": sum(1 for item in self.records if item["reuse_decision"] == "LINK_PLUS_METADATA"),
            "checkpoint": str(self.checkpoint_store.path),
            "output_csv": csv_path,
            "output_md": md_path,
            "status": "metadata-only dry run; no file copies performed",
        }
        if self.error_log_path.exists():
            summary["errors"] = sum(1 for line in self.error_log_path.read_text(encoding="utf-8").splitlines() if line.strip())
        return summary


def main() -> int:
    args = parse_args()
    session = DriveImportSession(
        root_folder_id=args.root_folder_id,
        auth_mode=args.auth_mode,
        credentials_file=args.credentials_file,
        token_file=args.token_file,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        checkpoint_path=args.checkpoint,
        audit_log_path=args.audit_log,
        error_log_path=args.error_log,
        output_csv_path=args.out_csv,
        output_md_path=args.out_md,
        source_url=args.source_url,
        mock_data_path=args.mock_data_path,
        resume=args.resume,
        limit=args.limit,
    )
    result = session.run()
    if args.report:
        print(json.dumps(session.build_dry_run_summary(), indent=2))
    else:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
