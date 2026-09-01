#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'website' / 'app' / 'globals.css').read_text(encoding='utf-8')
APP = ROOT / 'website' / 'app'

required_css = [
    'box-sizing:border-box',
    'display:flex; flex-wrap:wrap',
    '@media (max-width:820px)',
    '@media (prefers-reduced-motion:reduce)',
    'overflow:hidden',
]
for token in required_css:
    assert token in CSS, f'missing responsive/accessibility CSS contract: {token}'

routes = []
for page in APP.rglob('page.tsx'):
    rel = page.relative_to(APP)
    route = '/' if rel.as_posix() == 'page.tsx' else '/' + rel.parent.as_posix()
    routes.append(route)
    text = page.read_text(encoding='utf-8')
    assert '<main' in text or 'export default' in text, f'{route}: page source is malformed'

assert routes, 'no public routes discovered'

print('PUBLIC ROUTE QA v0.13 PASS:', len(routes), 'repository routes; source-testable responsive and reduced-motion contracts present')
print('MANUAL VISUAL QA REMAINS REQUIRED: breakpoint collision, clipping and artwork/control overlap cannot be inferred from source alone')
