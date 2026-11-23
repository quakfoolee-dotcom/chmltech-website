// V5.77 site SEO checks: clean internal links and the IndexNow key file.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const SKIP = new Set(['.git', 'assets', 'content', 'node_modules', 'WMS_demo']);
function pages(dir = ROOT, out = []) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) { if (!SKIP.has(f)) pages(p, out); }
    else if (f.endsWith('.html')) out.push(relative(ROOT, p).split(sep).join('/'));
  }
  return out;
}

test('internal links use clean URLs (no .html), matching canonicals', () => {
  const bad = [];
  for (const rel of pages()) {
    const s = readFileSync(join(ROOT, rel), 'utf8');
    for (const [, h] of s.matchAll(/href="([^"]*?\.html)(?:[?#][^"]*)?"/g)) {
      if (/^[a-z][a-z0-9+.-]*:|^\/\//i.test(h) && !h.startsWith('https://www.chmltech.com/')) continue;
      if (/(^|\/)WMS_demo\//.test(h)) continue;
      bad.push(`${rel}: ${h}`);
    }
  }
  assert.deepEqual(bad.slice(0, 10), [], `${bad.length} .html links left; run content/gen/seo_pass.py`);
});

test('IndexNow key file is served at the site root', () => {
  const key = 'c3bf155879376468e8bf014cf323cbef';
  assert.ok(existsSync(join(ROOT, `${key}.txt`)));
  assert.equal(readFileSync(join(ROOT, `${key}.txt`), 'utf8').trim(), key);
  assert.match(readFileSync(join(ROOT, '.github/indexnow.py'), 'utf8'), new RegExp(key));
});
