#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from collections import defaultdict, deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

SERVICE_NAME = 'AKASHICNET_RETRIEVAL_HTTP'
SERVICE_VERSION = '0.33'
UPSTREAM_API = 'AKASHICNET_RETRIEVAL_API'
UPSTREAM_SCHEMA = 'akashicnet://schemas/retrieval/v0.25'
MAX_QUERY_CHARS = int(os.getenv('AKASHICNET_MAX_QUERY_CHARS', '512'))
MAX_REQUEST_TARGET_CHARS = int(os.getenv('AKASHICNET_MAX_REQUEST_TARGET_CHARS', '2048'))
RATE_LIMIT_REQUESTS = int(os.getenv('AKASHICNET_RATE_LIMIT_REQUESTS', '60'))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv('AKASHICNET_RATE_LIMIT_WINDOW_SECONDS', '60'))
DEPLOYMENT_MODE = os.getenv('AKASHICNET_DEPLOYMENT_MODE', 'public').strip().lower()
ALLOW_INTERNAL_VISIBILITY = os.getenv('AKASHICNET_ALLOW_INTERNAL_VISIBILITY', 'false').strip().lower() == 'true'

if DEPLOYMENT_MODE not in {'public', 'internal'}:
    raise RuntimeError('AKASHICNET_DEPLOYMENT_MODE must be public or internal')
if DEPLOYMENT_MODE == 'public':
    ALLOW_INTERNAL_VISIBILITY = False

_request_times: dict[str, deque[float]] = defaultdict(deque)


def _safe_json(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.send_header('Cache-Control', 'no-store')
    handler.send_header('X-Content-Type-Options', 'nosniff')
    handler.end_headers()
    handler.wfile.write(body)


def _error(handler: BaseHTTPRequestHandler, status: int, code: str, public_message: str) -> None:
    _safe_json(handler, status, {'error': code, 'message': public_message})


def _rate_limited(client: str) -> bool:
    now = time.monotonic()
    q = _request_times[client]
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS
    while q and q[0] < cutoff:
        q.popleft()
    if len(q) >= RATE_LIMIT_REQUESTS:
        return True
    q.append(now)
    return False


def retrieve(query: str, domain: str, state: str, limit: int, visibility: str) -> dict:
    if domain not in {'all', 'reddit', 'library'}:
        raise ValueError('invalid domain')
    if state not in {'all', 'accepted', 'hold'}:
        raise ValueError('invalid state')
    if visibility not in {'internal', 'public'}:
        raise ValueError('invalid visibility')
    if visibility == 'internal' and not ALLOW_INTERNAL_VISIBILITY:
        raise PermissionError('internal visibility disabled')
    if limit < 1 or limit > 100:
        raise ValueError('invalid limit')
    if len(query) > MAX_QUERY_CHARS:
        raise ValueError('query too long')

    cmd = [
        'python', 'scripts/public_retrieval_gate_v029.py', query,
        '--domain', domain,
        '--state', state,
        '--limit', str(limit),
        '--visibility', visibility,
    ]
    payload = json.loads(subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL))
    if payload.get('api') != UPSTREAM_API or payload.get('schema_id') != UPSTREAM_SCHEMA:
        raise RuntimeError('upstream contract mismatch')
    return payload


class Handler(BaseHTTPRequestHandler):
    server_version = 'AkashicNETHTTP/0.33'
    sys_version = ''

    def log_message(self, fmt: str, *args) -> None:
        # Deliberately omit query strings, headers, result metadata and exception text.
        print(json.dumps({'event': 'http_request', 'method': self.command, 'path': urlparse(self.path).path}))

    def do_GET(self) -> None:
        if len(self.path) > MAX_REQUEST_TARGET_CHARS:
            _error(self, HTTPStatus.REQUEST_URI_TOO_LONG, 'request_too_large', 'request target too large')
            return

        client = self.client_address[0] if self.client_address else 'unknown'
        if _rate_limited(client):
            _error(self, HTTPStatus.TOO_MANY_REQUESTS, 'rate_limited', 'request rate limit exceeded')
            return

        parsed = urlparse(self.path)
        if parsed.path == '/livez':
            _safe_json(self, HTTPStatus.OK, {'status': 'alive', 'service_version': SERVICE_VERSION})
            return
        if parsed.path == '/readyz':
            ready = os.path.exists('scripts/public_retrieval_gate_v029.py')
            _safe_json(self, HTTPStatus.OK if ready else HTTPStatus.SERVICE_UNAVAILABLE,
                       {'status': 'ready' if ready else 'not_ready', 'service_version': SERVICE_VERSION})
            return
        if parsed.path == '/health':
            _safe_json(self, HTTPStatus.OK, {
                'service': SERVICE_NAME,
                'service_version': SERVICE_VERSION,
                'status': 'ok',
                'deployment_mode': DEPLOYMENT_MODE,
                'internal_visibility_enabled': ALLOW_INTERNAL_VISIBILITY,
                'public_retrieval_requires_public_verified': True,
            })
            return
        if parsed.path != '/v1/retrieve':
            _error(self, HTTPStatus.NOT_FOUND, 'not_found', 'endpoint not found')
            return

        params = parse_qs(parsed.query, keep_blank_values=True)
        query = (params.get('q') or [''])[0].strip()
        domain = (params.get('domain') or ['all'])[0]
        state = (params.get('state') or ['all'])[0]
        visibility_default = 'internal' if DEPLOYMENT_MODE == 'internal' else 'public'
        visibility = (params.get('visibility') or [visibility_default])[0]
        raw_limit = (params.get('limit') or ['50'])[0]

        if not query:
            _error(self, HTTPStatus.BAD_REQUEST, 'invalid_request', 'q is required')
            return
        try:
            result = retrieve(query, domain, state, int(raw_limit), visibility)
        except ValueError:
            _error(self, HTTPStatus.BAD_REQUEST, 'invalid_request', 'request parameters are invalid')
            return
        except PermissionError:
            _error(self, HTTPStatus.FORBIDDEN, 'visibility_forbidden', 'requested visibility is unavailable')
            return
        except subprocess.CalledProcessError:
            _error(self, HTTPStatus.BAD_GATEWAY, 'upstream_failure', 'retrieval service unavailable')
            return
        except Exception:
            _error(self, HTTPStatus.INTERNAL_SERVER_ERROR, 'internal_error', 'internal service error')
            return

        _safe_json(self, HTTPStatus.OK, {
            'service': SERVICE_NAME,
            'service_version': SERVICE_VERSION,
            'visibility': visibility,
            'upstream': result,
        })


def main() -> None:
    p = argparse.ArgumentParser(description='AkashicNET hardened retrieval service v0.33')
    p.add_argument('--host', default=os.getenv('AKASHICNET_HOST', '127.0.0.1'))
    p.add_argument('--port', type=int, default=int(os.getenv('AKASHICNET_PORT', '8787')))
    a = p.parse_args()
    server = ThreadingHTTPServer((a.host, a.port), Handler)
    print(json.dumps({'service': SERVICE_NAME, 'service_version': SERVICE_VERSION,
                      'deployment_mode': DEPLOYMENT_MODE, 'internal_visibility_enabled': ALLOW_INTERNAL_VISIBILITY,
                      'endpoints': ['/livez', '/readyz', '/health', '/v1/retrieve']}))
    server.serve_forever()


if __name__ == '__main__':
    main()
