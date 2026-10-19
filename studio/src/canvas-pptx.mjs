// PowerPoint canvas — same drawing API as SvgCanvas, rendered with PptxGenJS.
import PptxGenJS from 'pptxgenjs';
import { FONT } from './theme.mjs';
import { wrap, measure } from './text.mjs';

const hex = (c) => String(c).replace('#', '').toUpperCase();
const pct = (op) => Math.round((1 - (op ?? 1)) * 100);
const none = (v) => !v || v === 'none' || v === 'transparent';

export class PptxCanvas {
  constructor(pptx, slide, w = 13.3333, h = 7.5) {
    this.pptx = pptx;
    this.slide = slide;
    this.w = w; this.h = h;
  }

  rect(x, y, w, h, o = {}) {
    const type = o.radius ? this.pptx.ShapeType.roundRect : this.pptx.ShapeType.rect;
    const opts = {
      x, y, w, h,
      fill: none(o.fill) ? { color: 'FFFFFF', transparency: 100 } : { color: hex(o.fill), transparency: pct(o.opacity) },
      line: none(o.stroke) ? { color: 'FFFFFF', transparency: 100 } : { color: hex(o.stroke), width: (o.sw ?? 0.75), dashType: o.dash ? (o.dash === 'dot' ? 'sysDot' : 'dash') : 'solid', transparency: 0 },
    };
    if (o.radius) opts.rectRadius = Math.min(0.5, o.radius / Math.min(w, h));
    this.slide.addShape(type, opts);
  }

  line(x1, y1, x2, y2, o = {}) {
    const flipH = x2 < x1;
    const flipV = y2 < y1;
    const x = Math.min(x1, x2), y = Math.min(y1, y2);
    const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
    this.slide.addShape(this.pptx.ShapeType.line, {
      x, y, w: Math.max(w, 0.0001), h: Math.max(h, 0.0001),
      flipH, flipV,
      line: {
        color: hex(none(o.stroke) ? '#FFFFFF' : o.stroke),
        width: o.sw ?? 0.75,
        dashType: o.dash ? (o.dash === 'dot' ? 'sysDot' : o.dash === 'dash' ? 'dash' : o.dash) : 'solid',
        beginArrowType: o.arrowStart ? 'triangle' : 'none',
        endArrowType: o.arrowEnd ? 'triangle' : 'none',
        transparency: none(o.stroke) ? 100 : pct(o.opacity),
      },
    });
  }

  circle(cx, cy, r, o = {}) { this.ellipse(cx, cy, r, r, o); }

  ellipse(cx, cy, rx, ry, o = {}) {
    this.slide.addShape(this.pptx.ShapeType.ellipse, {
      x: cx - rx, y: cy - ry, w: rx * 2, h: ry * 2,
      fill: none(o.fill) ? { color: 'FFFFFF', transparency: 100 } : { color: hex(o.fill), transparency: pct(o.opacity) },
      line: none(o.stroke) ? { color: 'FFFFFF', transparency: 100 } : { color: hex(o.stroke), width: o.sw ?? 0.75, dashType: o.dash ? 'dash' : 'solid' },
    });
  }

  poly(points, o = {}) {
    for (let i = 0; i < points.length - 1; i++) {
      const last = i === points.length - 2;
      this.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], {
        ...o,
        arrowEnd: last ? o.arrowEnd : false,
        arrowStart: i === 0 ? o.arrowStart : false,
      });
    }
  }

  text(x, y, w, str, o = {}) {
    if (str === undefined || str === null || str === '') return;
    let s = String(str);
    if (o.caps) s = s.toUpperCase();
    const size = o.size || 12;
    const lh = o.lineHeight || 1.35;
    const ls = o.letterSpacing || 0;
    const font = o.font === 'serif' ? FONT.serif : FONT.sans;
    const opts = { font: o.font, bold: !!o.bold, italic: !!o.italic, weight: o.bold ? 700 : (o.weight || 400), letterSpacing: ls };

    const maxPt = w * 72;
    const res = wrap(s, maxPt, size, opts);
    let lines = res.lines;
    if (o.maxLines && lines.length > o.maxLines) {
      lines = lines.slice(0, o.maxLines);
      let last = lines[o.maxLines - 1];
      while (last.length > 1 && measure(last + '…', size, opts) > maxPt) last = last.slice(0, -1).trimEnd();
      lines[o.maxLines - 1] = last + '…';
    }
    const blockH = (lines.length * size * lh) / 72;
    let yy = y;
    if (o.valign === 'middle' && o.boxH) yy = y + (o.boxH - blockH) / 2;
    if (o.valign === 'bottom' && o.boxH) yy = y + o.boxH - blockH;

    const boxH = o.boxH ? Math.max(o.boxH, blockH + 0.02) : blockH + size / 72;

    this.slide.addText(lines.join('\n'), {
      x, y: yy, w, h: boxH,
      fontFace: font,
      fontSize: size,
      color: hex(o.color || '#000000'),
      bold: !!o.bold,
      italic: !!o.italic,
      align: o.align || 'left',
      valign: 'top',
      margin: 0,
      charSpacing: ls,
      lineSpacing: +(size * lh).toFixed(2),
      paraSpaceBefore: 0,
      paraSpaceAfter: 0,
      fit: 'none',
      wrap: true,
      isTextBox: true,
      transparency: o.opacity !== undefined ? pct(o.opacity) : 0,
    });
  }

  raw() { /* background is set as a slide image */ }

  image(x, y, w, h, file) {
    this.slide.addImage({ path: file, x, y, w, h });
  }

  vgrad() { return 'transparent'; }
  rgrad() { return 'transparent'; }
  toSVG() { return ''; }
}
