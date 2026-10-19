// Build the deck: SVG previews + PDF + native PowerPoint.
import fs from 'node:fs';
import path from 'node:path';
import PptxGenJS from 'pptxgenjs';
import { Resvg } from '@resvg/resvg-js';
import sharp from 'sharp';
import { PDFDocument } from 'pdf-lib';

import { SvgCanvas } from './canvas-svg.mjs';
import { PptxCanvas } from './canvas-pptx.mjs';
import { bgMarkup, writeBackgrounds } from './backgrounds.mjs';
import { setBackgrounds } from './slides.mjs';
import * as S from './slides.mjs';
import course from './content/mft701.mjs';

const ROOT = path.resolve(import.meta.dirname, '../..');
const OUT = path.join(ROOT, 'decks');
const PREV = path.join(ROOT, 'preview');
const FONT_DIR = path.resolve(import.meta.dirname, '../assets/fonts');
const BG = path.join(PREV, 'bg');

const SLUG = 'MFT-701_Fundamentals-of-Marriage-and-Family-Therapy';
const W = 13.3333, H = 7.5;

const fontFiles = fs.readdirSync(FONT_DIR).filter(f => f.endsWith('.ttf')).map(f => path.join(FONT_DIR, f));

function renderSVG(svg, width) {
  const resvg = new Resvg(svg, {
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: 'Gelasio', serifFamily: 'Gelasio', sansSerifFamily: 'Carlito' },
    fitTo: { mode: 'width', value: width },
  });
  return resvg.render().asPng();
}

function noteFor(week, sl) {
  if (sl.kind === 'concept') {
    return `Lecture ${week.n}. Begin from the essential question: “${week.question}” Do not resolve it for the class. Work through the three blocks, using a clinical example for each. Close by naming the one idea students must be able to use in supervision this week.`;
  }
  if (sl.kind === 'diagram') {
    return `Walk the diagram slowly, one element at a time. Ask a student to narrate it back to you in their own words, then ask what the diagram leaves out. The caption is part of the argument.`;
  }
  if (sl.kind === 'case') {
    return `Read the vignette aloud, then give pairs three minutes on the first prompt. Take responses without correcting them. Use the second prompt to surface what is absent from the room, and the third to move toward a testable hypothesis.`;
  }
  return `Seminar protocol: five minutes of silent writing, then pairs, then plenary. Protect the reflective frame — this is not a debate. Draw out two or three contributions and connect them back to the week’s reading.`;
}

function buildSlideList(course) {
  const list = [];
  list.push({
    kind: 'cover', bg: 'cover',
    note: `Welcome to MFT 701. Introduce the course as an invitation to see relationships rather than individuals as the unit of clinical work. Name the four phases and the assessment structure.`,
    draw: (c, p) => S.cover(c, course),
  });
  list.push({
    kind: 'about', bg: 'paper',
    note: `Read the course description slowly. Invite students to say, in one sentence, what they hope this course will change about how they listen.`,
    draw: (c, p) => S.about(c, course, p),
  });
  list.push({
    kind: 'outcomes', bg: 'paper',
    note: `These six outcomes are the contract for the semester. Point out that the final portfolio asks for evidence of all six, not a grade average.`,
    draw: (c, p) => S.outcomes(c, course, p),
  });
  list.push({
    kind: 'map', bg: 'paper',
    note: `Orient the class in time. Note that theory is front-loaded so that clinical work in the second half can be comparative rather than descriptive.`,
    draw: (c, p) => S.courseMap(c, course, p),
  });
  list.push({
    kind: 'rhythm', bg: 'paper',
    note: `Explain the weekly rhythm and the preparation expected before each lecture. The seminar is where the learning happens; the lecture only sets the table.`,
    draw: (c, p) => S.rhythm(c, course, p),
  });
  list.push({
    kind: 'assessment', bg: 'paper',
    note: `Walk through assessment. Emphasise that the case formulation is formative — feedback in Week 9 is meant to feed the final examination.`,
    draw: (c, p) => S.assessment(c, course, p),
  });

  course.phases.forEach((phase, pi) => {
    list.push({
      kind: 'phase', bg: 'section',
      note: `Phase ${phase.roman}: ${phase.name}. Read the phase description and name the four weeks ahead.`,
      draw: (c, p) => S.phaseDivider(c, course, phase, p),
    });
    course.weeks.filter(w => w.phase === pi).forEach(w => {
      list.push({
        kind: 'week', bg: 'section',
        note: `Week ${w.n}. Ask the essential question and let it sit. Preview the three outcomes; do not read the key terms aloud.`,
        draw: (c, p) => S.weekOpener(c, course, w, p),
      });
      w.slides.forEach(sl => {
        const bg = sl.kind === 'seminar' ? 'section' : 'paper';
        const fn = sl.kind === 'case' ? S.caseSlide : S[sl.kind];
        list.push({
          kind: sl.kind, bg,
          note: noteFor(w, sl),
          draw: (c, p) => fn(c, course, w, sl, p),
        });
      });
    });
  });

  list.push({
    kind: 'glossary', bg: 'paper',
    note: `A working vocabulary. Ask each student to choose one term they could not yet define precisely, and to write a definition in their journal.`,
    draw: (c, p) => S.glossary(c, course, p),
  });
  list.push({
    kind: 'references', bg: 'paper',
    note: `Point students to the primary texts. The deck is a map; the reading is the territory.`,
    draw: (c, p) => S.references(c, course, p),
  });
  list.push({
    kind: 'closing', bg: 'closing',
    note: `Close by returning to the opening claim: the family is the context of the solution. Invite one sentence from each student about what they will carry forward.`,
    draw: (c, p) => S.closingSlide(c, course, p),
  });

  return list;
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  fs.mkdirSync(PREV, { recursive: true });

  const slides = buildSlideList(course);
  course.slideCount = slides.length;
  console.log(`Composing ${slides.length} slides…`);

  setBackgrounds(bgMarkup);
  const bgFiles = await writeBackgrounds(BG);

  // ── SVG → JPEG (preview + PDF) ────────────────────────────────────────────
  const jpegs = [];
  for (let i = 0; i < slides.length; i++) {
    const sl = slides[i];
    const page = i + 1;
    const c = new SvgCanvas(W, H);
    sl.draw(c, page);
    if (sl.bg === 'paper') c.raw(bgMarkup('paper'));
    const svg = c.toSVG();
    const png = renderSVG(svg, 2000);
    const jpg = await sharp(png).jpeg({ quality: 88, chromaSubsampling: '4:4:4' }).toBuffer();
    const preview = await sharp(png).resize({ width: 1280 }).png({ compressionLevel: 9 }).toFile(path.join(PREV, `s${String(page).padStart(2, '0')}-${sl.kind}.png`));
    jpegs.push(jpg);
    if (i % 8 === 0) console.log(`  rendered ${page}/${slides.length}`);
    void preview;
  }

  // ── PDF ───────────────────────────────────────────────────────────────────
  const pdf = await PDFDocument.create();
  pdf.setTitle(`${course.code} — ${course.title}`);
  pdf.setAuthor('Master of Marriage and Family Therapy');
  pdf.setSubject('Sixteen-week graduate seminar deck');
  for (const jpg of jpegs) {
    const img = await pdf.embedJpg(jpg);
    const page = pdf.addPage([W * 72, H * 72]);
    page.drawImage(img, { x: 0, y: 0, width: W * 72, height: H * 72 });
  }
  const pdfPath = path.join(OUT, `${SLUG}_16-Week-Deck.pdf`);
  fs.writeFileSync(pdfPath, await pdf.save());
  console.log('PDF written', pdfPath);

  // ── PPTX ──────────────────────────────────────────────────────────────────
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'MFT_WIDE', width: W, height: H });
  pptx.layout = 'MFT_WIDE';
  pptx.title = `${course.code} — ${course.title}`;
  pptx.author = 'Master of Marriage and Family Therapy';
  pptx.subject = 'Sixteen-week graduate seminar deck';
  pptx.company = 'MFT Programme';

  for (let i = 0; i < slides.length; i++) {
    const sl = slides[i];
    const page = i + 1;
    const slide = pptx.addSlide();
    slide.background = { path: bgFiles[sl.bg] };
    const c = new PptxCanvas(pptx, slide, W, H);
    sl.draw(c, page);
    if (sl.note) slide.addNotes(sl.note);
    if (i % 8 === 0) console.log(`  pptx ${page}/${slides.length}`);
  }

  const pptxPath = path.join(OUT, `${SLUG}_16-Week-Deck.pptx`);
  await pptx.writeFile({ fileName: pptxPath });
  const size = fs.statSync(pptxPath).size / 1024 / 1024;
  console.log(`PPTX written ${pptxPath} (${size.toFixed(1)} MB)`);
}

main().catch(err => { console.error(err); process.exit(1); });
