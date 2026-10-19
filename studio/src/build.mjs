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
const WEB = path.join(PREV, 'web');
const THUMBS = path.join(PREV, 'thumbs');
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

const FRONT = 'Front Matter';
const BACK = 'Back Matter';

export function buildSlideList(course) {
  const list = [];
  const add = (entry, meta) => list.push({ ...entry, meta });

  add({
    kind: 'cover', bg: 'cover',
    note: `Welcome to MFT 701. Introduce the course as an invitation to see relationships rather than individuals as the unit of clinical work. Name the four phases and the assessment structure.`,
    draw: (c, p) => S.cover(c, course),
  }, { title: course.title, section: FRONT, week: null, phase: null });

  add({
    kind: 'about', bg: 'paper',
    note: `Read the course description slowly. Invite students to say, in one sentence, what they hope this course will change about how they listen.`,
    draw: (c, p) => S.about(c, course, p),
  }, { title: 'A discipline of relationship, not a technique of repair', section: FRONT, week: null, phase: null });

  add({
    kind: 'outcomes', bg: 'paper',
    note: `These six outcomes are the contract for the semester. Point out that the final portfolio asks for evidence of all six, not a grade average.`,
    draw: (c, p) => S.outcomes(c, course, p),
  }, { title: 'What you will be able to do', section: FRONT, week: null, phase: null });

  add({
    kind: 'map', bg: 'paper',
    note: `Orient the class in time. Note that theory is front-loaded so that clinical work in the second half can be comparative rather than descriptive.`,
    draw: (c, p) => S.courseMap(c, course, p),
  }, { title: 'The shape of the semester', section: FRONT, week: null, phase: null });

  add({
    kind: 'rhythm', bg: 'paper',
    note: `Explain the weekly rhythm and the preparation expected before each lecture. The seminar is where the learning happens; the lecture only sets the table.`,
    draw: (c, p) => S.rhythm(c, course, p),
  }, { title: 'Read, wrestle, practise, reflect', section: FRONT, week: null, phase: null });

  add({
    kind: 'assessment', bg: 'paper',
    note: `Walk through assessment. Emphasise that the case formulation is formative — feedback in Week 9 is meant to feed the final examination.`,
    draw: (c, p) => S.assessment(c, course, p),
  }, { title: 'How the course is examined', section: FRONT, week: null, phase: null });

  course.phases.forEach((phase, pi) => {
    const section = `Phase ${phase.roman} · ${phase.name}`;
    add({
      kind: 'phase', bg: 'section',
      note: `Phase ${phase.roman}: ${phase.name}. Read the phase description and name the four weeks ahead.`,
      draw: (c, p) => S.phaseDivider(c, course, phase, p),
    }, { title: phase.name, section, week: null, phase: phase.roman });

    course.weeks.filter(w => w.phase === pi).forEach(w => {
      add({
        kind: 'week', bg: 'section',
        note: `Week ${w.n}. Ask the essential question and let it sit. Preview the three outcomes; do not read the key terms aloud.`,
        draw: (c, p) => S.weekOpener(c, course, w, p),
      }, { title: w.title, section, week: w.n, phase: phase.roman });

      w.slides.forEach(sl => {
        const bg = sl.kind === 'seminar' ? 'section' : 'paper';
        const fn = sl.kind === 'case' ? S.caseSlide : S[sl.kind];
        add({
          kind: sl.kind, bg,
          note: noteFor(w, sl),
          draw: (c, p) => fn(c, course, w, sl, p),
        }, { title: sl.title || w.title, section, week: w.n, phase: phase.roman });
      });
    });
  });

  add({
    kind: 'glossary', bg: 'paper',
    note: `A working vocabulary. Ask each student to choose one term they could not yet define precisely, and to write a definition in their journal.`,
    draw: (c, p) => S.glossary(c, course, p),
  }, { title: 'A working vocabulary', section: BACK, week: null, phase: null });

  add({
    kind: 'references', bg: 'paper',
    note: `Point students to the primary texts. The deck is a map; the reading is the territory.`,
    draw: (c, p) => S.references(c, course, p),
  }, { title: 'Core readings', section: BACK, week: null, phase: null });

  add({
    kind: 'closing', bg: 'closing',
    note: `Close by returning to the opening claim: the family is the context of the solution. Invite one sentence from each student about what they will carry forward.`,
    draw: (c, p) => S.closingSlide(c, course, p),
  }, { title: course.closing.title, section: BACK, week: null, phase: null });

  return list;
}

function manifestFor(slides, course) {
  return {
    generated: new Date().toISOString(),
    course: {
      code: course.code,
      title: course.title,
      subtitle: course.subtitle,
      semester: course.semester,
      units: course.units,
      description: course.description,
    },
    total: slides.length,
    phases: course.phases.map(p => ({ roman: p.roman, name: p.name, start: p.start, end: p.end, blurb: p.blurb })),
    slides: slides.map((sl, i) => ({
      n: i + 1,
      kind: sl.kind,
      title: sl.meta.title,
      section: sl.meta.section,
      week: sl.meta.week,
      phase: sl.meta.phase,
      note: sl.note,
      image: `s${String(i + 1).padStart(2, '0')}-${sl.kind}.jpg`,
      thumb: `s${String(i + 1).padStart(2, '0')}-${sl.kind}.jpg`,
    })),
  };
}

export async function main() {
  const webOnly = process.env.MFT_WEB_ONLY === '1';
  fs.mkdirSync(OUT, { recursive: true });
  fs.mkdirSync(PREV, { recursive: true });
  fs.mkdirSync(WEB, { recursive: true });
  fs.mkdirSync(THUMBS, { recursive: true });

  const slides = buildSlideList(course);
  course.slideCount = slides.length;
  console.log(`Composing ${slides.length} slides…`);

  setBackgrounds(bgMarkup);
  const bgFiles = await writeBackgrounds(BG);

  // ── SVG → JPEG (web) + PNG (preview) ──────────────────────────────────────
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
    jpegs.push(jpg);
    const stem = `s${String(page).padStart(2, '0')}-${sl.kind}`;
    await sharp(png).resize({ width: 1280 }).png({ compressionLevel: 9 }).toFile(path.join(PREV, `${stem}.png`));
    // Full-bleed 1920px still for the web presentation viewer.
    await sharp(jpg).resize({ width: 1920 }).jpeg({ quality: 84, mozjpeg: true }).toFile(path.join(WEB, `${stem}.jpg`));
    // Small still for the filmstrip, contents grid, and week cards.
    await sharp(jpg).resize({ width: 480 }).jpeg({ quality: 76, mozjpeg: true }).toFile(path.join(THUMBS, `${stem}.jpg`));
    if (i % 8 === 0) console.log(`  rendered ${page}/${slides.length}`);
  }

  const manifest = manifestFor(slides, course);
  fs.writeFileSync(path.join(PREV, 'manifest.json'), JSON.stringify(manifest, null, 2));

  if (webOnly) {
    console.log(`Web stills written (${slides.length}). Manifest written.`);
    return;
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

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(import.meta.filename);
if (invokedDirectly) main().catch(err => { console.error(err); process.exit(1); });
