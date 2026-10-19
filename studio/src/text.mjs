// Text measurement + wrapping shared by the SVG and PPTX backends.
// Measuring with Gelasio/Carlito (metric-compatible with Georgia/Calibri)
// keeps the preview and the PowerPoint layout in agreement.

import fs from 'node:fs';
import path from 'node:path';
import opentype from 'opentype.js';

const FONT_DIR = path.resolve(import.meta.dirname, '../assets/fonts');

const FILES = {
  'serif-400': 'Gelasio_400Regular.ttf',
  'serif-400i': 'Gelasio_400Regular_Italic.ttf',
  'serif-500': 'Gelasio_500Medium.ttf',
  'serif-600': 'Gelasio_600SemiBold.ttf',
  'serif-700': 'Gelasio_700Bold.ttf',
  'sans-400': 'Carlito_400Regular.ttf',
  'sans-400i': 'Carlito_400Regular_Italic.ttf',
  'sans-700': 'Carlito_700Bold.ttf',
  'sans-700i': 'Carlito_700Bold_Italic.ttf',
};

const cache = new Map();

function keyFor(opts = {}) {
  const fam = opts.font === 'serif' ? 'serif' : 'sans';
  let w = opts.bold ? 700 : (opts.weight || 400);
  if (fam === 'serif' && ![400, 500, 600, 700].includes(w)) w = 400;
  if (fam === 'sans' && ![400, 700].includes(w)) w = 400;
  const italic = opts.italic ? 'i' : '';
  return `${fam}-${w}${italic}`;
}

export function loadFont(opts) {
  let k = keyFor(opts);
  if (!FILES[k]) k = k.replace(/-700i$/, '-700').replace(/-400i$/, '-400');
  if (cache.has(k)) return cache.get(k);
  const buf = fs.readFileSync(path.join(FONT_DIR, FILES[k]));
  const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  const f = opentype.parse(ab, { lowMemory: false });
  cache.set(k, f);
  return f;
}

// width of a string in points, for a given font at a given pt size
export function measure(str, sizePt, opts = {}) {
  const font = loadFont(opts);
  const ls = opts.letterSpacing || 0; // in pt
  // Sum raw glyph advances: deterministic, and matches PowerPoint's simple layout.
  let base = 0;
  for (const ch of str) {
    const g = font.charToGlyph(ch);
    base += (g.advanceWidth || 0) / font.unitsPerEm * sizePt;
  }
  return base + Math.max(0, str.length - 1) * ls;
}

/**
 * Greedy wrap. Returns { lines, width, height } where height is in points
 * and accounts for the line-height multiple.
 */
export function wrap(str, maxWidthPt, sizePt, opts = {}) {
  const lh = opts.lineHeight || 1.35;
  const paras = String(str).split('\n');
  const lines = [];
  for (const para of paras) {
    if (para.trim() === '') { lines.push(''); continue; }
    const words = para.split(/\s+/);
    let cur = '';
    for (const w of words) {
      const test = cur ? cur + ' ' + w : w;
      if (measure(test, sizePt, opts) <= maxWidthPt || !cur) {
        cur = test;
      } else {
        lines.push(cur);
        cur = w;
      }
    }
    if (cur) lines.push(cur);
  }
  const widest = Math.max(...lines.map(l => measure(l, sizePt, opts)), 0);
  return { lines, width: widest, height: lines.length * sizePt * lh, lh };
}

export function truncateToLines(str, maxWidthPt, sizePt, maxLines, opts = {}) {
  const w = wrap(str, maxWidthPt, sizePt, opts);
  if (w.lines.length <= maxLines) return w;
  const lines = w.lines.slice(0, maxLines);
  let last = lines[maxLines - 1];
  while (last.length > 1 && measure(last + '…', sizePt, opts) > maxWidthPt) {
    last = last.slice(0, -1).trimEnd();
  }
  lines[maxLines - 1] = last + '…';
  return { lines, width: maxWidthPt, height: lines.length * sizePt * (opts.lineHeight || 1.35), lh: opts.lineHeight || 1.35 };
}
