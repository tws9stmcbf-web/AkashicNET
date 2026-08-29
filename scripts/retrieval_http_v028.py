#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

SERVICE_NAME = 'AKASHICNET_RETRIEVAL_HTTP'
SERVICE_VERSION = '0.28'
UPSTREAM_API = 'AKASHICNET_RETRIEVAL_API'
UPSTREAM_SCHEMA = 'akashicnet://schemas/retrieval/v0.25'
OPENAPI_DOCUMENT = 'api/openapi-retrieval-v0.28.json'


def _json(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def retrieve(query: str, domain: str = 'all', state: str = 'all', limit: int = 100) -> dict:
    if domain not in {'all', 'reddit', 'library'}:
        raise ValueError('domain must be one of: all, reddit, library')
    if state not in {'all', 'accepted', 'hold'}:
        raise ValueError('state must be one of: all, accepted, hold')
    if limit < 1 or limit > 1000:
        raise ValueError('limit must be between 1 and 1000')

    cmd = [
        'python', 'scripts/query_api_v025.py', query,
        '--domain', domain,
        '--state', state,
        '--limit', str(limit),
    ]
    payload = json.loads(subprocess.check_output(cmd, text=True))
    if payload.get('api') != UPSTREAM_API:
        raise RuntimeError('unexpected upstream API name')
    if payload.get('schema_id') != UPSTREAM_SCHEMA:
        raise RuntimeError('unexpected upstream schema')
    return payload


def load_openapi() -> dict:
    with open(OPENAPI_DOCUMENT, 'r', encoding='utf-8') as fh:
        return json.load(fh)


class Handler(BaseHTTPRequestHandler):
    server_version = 'AkashicNETHTTP/0.28'

    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == '/health':
            _json(self, HTTPStatus.OK, {
                'service': SERVICE_NAME,
                'service_version': SERVICE_VERSION,
                'status': 'ok',
                'upstream_api': UPSTREAM_API,
                'upstream_schema': UPSTREAM_SCHEMA,
                'openapi': '/openapi.json',
                'epistemic_policy': {
                    'truth_inference_allowed': False,
                    'rights_promotion_allowed': False,
                    'scientific_evidence_promotion_allowed': False,
                },
            })
            return

        if parsed.path == '/openapi.json':
            try:
                _json(self, HTTPStatus.OK, load_openapi())
            except Exception as exc:
                _json(self, HTTPStatus.INTERNAL_SERVER_ERROR, {
                    'error': 'openapi_unavailable',
                    'message': str(exc),
                })
            return

        if parsed.path != '/v1/retrieve':
            _json(self, HTTPStatus.NOT_FOUND, {
                'error': 'not_found',
                'message': 'Use GET /health, GET /openapi.json, or GET /v1/retrieve?q=<query>.',
            })
            return

        params = parse_qs(parsed.query)
        query = (params.get('q') or [''])[0].strip()
        domain = (params.get('domain') or ['all'])[0]
        state = (params.get('state') or ['all'])[0]
        raw_limit = (params.get('limit') or ['100'])[0]

        if not query:
            _json(self, HTTPStatus.BAD_REQUEST, {
                'error': 'invalid_request',
                'message': 'q is required',
            })
            return

        try:
            limit = int(raw_limit)
            result = retrieve(query, domain, state, limit)
        except ValueError as exc:
            _json(self, HTTPStatus.BAD_REQUEST, {
                'error': 'invalid_request',
                'message': str(exc),
            })
            return
        except subprocess.CalledProcessError as exc:
            _json(self, HTTPStatus.INTERNAL_SERVER_ERROR, {
                'error': 'upstream_failure',
                'message': f'retrieval process failed with exit code {exc.returncode}',
            })
            return
        except Exception as exc:
            _json(self, HTTPStatus.INTERNAL_SERVER_ERROR, {
                'error': 'internal_error',
                'message': str(exc),
            })
            return

        _json(self, HTTPStatus.OK, {
            'service': SERVICE_NAME,
            'service_version': SERVICE_VERSION,
            'transport': 'http-json',
            'upstream': result,
        })


def main() -> None:
    p = argparse.ArgumentParser(description='AkashicNET retrieval HTTP service v0.28')
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=8787)
    args = p.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(json.dumps({
        'service': SERVICE_NAME,
        'service_version': SERVICE_VERSION,
        'listen': f'http://{args.host}:{args.port}',
        'endpoints': ['/health', '/openapi.json', '/v1/retrieve'],
    }))
    server.serve_forever()


if __name__ == '__main__':
    main()
