// SVG canvas — 1 unit = 1/96 inch (1280 × 720 for a 13.333 × 7.5 in slide).
import { PREVIEW_FONT } from './theme.mjs';
import { wrap, measure } from './text.mjs';

const PX = 96;            // px per inch
export const PT2PX = 96 / 72;

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

function fontFamily(font) {
  return font === 'serif' ? PREVIEW_FONT.serif : PREVIEW_FONT.sans;
}

export class SvgCanvas {
  constructor(w = 13.3333, h = 7.5) {
    this.w = w; this.h = h;
    this.body = [];
    this.pre = [];
    this.defs = [];
    this._grad = 0;
    this._marker = new Map();
  }

  _u(x) { return +(x * PX).toFixed(2); }

  rect(x, y, w, h, o = {}) {
    const fill = o.fill || 'none';
    const op = o.opacity ?? 1;
    const rx = o.radius ? Math.min(o.radius * PX, Math.min(w, h) * PX / 2) : 0;
    const stroke = o.stroke ? ` stroke="${o.stroke}" stroke-width="${(o.sw ?? 0.75) * PT2PX}"` : '';
    const dash = o.dash ? ` stroke-dasharray="${o.dash === 'dot' ? '4 5' : '8 6'}"` : '';
    this.body.push(`<rect x="${this._u(x)}" y="${this._u(y)}" width="${this._u(w)}" height="${this._u(h)}" rx="${rx.toFixed(2)}" fill="${fill}" fill-opacity="${op}"${stroke}${dash}/>`);
  }

  line(x1, y1, x2, y2, o = {}) {
    const stroke = o.stroke || '#000';
    const sw = (o.sw ?? 0.75) * PT2PX;
    const op = o.opacity ?? 1;
    const dash = o.dash ? ` stroke-dasharray="${o.dash === 'dot' ? '3 5' : o.dash === 'dash' ? '9 7' : o.dash}"` : '';
    const cap = ` stroke-linecap="${o.cap || 'butt'}"`;
    const mEnd = o.arrowEnd ? ` marker-end="url(#${this._markerId(stroke, o.arrowSize || 4.2)})"` : '';
    const mStart = o.arrowStart ? ` marker-start="url(#${this._markerId(stroke, o.arrowSize || 4.2)})"` : '';
    this.body.push(`<line x1="${this._u(x1)}" y1="${this._u(y1)}" x2="${this._u(x2)}" y2="${this._u(y2)}" stroke="${stroke}" stroke-width="${sw.toFixed(2)}" stroke-opacity="${op}"${dash}${cap}${mEnd}${mStart}/>`);
  }

  _markerId(color, sizePx) {
    const key = color + '|' + sizePx;
    if (this._marker.has(key)) return this._marker.get(key);
    const id = `ar${this._marker.size}`;
    this._marker.set(key, id);
    this.defs.push(`<marker id="${id}" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="${sizePx}" markerHeight="${sizePx}" orient="auto-start-reverse"><path d="M 1 1.4 L 9.2 5 L 1 8.6 z" fill="${color}"/></marker>`);
    return id;
  }

  circle(cx, cy, r, o = {}) {
    const fill = o.fill || 'none';
    const op = o.opacity ?? 1;
    const stroke = o.stroke ? ` stroke="${o.stroke}" stroke-width="${(o.sw ?? 0.75) * PT2PX}"` : '';
    const dash = o.dash ? ` stroke-dasharray="8 6"` : '';
    this.body.push(`<circle cx="${this._u(cx)}" cy="${this._u(cy)}" r="${this._u(r)}" fill="${fill}" fill-opacity="${op}"${stroke}${dash}/>`);
  }

  ellipse(cx, cy, rx, ry, o = {}) {
    const fill = o.fill || 'none';
    const op = o.opacity ?? 1;
    const stroke = o.stroke ? ` stroke="${o.stroke}" stroke-width="${(o.sw ?? 0.75) * PT2PX}"` : '';
    const dash = o.dash ? ` stroke-dasharray="8 6"` : '';
    this.body.push(`<ellipse cx="${this._u(cx)}" cy="${this._u(cy)}" rx="${this._u(rx)}" ry="${this._u(ry)}" fill="${fill}" fill-opacity="${op}"${stroke}${dash}/>`);
  }

  poly(points, o = {}) {
    const pts = points.map(([x, y]) => `${this._u(x)},${this._u(y)}`).join(' ');
    const tag = o.closed ? 'polygon' : 'polyline';
    const fill = o.fill || 'none';
    const stroke = o.stroke ? ` stroke="${o.stroke}" stroke-width="${(o.sw ?? 0.75) * PT2PX}"` : ' stroke="none"';
    const dash = o.dash ? ` stroke-dasharray="8 6"` : '';
    const mEnd = o.arrowEnd ? ` marker-end="url(#${this._markerId(o.stroke, o.arrowSize || 4.2)})"` : '';
    this.body.push(`<${tag} points="${pts}" fill="${fill}" stroke-linejoin="round" stroke-linecap="round"${stroke}${dash}${mEnd}/>`);
  }

  text(x, y, w, str, o = {}) {
    if (str === undefined || str === null || str === '') return;
    let s = String(str);
    if (o.caps) s = s.toUpperCase();
    const size = o.size || 12;
    const lh = o.lineHeight || 1.35;
    const ls = o.letterSpacing || 0;
    const align = o.align || 'left';
    const color = o.color || '#000';
    const op = o.opacity ?? 1;
    const weight = o.bold ? 700 : (o.weight || 400);
    const fam = fontFamily(o.font);
    const style = o.italic ? 'italic' : 'normal';
    const opts = { font: o.font, bold: !!o.bold, italic: !!o.italic, weight, letterSpacing: ls };

    const maxPt = w * 72;
    const res = o.noWrap ? { lines: [s], height: size * lh } : wrap(s, maxPt, size, opts);
    let lines = res.lines;
    if (o.maxLines && lines.length > o.maxLines) {
      lines = lines.slice(0, o.maxLines);
      let last = lines[o.maxLines - 1];
      while (last.length > 1 && measure(last + '…', size, opts) > maxPt) last = last.slice(0, -1).trimEnd();
      lines[o.maxLines - 1] = last + '…';
    }
    const blockH = lines.length * size * lh * PT2PX;
    let top = y * PX;
    if (o.valign === 'middle' && o.boxH) top = (y + (o.boxH - blockH / PX) / 2) * PX;
    if (o.valign === 'bottom' && o.boxH) top = (y + o.boxH - blockH / PX) * PX;

    const anchor = align === 'center' ? 'middle' : align === 'right' ? 'end' : 'start';
    const tx = align === 'center' ? (x + w / 2) * PX : align === 'right' ? (x + w) * PX : x * PX;

    const out = [];
    lines.forEach((ln, i) => {
      const baseline = top + (0.5 * (lh - 1) + 0.78) * size * PT2PX + i * size * lh * PT2PX;
      out.push(`<text x="${tx.toFixed(2)}" y="${baseline.toFixed(2)}" font-family="${fam}" font-size="${(size * PT2PX).toFixed(2)}" font-weight="${weight}" font-style="${style}" fill="${color}" fill-opacity="${op}" text-anchor="${anchor}" letter-spacing="${(ls * PT2PX).toFixed(2)}">${esc(ln)}</text>`);
    });
    this.body.push(out.join(''));
  }

  image(x, y, w, h, href, o = {}) {
    this.body.push(`<image x="${this._u(x)}" y="${this._u(y)}" width="${this._u(w)}" height="${this._u(h)}" href="${href}" preserveAspectRatio="${o.cover ? 'xMidYMid slice' : 'none'}" opacity="${o.opacity ?? 1}"/>`);
  }

  // ── composites ────────────────────────────────────────────────────────────
  vgrad(id, stops, { x1 = 0, y1 = 0, x2 = 0, y2 = 1 } = {}) {
    this.defs.push(`<linearGradient id="${id}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}">${stops.map(([o, c]) => `<stop offset="${o}" stop-color="${c}"/>`).join('')}</linearGradient>`);
    return `url(#${id})`;
  }

  rgrad(id, stops, { cx = 0.5, cy = 0.5, r = 0.5 } = {}) {
    this.defs.push(`<radialGradient id="${id}" cx="${cx}" cy="${cy}" r="${r}">${stops.map(([o, c, a = 1]) => `<stop offset="${o}" stop-color="${c}" stop-opacity="${a}"/>`).join('')}</radialGradient>`);
    return `url(#${id})`;
  }

  raw(markup) { this.pre.push(markup); }

  toSVG({ background } = {}) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${this.w * PX}" height="${this.h * PX}" viewBox="0 0 ${this.w * PX} ${this.h * PX}">
<defs>${this.defs.join('')}</defs>
${background ? `<rect width="100%" height="100%" fill="${background}"/>` : ''}
${this.pre.join('')}
${this.body.join('\n')}
</svg>`;
  }
}
