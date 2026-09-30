import { build } from 'esbuild';
import { readFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const { outputFiles } = await build({
  absWorkingDir: here,
  entryPoints: ['mount.tsx'],
  nodePaths: [here + 'node_modules'],
  bundle: true,
  jsx: 'automatic',
  outdir: 'bundle',
  write: false,
});
const assets = new Map(outputFiles.map(file => [file.path.split('/').pop(), file.contents]));
createServer((req, res) => {
  if (req.url === '/images/akashicnet-living-library-tree.webp') {
    res.setHeader('Content-Type', 'image/webp');
    return res.end(readFileSync(new URL('../../website/public/images/akashicnet-living-library-tree.webp', import.meta.url)));
  }
  const name = req.url.slice(1);
  if (assets.has(name)) {
    res.setHeader('Content-Type', name.endsWith('.css') ? 'text/css' : 'text/javascript');
    return res.end(assets.get(name));
  }
  if (req.url === '/living-library-map') {
    res.setHeader('Content-Type', 'text/html');
    return res.end('<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/mount.css"></head><body><div id="root"></div><script src="/mount.js"></script></body></html>');
  }
  // Destination requests deliberately return a new document: navigation is real,
  // never a mocked callback.
  res.setHeader('Content-Type', 'text/html');
  res.end('<!doctype html><title>Destination</title>');
}).listen(4173, '127.0.0.1');
