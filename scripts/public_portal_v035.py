#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path

PORTAL_VERSION='0.35'
INDEX_PATH=Path('web/public-v0.35/index.html')

os.environ.setdefault('AKASHICNET_DEPLOYMENT_MODE','public')

spec=importlib.util.spec_from_file_location('retrieval_v033','scripts/retrieval_http_v033.py')
retrieval=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(retrieval)


class PortalHandler(retrieval.Handler):
    server_version='AkashicNETPortal/0.35'

    def do_GET(self) -> None:
        path=self.path.split('?',1)[0]
        if path in {'/','/index.html'}:
            body=INDEX_PATH.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Referrer-Policy','no-referrer')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def main() -> None:
    p=argparse.ArgumentParser(description='AkashicNET same-origin public portal v0.35')
    p.add_argument('--host',default='127.0.0.1')
    p.add_argument('--port',type=int,default=8787)
    a=p.parse_args()
    if retrieval.DEPLOYMENT_MODE!='public':
        raise SystemExit('public portal requires AKASHICNET_DEPLOYMENT_MODE=public')
    server=retrieval.ThreadingHTTPServer((a.host,a.port),PortalHandler)
    print({'portal_version':PORTAL_VERSION,'listen':f'http://{a.host}:{a.port}','public_only':True},flush=True)
    server.serve_forever()


if __name__=='__main__':
    main()
