#!/usr/bin/env python3
"""Typeset the CPY 903 textbook as a print-ready PDF.

Pipeline
--------
pass A   body only, to resolve the folio (printed page number) of every
         chapter, part, section, figure and table heading;
pass B   complete book, with the table of contents, list of figures and list of
         tables filled from pass A. Page numbering is independent of front
         matter length because the body restarts at 1;
pass C   optional third pass that appends a subject index located by scanning
         the pass B PDF for the glossary headwords.

Running:  python3 typeset/build.py [--final]
"""

import argparse
import glob
import math
import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame,
                                FrameBreak, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmeta as META
import markup
from diagrams import ConceptualMap, CurveFigure
from style import (ACCENT, INK, INK_SOFT, M_BOTTOM, M_INNER, M_OUTER, M_TOP,
                   PAGE_H, PAGE_W, PANEL, RULE, RULE_LIGHT, STYLES, TEXT_H,
                   TEXT_W, register_fonts)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
OUT = os.path.join(ROOT, "output")
ROMAN = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi",
         "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx", "xxi",
         "xxii", "xxiii", "xxiv", "xxv", "xxvi", "xxvii", "xxviii", "xxix",
         "xxx", "xxxi", "xxxii"]


def roman(n):
    return ROMAN[n] if n < len(ROMAN) else str(n)


# --------------------------------------------------------------------------
# small flowables
# --------------------------------------------------------------------------
class Hr(Flowable):
    """A short horizontal rule used under chapter titles and part labels."""

    def __init__(self, width=54, thickness=0.9, space_before=6, space_after=8,
                 color=ACCENT):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.sb = space_before
        self.sa = space_after
        self.color = color

    def wrap(self, aw, ah):
        return (self.width, self.thickness + self.sb + self.sa)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.sa, self.width, self.sa)


class LeaderList(Flowable):
    """A table of contents / list of figures with dot leaders.

    Entries are pre-laid out into physical lines so the flowable can split
    across pages without losing the leaders or the right-aligned folios.
    """

    def __init__(self, entries, width=TEXT_W, font="Body", size=9.3,
                 leading=12.2, page_font="Body-Med"):
        Flowable.__init__(self)
        self.width = width
        self.font = font
        self.size = size
        self.leading = leading
        self.page_font = page_font
        self.lines = []          # (kind, indent, text, page, space_before)
        self._layout(entries)

    def _layout(self, entries):
        for e in entries:
            kind = e.get("kind", "entry")
            indent = e.get("indent", 0)
            font = e.get("font", self.font)
            size = e.get("size", self.size)
            page = str(e.get("page", ""))
            space_before = e.get("space_before", 0)
            avail = self.width - indent - stringWidth(page, self.page_font, size) - 8
            words = e["text"].split()
            cur = ""
            rows = []
            for w in words:
                trial = (cur + " " + w).strip()
                if stringWidth(trial, font, size) <= avail or not cur:
                    cur = trial
                else:
                    rows.append(cur)
                    cur = w
            if cur:
                rows.append(cur)
            for i, r in enumerate(rows):
                self.lines.append(
                    dict(kind=kind, indent=indent, text=r, font=font, size=size,
                         page=page if i == len(rows) - 1 else "",
                         space_before=space_before if i == 0 else 0))

    def wrap(self, aw, ah):
        h = sum(l["space_before"] + self.leading for l in self.lines)
        self.height = h
        return (self.width, h)

    def split(self, aw, ah):
        if ah <= self.leading:
            return []
        acc, cut = 0.0, 0
        for i, l in enumerate(self.lines):
            nxt = acc + l["space_before"] + self.leading
            if nxt > ah:
                break
            acc = nxt
            cut = i + 1
        if cut == 0:
            return []
        head = LeaderList([], width=self.width)
        head.lines = self.lines[:cut]
        head.lines[0]["space_before"] = 0
        tail = LeaderList([], width=self.width)
        tail.lines = self.lines[cut:]
        return [head, tail]

    def draw(self):
        c = self.canv
        y = self.height
        for l in self.lines:
            y -= l["space_before"]
            baseline = y - self.leading + 3.2
            font, size = l["font"], l["size"]
            c.setFont(font, size)
            c.setFillColor(INK)
            c.drawString(l["indent"], baseline, l["text"])
            if l["page"]:
                pw = stringWidth(l["page"], self.page_font, size)
                c.setFont(self.page_font, size)
                c.drawRightString(self.width, baseline, l["page"])
                # leaders
                start = l["indent"] + stringWidth(l["text"], font, size) + 4
                end = self.width - pw - 4
                if end - start > 8:
                    dot_w = stringWidth(". ", font, size)
                    n = max(2, int((end - start) / dot_w))
                    c.setFont(font, size)
                    c.setFillColor(RULE)
                    c.drawString(start, baseline, ". " * n)
            y -= self.leading
        c.setFillColor(INK)


# --------------------------------------------------------------------------
# document template
# --------------------------------------------------------------------------
class BookCanvas(canvas.Canvas):
    """Canvas whose initial font is the book's serif, not Helvetica, so that no
    non-embedded base-14 font resources enter the PDF."""

    def __init__(self, *a, **kw):
        kw.setdefault("initialFontName", "Body")
        kw.setdefault("initialFontSize", 11)
        kw.setdefault("initialLeading", 15.2)
        canvas.Canvas.__init__(self, *a, **kw)


class Book(BaseDocTemplate):
    def __init__(self, filename, pagemap=None, index_entries=None, **kw):
        BaseDocTemplate.__init__(
            self, filename, pagesize=(PAGE_W, PAGE_H), canvasmaker=BookCanvas,
            leftMargin=M_INNER, rightMargin=M_OUTER,
            topMargin=M_TOP, bottomMargin=M_BOTTOM,
            title=f"{META.COURSE}: {META.TITLE}. {META.SUBTITLE}",
            author=f"{META.AUTHOR}",
            subject=("Doctoral-level textbook in counselling psychology: "
                     "psychological assessment, psychometrics, diagnosis and "
                     "case formulation"),
            creator="Typeset with ReportLab; text set in EB Garamond and Source Serif 4",
            keywords=("psychological assessment, diagnosis, psychometrics, "
                      "counselling psychology, case formulation, DSM-5-TR, ICD-11"),
        )
        self.pagemap = pagemap or {}
        self.index_entries = index_entries or []
        self.body_start = None
        self.chapter_label = ""
        self.section_label = ""
        self.pending_opener = False
        self.opening_pages = set()
        self.head = "none"            # none | verso_title
        self.records = {"toc": [], "fig": [], "tab": [], "ol": [], "fm": []}
        self.part_count = 0
        self.marks = {}
        self.blank_before = set()
        self.blank_pages = set()
        self._build_templates()

    # ---------------------------------------------------------------- pages
    def _build_templates(self):
        recto_frame = Frame(M_INNER, M_BOTTOM, TEXT_W, TEXT_H, id="recto",
                            leftPadding=0, rightPadding=0, topPadding=0,
                            bottomPadding=0)
        verso_frame = Frame(M_OUTER, M_BOTTOM, TEXT_W, TEXT_H, id="verso",
                            leftPadding=0, rightPadding=0, topPadding=0,
                            bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="recto", frames=[recto_frame],
                         onPage=lambda c, d: d.page_start(d, "recto"),
                         onPageEnd=lambda c, d: d.page_end(c, "recto")),
            PageTemplate(id="verso", frames=[verso_frame],
                         onPage=lambda c, d: d.page_start(d, "verso"),
                         onPageEnd=lambda c, d: d.page_end(c, "verso")),
        ])

    def folio(self, page=None):
        page = self.page if page is None else page
        if self.body_start is None:
            return roman(page)
        return str(page - self.body_start + 1)

    def handle_pageBegin(self):
        BaseDocTemplate.handle_pageBegin(self)
        # alternate recto / verso for the *next* page
        nxt = "verso" if self.page % 2 == 1 else "recto"
        self.handle_nextPageTemplate(nxt)

    # ------------------------------------------------------------ furniture
    def page_start(self, doc, side):
        self._side = side
        self.page_opener = False

    def page_end(self, canv, side):
        """Running head and folio are drawn at page end, when it is known
        whether the page opened a chapter."""
        canv.saveState()
        page = self.page
        in_body = self.body_start is not None and page >= self.body_start
        if page in self.blank_pages:
            canv.restoreState()
            return
        if in_body and not getattr(self, "page_opener", False):
            head = self.chapter_label
            if head:
                canv.setFont("Body-Med", 7.1)
                canv.setFillColor(INK_SOFT)
                text = self._track(head.upper(), 0.6)
                if side == "verso":
                    canv.drawString(M_OUTER, PAGE_H - 44, text)
                else:
                    canv.drawRightString(PAGE_W - M_OUTER, PAGE_H - 44, text)
        if page not in (1, 2):
            canv.setFont("Body", 8.4)
            canv.setFillColor(INK)
            canv.drawCentredString(PAGE_W / 2.0, 38, self.folio())
        canv.restoreState()

    @staticmethod
    def _track(text, extra):
        """Light letterspacing for versal running heads."""
        return (u"\u2009" * 0).join(text)

    # ------------------------------------------------------- heading hooks
    def afterFlowable(self, flowable):
        rec = getattr(flowable, "_chap_record", None)
        if rec:
            kind = rec["kind"]
            key = rec["key"]
            self.canv.bookmarkPage(key)
            if kind == "part":
                self.canv.addOutlineEntry(rec["text"], key, level=0, closed=False)
                self.records["toc"].append(dict(kind="part", text=rec["text"],
                                                page=self.folio(), indent=0,
                                                space_before=11, font="Body-Semi",
                                                size=9.6))
            elif kind == "fm":
                self.canv.addOutlineEntry(rec["text"], key, level=0, closed=False)
                self.records["fm"].append(dict(text=markup.typographic(rec["text"]),
                                            page=self.folio(),
                                               indent=0, space_before=8,
                                               font="Body-Semi", size=9.4))
            elif kind == "back":
                self.canv.addOutlineEntry(rec["text"], key, level=0, closed=False)
                self.records["toc"].append(dict(kind="chapter", text=rec["text"],
                                                page=self.folio(), indent=0,
                                                space_before=11, font="Body-Semi",
                                                size=9.4))
                self.chapter_label = rec["short"]
            elif kind == "chapter":
                self.canv.addOutlineEntry(rec["text"], key, level=0, closed=False)
                self.records["toc"].append(dict(kind="chapter", text=rec["text"],
                                                page=self.folio(), indent=0,
                                                space_before=9, font="Body-Semi",
                                                size=9.4))
                self.chapter_label = rec["short"]
            elif kind == "fmsec":
                # front-matter subheads appear in the PDF outline but not in
                # the printed contents, which lists the front matter only once
                self.canv.addOutlineEntry(rec["text"], key, level=1, closed=True)
            elif kind == "section":
                self.canv.addOutlineEntry(rec["text"], key, level=1, closed=False)
                self.records["toc"].append(dict(kind="section",
                                                text=markup.typographic(rec["text"]),
                                                page=self.folio(), indent=14,
                                                size=8.8))
                self.section_label = rec["text"]
            elif kind == "figure":
                self.records["fig"].append(dict(text=markup.typographic(rec["text"]),
                                                page=self.folio(),
                                                indent=0, size=8.8))
            elif kind == "table":
                self.records["tab"].append(dict(text=markup.typographic(rec["text"]),
                                                page=self.folio(),
                                                indent=0, size=8.8))


# --------------------------------------------------------------------------
# flowable builders
# --------------------------------------------------------------------------
def para(text, style="Body"):
    return Paragraph(markup.inline(text), STYLES[style])


def make_table(block):
    rows = block.rows
    rules = block.rules
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    head_rows = rules[0] if rules else 1
    head_rows = max(1, head_rows)

    # column widths: start from measured content, keep every column wide
    # enough for its longest word, then distribute the remaining space to the
    # widest descriptive column
    natural, longest_word = [], []
    for c in range(ncols):
        w = 0.0
        lw = 0.0
        for i, r in enumerate(rows):
            f = "Body-Semi" if i < head_rows else "Body"
            s_ = 8.8 if i < head_rows else 9.0
            w = max(w, stringWidth(r[c], f, s_))
            for word in r[c].split():
                lw = max(lw, stringWidth(word, f, s_))
        natural.append(w + 8)
        longest_word.append(lw + 7)
    # balance the measure: allocate space by the square root of each column's
    # natural width, so a long prose column does not squeeze a short one to a
    # ribbon, then raise any column that would break its longest word
    total = sum(math.sqrt(max(n, 1.0)) for n in natural) or 1.0
    widths = [TEXT_W * math.sqrt(max(n, 1.0)) / total for n in natural]
    for _ in range(4):
        short = [i for i, w in enumerate(widths) if w < longest_word[i]]
        if not short:
            break
        fixed = sum(longest_word[i] for i in short)
        free = [i for i in range(ncols) if i not in short]
        tot = sum(math.sqrt(max(natural[i], 1.0)) for i in free) or 1.0
        for i in range(ncols):
            widths[i] = (longest_word[i] if i in short else
                         (TEXT_W - fixed) * math.sqrt(max(natural[i], 1.0)) / tot)

    data = [[Paragraph(markup.inline(cell), STYLES["TableHead" if i < head_rows
                                                 else "TableCell"])
             for cell in r] for i, r in enumerate(rows)]

    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, INK),
        ("LINEBELOW", (0, head_rows - 1), (-1, head_rows - 1), 0.5, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, INK),
    ]
    for r in rules[1:]:
        if 0 < r < len(rows):
            style.append(("LINEBELOW", (0, r - 1), (-1, r - 1), 0.35, RULE))
    t = Table(data, colWidths=widths, repeatRows=head_rows)
    t.setStyle(TableStyle(style))
    return t


def make_panel(block, styles=("Panel",)):
    """A shaded panel with a coloured edge bar that can split across pages."""
    inner = []
    if getattr(block, "title", ""):
        inner.append(Paragraph(markup.inline(block.title), STYLES["PanelHead"]))
    for b in block.blocks:
        if b.kind == "para":
            inner.append(Paragraph(markup.inline(b.text), STYLES["Panel"]))
        elif b.kind == "bullet":
            inner.append(Paragraph(markup.inline(b.text), STYLES["Panel"],
                                   bulletText="\u2022"))
        elif b.kind == "numbered":
            inner.append(Paragraph(markup.inline(b.text), STYLES["Panel"],
                                   bulletText=b.label))
        elif b.kind == "quote":
            inner.append(Paragraph(markup.inline(b.text), STYLES["Panel"]))
    if not inner:
        return Spacer(1, 1)
    # one flowable per row so that the panel can break between paragraphs
    data = [[f] for f in inner]
    t = Table(data, colWidths=[TEXT_W])
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), PANEL),
        ("LINEBEFORE", (0, 0), (0, -1), 1.6, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("TOPPADDING", (0, 0), (0, 0), 9),
        ("BOTTOMPADDING", (0, -1), (0, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    t.setStyle(TableStyle(style))
    t.spaceBefore = 4
    t.spaceAfter = 6
    return t


def make_figure(block):
    nodes = block.nodes
    if block.num == "3.2":
        fig = CurveFigure(0.90, 0.90)
    else:
        fig = ConceptualMap(nodes)
    cap = Paragraph(
        f'<b>Figure {block.num}.</b>&nbsp;{markup.inline(block.caption)}',
        STYLES["Caption"])
    cap._chap_record = dict(kind="figure",
                            text=f"Figure {block.num}. {markup.plain(block.caption)}",
                            key=f"fig{block.num}")
    parts = [fig, cap]
    if getattr(block, "note", ""):
        parts.append(Paragraph(markup.inline(block.note), STYLES["TableNote"]))
    parts.append(Spacer(1, 10))
    return [CondPageBreak(120)] + parts


# --------------------------------------------------------------------------
# front matter
# --------------------------------------------------------------------------
def front_matter(records, fm_entries=None):
    S = STYLES
    f = []
    # ---------------------------------------------------------- half-title
    f += [Spacer(1, 150),
          Paragraph(META.COURSE, S["FMImprint"]),
          Spacer(1, 10),
          Paragraph(META.TITLE, S["FMHalfTitle"]),
          Spacer(1, 8),
          Paragraph("A Textbook in Counselling Psychology", S["FMSub"]),
          PageBreak()]

    # ------------------------------------------------------------ title page
    f += [Spacer(1, 96),
          Paragraph(META.COURSE, ParagraphStyle("t1", parent=S["FMImprint"],
                                                fontSize=11, leading=16)),
          Spacer(1, 14),
          Paragraph(META.TITLE, ParagraphStyle("t2", parent=S["FMTitle"],
                                               fontSize=29, leading=33)),
          Spacer(1, 10),
          Table([[Hr(width=70, space_before=0, space_after=0)]],
                colWidths=[TEXT_W],
                style=TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                  ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                  ("TOPPADDING", (0, 0), (-1, -1), 0),
                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 0)])),
          Spacer(1, 12),
          Paragraph(META.SUBTITLE, ParagraphStyle("sub2", parent=S["FMSub"],
                                                  alignment=TA_CENTER)),
          Spacer(1, 40),
          Paragraph(META.AUTHOR, ParagraphStyle("auth", parent=S["FMCentre"],
                                                fontSize=10.2, leading=15,
                                                tracking=1.0)),
          Spacer(1, 120),
          Paragraph(META.EDITION, S["FMCentre"]),
          Spacer(1, 9),
          Paragraph(META.PLACE, S["FMCentre"]),
          PageBreak()]

    # -------------------------------------------------------- copyright page
    cp = ParagraphStyle("cp", parent=S["FMCopy"], spaceAfter=7)
    f += [Spacer(1, 170),
          Paragraph(f"{META.TITLE}: {META.SUBTITLE}. {META.COURSE}. "
                    f"{META.EDITION}.", cp),
          Paragraph(f"\u00a9 2026 {META.AUTHOR}. All rights reserved.", cp),
          Paragraph("Published by Triune Biblical University Global Extension, USA "
                    "(Online University, Shirley, New York, USA). "
                    f"{META.IMPRINT_URL}", cp),
          Paragraph("ISBN to be assigned by the publisher.", cp),
          Paragraph("All rights reserved. No part of this publication may be "
                    "reproduced, distributed, or transmitted in any form or by any "
                    "means without the prior written permission of the publisher, "
                    "except for brief quotations in reviews and for classroom use "
                    "within the licensee institution.", cp),
          Paragraph("This textbook is issued for academic use and is not for sale.", cp),
          Paragraph("The text does not reproduce proprietary test items or "
                    "copyrighted diagnostic criteria. Students must consult the "
                    "authorised manuals of individual instruments and the current "
                    "editions of diagnostic classifications. Clinical examples are "
                    "fictional composites and do not describe identifiable persons.",
                    cp),
          Paragraph(markup.typographic(
                    "Diagnostic criteria quoted or paraphrased in this book are "
                    "drawn from the Diagnostic and Statistical Manual of Mental "
                    "Disorders, Fifth Edition, Text Revision (American Psychiatric "
                    "Association, 2022) and from the Clinical Descriptions and "
                    "Diagnostic Requirements for ICD-11 Mental, Behavioural and "
                    "Neurodevelopmental Disorders (World Health Organization, 2024). "
                    "Copyright in those works remains with their respective owners."),
                    cp),
          Paragraph("Typeset in EB Garamond 11/15.2 pt with Source Serif 4 display "
                    "type. Trim size 152 × 229 mm.", cp),
          PageBreak()]

    # -------------------------------------------------------------------- TOC
    f += [Paragraph("Contents", ParagraphStyle("toch", parent=S["FMTitle"],
                                              fontSize=20, leading=24,
                                              alignment=0)),
          Hr(width=54, space_before=4, space_after=14),
          LeaderList((fm_entries or []) + records["toc"]),
          PageBreak()]

    # -------------------------------------------------------- list of figures
    lof = Paragraph("List of Figures", ParagraphStyle("lofh", parent=S["FMTitle"],
                                                      fontSize=20, leading=24,
                                                      alignment=0))
    lof._chap_record = dict(kind="fm", text="List of Figures", key="lof")
    f += [lof,
          Hr(width=54, space_before=4, space_after=14),
          LeaderList(records["fig"], size=9.0, leading=11.8),
          PageBreak()]

    # --------------------------------------------------------- list of tables
    lot = Paragraph("List of Tables", ParagraphStyle("loth", parent=S["FMTitle"],
                                                     fontSize=20, leading=24,
                                                     alignment=0))
    lot._chap_record = dict(kind="fm", text="List of Tables", key="lot")
    f += [lot,
          Hr(width=54, space_before=4, space_after=14),
          LeaderList(records["tab"], size=9.0, leading=11.8),
          PageBreak()]

    # ---------------------------------------------------------- abbreviations
    for name in ("abbreviations.md", "preface.md", "howto.md"):
        blocks = load_markdown_file(name)
        f += render_section(blocks, fm=True)
        f += [PageBreak()]
    return f


def load_markdown_file(name):
    path = os.path.join(BOOK, name)
    with open(path, encoding="utf-8") as fh:
        return markup.parse(fh.read())


def render_section(blocks, opener=False, fm=False):
    """Render a run of blocks that begins with a '# ' page title."""
    out = []
    fresh = True        # next paragraph starts a section: no first-line indent
    page_kind = ""      # 'refs' | 'glossary' | '' : drives paragraph style
    for b in blocks:
        if b.kind == "chapter":
            label = b.num.strip()
            is_chapter = label.upper().startswith("CHAPTER")
            title = b.title
            if is_chapter:
                num = label.split()[-1]
                numword = num_of(num)
                out.append(Spacer(1, 34))
                p = Paragraph(f"CHAPTER {num}", STYLES["ChapterNumber"])
                p._chap_record = dict(kind="chapter",
                                      text=f"Chapter {num}. {title}",
                                      short=f"{num} · {META.SHORT_TITLES.get(int(num), title)}",
                                      key=f"ch{num}")
                out.append(p)
            else:
                out.append(Spacer(1, 46))
                if not label:
                    p = Paragraph("", STYLES["ChapterNumber"])
                else:
                    p = Paragraph(label, STYLES["ChapterNumber"])
                p._chap_record = dict(kind="fm" if fm else "back",
                                      text=(b.toc or title), short=title,
                                      key=f"bk{len(out)}{title[:12]}")
                out.append(p)
            if title.strip().lower() == "references":
                page_kind = "refs"
            elif title.strip().lower() == "glossary":
                page_kind = "glossary"
            out.append(Paragraph(markup.typographic(title), STYLES["ChapterTitleNoHyph"]))
            out.append(Hr(width=60, space_before=8, space_after=16))
            fresh = True
        elif b.kind == "h1":
            label = f"{b.num}\u2002\u2002{b.title}" if b.num else b.title
            out.append(CondPageBreak(76))
            p = Paragraph(markup.typographic(label), STYLES["H1"])
            p._chap_record = dict(kind="fmsec" if fm else "section", text=label,
                                  key=f"s{len(out)}{label[:14]}")
            out.append(p)
            fresh = True
        elif b.kind == "h2":
            out.append(CondPageBreak(64))
            out.append(Paragraph(markup.typographic(b.title), STYLES["H2"]))
            fresh = True
        elif b.kind == "para":
            if page_kind == "refs":
                out.append(para(b.text, "RefEntry"))
            elif page_kind == "glossary":
                out.append(para(b.text, "GlossTerm"))
            else:
                out.append(para(b.text, "BodyFirst" if fresh else "Body"))
            fresh = False
        elif b.kind == "bullet":
            out.append(Paragraph(markup.inline(b.text), STYLES["Bullet"],
                                 bulletText="\u2022"))
        elif b.kind == "numbered":
            out.append(Paragraph(markup.inline(b.text), STYLES["Numbered"],
                                 bulletText=b.label))
        elif b.kind == "quote":
            out.append(Paragraph(markup.inline(b.text), STYLES["Quote"]))
        elif b.kind == "panel":
            out.append(Spacer(1, 6))
            out.append(make_panel(b))
            out.append(Spacer(1, 8))
        elif b.kind == "figure":
            out += make_figure(b)
        elif b.kind == "table":
            if b.num:
                cap = Paragraph(
                    f'<b>Table {b.num}.</b>&nbsp;' + markup.inline(b.caption),
                    STYLES["TableCaption"])
                cap._chap_record = dict(
                    kind="table",
                    text=f"Table {b.num}. {markup.plain(b.caption)}",
                    key=f"tab{b.num}")
            else:
                cap = Paragraph(markup.inline(b.caption) if b.caption else "&nbsp;",
                                STYLES["TableCaption"])
            out.append(KeepTogether([cap, make_table(b)]))
            out.append(Spacer(1, 8))
        elif b.kind == "pagebreak":
            out.append(PageBreak())
    return out


def num_of(num):
    words = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX",
             7: "SEVEN", 8: "EIGHT", 9: "NINE", 10: "TEN", 11: "ELEVEN",
             12: "TWELVE", 13: "THIRTEEN", 14: "FOURTEEN", 15: "FIFTEEN",
             16: "SIXTEEN", 17: "SEVENTEEN", 18: "EIGHTEEN", 19: "NINETEEN",
             20: "TWENTY"}
    return words.get(int(num), num)


def part_page(part):
    roman_no, title, blurb, chapters = part
    out = [Spacer(1, 150),
           Paragraph(roman_no, ParagraphStyle("pn", parent=STYLES["FMImprint"],
                                              fontSize=10, leading=14)),
           Spacer(1, 12),
           Paragraph(title, ParagraphStyle("pt", parent=STYLES["FMTitle"],
                                           fontSize=22, leading=27)),
           Spacer(1, 14),
           # rule is drawn by Hr but centred: wrap in a table to centre it
           Table([[Hr(width=54, space_before=0, space_after=0)]],
                 colWidths=[TEXT_W],
                 style=TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 0)])),
           Spacer(1, 16),
           Paragraph(blurb, ParagraphStyle("pb", parent=STYLES["FMCentre"],
                                           fontSize=10.6, leading=15.4)),
           Spacer(1, 26),
           Paragraph(" · ".join(f"Chapter {c}" for c in chapters),
                     ParagraphStyle("pc", parent=STYLES["FMCentre"],
                                    fontSize=9, leading=13, textColor=INK_SOFT)),
           PageBreak()]
    # part bookmark / TOC entry
    label = f"Part {roman_no.split()[-1]}: {title}"
    out[1]._chap_record = dict(kind="part", text=label,
                               short=title, key=f"part{roman_no.replace(' ', '')}")
    return out


# --------------------------------------------------------------------------
# body
# --------------------------------------------------------------------------
def body_story(doc):
    story = []
    part_lookup = {}
    for p in META.PARTS:
        for c in p[3]:
            part_lookup[c] = p
    files = sorted(glob.glob(os.path.join(BOOK, "ch[0-9][0-9].md")))
    first = True
    for path in files:
        blocks = markup.parse(open(path, encoding="utf-8").read())
        chapter_no = int(re.search(r"ch(\d+)\.md", path).group(1))
        if chapter_no in part_lookup:
            if not first:
                story.append(PageBreak())
            if first:
                story.append(_BodyStart(doc))
            part = part_lookup[chapter_no]
            if part[3][0] == chapter_no:
                if f"part{chapter_no}" in doc.blank_before:
                    story.append(_Blank(doc))
                    story.append(PageBreak())
                pp = part_page(part)
                pp.insert(0, _Mark(doc, f"part{chapter_no}"))
                story += pp
        elif not first:
            story.append(PageBreak())
        # chapter openers begin on a recto page without a running head
        if f"ch{chapter_no}" in doc.blank_before:
            story.append(_Blank(doc))
            story.append(PageBreak())
        story.append(_Mark(doc, f"ch{chapter_no}"))
        story.append(_Opener(doc))
        story += render_section(blocks)
        first = False
    return story


class _Mark(Flowable):
    """Zero-height marker that records the physical page it lands on."""

    def __init__(self, doc, key):
        Flowable.__init__(self)
        self.doc = doc
        self.key = key

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        self.doc.marks[self.key] = self.doc.page


class _Blank(Flowable):
    """Flags the current page as an intentional blank (no folio, no head)."""

    def __init__(self, doc):
        Flowable.__init__(self)
        self.doc = doc

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        self.doc.blank_pages.add(self.doc.page)


class _BodyStart(Flowable):
    """Marks the first page of the body, from which folios count in arabic."""

    def __init__(self, doc):
        Flowable.__init__(self)
        self.doc = doc

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        if self.doc.body_start is None:
            self.doc.body_start = self.doc.page


class _Opener(Flowable):
    """Zero-height marker that flags the current page as a chapter opener,
    suppressing the running head on that page."""

    def __init__(self, doc):
        Flowable.__init__(self)
        self.doc = doc

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        self.doc.page_opener = True
        self.doc.opening_pages.add(self.doc.page)


# --------------------------------------------------------------------------
# back matter
# --------------------------------------------------------------------------
def back_matter(doc, records, index_entries):
    out = [PageBreak(), _Opener(doc)]
    for name in ("references.md", "glossary.md", "appendix_a.md",
                 "appendix_b.md", "appendix_c.md", "about.md"):
        path = os.path.join(BOOK, name)
        if not os.path.exists(path):
            continue
        blocks = markup.parse(open(path, encoding="utf-8").read())
        key = "back" + name
        if key in doc.blank_before:
            out.append(_Blank(doc))
            out.append(PageBreak())
        out.append(_Opener(doc))
        out.append(_Mark(doc, key))
        out += render_section(blocks)
        out.append(PageBreak())
    if index_entries:
        if "backindex" in doc.blank_before:
            out.append(_Blank(doc))
            out.append(PageBreak())
        out.append(_Mark(doc, "backindex"))
        out.append(_Opener(doc))
        out += render_section(markup.parse("# |Index"))
        for e in index_entries:
            out.append(Paragraph(
                f"{markup.inline(e['term'])}, {e['pages']}", STYLES["IndexEntry"]))
    return out


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------
def build(path, pagemap=None, index_entries=None, body_only=False):
    doc = Book(path, pagemap=pagemap, index_entries=index_entries)
    story = []
    if body_only:
        doc.body_start = 1
        story += body_story(doc)
    else:
        story += front_matter(doc.records)
        story += body_story(doc)
        story += back_matter(doc, doc.records, index_entries)
    doc.build(story)
    return doc


def _assemble(doc, records, fm_entries, pad):
    story = front_matter(records, fm_entries)
    if pad:
        story.append(Spacer(1, 1))
        story.append(PageBreak())
    story += body_story(doc)
    story += back_matter(doc, doc.records, doc._index_entries)
    return story


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args()
    register_fonts()

    tmp = os.path.join(OUT, ".pass1.pdf")
    d1 = build(tmp, body_only=True)
    records = {k: list(v) for k, v in d1.records.items()}

    final = os.path.join(OUT, "CPY903_Advanced_Assessment_and_Diagnosis.pdf")
    index_path = os.path.join(OUT, "index.json")
    index_entries = []
    if os.path.exists(index_path) and os.environ.get("SKIPINDEX") != "1":
        index_entries = json.load(open(index_path))

    fm_entries, pages, blanks, pad = [], 0, set(), False
    for attempt in range(6):
        # the front-matter sections carry roman folios that are listed in the
        # contents, so build the front matter until those folios stop moving
        for _ in range(4):
            probe = Book(tmp + ".fm.pdf")
            probe.build(front_matter(records, fm_entries))
            new = list(probe.records["fm"])
            if [(e["text"], e["page"]) for e in new] == \
               [(e["text"], e["page"]) for e in fm_entries]:
                break
            fm_entries = new
        fm_pages = probe.page
        pad = fm_pages % 2 == 1

        # base layout: every chapter, part and back-matter section should open
        # on a recto page. A blank page carries no text, so the pages that must
        # be inserted can be simulated exactly from this single base layout.
        base = Book(final)
        base._index_entries = index_entries
        base.build(_assemble(base, records, fm_entries, pad))
        marks = dict(base.marks)
        shift, blanks = 0, set()
        for page, key in sorted((p, k) for k, p in marks.items()):
            if (page + shift) % 2 == 0:
                blanks.add(key)
                shift += 1

        doc = Book(final)
        doc._index_entries = index_entries
        doc.blank_before = blanks
        if pad:
            # the strut that evens out the front matter leaves one empty page
            # before the part title; it carries neither head nor folio
            doc.blank_pages.add(base.body_start - 1)
        doc.build(_assemble(doc, records, fm_entries, pad))
        pages = doc.page

        # the contents and the lists must cite the final pagination
        if [(e["text"], e["page"]) for e in doc.records["toc"]] == \
           [(e["text"], e["page"]) for e in records["toc"]]:
            break
        records["toc"] = doc.records["toc"]
        records["fig"] = doc.records["fig"]
        records["tab"] = doc.records["tab"]

    # final pass: drop unused resources and compress streams so that the only
    # fonts in the file are the embedded text faces
    import pymupdf
    tmpout = final + ".tmp.pdf"
    os.replace(final, tmpout)
    src = pymupdf.open(tmpout)
    # ReportLab registers a default Helvetica (/F1) in every page's resource
    # dictionary although no text uses it. Drop the dead reference so that the
    # only fonts in the file are the six embedded text faces.
    for page in src:
        for key in ("F1",):
            try:
                if src.xref_get_key(page.xref, f"Resources/Font/{key}")[0] != "null":
                    src.xref_set_key(page.xref, f"Resources/Font/{key}", "null")
            except Exception:
                pass
    src.save(final, garbage=4, deflate=True, clean=True)
    src.close()
    os.remove(tmpout)

    with open(os.path.join(OUT, "bookmap.json"), "w") as fh:
        json.dump({"records": records, "fm": fm_entries,
                   "body_start": doc.body_start, "pages": pages,
                   "marks": doc.marks, "blanks": sorted(blanks)}, fh, indent=1)
    print("pass A pages:", d1.page, "| front matter:", fm_pages,
          "| pages:", pages, "| body starts at", doc.body_start,
          "| blanks:", len(blanks), "| attempts:", attempt + 1)


if __name__ == "__main__":
    main()
