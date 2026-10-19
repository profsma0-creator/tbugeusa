/* MFT 701 — presentation viewer */
(() => {
  'use strict';

  const $ = (sel) => document.querySelector(sel);
  const body = document.body;

  const KIND = {
    cover: 'Cover',
    about: 'Course Description',
    outcomes: 'Learning Outcomes',
    map: 'Semester Arc',
    rhythm: 'Weekly Rhythm',
    assessment: 'Assessment',
    phase: 'Phase',
    week: 'Week',
    concept: 'Lecture',
    diagram: 'Diagram',
    case: 'Clinical Case',
    seminar: 'Seminar',
    glossary: 'Glossary',
    references: 'References',
    closing: 'Closing',
  };

  const state = {
    manifest: null,
    slides: [],
    n: 1,
    layers: [],
    activeLayer: 0,
    token: 0,
    entered: false,
  };

  const el = {
    boot: $('#boot'),
    intro: $('#intro'),
    deck: $('#deck'),
    frame: $('#frame'),
    stage: $('#stage'),
    layerA: $('#layerA'),
    layerB: $('#layerB'),
    spinner: $('#spinner'),
    prev: $('#prevBtn'),
    next: $('#nextBtn'),
    counter: $('#counter'),
    total: $('#total'),
    progress: $('#progressFill'),
    rail: $('#weekRail'),
    film: $('#filmstrip'),
    kind: $('#slideKind'),
    title: $('#slideTitle'),
    section: $('#sectionLabel'),
    drawer: $('#drawer'),
    drawerBody: $('#drawerBody'),
    scrim: $('#scrim'),
    notes: $('#notes'),
    notesKind: $('#notesKind'),
    notesTitle: $('#notesTitle'),
    notesText: $('#notesText'),
    notesCount: $('#notesCount'),
    grid: $('#grid'),
    gridBody: $('#gridBody'),
    help: $('#help'),
    menu: $('#downloadMenu'),
    menuBtn: $('#downloadBtn'),
    live: $('#live'),
  };

  const pad = (n) => String(n).padStart(2, '0');
  const storage = {
    get(k, fb) { try { const v = localStorage.getItem(k); return v === null ? fb : v; } catch { return fb; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* ignore */ } },
  };

  // ── data ──────────────────────────────────────────────────────────────────
  async function load() {
    const res = await fetch('/api/manifest', { cache: 'no-store' });
    if (!res.ok) throw new Error(`Manifest unavailable (${res.status})`);
    const data = await res.json();
    state.manifest = data;
    state.slides = data.slides;
    buildChrome();
    return data;
  }

  const slideAt = (n) => state.slides[n - 1];

  function buildChrome() {
    el.total.textContent = state.slides.length;

    // week rail (16 ticks)
    el.rail.innerHTML = '';
    for (let w = 1; w <= 16; w++) {
      const target = weekSlide(w);
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'rail__tick';
      b.dataset.week = String(w);
      b.innerHTML = `<span>${pad(w)}</span>`;
      b.title = target ? `Week ${pad(w)} — ${target.title}` : `Week ${pad(w)}`;
      b.setAttribute('aria-label', b.title);
      if (target) b.addEventListener('click', () => go(target.n));
      else b.disabled = true;
      el.rail.appendChild(b);
    }

    // filmstrip
    el.film.innerHTML = '';
    state.slides.forEach((s) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'thumb';
      b.dataset.n = String(s.n);
      b.title = `${pad(s.n)} — ${s.title}`;
      b.setAttribute('aria-label', `Go to slide ${s.n}: ${s.title}`);
      b.innerHTML = `<img loading="lazy" src="/thumbs/${s.thumb || s.image}" alt=""><span class="thumb__n">${pad(s.n)}</span>`;
      b.addEventListener('click', () => go(s.n));
      el.film.appendChild(b);
    });

    buildDrawer();
    buildGrid();
  }

  function weekSlide(w) {
    return state.slides.find((s) => s.kind === 'week' && s.week === w);
  }

  // ── drawer ────────────────────────────────────────────────────────────────
  function buildDrawer() {
    const sections = [];
    for (const s of state.slides) {
      let sec = sections.find((x) => x.name === s.section);
      if (!sec) { sec = { name: s.section, slides: [] }; sections.push(sec); }
      sec.slides.push(s);
    }

    el.drawerBody.innerHTML = '';
    sections.forEach((sec) => {
      const wrap = document.createElement('div');
      wrap.className = 'drawer__group';

      const head = document.createElement('div');
      head.className = 'drawer__group-head';
      const isPhase = /^Phase/.test(sec.name);
      const weeksIn = new Set(sec.slides.map((s) => s.week).filter(Boolean)).size;
      const count = isPhase ? `${weeksIn} weeks` : `${sec.slides.length} slides`;
      head.innerHTML = `<h3>${escapeHtml(sec.name)}</h3><span>${count}</span>`;
      wrap.appendChild(head);

      const rows = isPhase
        ? sec.slides.filter((s) => s.kind === 'phase' || s.kind === 'week')
        : sec.slides;

      rows.forEach((s) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = `drawer__link${s.kind === 'phase' ? ' is-phase' : ''}`;
        b.dataset.n = String(s.n);
        const label = s.kind === 'phase' ? 'Phase opening' : s.title;
        b.innerHTML = `<span class="drawer__n">${s.kind === 'week' ? pad(s.week) : s.kind === 'phase' ? s.phase : pad(s.n)}</span><span class="drawer__t">${escapeHtml(label)}</span>`;
        b.addEventListener('click', () => { if (isIntro()) enter(); go(s.n); closePanels(); });
        wrap.appendChild(b);
      });

      el.drawerBody.appendChild(wrap);
    });

    const sub = document.createElement('p');
    sub.className = 'drawer__sub';
    sub.textContent = 'Sixteen weeks · four phases';
    el.drawerBody.appendChild(sub);
  }

  // ── grid ──────────────────────────────────────────────────────────────────
  function buildGrid() {
    const sections = [];
    for (const s of state.slides) {
      let sec = sections.find((x) => x.name === s.section);
      if (!sec) { sec = { name: s.section, slides: [] }; sections.push(sec); }
      sec.slides.push(s);
    }

    el.gridBody.innerHTML = '';
    sections.forEach((sec) => {
      const block = document.createElement('section');
      block.className = 'grid__section';
      const weeks = [...new Set(sec.slides.map((s) => s.week).filter(Boolean))];
      const meta = weeks.length
        ? `Weeks ${pad(Math.min(...weeks))}–${pad(Math.max(...weeks))}`
        : sec.name === 'Front Matter' ? 'Introduction' : 'Closing material';
      block.innerHTML = `<div class="grid__section-head"><h3>${escapeHtml(sec.name)}</h3><span>${meta}</span></div>`;

      const cards = document.createElement('div');
      cards.className = 'grid__cards';
      sec.slides.forEach((s) => {
        const c = document.createElement('button');
        c.type = 'button';
        c.className = 'card';
        c.dataset.n = String(s.n);
        c.innerHTML = `
          <span class="card__img">
            <img loading="lazy" src="/thumbs/${s.thumb || s.image}" alt="">
            <span class="card__n">${pad(s.n)}</span>
          </span>
          <span class="card__meta">
            <span class="card__kind">${kindLabel(s)}</span>
            <span class="card__title">${escapeHtml(s.title)}</span>
          </span>`;
        c.addEventListener('click', () => { if (isIntro()) enter(); go(s.n); closePanels(); });
        cards.appendChild(c);
      });
      block.appendChild(cards);
      el.gridBody.appendChild(block);
    });
  }

  function kindLabel(s) {
    if (s.kind === 'week') return `Week ${pad(s.week)}`;
    if (s.week) return `Week ${pad(s.week)} · ${KIND[s.kind] || s.kind}`;
    return KIND[s.kind] || s.kind;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  // ── slide rendering ───────────────────────────────────────────────────────
  function go(n, opts = {}) {
    n = Math.min(Math.max(1, Number(n) || 1), state.slides.length);
    if (n === state.n && state.entered && !opts.force) { syncHash(); return; }
    state.n = n;
    const s = slideAt(n);
    if (!s) return;

    const token = ++state.token;
    const incoming = state.layers[1 - state.activeLayer];
    const outgoing = state.layers[state.activeLayer];
    const src = `/slides/${s.image}`;

    let done = false;
    const activate = () => {
      if (done || token !== state.token) return;
      done = true;
      el.frame.classList.remove('is-loading');
      outgoing.classList.remove('is-active');
      incoming.classList.add('is-active');
      state.activeLayer = 1 - state.activeLayer;
      incoming.alt = s.title;
      preload(n + 1);
      preload(n + 2);
      preload(n - 1);
    };

    if (incoming.getAttribute('src') === src && incoming.complete) {
      activate();
    } else {
      el.frame.classList.add('is-loading');
      incoming.onload = activate;
      incoming.onerror = () => {
        el.frame.classList.remove('is-loading');
        activate();
      };
      incoming.src = src;
      if (incoming.complete) activate();
    }

    updateChrome(s);
    syncHash();
  }

  function preload(n) {
    const s = slideAt(n);
    if (!s) return;
    const img = new Image();
    img.decoding = 'async';
    img.src = `/slides/${s.image}`;
  }

  function updateChrome(s) {
    el.section.textContent = s.section;
    el.kind.textContent = kindLabel(s);
    el.title.textContent = s.title;
    el.counter.textContent = pad(s.n);
    el.progress.style.width = `${(s.n / state.slides.length) * 100}%`;
    el.prev.disabled = s.n === 1;
    el.next.disabled = s.n === state.slides.length;

    // rail
    const currentWeek = s.week;
    [...el.rail.children].forEach((tick) => {
      const w = Number(tick.dataset.week);
      const target = weekSlide(w);
      tick.classList.toggle('is-current', w === currentWeek);
      tick.classList.toggle('is-visited', Boolean(target && target.n <= s.n));
    });

    // filmstrip
    [...el.film.children].forEach((t) => t.classList.toggle('is-active', Number(t.dataset.n) === s.n));
    const activeThumb = el.film.querySelector('.thumb.is-active');
    if (activeThumb && !body.classList.contains('no-film')) {
      const fr = el.film.getBoundingClientRect();
      const tr = activeThumb.getBoundingClientRect();
      if (tr.left < fr.left + 40 || tr.right > fr.right - 40) {
        activeThumb.scrollIntoView({ inline: 'center', block: 'nearest', behavior: 'smooth' });
      }
    }

    // drawer + grid active states
    el.drawerBody.querySelectorAll('.drawer__link').forEach((r) => {
      r.classList.toggle('is-active', Number(r.dataset.n) === s.n);
    });
    el.gridBody.querySelectorAll('.card').forEach((c) => {
      c.classList.toggle('is-active', Number(c.dataset.n) === s.n);
    });

    // notes
    el.notesKind.textContent = kindLabel(s);
    el.notesTitle.textContent = s.title;
    el.notesText.textContent = s.note || 'No speaker note for this slide.';
    el.notesCount.textContent = `${pad(s.n)} / ${state.slides.length}`;

    el.live.textContent = `Slide ${s.n} of ${state.slides.length}. ${s.title}`;
    document.title = `MFT 701 · ${pad(s.n)} — ${s.title}`;
  }

  // ── hash ──────────────────────────────────────────────────────────────────
  function syncHash() {
    if (!state.entered) return;
    const target = `#/s${state.n}`;
    if (location.hash !== target) history.replaceState(null, '', target);
  }

  function hashSlide() {
    const m = location.hash.match(/s(\d+)/);
    return m ? Number(m[1]) : null;
  }

  // ── intro / entry ─────────────────────────────────────────────────────────
  const isIntro = () => body.classList.contains('is-intro');

  function enter() {
    if (state.entered) return;
    state.entered = true;
    body.classList.add('is-entering');
    el.deck.setAttribute('aria-hidden', 'false');
    setTimeout(() => {
      body.classList.remove('is-intro');
      body.classList.add('is-deck');
      el.intro.setAttribute('aria-hidden', 'true');
    }, 520);
  }

  // ── panels ────────────────────────────────────────────────────────────────
  let openPanel = null;

  function setPanel(name) {
    const wanted = openPanel === name ? null : name;
    openPanel = wanted;

    const drawerOpen = wanted === 'drawer';
    const notesOpen = wanted === 'notes';
    const gridOpen = wanted === 'grid';
    const helpOpen = wanted === 'help';

    el.drawer.classList.toggle('is-open', drawerOpen);
    el.drawer.setAttribute('aria-hidden', String(!drawerOpen));
    el.notes.classList.toggle('is-open', notesOpen);
    el.notes.setAttribute('aria-hidden', String(!notesOpen));
    el.grid.classList.toggle('is-open', gridOpen);
    el.grid.setAttribute('aria-hidden', String(!gridOpen));
    el.help.classList.toggle('is-open', helpOpen);
    el.help.setAttribute('aria-hidden', String(!helpOpen));
    el.scrim.classList.toggle('is-open', drawerOpen || notesOpen);

    document.querySelector('[data-action="notes"]').classList.toggle('is-on', notesOpen);
    document.querySelector('[data-action="contents"]').classList.toggle('is-on', drawerOpen);
    document.querySelector('[data-action="grid"]').classList.toggle('is-on', gridOpen);

    if (drawerOpen) {
      el.drawer.querySelector('.icon-btn').focus({ preventScroll: true });
      el.drawerBody.querySelector('.drawer__link.is-active')?.scrollIntoView({ block: 'center' });
    }
    if (gridOpen) {
      requestAnimationFrame(() => { el.gridBody.scrollTop = 0; });
    }
  }

  function closePanels() {
    if (openPanel) setPanel(openPanel); // toggles the open one shut
    el.menu.classList.remove('is-open');
    el.menu.setAttribute('aria-hidden', 'true');
    el.menuBtn.setAttribute('aria-expanded', 'false');
  }

  // ── misc UI ───────────────────────────────────────────────────────────────
  function toggleFullscreen() {
    const root = document.documentElement;
    if (!document.fullscreenElement) {
      if (root.requestFullscreen) root.requestFullscreen().catch(() => {});
    } else if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  }

  function toggleFilm() {
    const on = body.classList.toggle('no-film') === false;
    $('#filmToggle').setAttribute('aria-pressed', String(on));
    storage.set('mft701.film', on ? 'on' : 'off');
  }

  // ── events ────────────────────────────────────────────────────────────────
  function bind() {
    $('#enterBtn').addEventListener('click', () => { enter(); go(state.n, { force: true }); });
    $('#introContentsBtn').addEventListener('click', () => setPanel('drawer'));

    el.prev.addEventListener('click', () => go(state.n - 1));
    el.next.addEventListener('click', () => go(state.n + 1));
    el.frame.addEventListener('click', () => go(state.n + 1));

    document.querySelectorAll('[data-action]').forEach((b) => {
      b.addEventListener('click', () => {
        const a = b.dataset.action;
        if (a === 'contents') setPanel('drawer');
        if (a === 'notes') setPanel('notes');
        if (a === 'grid') setPanel('grid');
        if (a === 'fullscreen') toggleFullscreen();
      });
    });

    document.querySelectorAll('[data-close]').forEach((b) => {
      b.addEventListener('click', () => setPanel(b.dataset.close));
    });

    el.scrim.addEventListener('click', closePanels);

    el.menuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = el.menu.classList.toggle('is-open');
      el.menu.setAttribute('aria-hidden', String(!open));
      el.menuBtn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', (e) => {
      if (!el.menu.classList.contains('is-open')) return;
      if (!e.target.closest('.menu-wrap')) {
        el.menu.classList.remove('is-open');
        el.menu.setAttribute('aria-hidden', 'true');
        el.menuBtn.setAttribute('aria-expanded', 'false');
      }
    });

    $('#filmToggle').addEventListener('click', toggleFilm);

    el.help.addEventListener('click', (e) => {
      if (e.target === el.help) setPanel('help');
    });

    // keyboard
    document.addEventListener('keydown', (e) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;

      if (e.key === 'Escape') {
        if (openPanel) { setPanel(openPanel); return; }
        if (el.menu.classList.contains('is-open')) { el.menu.classList.remove('is-open'); return; }
        if (!isIntro()) { history.replaceState(null, '', location.pathname); return; }
      }

      if (isIntro()) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); enter(); go(state.n, { force: true }); }
        return;
      }

      switch (e.key) {
        case 'ArrowRight':
        case 'PageDown':
        case ' ':
          e.preventDefault(); go(state.n + 1); break;
        case 'ArrowLeft':
        case 'PageUp':
          e.preventDefault(); go(state.n - 1); break;
        case 'Home':
          e.preventDefault(); go(1); break;
        case 'End':
          e.preventDefault(); go(state.slides.length); break;
        case 'g': case 'G':
          setPanel('grid'); break;
        case 'c': case 'C':
          setPanel('drawer'); break;
        case 'n': case 'N':
          setPanel('notes'); break;
        case 'f': case 'F':
          toggleFullscreen(); break;
        case 't': case 'T':
          toggleFilm(); break;
        case '?':
          setPanel('help'); break;
        default:
          break;
      }
    });

    // swipe
    let touchX = null;
    let touchY = null;
    el.stage.addEventListener('touchstart', (e) => {
      touchX = e.changedTouches[0].clientX;
      touchY = e.changedTouches[0].clientY;
    }, { passive: true });
    el.stage.addEventListener('touchend', (e) => {
      if (touchX === null) return;
      const dx = e.changedTouches[0].clientX - touchX;
      const dy = e.changedTouches[0].clientY - touchY;
      if (Math.abs(dx) > 52 && Math.abs(dx) > Math.abs(dy) * 1.4) {
        go(state.n + (dx < 0 ? 1 : -1));
      }
      touchX = touchY = null;
    }, { passive: true });

    window.addEventListener('hashchange', () => {
      const n = hashSlide();
      if (n && n !== state.n) {
        if (isIntro()) enter();
        go(n);
      }
    });
  }

  // ── boot ──────────────────────────────────────────────────────────────────
  async function start() {
    state.layers = [el.layerA, el.layerB];
    el.layerA.alt = '';

    try {
      await load();
    } catch (err) {
      el.boot.querySelector('.boot__label').textContent = 'The deck could not be loaded. Run the build first.';
      el.boot.querySelector('.boot__ring').style.display = 'none';
      console.error(err);
      return;
    }

    bind();

    const stored = storage.get('mft701.film', 'on');
    if (stored === 'off') {
      body.classList.add('no-film');
      $('#filmToggle').setAttribute('aria-pressed', 'false');
    }

    const deep = hashSlide();
    state.n = deep && deep >= 1 && deep <= state.slides.length ? deep : 1;

    // paint the first (or deep-linked) frame behind the intro
    go(state.n, { force: true });
    updateChrome(slideAt(state.n));

    if (deep) {
      state.entered = true;
      body.classList.remove('is-intro');
      body.classList.add('is-deck');
      el.deck.setAttribute('aria-hidden', 'false');
      el.intro.setAttribute('aria-hidden', 'true');
    }

    requestAnimationFrame(() => requestAnimationFrame(() => body.classList.add('is-ready')));
  }

  start();
})();
