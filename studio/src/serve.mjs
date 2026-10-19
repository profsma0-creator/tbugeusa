// Static presentation server for the MFT 701 deck.
// Serves the viewer, the rendered stills, the fonts, and the downloadable deck files.
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';

import course from './content/mft701.mjs';
import { buildSlideList } from './build.mjs';

const ROOT = path.resolve(import.meta.dirname, '../..');
const VIEWER = path.join(ROOT, 'viewer');
const WEB = path.join(ROOT, 'preview', 'web');
const THUMBS = path.join(ROOT, 'preview', 'thumbs');
const PREVIEW = path.join(ROOT, 'preview');
const FONTS = path.resolve(import.meta.dirname, '../assets/fonts');
const DECKS = path.join(ROOT, 'decks');

const PORT = Number(process.env.PORT || 4173);
const HOST = process.env.HOST || '0.0.0.0';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.pdf': 'application/pdf',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
};

function safeJoin(base, rel) {
  const target = path.resolve(base, '.' + path.posix.normalize('/' + rel));
  return target.startsWith(base + path.sep) ? target : null;
}

function sendFile(res, file, { cache = 'public, max-age=86400', download = null } = {}) {
  fs.stat(file, (err, stat) => {
    if (err || !stat.isFile()) {
      res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
      res.end('Not found');
      return;
    }
    const headers = {
      'content-type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'content-length': stat.size,
      'cache-control': cache,
      'access-control-allow-origin': '*',
    };
    if (download) headers['content-disposition'] = `attachment; filename="${download}"`;
    res.writeHead(200, headers);
    fs.createReadStream(file).pipe(res);
  });
}

function manifest() {
  const slides = buildSlideList(course);
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

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname;
  try { pathname = decodeURIComponent(url.pathname); } catch { pathname = '/'; }

  if (pathname === '/api/manifest') {
    const body = JSON.stringify(manifest());
    res.writeHead(200, {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      'access-control-allow-origin': '*',
    });
    res.end(body);
    return;
  }

  if (pathname === '/api/health') {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ ok: true, slides: course.slideCount }));
    return;
  }

  if (pathname.startsWith('/slides/')) {
    const f = safeJoin(WEB, pathname.slice('/slides/'.length));
    if (f) return sendFile(res, f);
  }
  if (pathname.startsWith('/thumbs/')) {
    const f = safeJoin(THUMBS, pathname.slice('/thumbs/'.length));
    if (f) return sendFile(res, f);
  }
  if (pathname.startsWith('/preview/')) {
    const f = safeJoin(PREVIEW, pathname.slice('/preview/'.length));
    if (f) return sendFile(res, f);
  }
  if (pathname.startsWith('/fonts/')) {
    const f = safeJoin(FONTS, pathname.slice('/fonts/'.length));
    if (f) return sendFile(res, f, { cache: 'public, max-age=604800' });
  }
  if (pathname.startsWith('/download/')) {
    const name = pathname.slice('/download/'.length);
    const mapping = {
      pptx: 'MFT-701_Fundamentals-of-Marriage-and-Family-Therapy_16-Week-Deck.pptx',
      pdf: 'MFT-701_Fundamentals-of-Marriage-and-Family-Therapy_16-Week-Deck.pdf',
    };
    if (mapping[name]) {
      return sendFile(res, path.join(DECKS, mapping[name]), { download: mapping[name], cache: 'no-store' });
    }
  }

  const rel = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const file = safeJoin(VIEWER, rel);
  if (!file) {
    res.writeHead(403); res.end('Forbidden'); return;
  }
  if (fs.existsSync(file) && fs.statSync(file).isFile()) {
    const cache = /\.(png|jpg|jpeg|svg|woff2|ttf)$/i.test(file)
      ? 'public, max-age=604800'
      : 'no-cache';
    return sendFile(res, file, { cache });
  }

  // SPA fallback
  return sendFile(res, path.join(VIEWER, 'index.html'), { cache: 'no-cache' });
});

server.listen(PORT, HOST, () => {
  console.log(`MFT 701 presentation viewer → http://${HOST}:${PORT}`);
});
