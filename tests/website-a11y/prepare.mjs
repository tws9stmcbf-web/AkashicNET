import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';

// The repository is a source snapshot, not the deployed Sites project.
// Exercise the real layout, middleware and five homepages in an isolated Next app.
await rm('fixture', { recursive: true, force: true });
await mkdir('fixture/app', { recursive: true });
for (const file of ['layout.tsx', 'page.tsx', 'localizedHome.module.css', 'de', 'es', 'pt', 'fr']) {
  await cp(`../../website/app/${file}`, `fixture/app/${file}`, { recursive: true });
}
await cp('../../website/middleware.ts', 'fixture/middleware.ts');
const css = await readFile('../../website/app/globals.css', 'utf8');
// Hosting-only framework/vendor imports are absent from the snapshot; retain all authored CSS.
await writeFile('fixture/app/globals.css', css.replace(/^@import .*;\s*$/gm, ''));
await writeFile('fixture/package.json', '{"private":true}');
await writeFile('fixture/next.config.mjs', 'export default { experimental: { cpus: 2 } };\n');
