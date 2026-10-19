// Slide archetypes. Every function draws with the shared canvas API,
// so the same composition becomes SVG (preview/PDF) and native PowerPoint.
import { C, SLIDE, LAYOUT } from './theme.mjs';
import { wrap } from './text.mjs';
import { drawDiagram } from './diagrams.mjs';

const M = LAYOUT.m;
const R = SLIDE.w - M;

const caps = (s) => String(s).toUpperCase();

// ── chrome ──────────────────────────────────────────────────────────────────
function chrome(c, course, page, right) {
  c.text(M, 0.46, 9.2, `${course.code}  ·  ${caps(course.title)}`, {
    size: 6.9, letterSpacing: 1.5, color: C.goldDeep, caps: true,
  });
  if (right) c.text(R - 3.6, 0.46, 3.6, right, {
    size: 6.9, letterSpacing: 1.5, color: C.muted, caps: true, align: 'right',
  });
  c.line(M, 0.79, R, 0.79, { stroke: C.rule, sw: 0.45, opacity: 0.9 });
  c.line(M, 6.76, R, 6.76, { stroke: C.rule, sw: 0.45, opacity: 0.75 });
  c.text(M, 6.87, 7.0, 'Master of Marriage and Family Therapy  ·  16-Week Seminar', {
    size: 6.5, letterSpacing: 0.5, color: C.muted,
  });
  c.text(R - 0.9, 6.84, 0.9, String(page).padStart(2, '0'), {
    font: 'serif', size: 9.5, color: C.inkSoft, align: 'right',
  });
}

function darkChrome(c, course, page) {
  c.line(M, 0.79, R, 0.79, { stroke: C.ruleDark, sw: 0.5 });
  c.text(M, 6.87, 7.0, 'Master of Marriage and Family Therapy  ·  16-Week Seminar', {
    size: 6.5, letterSpacing: 0.5, color: C.muted,
  });
  c.text(R - 0.9, 6.84, 0.9, String(page).padStart(2, '0'), {
    font: 'serif', size: 9.5, color: C.goldLight, align: 'right',
  });
}

function head(c, { x = M, y = 1.08, w = 10.9, kicker, title, lead, size = 29 }) {
  let yy = y;
  if (kicker) {
    c.text(x, yy, w, kicker, {
      size: 7.4, letterSpacing: 2.0, color: C.goldDeep, caps: true, bold: true,
    });
    yy += 0.3;
  }
  c.text(x, yy, w, title, { font: 'serif', size, color: C.ink, lineHeight: 1.12 });
  const th = wrap(title, w * 72, size, { font: 'serif', lineHeight: 1.12 }).height / 72;
  yy += th + 0.14;
  if (lead) {
    c.text(x, yy, Math.min(w, 8.9), lead, { size: 12.6, color: C.inkMid, lineHeight: 1.42 });
    yy += wrap(lead, Math.min(w, 8.9) * 72, 12.6, { lineHeight: 1.42 }).height / 72;
  }
  return yy;
}

function bulletList(c, x, y, w, items, o = {}) {
  const size = o.size || 9.6;
  const gap = o.gap || 0.12;
  let yy = y;
  items.forEach((it) => {
    c.line(x, yy + 0.105, x + 0.14, yy + 0.105, { stroke: o.mark || C.gold, sw: 0.9 });
    c.text(x + 0.24, yy, w - 0.24, it, { size, color: o.color || C.inkSoft, lineHeight: 1.38 });
    yy += wrap(it, (w - 0.24) * 72, size, { lineHeight: 1.38 }).height / 72 + gap;
  });
  return yy;
}

function blockHeading(c, x, y, w, label, color = C.goldDeep) {
  c.text(x, y, w, label, { size: 7.5, letterSpacing: 1.7, caps: true, bold: true, color });
  c.line(x, y + 0.22, x + 0.34, y + 0.22, { stroke: color, sw: 0.8 });
}

function numBadge(c, x, y, n, color = C.goldDeep, fill = 'none') {
  c.circle(x + 0.12, y + 0.13, 0.135, { fill, stroke: color, sw: 0.7 });
  c.text(x, y, 0.24, String(n), { size: 7.2, color, align: 'center', valign: 'middle', boxH: 0.26, lineHeight: 1 });
}

// ── front matter ────────────────────────────────────────────────────────────
export function cover(c, course) {
  c.raw(bgRaw('cover'));
  const inset = 0.4;
  c.rect(inset, inset, SLIDE.w - inset * 2, SLIDE.h - inset * 2, { stroke: C.gold, sw: 0.5, opacity: 0.45 });
  c.line(inset + 0.14, inset + 0.14, inset + 0.62, inset + 0.14, { stroke: C.goldLight, sw: 0.8, opacity: 0.7 });
  c.line(inset + 0.14, inset + 0.14, inset + 0.14, inset + 0.62, { stroke: C.goldLight, sw: 0.8, opacity: 0.7 });

  c.text(1.0, 1.05, 8.2, 'Master of Marriage and Family Therapy', {
    size: 8.8, letterSpacing: 3.2, color: C.goldLight, caps: true,
  });
  c.line(1.02, 1.42, 2.1, 1.42, { stroke: C.gold, sw: 0.8, opacity: 0.8 });

  c.text(0.98, 2.06, 8.9, course.title, {
    font: 'serif', size: 54, color: C.paper, lineHeight: 1.06,
  });
  const th = wrap(course.title, 8.9 * 72, 54, { font: 'serif', lineHeight: 1.06 }).height / 72;
  const ry = 2.06 + th + 0.34;
  c.line(1.02, ry, 3.3, ry, { stroke: C.gold, sw: 0.9 });
  c.text(1.0, ry + 0.18, 8.4, course.subtitle, {
    font: 'serif', size: 16, italic: true, color: C.goldLight, lineHeight: 1.4,
  });
  c.text(1.0, ry + 0.78, 8.0, course.coverLine, {
    size: 9.2, letterSpacing: 1.2, color: C.parchment, caps: true,
  });

  // course monogram
  c.text(9.55, 2.02, 3.1, 'MFT', { size: 11, letterSpacing: 8, color: C.gold, align: 'right' });
  c.line(10.72, 2.34, 12.3, 2.34, { stroke: C.gold, sw: 0.6, opacity: 0.7 });
  c.text(9.35, 2.42, 3.05, course.code.split(' ')[1], {
    font: 'serif', size: 92, color: C.goldLight, align: 'right', lineHeight: 1,
  });
  c.text(9.4, 4.05, 3.0, 'COURSE DECK', { size: 8, letterSpacing: 3.2, color: C.parchment, align: 'right' });
  c.text(9.4, 4.32, 3.0, 'Weeks 1 – 16', { font: 'serif', size: 13, italic: true, color: C.parchment, align: 'right' });

  c.line(1.0, 5.86, 8.6, 5.86, { stroke: C.gold, sw: 0.5, opacity: 0.35 });
  c.text(1.0, 6.0, 5.4, course.semester, { size: 8, letterSpacing: 1.8, color: C.parchment, caps: true });
  c.text(6.6, 6.0, 2.6, `${course.units} Units`, { size: 8, letterSpacing: 1.8, color: C.parchment, caps: true });
  c.text(9.4, 6.0, 3.0, `16 Weeks  ·  ${course.slideCount} Slides`, { size: 8, letterSpacing: 1.8, color: C.muted, caps: true, align: 'right' });
}

export function about(c, course, page) {
  chrome(c, course, page, 'Course Description');
  const tTitle = 'A discipline of relationship, not a technique of repair';
  const tSize = 25;
  c.text(M, 1.05, 7.45, tTitle, { font: 'serif', size: tSize, color: C.ink, lineHeight: 1.12 });
  const tH = wrap(tTitle, 7.45 * 72, tSize, { font: 'serif', lineHeight: 1.12 }).height / 72;
  c.text(M, 1.05 + tH + 0.16, 7.3, course.description, { size: 10.6, color: C.inkMid, lineHeight: 1.5, maxLines: 6 });

  // at-a-glance panel
  const px = 8.62, pw = 3.81;
  c.rect(px, 1.2, pw, 3.34, { fill: C.parchment, opacity: 0.5, radius: 0.02 });
  c.text(px + 0.28, 1.42, pw - 0.5, 'AT A GLANCE', { size: 6.6, letterSpacing: 1.9, color: C.goldDeep, caps: true, bold: true });
  const facts = [
    ['Semester', course.semester],
    ['Credit', `${course.units} units`],
    ['Duration', '16 weeks · 4 phases'],
    ['Structure', 'Lecture · seminar · skills lab'],
    ['Assessment', 'Formulation · exam · participation'],
  ];
  facts.forEach(([k, v], i) => {
    const yy = 1.78 + i * 0.5;
    c.text(px + 0.28, yy, 1.05, k, { size: 7.0, color: C.muted, caps: true, letterSpacing: 1.1 });
    c.text(px + 1.36, yy - 0.03, pw - 1.6, v, { size: 8.4, color: C.inkSoft, lineHeight: 1.25, maxLines: 2 });
    if (i < facts.length - 1) c.line(px + 0.28, yy + 0.38, px + pw - 0.26, yy + 0.38, { stroke: C.rule, sw: 0.35 });
  });

  // aims + distinctiveness
  const y = 4.82;
  const cols = [
    { h: 'Aim of the course', items: course.aims },
    { h: 'What makes MFT distinct', items: course.distinct },
  ];
  cols.forEach((col, i) => {
    const x = M + i * 5.95;
    blockHeading(c, x, y, 5.3, col.h, i ? C.sage : C.goldDeep);
    bulletList(c, x, y + 0.4, 5.35, col.items, { size: 8.6, gap: 0.06 });
  });
}

export function outcomes(c, course, page) {
  chrome(c, course, page, 'Learning Outcomes');
  const y = head(c, {
    y: 1.02,
    w: 9.4,
    kicker: 'On completion',
    title: 'What you will be able to do',
    lead: 'Six outcomes frame the course. Each week names the subset it develops; the final portfolio invites you to evidence all six.',
    size: 27,
  });
  const startY = 2.62;
  const colW = 5.72;
  course.outcomes.forEach((o, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = M + col * 6.05;
    const yy = startY + row * 1.22;
    c.text(x, yy - 0.42, 0.6, `0${i + 1}`, { font: 'serif', size: 10, color: C.gold });
    c.line(x + 0.42, yy - 0.32, x + colW - 0.1, yy - 0.32, { stroke: C.rule, sw: 0.45 });
    c.text(x, yy - 0.1, colW - 0.2, o, { size: 10.4, color: C.inkSoft, lineHeight: 1.4 });
  });
  c.line(M, 6.06, R, 6.06, { stroke: C.rule, sw: 0.5 });
  c.text(M, 6.18, 11.5, 'Mapping · each week names the outcomes it develops, so you can trace your own progress across the sixteen weeks.', {
    size: 8.2, italic: true, color: C.muted,
  });
}

export function courseMap(c, course, page) {
  chrome(c, course, page, 'The Sixteen-Week Arc');
  c.text(M, 1.0, 10.5, 'The shape of the semester', { font: 'serif', size: 28, color: C.ink });
  c.text(M, 1.5, 9.6, 'Four phases, each a distinct mode of learning: foundations, theoretical cartography, clinical encounter, then integration.', {
    size: 11.6, color: C.inkMid, lineHeight: 1.4,
  });
  drawDiagram(c, 'phaseCards', { x: M, y: 2.05, w: 11.53, h: 4.35 }, { phases: course.phases });
}

export function rhythm(c, course, page) {
  chrome(c, course, page, 'The Weekly Rhythm');
  const y = head(c, {
    y: 1.02, w: 9.8, kicker: 'How each week works',
    title: 'Read, wrestle, practise, reflect',
    lead: 'Each week follows the same four-beat structure. The deck is a teaching instrument, not a transcript: the slides carry the argument, the seminar does the work.',
    size: 27,
  });
  const steps = course.rhythm;
  const startY = 3.28;
  const w = (11.53 - 3 * 0.24) / 4;
  steps.forEach((s, i) => {
    const x = M + i * (w + 0.24);
    c.rect(x, startY, w, 2.62, { fill: i % 2 ? '#FCF8EF' : C.paperWarm, stroke: C.rule, sw: 0.6, radius: 0.03 });
    c.rect(x, startY, w, 0.05, { fill: i % 2 ? C.sage : C.gold });
    c.text(x + 0.2, startY + 0.22, w - 0.4, `0${i + 1}`, { size: 7.2, letterSpacing: 1.8, color: i % 2 ? C.sage : C.goldDeep });
    c.text(x + 0.2, startY + 0.5, w - 0.4, s.title, { font: 'serif', size: 15, color: C.ink, lineHeight: 1.15 });
    c.text(x + 0.2, startY + 1.02, w - 0.4, s.body, { size: 9.0, color: C.inkSoft, lineHeight: 1.42 });
    c.text(x + 0.2, startY + 2.3, w - 0.4, s.time, { size: 7, color: C.muted, letterSpacing: 1.2, caps: true });
  });
  c.line(M, 6.1, R, 6.1, { stroke: C.rule, sw: 0.5 });
  c.text(M, 6.22, 11.5, 'Preparation is not optional: seminar time is spent applying the reading, not summarising it.', {
    size: 8.2, italic: true, color: C.muted,
  });
}

export function assessment(c, course, page) {
  chrome(c, course, page, 'Teaching & Assessment');
  const y = head(c, {
    y: 1.02, w: 9.6, kicker: 'Assessment',
    title: 'How the course is examined',
    lead: 'Assessment is cumulative and clinical in character: you are asked to show that you can think systemically, write clearly, and defend a formulation.',
    size: 27,
  });
  const rows = course.assessment;
  const startY = 3.18;
  const colX = [M, M + 4.2, M + 7.2, R];
  c.line(M, startY - 0.12, R, startY - 0.12, { stroke: C.gold, sw: 0.9 });
  ['Component', 'Format', 'Weight'].forEach((h, i) => {
    c.text(colX[i], startY, colX[i + 1] - colX[i] - 0.2, h, { size: 7.2, letterSpacing: 1.5, color: C.goldDeep, caps: true, bold: true });
  });
  rows.forEach((r, i) => {
    const yy = startY + 0.38 + i * 0.66;
    c.text(colX[0], yy, 4.0, r[0], { font: 'serif', size: 12.6, color: C.ink });
    c.text(colX[1], yy + 0.02, 2.8, r[1], { size: 9.0, color: C.inkSoft, lineHeight: 1.3 });
    c.text(colX[2], yy, 1.0, r[2], { font: 'serif', size: 14, color: C.goldDeep });
    c.line(M, yy + 0.48, R, yy + 0.48, { stroke: C.rule, sw: 0.45, opacity: 0.8 });
  });
  const py = startY + 0.38 + rows.length * 0.66 + 0.14;
  c.line(M, py, R, py, { stroke: C.gold, sw: 0.8 });
  ['Feedback before grades', 'Formulation over recall', 'Ethical reasoning evidenced'].forEach((t, i) => {
    const x = M + i * 3.9;
    c.circle(x + 0.08, py + 0.32, 0.035, { fill: C.gold });
    c.text(x + 0.24, py + 0.18, 3.5, t, { size: 8.6, color: C.goldDeep, italic: true });
  });
}

// ── phase divider ───────────────────────────────────────────────────────────
export function phaseDivider(c, course, phase, page) {
  c.raw(bgRaw('section'));
  c.text(M, 0.6, 7.0, `PHASE ${phase.roman}  ·  WEEKS ${cap(phase.range)}`, {
    size: 8, letterSpacing: 3, color: C.gold, caps: true,
  });
  c.text(6.6, -0.5, 6.0, String(phase.start).padStart(2, '0'), {
    font: 'serif', size: 300, color: '#181611', align: 'right', lineHeight: 1,
  });
  c.text(M, 2.05, 7.4, phase.name, { font: 'serif', size: 46, color: C.paper, lineHeight: 1.08 });
  c.text(M, 3.75, 6.6, phase.blurb, { font: 'serif', size: 14.5, italic: true, color: C.goldLight, lineHeight: 1.5 });
  c.line(M, 5.0, M + 1.7, 5.0, { stroke: C.gold, sw: 0.8 });
  phase.weeks.forEach((w, i) => {
    const x = M + i * 1.55;
    c.text(x, 5.3, 0.5, `0${phase.start + i}`, { font: 'serif', size: 10, color: C.gold });
    c.text(x, 5.55, 1.35, w, { size: 7.6, color: C.parchment, lineHeight: 1.25 });
  });
  drawRail(c, M, 6.28, 11.5, phase.end, 'dark');
  darkChrome(c, course, page);
}

function cap(s) { return String(s).replace(/–/g, '–'); }

function drawRail(c, x, y, w, current, tone = 'light') {
  const n = 16, step = w / (n - 1);
  c.line(x, y, x + w, y, { stroke: tone === 'dark' ? C.ruleDark : C.rule, sw: 0.8 });
  for (let i = 0; i < n; i++) {
    const cx = x + step * i;
    const isCur = i + 1 <= current;
    const active = i + 1 === current;
    c.circle(cx, y, active ? 0.07 : 0.032, {
      fill: active ? C.gold : (isCur ? C.goldDeep : (tone === 'dark' ? C.night3 : C.rule)),
      stroke: active ? C.goldLight : 'none', sw: 0.7,
    });
  }
  if (tone !== 'dark') {
    c.text(x, y + 0.18, 0.8, '01', { size: 6.2, color: C.muted, letterSpacing: 1.1 });
    c.text(x + w - 0.8, y + 0.18, 0.8, '16', { size: 6.2, color: C.muted, letterSpacing: 1.1, align: 'right' });
  }
}

// ── week opener ─────────────────────────────────────────────────────────────
export function weekOpener(c, course, week, page) {
  c.raw(bgRaw('section'));
  c.text(M, 0.58, 7.0, `WEEK ${String(week.n).padStart(2, '0')}  ·  PHASE ${course.phases[week.phase].roman} — ${caps(course.phases[week.phase].name)}`, {
    size: 7.6, letterSpacing: 2.4, color: C.gold, caps: true,
  });
  c.text(7.0, -0.42, 6.0, String(week.n).padStart(2, '0'), {
    font: 'serif', size: 250, color: '#191710', align: 'right', lineHeight: 1,
  });

  c.text(M, 1.72, 8.3, week.title, { font: 'serif', size: 39, color: C.paper, lineHeight: 1.1 });
  const th = wrap(week.title, 8.3 * 72, 39, { font: 'serif', lineHeight: 1.1 }).height / 72;
  const ry = 1.72 + th + 0.22;
  c.line(M, ry, M + 1.6, ry, { stroke: C.gold, sw: 0.9 });

  c.text(M, ry + 0.26, 8.1, 'ESSENTIAL QUESTION', { size: 7, letterSpacing: 2.2, color: C.gold, caps: true });
  c.text(M, ry + 0.5, 7.9, week.question, { font: 'serif', size: 15.5, italic: true, color: C.goldLight, lineHeight: 1.42 });
  const qH = wrap(week.question, 7.9 * 72, 15.5, { font: 'serif', italic: true, lineHeight: 1.42 }).height / 72;

  // in-week agenda
  const ay = Math.max(ry + 0.5 + qH + 0.5, 3.45);
  c.line(M, ay - 0.16, M + 7.9, ay - 0.16, { stroke: C.ruleDark, sw: 0.5 });
  const kinds = { concept: 'Lecture', diagram: 'Diagram', case: 'Clinical case', seminar: 'Seminar' };
  const gw = 2.55;
  week.slides.forEach((sl, i) => {
    const x = M + i * (gw + 0.14);
    c.text(x, ay, gw, `0${i + 1}  ·  ${(kinds[sl.kind] || sl.kind).toUpperCase()}`, {
      size: 6.2, letterSpacing: 1.4, color: C.gold, caps: true,
    });
    c.text(x, ay + 0.21, gw - 0.1, sl.title, { size: 8.5, color: C.parchment, lineHeight: 1.25, maxLines: 2 });
  });

  // outcomes panel
  const px = 9.55;
  c.line(px - 0.4, 1.5, px - 0.4, 4.75, { stroke: C.ruleDark, sw: 0.5 });
  c.text(px, 1.55, 2.9, 'THIS WEEK', { size: 7, letterSpacing: 2.2, color: C.gold, caps: true });
  week.outcomes.forEach((o, i) => {
    const yy = 1.92 + i * 0.98;
    c.text(px, yy, 0.3, `0${i + 1}`, { font: 'serif', size: 9, color: C.gold });
    c.text(px + 0.34, yy - 0.02, 2.52, o, { size: 8.4, color: C.parchment, lineHeight: 1.35 });
  });

  const ky = 5.3;
  c.text(M, ky, 2.4, 'KEY TERMS', { size: 6.6, letterSpacing: 1.8, color: C.gold, caps: true });
  c.text(M, ky + 0.22, 7.4, week.terms.join('   ·   '), { size: 8.6, color: C.parchment, italic: true });

  c.text(M, 6.06, 8.4, week.reading, { size: 7.4, color: C.muted, italic: true, maxLines: 1 });

  drawRail(c, M, 6.3, 11.5, week.n, 'dark');
  darkChrome(c, course, page);
}

// ── content: concept ────────────────────────────────────────────────────────
export function concept(c, course, week, slide, page) {
  chrome(c, course, page, `Week ${String(week.n).padStart(2, '0')}  ·  ${slide.kicker || 'Lecture'}`);
  head(c, {
    y: 1.05, w: 10.9, size: 28,
    title: slide.title,
    lead: slide.lead,
  });

  const bandH = 0.98;
  const bandY = 5.78;
  const top = 3.02;
  const cols = slide.blocks.length;
  const gap = 0.42;
  const colW = (11.53 - gap * (cols - 1)) / cols;
  const num = (i) => String(i + 1).padStart(2, '0');

  slide.blocks.forEach((b, i) => {
    const x = M + i * (colW + gap);
    c.text(x, top - 0.42, 0.5, num(i), { font: 'serif', size: 11, color: C.gold });
    c.line(x + 0.4, top - 0.34, x + colW, top - 0.34, { stroke: C.rule, sw: 0.45 });
    c.text(x, top - 0.19, colW, b.h, {
      size: 7.5, letterSpacing: 1.7, caps: true, bold: true, color: i === 1 ? C.sage : C.goldDeep,
    });
    let yy = top + 0.08;
    if (b.body) {
      c.text(x, yy, colW, b.body, { size: 9.0, color: C.inkSoft, lineHeight: 1.44 });
      yy += wrap(b.body, colW * 72, 9.0, { lineHeight: 1.44 }).height / 72 + 0.12;
    }
    if (b.items) {
      b.items.forEach((it) => {
        c.line(x, yy + 0.1, x + 0.13, yy + 0.1, { stroke: C.gold, sw: 0.8 });
        c.text(x + 0.23, yy, colW - 0.23, it, { size: 8.8, color: C.inkSoft, lineHeight: 1.38 });
        yy += wrap(it, (colW - 0.23) * 72, 8.8, { lineHeight: 1.38 }).height / 72 + 0.1;
      });
    }
  });

  if (slide.callout) {
    c.rect(M, bandY, 11.53, bandH, { fill: C.ink, radius: 0.02 });
    c.rect(M + 0.02, bandY, 0.05, bandH, { fill: C.gold });
    c.text(M + 0.3, bandY + 0.15, 2.7, slide.callout.label, {
      size: 6.4, letterSpacing: 1.7, caps: true, color: C.gold,
    });
    c.text(M + 0.3, bandY + 0.33, 3.3, slide.callout.title, {
      font: 'serif', size: 13, color: C.paper, lineHeight: 1.15, maxLines: 1,
    });
    c.text(M + 3.95, bandY + 0.16, 5.45, slide.callout.body, {
      size: 8.6, color: C.parchment, lineHeight: 1.45, maxLines: 2,
    });
    if (slide.footnote) {
      c.line(M + 9.6, bandY + 0.16, M + 9.6, bandY + bandH - 0.16, { stroke: C.ruleDark, sw: 0.5 });
      c.text(M + 9.78, bandY + 0.14, 1.6, slide.footnote, {
        size: 6.2, italic: true, color: '#B9AE9C', lineHeight: 1.35, maxLines: 3,
      });
    }
  }
}

// ── content: diagram ────────────────────────────────────────────────────────
export function diagram(c, course, week, slide, page) {
  chrome(c, course, page, `Week ${String(week.n).padStart(2, '0')}  ·  Diagram`);
  c.text(M, 1.02, 10.9, slide.title, { font: 'serif', size: 27, color: C.ink, lineHeight: 1.12 });
  if (slide.lead) c.text(M, 1.55, 10.0, slide.lead, { size: 10.6, color: C.inkMid, lineHeight: 1.4 });
  const top = slide.lead ? 1.98 : 1.55;
  drawDiagram(c, slide.diagram, { x: M, y: top, w: 11.53, h: 4.4 }, { phases: course.phases });
  if (slide.caption) {
    c.text(M, 6.4, 10.6, slide.caption, { size: 7.4, italic: true, color: C.muted, lineHeight: 1.3 });
  }
}

// ── content: case / seminar ─────────────────────────────────────────────────
export function caseSlide(c, course, week, slide, page) {
  chrome(c, course, page, `Week ${String(week.n).padStart(2, '0')}  ·  Clinical Application`);
  c.text(M, 1.02, 10.4, slide.title, { font: 'serif', size: 26, color: C.ink });

  const vy = 1.6, vh = 2.02;
  c.rect(M, vy, 7.72, vh, { fill: C.parchment, opacity: 0.5, radius: 0.02 });
  c.rect(M, vy, 0.05, vh, { fill: C.copper });
  c.text(M + 0.32, vy + 0.18, 3.0, 'CLINICAL VIGNETTE', {
    size: 6.8, letterSpacing: 2.0, color: C.copper, caps: true, bold: true,
  });
  c.text(M + 0.32, vy + 0.46, 7.05, slide.vignette, {
    font: 'serif', size: 11.6, italic: true, color: C.ink, lineHeight: 1.52, valign: 'middle', boxH: vh - 0.62,
  });

  const sx = 8.86, sw = 3.57;
  c.rect(sx, vy, sw, vh, { fill: 'none', stroke: C.rule, sw: 0.6, radius: 0.02 });
  c.text(sx + 0.22, vy + 0.18, sw - 0.4, 'APPLY THIS WEEK', {
    size: 6.6, letterSpacing: 1.8, color: C.sage, caps: true, bold: true,
  });
  const apply = slide.apply || week.terms;
  apply.slice(0, 4).forEach((t, i) => {
    const yy = vy + 0.52 + i * 0.36;
    c.circle(sx + 0.27, yy + 0.06, 0.028, { fill: C.sage });
    c.text(sx + 0.42, yy - 0.03, sw - 0.55, t, { size: 8.3, color: C.inkSoft, lineHeight: 1.25 });
  });

  c.text(M, 4.02, 4.0, 'REFLECTION', { size: 7.2, letterSpacing: 2.0, color: C.goldDeep, caps: true, bold: true });
  c.line(M + 1.1, 4.08, M + 1.7, 4.08, { stroke: C.gold, sw: 0.8 });

  const pw = (11.53 - 2 * 0.32) / 3;
  slide.prompts.forEach((p, i) => {
    const x = M + i * (pw + 0.32);
    const y = 4.42;
    c.rect(x, y, pw, 1.78, { fill: '#FCF8EF', stroke: C.rule, sw: 0.5, radius: 0.02 });
    c.text(x + 0.22, y + 0.17, 0.5, `0${i + 1}`, { font: 'serif', size: 11, color: C.gold });
    c.text(x + 0.22, y + 0.44, pw - 0.44, p, { size: 9.2, color: C.inkSoft, lineHeight: 1.42 });
    for (let k = 0; k < 2; k++) {
      c.line(x + 0.22, y + 1.32 + k * 0.24, x + pw - 0.22, y + 1.32 + k * 0.24, {
        stroke: C.rule, sw: 0.3, opacity: 0.75, dash: 'dot',
      });
    }
  });

  c.text(M, 6.28, 10.8, slide.footnote || 'Discuss in seminar · bring one formulation to supervision.', {
    size: 8.2, italic: true, color: C.muted,
  });
}

export function seminar(c, course, week, slide, page) {
  c.raw(bgRaw('section'));
  c.text(M, 0.6, 9.0, `WEEK ${String(week.n).padStart(2, '0')}  ·  SEMINAR`, { size: 7.6, letterSpacing: 2.4, color: C.gold, caps: true });
  c.text(M, 1.55, 8.6, slide.title, { font: 'serif', size: 34, color: C.paper, lineHeight: 1.12 });
  c.line(M, 2.62, M + 1.4, 2.62, { stroke: C.gold, sw: 0.9 });
  c.text(M, 2.9, 7.6, slide.lead, { font: 'serif', size: 13, italic: true, color: C.goldLight, lineHeight: 1.45 });

  const qs = slide.questions;
  const colW = 5.45;
  qs.forEach((q, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = M + col * 6.1;
    const y = 4.1 + row * 1.15;
    c.text(x, y, 0.5, `0${i + 1}`, { font: 'serif', size: 15, color: C.gold });
    c.text(x + 0.5, y, colW - 0.5, q, { size: 9.8, color: C.parchment, lineHeight: 1.4 });
  });
  const py = 6.02;
  c.line(M, py - 0.18, R, py - 0.18, { stroke: C.ruleDark, sw: 0.5 });
  const protocol = course.seminarProtocol || [
    ['05', 'Silent writing'], ['10', 'Pairs'], ['20', 'Plenary'], ['05', 'Close'],
  ];
  protocol.forEach(([t, lab], i) => {
    const x = M + i * 2.95;
    c.text(x, py, 0.6, t, { font: 'serif', size: 11, color: C.gold });
    c.text(x + 0.42, py + 0.02, 2.2, lab, { size: 6.8, color: C.muted, caps: true, letterSpacing: 1.2 });
  });
  c.text(R - 3.2, py + 0.02, 3.2, 'MINUTES', { size: 6.4, color: C.muted, caps: true, letterSpacing: 1.6, align: 'right' });
  darkChrome(c, course, page);
}

// ── back matter ─────────────────────────────────────────────────────────────
export function glossary(c, course, page) {
  chrome(c, course, page, 'Glossary of Core Terms');
  c.text(M, 1.0, 10.6, 'A working vocabulary', { font: 'serif', size: 28, color: C.ink });
  c.text(M, 1.5, 9.6, 'Terms you should be able to use precisely, in writing and in supervision.', { size: 10.6, color: C.inkMid });
  const entries = course.glossary;
  const cols = 3;
  const colW = 3.6;
  const per = Math.ceil(entries.length / cols);
  entries.forEach((e, i) => {
    const col = Math.floor(i / per);
    const row = i % per;
    const x = M + col * (colW + 0.36);
    const y = 2.12 + row * 0.76;
    c.text(x, y, colW, e[0], { font: 'serif', size: 9.6, color: C.ink, maxLines: 1 });
    c.text(x, y + 0.21, colW, e[1], { size: 7.3, color: C.muted, lineHeight: 1.3, maxLines: 2 });
    if (row < per - 1) c.line(x, y + 0.63, x + colW, y + 0.63, { stroke: C.rule, sw: 0.35, opacity: 0.7 });
  });
}

export function references(c, course, page) {
  chrome(c, course, page, 'References');
  c.text(M, 1.0, 10.6, 'Core readings', { font: 'serif', size: 28, color: C.ink });
  c.text(M, 1.5, 9.8, 'Students are expected to engage the primary texts, not only the summaries in this deck.', { size: 10.2, color: C.inkMid });
  const refs = course.references;
  const n = Math.ceil(refs.length / 2);
  refs.forEach((r, i) => {
    const col = i < n ? 0 : 1;
    const row = i < n ? i : i - n;
    const x = M + col * 6.05;
    const y = 2.12 + row * 0.6;
    c.text(x, y, 0.3, `${String(i + 1).padStart(2, '0')}`, { size: 6.6, color: C.goldDeep, bold: true });
    c.text(x + 0.36, y - 0.02, 5.25, r, { size: 7.35, color: C.inkSoft, lineHeight: 1.3, maxLines: 2 });
  });
}

export function closingSlide(c, course, page) {
  c.raw(bgRaw('closing'));
  c.rect(0.4, 0.4, SLIDE.w - 0.8, SLIDE.h - 0.8, { stroke: C.gold, sw: 0.5, opacity: 0.35 });
  c.text(1.35, 1.55, 10.6, 'END OF COURSE', { size: 7.8, letterSpacing: 3.4, color: C.gold, caps: true, align: 'center' });
  c.text(1.35, 2.15, 10.6, course.closing.title, { font: 'serif', size: 38, color: C.paper, align: 'center', lineHeight: 1.15 });
  c.line(5.55, 4.15, 7.75, 4.15, { stroke: C.gold, sw: 0.8 });
  c.text(2.4, 4.4, 8.5, course.closing.body, { font: 'serif', size: 13.5, italic: true, color: C.goldLight, align: 'center', lineHeight: 1.55 });
  c.text(1.35, 5.85, 10.6, course.closing.next, { size: 8.4, letterSpacing: 1.6, color: C.parchment, caps: true, align: 'center' });
  c.text(1.35, 6.6, 10.6, `${course.code}  ·  Master of Marriage and Family Therapy`, { size: 7.4, letterSpacing: 1.8, color: C.muted, caps: true, align: 'center' });
  c.text(R - 0.9, 6.84, 0.9, String(page).padStart(2, '0'), { font: 'serif', size: 9.5, color: C.goldLight, align: 'right' });
}

// backgrounds are inlined as vectors so preview == PowerPoint
let _bg = null;
export function setBackgrounds(bg) { _bg = bg; }
function bgRaw(kind) { return _bg ? _bg(kind) : ''; }
