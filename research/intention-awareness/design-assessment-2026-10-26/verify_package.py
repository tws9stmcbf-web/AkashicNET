#!/usr/bin/env python3
"""Verify locally retained reviewed bytes, without claiming scientific validation."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'package-sha256.json').read_text())
for name,digest in manifest.items():
    path=root/name
    if path.resolve().parent != root.resolve() and root.resolve() not in path.resolve().parents:
        raise ValueError('Out-of-package path')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise ValueError(f'Hash mismatch: {name}')
print(f'{len(manifest)} package hashes match; synthetic-only review status unchanged')
