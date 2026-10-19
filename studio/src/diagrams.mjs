// Bespoke, hand-composed diagrams. Every function draws to the canvas passed in,
// so the identical geometry is emitted as SVG (preview/PDF) and PowerPoint shapes.
import { C } from './theme.mjs';

const INK = C.ink;
const SOFT = C.inkSoft;
const MUT = C.inkMid;

const T = (c, x, y, w, s, o = {}) => c.text(x, y, w, s, {
  font: 'sans', size: 9.4, color: SOFT, lineHeight: 1.3, ...o,
});
const H = (c, x, y, w, s, o = {}) => c.text(x, y, w, s, {
  font: 'serif', size: 12.5, color: INK, lineHeight: 1.22, ...o,
});

function card(c, x, y, w, h, o = {}) {
  c.rect(x, y, w, h, {
    fill: o.fill ?? C.paperWarm,
    stroke: o.stroke ?? C.rule,
    sw: o.sw ?? 0.7,
    radius: o.radius ?? 0.045,
    dash: o.dash,
  });
}

function num(c, cx, cy, r, n, o = {}) {
  c.circle(cx, cy, r, { fill: o.fill ?? C.gold, stroke: o.stroke, sw: 0.6 });
  c.text(cx - r, cy - r, r * 2, String(n), {
    font: 'sans', size: o.size ?? 8.5, bold: true, align: 'center',
    color: o.color ?? C.paper, valign: 'middle', boxH: r * 2, lineHeight: 1,
  });
}

function edgePoint(cx, cy, w, h, tx, ty) {
  const dx = tx - cx, dy = ty - cy;
  if (!dx && !dy) return [cx, cy];
  const sx = dx === 0 ? Infinity : (w / 2) / Math.abs(dx);
  const sy = dy === 0 ? Infinity : (h / 2) / Math.abs(dy);
  const s = Math.min(sx, sy);
  return [cx + dx * s, cy + dy * s];
}

function node(c, x, y, w, h, title, sub, o = {}) {
  card(c, x, y, w, h, o);
  const pad = 0.14;
  if (sub) {
    T(c, x + pad, y + h / 2 - 0.30, w - pad * 2, title, {
      font: 'sans', size: 10, bold: true, color: INK, align: o.align || 'center', lineHeight: 1.2,
    });
    T(c, x + pad, y + h / 2 + 0.02, w - pad * 2, sub, {
      size: 8.2, color: MUT, align: o.align || 'center', lineHeight: 1.25,
    });
  } else {
    T(c, x + pad, y, w - pad * 2, title, {
      size: 9.4, bold: o.bold, color: o.color || INK, align: o.align || 'center',
      valign: 'middle', boxH: h, lineHeight: 1.25,
    });
  }
}

function arrowsAround(c, a, b, color = C.gold, sw = 1.0) {
  const [ax, ay] = edgePoint(a.cx, a.cy, a.w, a.h, b.cx, b.cy);
  const [bx, by] = edgePoint(b.cx, b.cy, b.w, b.h, a.cx, a.cy);
  c.line(ax, ay, bx, by, { stroke: color, sw, arrowEnd: true, arrowSize: 3.6 });
}

export const DIAGRAMS = {
  // ───────────────────────────────────────────────────────────── Course arc ──
  phaseCards(c, b, ctx = {}) {
    const phases = ctx.phases || [];
    const n = phases.length || 4;
    const gap = 0.26;
    const w = (b.w - gap * (n - 1)) / n;
    phases.forEach((p, i) => {
      const x = b.x + i * (w + gap);
      card(c, x, b.y + 0.42, w, b.h - 0.72, { fill: i % 2 ? C.paperWarm : '#FDFAF3' });
      c.rect(x, b.y + 0.42, w, 0.055, { fill: i % 2 ? C.sage : C.gold });
      c.text(x + 0.18, b.y + 0.62, w - 0.36, `PHASE ${p.roman}`, {
        caps: true, size: 7.6, letterSpacing: 1.8, color: i % 2 ? C.sage : C.goldDeep, bold: true,
      });
      H(c, x + 0.18, b.y + 0.86, w - 0.36, p.name, { size: 15.5, lineHeight: 1.14 });
      T(c, x + 0.18, b.y + 1.64, w - 0.36, `Weeks ${p.range}`, { size: 8.2, color: MUT, letterSpacing: 0.6 });
      c.line(x + 0.18, b.y + 1.86, x + 0.72, b.y + 1.86, { stroke: C.rule, sw: 0.6 });
      p.weeks.forEach((wt, j) => {
        const yy = b.y + 2.0 + j * 0.44;
        num(c, x + 0.255, yy + 0.09, 0.105, p.start + j, {
          fill: 'none', stroke: C.gold, color: C.goldDeep, size: 6.6,
        });
        T(c, x + 0.44, yy - 0.03, w - 0.55, wt, { size: 8.4, color: SOFT, lineHeight: 1.18 });
      });
    });
    // progress rail
    const ry = b.y + 0.18;
    c.line(b.x, ry, b.x + b.w, ry, { stroke: C.rule, sw: 0.8 });
    for (let i = 0; i < 16; i++) {
      const x = b.x + (b.w / 15) * i;
      c.circle(x, ry, i % 4 === 0 ? 0.045 : 0.03, { fill: i % 4 === 0 ? C.gold : C.rule, });
    }
    c.text(b.x, ry - 0.3, b.w, 'WEEK 1  ·  A SIXTEEN-WEEK PROGRESSION  ·  WEEK 16', {
      caps: true, size: 6.6, letterSpacing: 1.4, color: MUT, align: 'center',
    });
  },

  rail(c, x, y, w, current) {
    const n = 16;
    const step = w / (n - 1);
    c.line(x, y, x + w, y, { stroke: C.ruleDark, sw: 0.9 });
    for (let i = 0; i < n; i++) {
      const cx = x + step * i;
      const active = i + 1 === current;
      const past = i + 1 < current;
      c.circle(cx, y, active ? 0.075 : 0.042, {
        fill: active ? C.gold : past ? C.goldDeep : C.night3,
        stroke: active ? C.goldLight : 'none', sw: 0.8,
      });
      if (active) c.circle(cx, y, 0.16, { stroke: C.gold, sw: 0.55, opacity: 0.55 });
    }
    c.text(x, y + 0.22, w, 'WEEK 1', { size: 6.4, color: MUT, letterSpacing: 1.2, caps: true });
    c.text(x + w - 0.7, y + 0.22, 0.7, 'WEEK 16', { size: 6.4, color: MUT, letterSpacing: 1.2, align: 'right', caps: true });
  },

  // ────────────────────────────────────────────────────── Ecological systems ──
  ecological(c, b) {
    const cx = b.x + 3.55;
    const cy = b.y + b.h / 2 - 0.05;
    const rings = [
      { rx: 0.92, ry: 0.52, label: 'The individual', sub: 'presenting concern, development, biology', fill: C.gold, op: 0.14 },
      { rx: 1.92, ry: 1.06, label: 'Family & household', sub: 'roles, rules, coalitions, daily routines', fill: C.parchment, op: 0.55 },
      { rx: 2.92, ry: 1.60, label: 'Extended kin, community & faith', sub: 'grandparents, aunts, church, mosque, neighbours', fill: C.sage, op: 0.07 },
      { rx: 3.95, ry: 2.14, label: 'Institutions', sub: 'school, health care, workplace, courts', fill: C.copper, op: 0.06 },
    ];
    rings.forEach((r, i) => {
      c.ellipse(cx, cy, r.rx, r.ry, { fill: r.fill, opacity: r.op, stroke: C.rule, sw: 0.7, dash: i > 0 ? 'dash' : undefined });
    });
    c.circle(cx, cy, 0.06, { fill: C.goldDeep });
    T(c, cx - 0.55, cy + 0.09, 1.1, 'person', { size: 7.6, align: 'center', color: C.goldDeep, caps: true, letterSpacing: 1.2 });

    const labels = [
      { y: b.y + 0.42, title: 'Culture, economy & policy', sub: 'values, migration, employment, housing, law', ring: 3 },
      { y: b.y + 1.34, title: 'Institutions', sub: 'school, health care, workplace, courts', ring: 2 },
      { y: b.y + 2.26, title: 'Extended kin & community', sub: 'grandparents, kin networks, faith communities', ring: 1 },
      { y: b.y + 3.18, title: 'Family & household', sub: 'roles, rules, coalitions, routines', ring: 0 },
    ];
    labels.forEach((L, i) => {
      const r = rings[Math.min(L.ring + 1, 3)];
      const px = cx + r.rx * Math.cos(-0.42);
      const py = cy + r.ry * Math.sin(-0.42);
      c.line(px + 0.05, py, b.x + 7.5, L.y + 0.22, { stroke: C.rule, sw: 0.6 });
      c.circle(px, py, 0.035, { fill: C.gold });
      c.text(b.x + 7.62, L.y, 3.85, L.title, { font: 'serif', size: 11.2, color: INK });
      T(c, b.x + 7.62, L.y + 0.27, 3.85, L.sub, { size: 8.2, color: MUT });
    });
    c.line(b.x + 7.62, b.y + 4.02, b.x + 8.25, b.y + 4.02, { stroke: C.gold, sw: 1.1 });
    T(c, b.x + 8.35, b.y + 3.93, 3.1, 'the relational unit of treatment', { size: 8.2, italic: true, color: C.goldDeep });
  },

  // ──────────────────────────────────────────────────────── Circular causality ──
  causalLoop(c, b) {
    const cx = b.x + 3.72;
    const cy = b.y + 2.05;
    const w = 2.26, h = 0.9;
    const dx = 2.7, dy = 1.36;
    const nodes = [
      { title: 'Presenting concern', sub: 'a son withdraws, a daughter rebels', cx, cy: cy - dy },
      { title: 'Family response', sub: 'worry, monitoring, criticism', cx: cx + dx, cy },
      { title: 'Escalating meaning', sub: '“he is defiant” · “she is cold”', cx, cy: cy + dy },
      { title: 'Attempted solution', sub: 'more of the same — firmer, louder', cx: cx - dx, cy },
    ];
    nodes.forEach(n => { n.x = n.cx - w / 2; n.y = n.cy - h / 2; n.w = w; n.h = h; });

    // ring through the node centres; the boxes mask it, leaving four arrowed arcs
    c.ellipse(cx, cy, dx, dy, { stroke: C.gold, sw: 0.9, opacity: 0.75 });
    for (let k = 0; k < 4; k++) {
      const th = Math.PI / 4 + k * Math.PI / 2;
      const px = cx + dx * Math.cos(th), py = cy + dy * Math.sin(th);
      const tx = -dx * Math.sin(th), ty = dy * Math.cos(th);
      const L = Math.hypot(tx, ty);
      const ux = tx / L, uy = ty / L;
      c.line(px - ux * 0.30, py - uy * 0.30, px + ux * 0.22, py + uy * 0.22, {
        stroke: C.goldDeep, sw: 0.9, arrowEnd: true, arrowSize: 3.0,
      });
    }

    nodes.forEach(n => {
      card(c, n.x, n.y, n.w, n.h, { fill: C.paperWarm, stroke: C.rule });
      c.text(n.x + 0.1, n.y + 0.14, n.w - 0.2, n.title, { font: 'serif', size: 11.2, color: INK, align: 'center' });
      T(c, n.x + 0.1, n.y + 0.48, n.w - 0.2, n.sub, { size: 7.7, color: MUT, align: 'center', maxLines: 1 });
    });
    c.text(cx - 1.05, cy - 0.24, 2.1, 'CIRCULAR CAUSALITY', {
      caps: true, size: 7.2, letterSpacing: 1.9, color: C.goldDeep, align: 'center', bold: true,
    });
    T(c, cx - 1.0, cy + 0.02, 2.0, 'The sequence — not the person — is the unit of analysis.', {
      size: 8.2, italic: true, align: 'center', color: MUT, maxLines: 2,
    });

    const px = b.x + 8.35;
    c.text(px, b.y + 0.5, 3.2, 'Punctuation', { font: 'serif', size: 13, color: INK });
    T(c, px, b.y + 0.86, 3.2, 'Each member sees their own response as reasonable and the other’s as the cause. The therapist’s first move is to punctuate the sequence, not to assign blame.', { size: 8.3, color: MUT, lineHeight: 1.45 });
    c.line(px, b.y + 2.36, px + 2.4, b.y + 2.36, { stroke: C.rule, sw: 0.7 });
    c.text(px, b.y + 2.52, 3.2, 'Clinical implication', { font: 'serif', size: 13, color: INK });
    T(c, px, b.y + 2.88, 3.2, 'Ask “what happens next?” rather than “why did you do that?” Map the loop before attempting to change it.', { size: 8.3, color: MUT, lineHeight: 1.45 });
  },

  // ──────────────────────────────────────────────────────────────── Timeline ──
  timeline(c, b) {
    const x0 = b.x + 0.25, x1 = b.x + b.w - 0.25;
    const y = b.y + 2.05;
    c.line(x0, y, x1, y, { stroke: C.rule, sw: 1.0 });
    c.line(x0, y, x1, y, { stroke: C.gold, sw: 0.5, opacity: 0.55 });
    const events = [
      { y: '1940s', t: 'Child guidance & marriage counselling', d: 'two separate traditions' },
      { y: '1959', t: 'Palo Alto & the double bind', d: 'Bateson, Jackson, Haley, Weakland' },
      { y: '1965', t: 'Structural & strategic therapy', d: 'Minuchin · Haley · Madanes' },
      { y: '1971', t: 'Milan systemic therapy', d: 'hypothesising, circularity, neutrality' },
      { y: '1980s', t: 'Postmodern & EFT turns', d: 'narrative, solution-focused, attachment' },
      { y: '1990s', t: 'Evidence-based practice', d: 'manualised models, outcome research' },
      { y: '2010s', t: 'Integration & teletherapy', d: 'common factors, digital practice' },
    ];
    const step = (x1 - x0) / (events.length - 1);
    events.forEach((e, i) => {
      const cx = x0 + step * i;
      const up = i % 2 === 0;
      c.circle(cx, y, 0.055, { fill: C.paper, stroke: C.gold, sw: 1.0 });
      c.circle(cx, y, 0.018, { fill: C.goldDeep });
      const ly = up ? y - 1.42 : y + 0.42;
      if (up) c.line(cx, y - 0.08, cx, y - 0.5, { stroke: C.rule, sw: 0.6 });
      else c.line(cx, y + 0.08, cx, y + 0.38, { stroke: C.rule, sw: 0.6 });
      c.text(cx - 0.95, ly, 1.9, e.y, { font: 'serif', size: 15, color: C.goldDeep, align: 'center' });
      c.text(cx - 0.95, ly + 0.36, 1.9, e.t, { font: 'sans', size: 8.4, bold: true, color: INK, align: 'center', lineHeight: 1.2 });
      T(c, cx - 0.95, ly + 0.36 + (e.t.length > 24 ? 0.34 : 0.19), 1.9, e.d, { size: 7.4, color: MUT, align: 'center', lineHeight: 1.25 });
    });
    c.text(b.x, b.y + 4.02, b.w, 'A field born at the intersection of cybernetics, child guidance, and the clinic.', {
      size: 8.2, italic: true, color: MUT, align: 'center',
    });
  },

  // ─────────────────────────────────────────────────────────── Structural map ──
  structuralMap(c, b) {
    const x = b.x + 0.25;
    const y = b.y;
    const gm = [x + 2.10, y + 0.52];
    const gf = [x + 3.00, y + 0.52];
    const mo = [x + 2.10, y + 1.95];
    const fa = [x + 3.00, y + 1.95];
    const da = [x + 1.62, y + 3.36];
    const so = [x + 2.52, y + 3.36];
    const R = 0.25, S = 0.25;

    // generation 1
    c.circle(gm[0], gm[1], R, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
    c.rect(gf[0] - S, gf[1] - S, S * 2, S * 2, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
    c.line(gm[0] + S, gm[1], gf[0] - S, gf[1], { stroke: INK, sw: 1.1 });
    T(c, gm[0] - 0.62, gm[1] - 0.46, 1.24, 'Grandmother', { size: 7.4, align: 'center', color: MUT });
    T(c, gf[0] - 0.55, gf[1] - 0.46, 1.24, 'Grandfather', { size: 7.4, align: 'center', color: MUT });

    // descent to mother
    const mid1 = (gm[0] + gf[0]) / 2;
    c.line(mid1, gm[1] + S, mid1, y + 1.18, { stroke: INK, sw: 0.9 });
    c.line(mid1, y + 1.18, mo[0], y + 1.18, { stroke: INK, sw: 0.9 });
    c.line(mo[0], y + 1.18, mo[0], mo[1] - R, { stroke: INK, sw: 0.9 });

    // generation 2
    c.circle(mo[0], mo[1], R, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
    c.rect(fa[0] - S, fa[1] - S, S * 2, S * 2, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
    c.line(mo[0] + R, mo[1], fa[0] - S, fa[1], { stroke: INK, sw: 1.1 });
    T(c, mo[0] - 1.05, mo[1] - 0.09, 0.78, 'Mother', { size: 7.4, align: 'right', color: MUT });
    T(c, fa[0] + S + 0.1, fa[1] - 0.09, 0.9, 'Father', { size: 7.4, color: MUT });

    // conflict across the marriage line
    const zx = (mo[0] + fa[0]) / 2;
    c.line(zx - 0.03, mo[1] + 0.06, zx + 0.08, mo[1] + 0.15, { stroke: C.copper, sw: 1.1 });
    c.line(zx + 0.08, mo[1] + 0.05, zx - 0.07, mo[1] + 0.2, { stroke: C.copper, sw: 1.1 });

    // members below parental subsystem
    c.text(mo[0] - 0.7, mo[1] - 0.82, 2.35, 'PARENTAL SUBSYSTEM', {
      size: 6.3, color: C.sage, letterSpacing: 1.5, align: 'right',
    });

    // generation 3
    const mid2 = (mo[0] + fa[0]) / 2;
    c.line(mid2, fa[1] + S, mid2, y + 2.62, { stroke: INK, sw: 0.9 });
    c.line(da[0], y + 2.62, so[0], y + 2.62, { stroke: INK, sw: 0.9 });
    c.line(da[0], y + 2.62, da[0], da[1] - R, { stroke: INK, sw: 0.9 });
    c.line(so[0], y + 2.62, so[0], so[1] - S, { stroke: INK, sw: 0.9 });
    c.circle(da[0], da[1], R, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
    c.rect(so[0] - S, so[1] - S, S * 2, S * 2, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
    c.rect(so[0] - S - 0.05, so[1] - S - 0.05, (S + 0.05) * 2, (S + 0.05) * 2, { fill: 'none', stroke: INK, sw: 0.6 });

    // enmeshment: mother–daughter
    const dx = da[0] - mo[0], dy = da[1] - mo[1];
    const L = Math.hypot(dx, dy);
    const nx = -dy / L, ny = dx / L;
    [-0.032, 0, 0.032].forEach(off => {
      c.line(mo[0] + nx * off + dx / L * R, mo[1] + ny * off + dy / L * R,
        da[0] + nx * off - dx / L * R, da[1] + ny * off - dy / L * R,
        { stroke: C.copper, sw: 0.55 });
    });

    // boundaries
    c.rect(mo[0] - 0.66, mo[1] - 0.6, (fa[0] - mo[0]) + 1.32, 1.24, {
      fill: 'none', stroke: C.sage, sw: 0.8, dash: 'dash', radius: 0.16,
    });
    c.rect(da[0] - 0.5, da[1] - 0.52, (so[0] - da[0]) + 1.0, 1.06, {
      fill: 'none', stroke: C.sage, sw: 0.8, dash: 'dash', radius: 0.16,
    });
    c.text(da[0] - 0.5, da[1] + 0.72, (so[0] - da[0]) + 1.0, 'SIBLING SUBSYSTEM', {
      size: 6.3, color: C.sage, letterSpacing: 1.5, align: 'center',
    });
    T(c, da[0] - 0.6, da[1] + 0.34, 0.86, 'Daughter, 16', { size: 7.2, align: 'center', color: MUT, maxLines: 2 });
    T(c, so[0] - 0.44, so[1] + 0.34, 0.98, 'Son, 11 · IP', { size: 7.2, align: 'center', color: MUT, maxLines: 2 });

    // legend
    const lx = b.x + 6.55;
    const ly = b.y + 0.2;
    card(c, lx, ly, 4.72, 3.55, { fill: '#FDFAF3' });
    T(c, lx + 0.22, ly + 0.18, 4.2, 'Reading the map', { font: 'serif', size: 12.5, color: INK });
    const rows = [
      ['male', 'square'], ['female', 'circle'], ['deceased', 'cross'], ['marriage', 'double'],
      ['conflict', 'zigzag'], ['enmeshment', 'triple'], ['subsystem boundary', 'dash'], ['index patient', 'doublebox'],
    ];
    rows.forEach(([lab, type], i) => {
      const yy = ly + 0.64 + i * 0.36;
      const sx = lx + 0.3;
      if (type === 'square') c.rect(sx - 0.075, yy - 0.075, 0.15, 0.15, { fill: C.paperWarm, stroke: INK, sw: 0.7 });
      if (type === 'circle') c.circle(sx, yy, 0.078, { fill: C.paperWarm, stroke: INK, sw: 0.7 });
      if (type === 'cross') { c.rect(sx - 0.075, yy - 0.075, 0.15, 0.15, { fill: C.paperWarm, stroke: INK, sw: 0.7 }); c.line(sx - 0.075, yy - 0.075, sx + 0.075, yy + 0.075, { stroke: INK, sw: 0.6 }); c.line(sx - 0.075, yy + 0.075, sx + 0.075, yy - 0.075, { stroke: INK, sw: 0.6 }); }
      if (type === 'double') { c.line(sx - 0.14, yy - 0.02, sx + 0.14, yy - 0.02, { stroke: INK, sw: 0.6 }); c.line(sx - 0.14, yy + 0.03, sx + 0.14, yy + 0.03, { stroke: INK, sw: 0.6 }); }
      if (type === 'zigzag') { c.line(sx - 0.03, yy - 0.05, sx + 0.06, yy + 0.03, { stroke: C.copper, sw: 0.9 }); c.line(sx + 0.06, yy - 0.05, sx - 0.05, yy + 0.06, { stroke: C.copper, sw: 0.9 }); }
      if (type === 'triple') [-0.032, 0, 0.032].forEach(o => c.line(sx - 0.14, yy + o, sx + 0.14, yy + o, { stroke: C.copper, sw: 0.5 }));
      if (type === 'dash') c.line(sx - 0.16, yy, sx + 0.16, yy, { stroke: C.sage, sw: 0.8, dash: 'dash' });
      if (type === 'doublebox') { c.rect(sx - 0.085, yy - 0.085, 0.17, 0.17, { fill: 'none', stroke: INK, sw: 0.55 }); c.rect(sx - 0.06, yy - 0.06, 0.12, 0.12, { fill: 'none', stroke: INK, sw: 0.55 }); }
      T(c, sx + 0.32, yy - 0.075, 3.6, lab, { size: 8.4, color: SOFT });
    });
    T(c, lx + 0.22, ly + 3.34, 4.3, 'Conventions after McGoldrick, Gerson & Petry (2008).', { size: 6.8, color: MUT, italic: true });
  },

  // ───────────────────────────────────────────────────────────── Bowen triangle ──
  triangle(c, b) {
    const cx = b.x + 3.2;
    const top = [cx, b.y + 0.55];
    const left = [cx - 2.25, b.y + 3.35];
    const right = [cx + 2.25, b.y + 3.35];
    const R = 0.62;
    c.poly([top, right, left], { closed: true, stroke: C.rule, sw: 1.2 });
    [[top, right], [right, left], [left, top]].forEach(([a, bb]) => {
      const dx = bb[0] - a[0], dy = bb[1] - a[1];
      const L = Math.hypot(dx, dy);
      const ux = dx / L, uy = dy / L;
      c.line(a[0] + ux * R, a[1] + uy * R, bb[0] - ux * R, bb[1] - uy * R, { stroke: C.goldDeep, sw: 0.9, arrowStart: true, arrowEnd: true, arrowSize: 3.4 });
    });
    const people = [
      { p: top, label: 'Spouse A', sub: 'pursuer' },
      { p: right, label: 'Child', sub: 'the third point' },
      { p: left, label: 'Spouse B', sub: 'distancer' },
    ];
    people.forEach(({ p, label, sub }) => {
      c.circle(p[0], p[1], R, { fill: C.paperWarm, stroke: C.gold, sw: 0.9 });
      c.text(p[0] - R, p[1] - 0.22, R * 2, label, { font: 'serif', size: 11, align: 'center', color: INK });
      T(c, p[0] - R, p[1] + 0.03, R * 2, sub, { size: 7.2, align: 'center', color: MUT, caps: true, letterSpacing: 0.8 });
    });
    c.text(cx - 1.2, b.y + 1.85, 2.4, 'TRIANGULATION', { caps: true, size: 7.4, letterSpacing: 2, color: C.goldDeep, align: 'center', bold: true });
    T(c, cx - 1.35, b.y + 2.08, 2.7, 'Anxiety between two people recruits a third. The triangle stabilises the system — and freezes the symptom.', { size: 8.0, italic: true, align: 'center', color: MUT, lineHeight: 1.35 });

    const px = b.x + 7.55;
    T(c, px, b.y + 0.45, 3.85, 'What the therapist watches', { font: 'serif', size: 13.5, color: INK });
    const items = [
      ['1', 'Who is drawn in when tension rises?'],
      ['2', 'Which side of the triangle carries the symptom?'],
      ['3', 'Can each dyad be strengthened without the third?'],
    ];
    items.forEach(([n, s], i) => {
      const yy = b.y + 1.0 + i * 1.06;
      num(c, px + 0.11, yy + 0.13, 0.13, n, { fill: 'none', stroke: C.gold, color: C.goldDeep, size: 7.6 });
      T(c, px + 0.38, yy, 3.25, s, { size: 9.2, color: SOFT, lineHeight: 1.35 });
    });
    c.line(px, b.y + 3.7, px + 3.4, b.y + 3.7, { stroke: C.rule, sw: 0.6 });
    T(c, px, b.y + 3.82, 3.5, 'Detriangling begins with the therapist staying out of the triangle.', { size: 7.8, italic: true, color: MUT, lineHeight: 1.35 });
  },

  // ─────────────────────────────────────────────────────────── Satir stances ──
  stances(c, b) {
    const gap = 0.24;
    const w = (b.w - 0.2 - gap * 3) / 4;
    const items = [
      { n: '01', title: 'Placator', line: '“Whatever you want.”', cost: 'Self erased to keep the peace.', ang: 38 },
      { n: '02', title: 'Blamer', line: '“It is all your fault.”', cost: 'Connection traded for control.', ang: -38 },
      { n: '03', title: 'Super-reasonable', line: '“Let us be logical.”', cost: 'Feeling exiled from the room.', ang: 0 },
      { n: '04', title: 'Irrelevant', line: '“Anyway — did you see…?”', cost: 'The real subject never lands.', ang: 62 },
    ];
    items.forEach((it, i) => {
      const x = b.x + 0.1 + i * (w + gap);
      card(c, x, b.y + 0.12, w, 3.15, { fill: '#FDFAF3' });
      const gx = x + w / 2;
      const gy = b.y + 1.05;
      c.circle(gx, gy - 0.28, 0.115, { fill: 'none', stroke: C.goldDeep, sw: 0.9 });
      const a = (it.ang * Math.PI) / 180;
      c.line(gx, gy - 0.16, gx + Math.sin(a) * 0.55, gy + Math.cos(a) * 0.55, { stroke: C.goldDeep, sw: 1.0 });
      c.circle(gx, gy - 0.28, 0.36, { stroke: C.rule, sw: 0.5, opacity: 0.6 });
      T(c, x + 0.14, b.y + 0.28, w - 0.28, it.n, { size: 7, letterSpacing: 1.6, color: C.goldDeep, caps: true });
      c.text(x + 0.14, b.y + 1.62, w - 0.28, it.title, { font: 'serif', size: 14.5, color: INK });
      T(c, x + 0.14, b.y + 1.98, w - 0.28, it.line, { size: 8.6, italic: true, color: C.goldDeep });
      c.line(x + 0.14, b.y + 2.42, x + 0.62, b.y + 2.42, { stroke: C.rule, sw: 0.6 });
      T(c, x + 0.14, b.y + 2.55, w - 0.28, it.cost, { size: 8.0, color: MUT, lineHeight: 1.3 });
    });
    c.text(b.x + 0.1, b.y + 3.62, b.w - 0.2, 'The goal is not a fifth stance but congruence — the body, the words and the feeling saying the same thing.', {
      size: 8.6, italic: true, color: C.goldDeep, align: 'center',
    });
  },

  // ─────────────────────────────────────────────────── Modern / postmodern grid ──
  matrix(c, b) {
    const leftW = 2.35;
    const colW = (b.w - leftW - 0.3) / 2;
    const x0 = b.x + 0.1;
    const y0 = b.y + 0.1;
    const rowH = 0.74;
    c.text(x0 + leftW + 0.15, y0, colW, 'First-order systemic', { font: 'serif', size: 15, color: INK });
    c.text(x0 + leftW + 0.15 + colW, y0, colW, 'Postmodern / constructivist', { font: 'serif', size: 15, color: INK });
    c.line(x0 + leftW + 0.15, y0 + 0.42, x0 + b.w - 0.1, y0 + 0.42, { stroke: C.gold, sw: 0.9 });

    const rows = [
      ['Locus of meaning', 'In structure and interaction patterns observable by the therapist', 'In language, story and relationship; meanings are co-created'],
      ['Therapist stance', 'Expert observer and agent of change', 'Curious co-author; not-knowing'],
      ['Use of diagnosis', 'Descriptive; guides systemic intervention', 'Provisional; risks totalising the family'],
      ['Mechanism of change', 'Restructure, reframe, interrupt sequences', 'Deconstruct, re-author, open new meanings'],
      ['Signature methods', 'Enactment, directives, genograms, boundaries', 'Reflecting teams, externalising, miracle question'],
    ];
    rows.forEach((r, i) => {
      const y = y0 + 0.62 + i * rowH;
      if (i % 2 === 0) c.rect(x0, y - 0.08, b.w - 0.1, rowH - 0.04, { fill: C.parchment, opacity: 0.28 });
      c.text(x0, y + 0.05, leftW - 0.1, r[0], { size: 8.4, bold: true, color: C.goldDeep, caps: true, letterSpacing: 0.9 });
      T(c, x0 + leftW + 0.15, y, colW - 0.2, r[1], { size: 8.6, color: SOFT, lineHeight: 1.3 });
      T(c, x0 + leftW + 0.15 + colW, y, colW - 0.2, r[2], { size: 8.6, color: SOFT, lineHeight: 1.3 });
      c.line(x0, y + rowH - 0.12, x0 + b.w - 0.1, y + rowH - 0.12, { stroke: C.rule, sw: 0.5, opacity: 0.7 });
    });
    c.line(x0 + leftW, y0 + 0.62, x0 + leftW, y0 + 0.62 + 5 * rowH - 0.1, { stroke: C.rule, sw: 0.6 });
    c.line(x0 + leftW + 0.15 + colW, y0 + 0.62, x0 + leftW + 0.15 + colW, y0 + 0.62 + 5 * rowH - 0.1, { stroke: C.rule, sw: 0.6 });
  },

  // ──────────────────────────────────────────────── Four-model formulation grid ──
  formulation(c, b) {
    const x0 = b.x + 0.05, y0 = b.y + 0.05;
    const cols = [1.95, 3.05, 3.15, 3.15];
    const rows = [
      ['Structural', 'Boundaries, hierarchy, subsystems', 'Enmeshed or disengaged boundaries; cross-generational coalitions', 'Enactment, boundary-making, unbalancing'],
      ['Strategic', 'Attempted solutions maintaining the problem', 'Circular feedback; power in the symptom', 'Directives, paradoxical tasks, reframing'],
      ['Intergenerational', 'Differentiation and multigenerational transmission', 'Triangulation; unresolved legacy and loyalty', 'Genogram, detriangling, coaching the dyad'],
      ['Narrative', 'Dominant stories and their effects', 'Problem-saturated identity; internalised deficit', 'Externalising, unique outcomes, re-authoring'],
    ];
    const headY = y0;
    c.rect(x0, headY, b.w - 0.1, 0.46, { fill: C.ink });
    const heads = ['Model', 'Focus of formulation', 'Mechanism of the problem', 'Signature intervention'];
    let cx = x0;
    heads.forEach((h, i) => {
      c.text(cx + 0.12, headY, cols[i] - 0.2, h, {
        size: 7.4, bold: true, color: C.goldLight, caps: true, letterSpacing: 1.3, valign: 'middle', boxH: 0.46, lineHeight: 1.2,
      });
      cx += cols[i];
    });
    rows.forEach((r, i) => {
      const y = headY + 0.46 + i * 0.88;
      if (i % 2 === 0) c.rect(x0, y, b.w - 0.1, 0.88, { fill: C.parchment, opacity: 0.3 });
      let xx = x0;
      r.forEach((cell, j) => {
        if (j === 0) {
          c.text(xx + 0.12, y, cols[j] - 0.18, cell, { font: 'serif', size: 12.5, color: INK, valign: 'middle', boxH: 0.88, lineHeight: 1.2 });
        } else {
          T(c, xx + 0.12, y + 0.1, cols[j] - 0.24, cell, { size: 8.1, color: SOFT, lineHeight: 1.3, valign: 'middle', boxH: 0.7 });
        }
        xx += cols[j];
      });
      c.line(x0, y + 0.86, x0 + b.w - 0.1, y + 0.86, { stroke: C.rule, sw: 0.55 });
    });
    let xx = x0;
    cols.slice(0, -1).forEach(w => { xx += w; c.line(xx, headY + 0.46, xx, headY + 0.46 + 4 * 0.88, { stroke: C.rule, sw: 0.5, opacity: 0.8 }); });
  },

  // ────────────────────────────────────────────────────────── Alliance map ──
  alliance(c, b) {
    const cx = b.x + 3.0;
    const th = [cx, b.y + 0.5];
    const members = [
      { x: b.x + 0.95, y: b.y + 3.25, label: 'Mother', shape: 'circle' },
      { x: b.x + 2.9, y: b.y + 3.45, label: 'Father', shape: 'square' },
      { x: b.x + 4.85, y: b.y + 3.25, label: 'Adolescent', shape: 'square' },
    ];
    c.circle(th[0], th[1], 0.45, { fill: C.ink, stroke: C.gold, sw: 0.8 });
    c.text(th[0] - 0.45, th[1] - 0.16, 0.9, 'Th', { font: 'serif', size: 12, color: C.goldLight, align: 'center' });
    c.text(th[0] - 1.5, th[1] - 0.09, 0.95, 'therapist', { size: 6.8, color: MUT, align: 'right', caps: true, letterSpacing: 1.2 });

    members.forEach((m, i) => {
      const strong = i === 0 || i === 1;
      const [ex, ey] = edgePoint(th[0], th[1], 0.9, 0.9, m.x, m.y);
      c.line(ex, ey, m.x, m.y - 0.3, { stroke: strong ? C.goldDeep : C.rule, sw: strong ? 1.5 : 0.7, dash: strong ? undefined : 'dash' });
      if (m.shape === 'circle') c.circle(m.x, m.y, 0.28, { fill: C.paperWarm, stroke: INK, sw: 1.0 });
      else { c.rect(m.x - 0.28, m.y - 0.28, 0.56, 0.56, { fill: C.paperWarm, stroke: INK, sw: 1.0 }); }
      T(c, m.x - 0.6, m.y + 0.36, 1.2, m.label, { size: 7.6, align: 'center', color: MUT });
    });
    // split alliance between parents
    c.line(members[0].x + 0.3, members[0].y + 0.14, members[1].x - 0.3, members[1].y + 0.14, { stroke: C.copper, sw: 1.1, dash: 'dash' });
    c.text(b.x + 1.45, b.y + 2.58, 1.8, 'SPLIT ALLIANCE', { size: 6.6, color: C.copper, caps: true, letterSpacing: 1.3, align: 'center' });

    const px = b.x + 7.35;
    T(c, px, b.y + 0.35, 4.0, 'Reading the alliance map', { font: 'serif', size: 13.5, color: INK });
    const pts = [
      ['Triadic by nature', 'Every statement is heard by more than one person, and heard differently.'],
      ['Split alliances', 'A strong bond with one member, paid for by distance from another, reproduces the family’s own triangle.'],
      ['Repair in session', 'Name the rupture, validate both positions, and re-establish the therapist as available to all.'],
    ];
    pts.forEach(([h, s], i) => {
      const y = b.y + 0.95 + i * 1.12;
      c.line(px, y + 0.06, px + 0.28, y + 0.06, { stroke: C.gold, sw: 1.2 });
      T(c, px + 0.4, y - 0.06, 3.35, h, { size: 9.4, bold: true, color: INK });
      T(c, px + 0.4, y + 0.21, 3.35, s, { size: 8.2, color: MUT, lineHeight: 1.35 });
    });
    T(c, b.x + 0.35, b.y + 4.02, 5.0, 'Solid line: strong alliance  ·  dashed: weak or cut-off.', { size: 7, italic: true, color: MUT });
  },

  // ───────────────────────────────────────────────────────────────── Genogram ──
  genogram(c, b) {
    const y = b.y;
    const sq = 0.34;
    // generation 1
    const gm = [b.x + 1.55, y + 0.55], gf = [b.x + 2.35, y + 0.55];
    c.circle(gm[0], gm[1], 0.19, { fill: C.paperWarm, stroke: INK, sw: 0.9 });
    c.rect(gf[0] - 0.19, gf[1] - 0.19, 0.38, 0.38, { fill: C.paperWarm, stroke: INK, sw: 0.9 });
    c.line(gm[0] + 0.19, gm[1], gf[0] - 0.19, gf[1], { stroke: INK, sw: 0.9 });
    T(c, gm[0] - 0.62, gm[1] - 0.40, 1.2, 'Grandmother', { size: 6.6, align: 'center', color: MUT });
    T(c, gf[0] - 0.60, gf[1] - 0.40, 1.2, 'Grandfather', { size: 6.6, align: 'center', color: MUT });
    // gen 2
    const mo = [b.x + 1.55, y + 1.85], fa = [b.x + 2.35, y + 1.85];
    c.line((gm[0] + gf[0]) / 2, gm[1] + 0.19, (gm[0] + gf[0]) / 2, y + 1.25, { stroke: INK, sw: 0.8 });
    c.line((gm[0] + gf[0]) / 2, y + 1.25, mo[0], y + 1.25, { stroke: INK, sw: 0.8 });
    c.line(mo[0], y + 1.25, mo[0], mo[1] - 0.19, { stroke: INK, sw: 0.8 });
    c.circle(mo[0], mo[1], 0.19, { fill: C.paperWarm, stroke: INK, sw: 0.9 });
    c.rect(fa[0] - 0.19, fa[1] - 0.19, 0.38, 0.38, { fill: C.paperWarm, stroke: INK, sw: 0.9 });
    c.line(mo[0] + 0.19, mo[1], fa[0] - 0.19, fa[1], { stroke: INK, sw: 0.9 });
    T(c, mo[0] - 1.15, mo[1] - 0.10, 0.85, 'Mother, 44', { size: 6.6, align: 'right', color: MUT });
    T(c, fa[0] + 0.30, fa[1] - 0.10, 1.0, 'Father, 47', { size: 6.6, align: 'left', color: MUT });
    // gen 3
    const kids = [[b.x + 0.95, y + 3.15], [b.x + 1.75, y + 3.15], [b.x + 2.55, y + 3.15]];
    const mid = (mo[0] + fa[0]) / 2;
    c.line(mid, mo[1] + 0.19, mid, y + 2.65, { stroke: INK, sw: 0.8 });
    c.line(kids[0][0], y + 2.65, kids[2][0], y + 2.65, { stroke: INK, sw: 0.8 });
    kids.forEach(([kx, ky], i) => {
      c.line(kx, y + 2.65, kx, ky - 0.19, { stroke: INK, sw: 0.8 });
      if (i === 1) c.rect(kx - 0.19, ky - 0.19, 0.38, 0.38, { fill: C.paperWarm, stroke: INK, sw: 0.9 });
      else c.circle(kx, ky, 0.19, { fill: C.paperWarm, stroke: INK, sw: 0.9 });
      if (i === 2) { c.rect(kx - 0.23, ky - 0.23, 0.46, 0.46, { fill: 'none', stroke: INK, sw: 0.6 }); }
    });
    T(c, kids[0][0] - 0.55, y + 3.42, 1.1, 'Daughter, 17', { size: 6.6, align: 'center', color: MUT });
    T(c, kids[1][0] - 0.55, y + 3.42, 1.1, 'Son, 14', { size: 6.6, align: 'center', color: MUT });
    T(c, kids[2][0] - 0.55, y + 3.48, 1.1, 'Daughter, 9\nIP', { size: 6.6, align: 'center', color: C.goldDeep, lineHeight: 1.1 });
    // close relationship mother–daughter, clipped to the figures
    {
      const ddx = kids[0][0] - mo[0], ddy = (y + 3.15) - mo[1];
      const dl = Math.hypot(ddx, ddy), ux = ddx / dl, uy = ddy / dl, nx = -uy, ny = ux;
      [-0.03, 0, 0.03].forEach(o => c.line(
        mo[0] + ux * 0.19 + nx * o, mo[1] + uy * 0.19 + ny * o,
        kids[0][0] - ux * 0.19 + nx * o, (y + 3.15) - uy * 0.19 + ny * o,
        { stroke: C.sage, sw: 0.5, opacity: 0.9 },
      ));
    }
    // conflict parents
    c.line(mid, mo[1] + 0.05, mid + 0.09, mo[1] + 0.15, { stroke: C.copper, sw: 1.0 });
    c.line(mid + 0.09, mo[1] + 0.03, mid - 0.06, mo[1] + 0.2, { stroke: C.copper, sw: 1.0 });

    // legend
    const lx = b.x + 4.55;
    card(c, lx, y + 0.15, 4.6, 3.72, { fill: '#FDFAF3' });
    T(c, lx + 0.22, y + 0.3, 4.2, 'Genogram conventions', { font: 'serif', size: 12, color: INK });
    const rows = [
      ['male', 'square'], ['female', 'circle'], ['index patient', 'index'], ['deceased', 'cross'],
      ['marriage', 'marriage'], ['conflict', 'zigzag'], ['close / fused', 'triple'], ['cut-off', 'cut'],
    ];
    rows.forEach(([lab, type], i) => {
      const yy = y + 0.72 + i * 0.36;
      const sx = lx + 0.34;
      if (type === 'square') c.rect(sx - 0.075, yy - 0.075, 0.15, 0.15, { fill: C.paperWarm, stroke: INK, sw: 0.7 });
      if (type === 'circle') c.circle(sx, yy, 0.075, { fill: C.paperWarm, stroke: INK, sw: 0.7 });
      if (type === 'index') { c.rect(sx - 0.08, yy - 0.08, 0.16, 0.16, { fill: 'none', stroke: INK, sw: 0.55 }); c.rect(sx - 0.055, yy - 0.055, 0.11, 0.11, { fill: 'none', stroke: INK, sw: 0.55 }); }
      if (type === 'cross') { c.rect(sx - 0.075, yy - 0.075, 0.15, 0.15, { fill: C.paperWarm, stroke: INK, sw: 0.7 }); c.line(sx - 0.075, yy - 0.075, sx + 0.075, yy + 0.075, { stroke: INK, sw: 0.6 }); c.line(sx - 0.075, yy + 0.075, sx + 0.075, yy - 0.075, { stroke: INK, sw: 0.6 }); }
      if (type === 'marriage') { c.line(sx - 0.14, yy - 0.025, sx + 0.14, yy - 0.025, { stroke: INK, sw: 0.6 }); c.line(sx - 0.14, yy + 0.03, sx + 0.14, yy + 0.03, { stroke: INK, sw: 0.6 }); }
      if (type === 'zigzag') c.poly([[sx - 0.14, yy - 0.05], [sx - 0.05, yy + 0.04], [sx + 0.04, yy - 0.05], [sx + 0.12, yy + 0.04]], { stroke: C.copper, sw: 0.9 });
      if (type === 'triple') [-0.035, 0, 0.035].forEach(o => c.line(sx - 0.14, yy + o, sx + 0.14, yy + o, { stroke: C.sage, sw: 0.5 }));
      if (type === 'cut') {
        c.line(sx - 0.15, yy, sx + 0.15, yy, { stroke: INK, sw: 0.5 });
        c.line(sx - 0.07, yy - 0.06, sx - 0.01, yy + 0.06, { stroke: C.copper, sw: 0.8 });
        c.line(sx + 0.01, yy - 0.06, sx + 0.07, yy + 0.06, { stroke: C.copper, sw: 0.8 });
      }
      T(c, sx + 0.3, yy - 0.065, 3.5, lab, { size: 8.2, color: SOFT });
    });
    c.text(lx + 0.22, y + 3.46, 4.2, 'Three generations, one view: pattern, not blame.', { size: 6.9, italic: true, color: MUT });
  },

  // ─────────────────────────────────────────────────────── Confidentiality tree ──
  ethicsTree(c, b) {
    const cx = b.x + 2.55;
    const bw = 4.55;
    const rows = [
      { y: b.y + 0.1, h: 0.72, text: 'A family member asks you to keep a secret from the others', fill: C.ink, color: C.paper, size: 9.4 },
      { y: b.y + 1.12, h: 0.78, text: 'Is there a legal duty to disclose, or a serious risk of harm?', fill: C.parchment, color: INK, size: 9.2, q: true },
      { y: b.y + 2.24, h: 0.78, text: 'Does the third party have a legitimate claim to the information?', fill: C.parchment, color: INK, size: 9.2, q: true },
      { y: b.y + 3.36, h: 0.62, text: 'Document the decision, the rationale, and the consultation', fill: C.ink, color: C.paper, size: 8.8 },
    ];
    rows.forEach(r => {
      card(c, cx - bw / 2, r.y, bw, r.h, { fill: r.fill, stroke: r.q ? C.gold : 'none' });
      c.text(cx - bw / 2 + 0.18, r.y, bw - 0.36, r.text, {
        size: r.size, color: r.color, align: 'center', valign: 'middle', boxH: r.h, lineHeight: 1.25,
      });
    });
    for (let i = 0; i < 3; i++) {
      const y1 = rows[i].y + rows[i].h;
      const y2 = rows[i + 1].y;
      c.line(cx, y1 + 0.03, cx, y2 - 0.05, { stroke: C.goldDeep, sw: 0.9, arrowEnd: true, arrowSize: 3.2 });
      if (i < 2) c.text(cx + 0.08, (y1 + y2) / 2 - 0.14, 0.5, 'NO', { size: 6.4, color: C.goldDeep, bold: true, letterSpacing: 0.8 });
    }
    // branch 1
    const bx = b.x + 6.05, bw2 = 4.6;
    card(c, bx, rows[1].y - 0.05, bw2, 0.9, { fill: '#FDFAF3', stroke: C.copper });
    T(c, bx + 0.16, rows[1].y + 0.06, bw2 - 0.3, 'Disclose to the minimum necessary. Consult your supervisor, follow the governing statute, and record what you did and why.', { size: 8.0, color: SOFT, lineHeight: 1.3 });
    c.line(cx + bw / 2 + 0.02, rows[1].y + 0.39, bx - 0.06, rows[1].y + 0.39, { stroke: C.copper, sw: 0.9, arrowEnd: true, arrowSize: 3.2 });
    c.text(cx + bw / 2 + 0.12, rows[1].y + 0.14, 0.6, 'YES', { size: 6.4, color: C.copper, bold: true, letterSpacing: 0.8 });

    // branch 2
    card(c, bx, rows[2].y - 0.05, bw2, 0.9, { fill: '#FDFAF3', stroke: C.sage });
    T(c, bx + 0.16, rows[2].y + 0.06, bw2 - 0.3, 'Obtain a written, informed release that names the recipient and the scope of information to be shared.', { size: 8.0, color: SOFT, lineHeight: 1.3 });
    c.line(cx + bw / 2 + 0.02, rows[2].y + 0.39, bx - 0.06, rows[2].y + 0.39, { stroke: C.sage, sw: 0.9, arrowEnd: true, arrowSize: 3.2 });
    c.text(cx + bw / 2 + 0.12, rows[2].y + 0.14, 0.6, 'YES', { size: 6.4, color: C.sage, bold: true, letterSpacing: 0.8 });
    c.line(cx, rows[2].y + rows[2].h + 0.02, cx, rows[3].y - 0.05, { stroke: C.goldDeep, sw: 0.9, arrowEnd: true, arrowSize: 3.2 });
    c.text(cx + 0.08, rows[2].y + rows[2].h + 0.1, 0.6, 'NO', { size: 6.4, color: C.goldDeep, bold: true, letterSpacing: 0.8 });
  },

  // ─────────────────────────────────────────────────────── Cultural kaleidoscope ──
  addressing(c, b) {
    const cx = b.x + 3.55, cy = b.y + b.h / 2;
    c.circle(cx, cy, 0.92, { fill: C.parchment, stroke: C.gold, sw: 0.8 });
    c.text(cx - 0.8, cy - 0.3, 1.6, 'Cultural\nhumility', { font: 'serif', size: 13, color: INK, align: 'center', lineHeight: 1.15 });
    T(c, cx - 0.8, cy + 0.3, 1.6, 'a stance, not a technique', { size: 7, align: 'center', color: MUT, italic: true });

    const items = [
      'Age & generation', 'Disability status', 'Religion & spirituality', 'Ethnic identity',
      'Socio-economic status', 'Sexual orientation', 'Gender', 'Indigenous heritage', 'National origin',
    ];
    items.forEach((label, i) => {
      const ang = -Math.PI / 2 + (i * 2 * Math.PI) / items.length;
      const rx = 3.05, ry = 1.72;
      const px = cx + rx * Math.cos(ang);
      const py = cy + ry * Math.sin(ang);
      c.line(cx + 0.92 * Math.cos(ang), cy + 0.92 * Math.sin(ang), px, py, { stroke: C.rule, sw: 0.6 });
      c.circle(px, py, 0.035, { fill: C.gold });
      const w = 1.9;
      c.text(px - w / 2, py - 0.23, w, label, { size: 7.8, color: SOFT, align: 'center', lineHeight: 1.15, maxLines: 2 });
    });
    const px = b.x + 7.6;
    T(c, px, b.y + 0.35, 3.9, 'Working principles', { font: 'serif', size: 13.5, color: INK });
    const pts = [
      ['Self-reflection', 'Notice your own cultural location, assumptions and discomfort.'],
      ['Power', 'Ask who is speaking, who is being spoken about, and who is absent.'],
      ['Learning', 'Treat the family as the expert on its own culture; remain a learner.'],
    ];
    pts.forEach(([h, s], i) => {
      const y = b.y + 0.95 + i * 1.05;
      num(c, px + 0.11, y + 0.12, 0.12, i + 1, { fill: 'none', stroke: C.gold, color: C.goldDeep, size: 7.2 });
      T(c, px + 0.38, y - 0.04, 3.3, h, { size: 9.4, bold: true, color: INK });
      T(c, px + 0.38, y + 0.23, 3.3, s, { size: 8.2, color: MUT, lineHeight: 1.35 });
    });
    T(c, b.x + 0.3, b.y + 4.02, 6.3, 'Framework adapted from Hays (2016); see also Hardy & Laszloffy (1995) on the cultural genogram.', { size: 7, italic: true, color: MUT });
  },

  // ───────────────────────────────────────────────────── Developmental timeline ──
  devTimeline(c, b) {
    const stages = [
      ['0–3', 'Infancy & toddlerhood', 'Attachment, regulation, co-regulation', 'Include caregivers; observe the dyad'],
      ['4–6', 'Early childhood', 'Language, play, initiative', 'Play-based methods; parent guidance'],
      ['7–11', 'Middle childhood', 'School, peers, competence', 'School–family liaison; structure'],
      ['12–18', 'Adolescence', 'Identity, autonomy, sexuality', 'Negotiate privacy; alliance with teen'],
      ['19+', 'Emerging adulthood', 'Launching, individuation', 'Re-contract the parent–child bond'],
    ];
    const w = (b.w - 0.2) / stages.length;
    const y0 = b.y + 0.55;
    c.rect(b.x, y0, b.w, 0.46, { fill: C.ink });
    stages.forEach((s, i) => {
      const x = b.x + i * w;
      c.text(x, y0, w, s[0], { font: 'serif', size: 14, color: C.goldLight, align: 'center', valign: 'middle', boxH: 0.46 });
      c.text(x, y0 + 0.6, w, s[1], { font: 'serif', size: 11.2, color: INK, align: 'center', lineHeight: 1.15 });
      T(c, x + 0.12, y0 + 1.34, w - 0.24, s[2], { size: 8.0, color: MUT, align: 'center', lineHeight: 1.35 });
      c.line(x + 0.22, y0 + 2.02, x + w - 0.22, y0 + 2.02, { stroke: C.rule, sw: 0.6 });
      T(c, x + 0.12, y0 + 2.2, w - 0.24, s[3], { size: 8.2, color: SOFT, align: 'center', lineHeight: 1.35 });
      c.text(x, y0 + 2.6, w, 'CLINICAL FOCUS', { size: 6.0, color: C.goldDeep, letterSpacing: 1.2, caps: true, align: 'center', opacity: 0.75 });
      if (i > 0) c.line(x, y0 + 0.55, x, y0 + 3.4, { stroke: C.rule, sw: 0.5, opacity: 0.6 });
    });
    c.line(b.x, y0 + 2.92, b.x + b.w, y0 + 2.92, { stroke: C.gold, sw: 0.7, opacity: 0.55 });
    T(c, b.x, y0 + 3.05, b.w, 'Development is not a backdrop to family life — it is one of the family’s organising constraints.', { size: 8.0, italic: true, color: MUT, align: 'center' });
  },

  // ─────────────────────────────────────────────────────────── Negative cycle ──
  cycle(c, b) {
    const cx = b.x + 3.6;
    const w = 2.55, h = 0.96;
    const top = b.y + 0.42;
    const left = { x: cx - 3.05, y: top, w: 2.45, h };
    const right = { x: cx + 0.6, y: top, w: 2.45, h };
    const fear = { x: cx - 1.28, y: top + 1.95, w: 2.56, h: 0.98 };

    card(c, left.x, left.y, 2.45, h, { fill: C.paperWarm, stroke: C.rule });
    c.text(left.x + 0.1, left.y + 0.15, 2.25, 'Pursuer', { font: 'serif', size: 12.4, color: INK, align: 'center' });
    T(c, left.x + 0.1, left.y + 0.52, 2.25, 'protest, criticism, pursuit', { size: 7.8, color: MUT, align: 'center' });

    card(c, right.x, right.y, 2.45, h, { fill: C.paperWarm, stroke: C.rule });
    c.text(right.x + 0.1, right.y + 0.15, 2.25, 'Withdrawer', { font: 'serif', size: 12.4, color: INK, align: 'center' });
    T(c, right.x + 0.1, right.y + 0.52, 2.25, 'silence, distance, shutdown', { size: 7.8, color: MUT, align: 'center' });

    // mutual arrow between the two positions
    c.line(cx - 0.48, top + 0.30, cx + 0.44, top + 0.30, { stroke: C.goldDeep, sw: 1.0, arrowEnd: true, arrowSize: 4.2 });
    c.line(cx + 0.44, top + 0.64, cx - 0.48, top + 0.64, { stroke: C.goldDeep, sw: 1.0, arrowEnd: true, arrowSize: 4.2 });
    c.text(cx - 0.72, top - 0.16, 1.44, 'MUTUAL TRIGGER', { size: 6.0, letterSpacing: 1.4, color: C.goldDeep, align: 'center', caps: true });

    card(c, fear.x, fear.y, fear.w, fear.h, { fill: C.ink, stroke: C.gold, sw: 0.6 });
    c.text(fear.x + 0.12, fear.y + 0.16, fear.w - 0.24, 'ATTACHMENT FEAR', { size: 6.2, letterSpacing: 1.5, color: C.gold, align: 'center', caps: true });
    c.text(fear.x + 0.12, fear.y + 0.42, fear.w - 0.24, '“I do not matter to you”', { font: 'serif', size: 11, italic: true, color: C.paperWarm, align: 'center' });

    c.line(cx - 1.5, fear.y - 0.04, cx - 1.5, top + h + 0.06, { stroke: C.gold, sw: 0.8, arrowEnd: false });
    c.line(cx + 1.5, fear.y - 0.04, cx + 1.5, top + h + 0.06, { stroke: C.gold, sw: 0.8 });
    c.circle(cx - 1.5, fear.y - 0.06, 0.032, { fill: C.gold });
    c.circle(cx + 1.5, fear.y - 0.06, 0.032, { fill: C.gold });
    T(c, cx + 1.72, fear.y - 0.2, 1.75, 'beneath both moves, one fear', { size: 7.0, italic: true, color: MUT, align: 'left', maxLines: 2 });

    const px = b.x + 7.5;
    c.text(px, b.y + 0.34, 3.9, 'Interrupting the cycle', { font: 'serif', size: 13.5, color: INK });
    const steps = [
      ['Name it', '“Can we slow this down and look at the loop together?”'],
      ['Validate both', 'Each response makes sense given the attachment fear beneath it.'],
      ['Create a new move', 'Risk a softer signal; respond with accessibility and responsiveness.'],
    ];
    steps.forEach(([h2, s2], i) => {
      const y = b.y + 0.94 + i * 1.12;
      num(c, px + 0.11, y + 0.13, 0.13, i + 1, { fill: 'none', stroke: C.gold, color: C.goldDeep, size: 7.4 });
      T(c, px + 0.4, y - 0.04, 3.25, h2, { size: 9.4, bold: true, color: INK });
      T(c, px + 0.4, y + 0.23, 3.25, s2, { size: 8.2, color: MUT, lineHeight: 1.35 });
    });
  },

  // ─────────────────────────────────────────────────────────── Family life cycle ──
  lifeCycle(c, b) {
    const stages = [
      ['Leaving home', 'Differentiate without cutting off'],
      ['Joining families', 'Negotiate a new couple system'],
      ['Young children', 'Expand the system; share care'],
      ['Adolescents', 'Increase flexibility; open boundaries'],
      ['Launching', 'Re-negotiate the couple bond'],
      ['Later life', 'Accept shifts in roles and loss'],
    ];
    const x0 = b.x + 0.3;
    const stepW = (b.w - 0.6) / 6;
    const baseY = b.y + 3.62;
    const maxH = 1.9;

    stages.forEach((s2, i) => {
      const x = x0 + i * stepW;
      const h = 0.5 + (i * maxH) / 5.5;
      c.rect(x, baseY - h, stepW - 0.1, h, { fill: i % 2 ? C.parchment : '#EFE3CF', opacity: 0.5 });
      c.line(x, baseY - h, x + stepW - 0.1, baseY - h, { stroke: C.gold, sw: 1.0 });
      c.text(x + 0.1, baseY - h + 0.12, stepW - 0.28, s2[1], {
        size: 7.2, color: MUT, lineHeight: 1.25, maxLines: 3,
      });
      c.text(x, b.y + 0.98, stepW - 0.14, s2[0], {
        font: 'serif', size: 10.8, color: INK, lineHeight: 1.06, maxLines: 2,
      });
      c.text(x + stepW - 0.26, b.y + 0.62, 0.22, String(i + 1), {
        font: 'serif', size: 9.5, color: C.goldDeep, align: 'right',
      });
      if (i < stages.length - 1) {
        c.line(x + stepW - 0.1, baseY - h, x + stepW - 0.1, baseY, { stroke: C.rule, sw: 0.45, dash: 'dot' });
      }
    });
    c.line(x0, b.y + 1.62, x0 + stepW * 6 - 0.1, b.y + 1.62, { stroke: C.rule, sw: 0.5 });
    c.line(x0, baseY, x0 + stepW * 6 - 0.1, baseY, { stroke: C.gold, sw: 1.1 });
    T(c, x0, baseY + 0.16, 6.4, 'Vertical stressors  ·  family history, legacy, scripts', { size: 7.4, color: MUT, italic: true });
    T(c, x0 + 5.6, baseY + 0.16, 5.6, 'Horizontal stressors  ·  transitions, events, time', { size: 7.4, color: MUT, italic: true, align: 'right' });
    c.line(x0, b.y + 0.36, x0 + 0.5, b.y + 0.36, { stroke: C.copper, sw: 1.2 });
    T(c, x0 + 0.62, b.y + 0.26, 9.4, 'The symptom often appears at the transition, not inside the stage itself.', { size: 8.4, color: C.goldDeep, italic: true });
  },

  // ───────────────────────────────────────────────────────── Outcome feedback ──
  outcomes(c, b) {
    const cx = b.x + 2.62, cy = b.y + 2.0;
    const w = 2.05, h = 0.86;
    const nodes = [
      { t: 'Engage', s: 'alliance & goals', x: cx - w / 2, y: cy - 1.55 },
      { t: 'Measure', s: 'ORS / SRS each session', x: cx + 0.85, y: cy - 0.43 },
      { t: 'Review', s: 'with the client, openly', x: cx - w / 2, y: cy + 0.69 },
      { t: 'Adapt', s: 'plan, method, or therapist', x: cx - 1.95, y: cy - 0.43 },
    ];
    nodes.forEach(n => { n.cx = n.x + w / 2; n.cy = n.y + h / 2; n.w = w; n.h = h; });
    [[0, 1], [1, 2], [2, 3], [3, 0]].forEach(([a, bb]) => {
      const A = nodes[a], B = nodes[bb];
      const [ax, ay] = edgePoint(A.cx, A.cy, w, h, B.cx, B.cy);
      const [bx, by] = edgePoint(B.cx, B.cy, w, h, A.cx, A.cy);
      c.line(ax, ay, bx, by, { stroke: C.goldDeep, sw: 0.9, arrowEnd: true, arrowSize: 3.2 });
    });
    nodes.forEach(n => {
      card(c, n.x, n.y, w, h, { fill: C.paperWarm, stroke: C.rule });
      c.text(n.x + 0.08, n.y + 0.14, w - 0.16, n.t, { font: 'serif', size: 11.5, color: INK, align: 'center' });
      T(c, n.x + 0.08, n.y + 0.48, w - 0.16, n.s, { size: 7.2, color: MUT, align: 'center', lineHeight: 1.2 });
    });
    c.text(cx - 1.55, cy + 1.62, 3.1, 'FEEDBACK-INFORMED', { size: 6.6, letterSpacing: 1.4, color: C.goldDeep, align: 'center', caps: true, bold: true });
    T(c, cx - 1.55, cy + 1.8, 3.1, 'each session, not each discharge', { size: 6.6, italic: true, color: MUT, align: 'center', maxLines: 1 });

    // chart
    const gx = b.x + 6.6, gy = b.y + 0.45, gw = 4.6, gh = 2.75;
    c.line(gx, gy, gx, gy + gh, { stroke: C.rule, sw: 0.8 });
    c.line(gx, gy + gh, gx + gw, gy + gh, { stroke: C.rule, sw: 0.8 });
    c.rect(gx, gy + gh * 0.35, gw, gh * 0.22, { fill: C.sage, opacity: 0.10 });
    T(c, gx + 0.1, gy + gh * 0.37, 2.2, 'expected change band', { size: 6.6, color: C.sage });
    const pts = [[0, 0.95], [0.18, 0.85], [0.36, 0.8], [0.54, 0.62], [0.72, 0.55], [0.9, 0.32]];
    c.poly(pts.map(([x, y]) => [gx + 0.2 + x * (gw - 0.35), gy + gh - 0.2 - y * (gh - 0.45)]), { stroke: C.goldDeep, sw: 1.6 });
    const pts2 = [[0, 0.95], [0.18, 0.9], [0.36, 0.88], [0.54, 0.84], [0.72, 0.8], [0.9, 0.76]];
    c.poly(pts2.map(([x, y]) => [gx + 0.2 + x * (gw - 0.35), gy + gh - 0.2 - y * (gh - 0.45)]), { stroke: C.copper, sw: 1.4, dash: 'dash' });
    T(c, gx - 0.1, gy - 0.22, 4.4, 'Session-by-session change', { font: 'serif', size: 11, color: INK });
    c.line(gx + gw - 1.55, gy - 0.12, gx + gw - 1.2, gy - 0.12, { stroke: C.goldDeep, sw: 1.6 });
    T(c, gx + gw - 1.1, gy - 0.22, 1.2, 'actual', { size: 6.6, color: MUT });
    c.line(gx + gw - 1.55, gy + 0.02, gx + gw - 1.2, gy + 0.02, { stroke: C.copper, sw: 1.4, dash: 'dash' });
    T(c, gx + gw - 1.1, gy - 0.06, 1.4, 'expected', { size: 6.6, color: MUT });
    T(c, gx, gy + gh + 0.12, gw, 'Sessions →', { size: 6.6, color: MUT, align: 'right' });
    T(c, gx + 0.15, gy + gh * 0.08, 2.4, 'Deterioration is visible early — and actionable.', { size: 7.4, italic: true, color: C.goldDeep, lineHeight: 1.25 });
  },

  // ─────────────────────────────────────────────────────── Integrative Venn ──
  integration(c, b) {
    const cx = b.x + 3.55, cy = b.y + 2.05, r = 1.55;
    const circles = [
      { x: cx, y: cy - 0.55, label: 'Knowledge', sub: 'theory, evidence, context' },
      { x: cx - 0.8, y: cy + 0.55, label: 'Skills', sub: 'joining, enactment, intervention' },
      { x: cx + 0.8, y: cy + 0.55, label: 'Identity', sub: 'ethics, reflexivity, presence' },
    ];
    circles.forEach((cc, i) => {
      c.circle(cc.x, cc.y, r, { fill: [C.gold, C.sage, C.copper][i], opacity: 0.10, stroke: C.rule, sw: 0.7 });
      const ly = i === 0 ? cc.y - r - 0.3 : cc.y + r + 0.12;
      c.text(cc.x - 1.2, ly, 2.4, cc.label, { font: 'serif', size: 11.5, color: INK, align: 'center' });
      T(c, cc.x - 1.2, ly + 0.24, 2.4, cc.sub, { size: 7.2, color: MUT, align: 'center' });
    });
    c.text(cx - 0.85, cy + 0.3, 1.7, 'SYSTEMIC\nPRACTITIONER', { size: 7.6, letterSpacing: 1.4, color: C.ink, align: 'center', bold: true, lineHeight: 1.35 });

    const px = b.x + 7.55;
    T(c, px, b.y + 0.3, 3.9, 'From course to clinic', { font: 'serif', size: 13.5, color: INK });
    const items = [
      ['Practicum', 'Supervised cases; live observation and recording.'],
      ['Supervision', 'A space to see your own part in the system.'],
      ['Thesis', 'A question that matters to families you serve.'],
      ['Continuing development', 'CPD, peer consultation, personal therapy.'],
    ];
    items.forEach(([h, s], i) => {
      const y = b.y + 0.9 + i * 0.95;
      c.line(px, y + 0.05, px + 0.26, y + 0.05, { stroke: C.gold, sw: 1.1 });
      T(c, px + 0.38, y - 0.06, 3.3, h, { size: 9.2, bold: true, color: INK });
      T(c, px + 0.38, y + 0.2, 3.3, s, { size: 7.9, color: MUT, lineHeight: 1.3 });
    });
  },
};

export function drawDiagram(c, name, box, ctx) {
  const fn = DIAGRAMS[name];
  if (!fn) throw new Error('Unknown diagram: ' + name);
  fn(c, box, ctx);
}
