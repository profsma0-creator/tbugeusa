"""
bookkit.document — the book's typographic engine.

Owns page geometry (mirrored margins), running heads, folios, part and chapter
openers, the table of contents, PDF bookmarks and the multi-pass build.
"""
from __future__ import annotations

import re

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer)
from reportlab.platypus.tableofcontents import TableOfContents

from . import indexes, theme as T

BODY_START = 0          # physical page on which the printed arabic sequence begins


# ---------------------------------------------------------------------------
# page labels
# ---------------------------------------------------------------------------
_ROMAN = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"),
          (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"),
          (5, "v"), (4, "iv"), (1, "i")]


def roman(n: int) -> str:
    out = ""
    for v, s in _ROMAN:
        while n >= v:
            out += s
            n -= v
    return out


def label(page: int, body_start: int) -> str:
    """Printed folio for a physical PDF page number."""
    if body_start and page >= body_start:
        return str(page - body_start + 1)
    return roman(max(page, 1))


# ---------------------------------------------------------------------------
# invisible markers used to steer page furniture
# ---------------------------------------------------------------------------
class Marker(Flowable):
    """Zero-height flowable whose only purpose is a side effect."""

    def __init__(self, kind: str):
        super().__init__()
        self.kind = kind

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        return


class HeadSuppress(Marker):
    """Marks the page it lands on as carrying no running head."""

    def __init__(self):
        super().__init__("head_suppress")

    def draw(self):
        self.canv._book_no_head = True


class BodyStart(Marker):
    """Marks the first page of the printed arabic sequence."""

    def __init__(self):
        super().__init__("body_start")

    def draw(self):
        global BODY_START
        BODY_START = self.canv.getPageNumber()


class FolioSuppress(Marker):
    """Marks the page it lands on as carrying no page number."""

    def __init__(self):
        super().__init__("folio_suppress")

    def draw(self):
        self.canv._book_no_folio = True


class RunningHead(Marker):
    """Sets the recto running head for the pages that follow."""

    def __init__(self, text):
        super().__init__("running_head")
        self.text = text

    def draw(self):
        self.canv._book_running = self.text
        self.canv._doc_running = self.text


class BlankPage(Marker):
    """Marks a page that should print nothing at all."""

    def __init__(self):
        super().__init__("blank_page")

    def draw(self):
        self.canv._book_blank = True
        self.canv._book_no_folio = True
        self.canv._book_no_head = True


# ---------------------------------------------------------------------------
# page decoration
# ---------------------------------------------------------------------------
def _track(canv, amount: float):
    """Set letter-spacing (reportlab exposes it only on text objects)."""
    canv._charSpace = amount
    canv._code.append(f"{amount:g} Tc")


def _paint(canv, doc, mode: str):
    page = canv.getPageNumber()
    body_start = BODY_START or getattr(doc, "body_start", 0)
    recto = page % 2 == 1
    text_w = T.TEXT_W
    left = T.MARGIN_INSIDE if recto else T.MARGIN_OUTSIDE

    canv.saveState()
    if mode == "blank" or getattr(canv, "_book_blank", False):
        canv.restoreState()
        return

    folio = label(page, body_start if body_start else doc.body_start)
    show_folio = not getattr(canv, "_book_no_folio", False)

    # ---- running head (body pages only, never on part/chapter openers) ----
    if mode == "body" and not getattr(canv, "_book_no_head", False):
        canv.setFont("Lato", 7.2)
        canv.setFillColor(T.WARM_GRAY)
        _track(canv, 0.7)
        if recto:
            head = getattr(canv, "_book_running", "") or doc.running_chapter
        else:
            head = doc.book_title
        if head:
            canv.drawCentredString(T.PAGE_W / 2.0, T.HEAD_BASELINE, head.upper())
        _track(canv, 0)

    if mode in ("body", "front") and show_folio:
        canv.setFont("Cinzel", 8.4)
        canv.setFillColor(T.GOLD)
        if mode == "front" or getattr(canv, "_book_no_head", False):
            canv.drawCentredString(T.PAGE_W / 2.0,
                                   T.MARGIN_BOTTOM - 30 + 6, folio)
        else:
            if recto:
                canv.drawRightString(T.PAGE_W - T.MARGIN_OUTSIDE,
                                     T.HEAD_BASELINE, folio)
            else:
                canv.drawString(T.MARGIN_OUTSIDE, T.HEAD_BASELINE, folio)
    canv.restoreState()


# ---------------------------------------------------------------------------
# mirrored page frame
# ---------------------------------------------------------------------------
class MirrorPage(PageTemplate):
    """A page template whose single frame is re-positioned to the correct
    margin (inside on the recto, outside on the verso) at the start of every
    page.  Frame geometry is set directly because reportlab's Frame consults
    _x1/_x2/_aW when it wraps and splits content."""

    def __init__(self, ident, mode="body"):
        self.mode = mode
        f = Frame(0, 0, T.TEXT_W, T.TEXT_H, id=f"f-{ident}",
                  leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
        super().__init__(id=ident, frames=[f], pagesize=(T.PAGE_W, T.PAGE_H))

    def set_frame_for(self, page: int):
        recto = page % 2 == 1
        x = T.MARGIN_INSIDE if recto else T.MARGIN_OUTSIDE
        f = self.frames[0]
        f.__dict__["_x1"] = x
        f.__dict__["_x2"] = x + T.TEXT_W
        f.__dict__["_aW"] = T.TEXT_W
        return f

    def afterDrawPage(self, canv, doc):
        _paint(canv, doc, self.mode)
        for attr in ("_book_no_head", "_book_blank", "_book_no_folio"):
            if hasattr(canv, attr):
                delattr(canv, attr)


# ---------------------------------------------------------------------------
# table of contents
# ---------------------------------------------------------------------------
class BookTOC(TableOfContents):
    def __init__(self, body_start_getter):
        super().__init__()
        self.dotsMinLevel = 1
        self._bs = body_start_getter
        self.levelStyles = [T.STYLES["toc_part"], T.STYLES["toc_entry"]]
        self.formatter = self._fmt

    def _fmt(self, page):
        bs = self._bs()
        if isinstance(page, int):
            return label(page, bs)
        return str(page)


# ---------------------------------------------------------------------------
# the document
# ---------------------------------------------------------------------------
class BookDoc(BaseDocTemplate):
    def __init__(self, filename, title, author, subject="", **kw):
        super().__init__(
            filename, pagesize=(T.PAGE_W, T.PAGE_H),
            leftMargin=T.MARGIN_OUTSIDE, rightMargin=T.MARGIN_OUTSIDE,
            topMargin=T.MARGIN_TOP, bottomMargin=T.MARGIN_BOTTOM,
            title=title, author=author, subject=subject,
            creator="Why God Left It to the Young — typeset with bookkit",
            **kw)
        self.body_start = 0
        self.book_title = title
        self.running_chapter = ""
        self.running_part = ""
        self._bm_seq = 0
        self.addPageTemplates([
            MirrorPage("blank", "blank"),
            MirrorPage("front", "front"),
            MirrorPage("body", "body"),
        ])

    def handle_pageBegin(self):
        tmpl = self.pageTemplate
        if isinstance(tmpl, MirrorPage):
            tmpl.set_frame_for(self.page)
        BaseDocTemplate.handle_pageBegin(self)

    # ---- running head ---------------------------------------------------
    def running_head(self, recto: bool) -> str:
        if recto:
            return self.running_chapter.upper()
        return self.book_title.upper()

    def set_running(self, text: str):
        self.running_chapter = text

    def sync_body_start(self):
        self.body_start = BODY_START or self.body_start

    # ---- flowable hooks -------------------------------------------------
    @staticmethod
    def _key(text: str, level: int) -> str:
        """Deterministic bookmark name — must not change between passes, or
        the table of contents never converges."""
        slug = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")[:56]
        return f"toc-{level}-{slug}"

    def afterFlowable(self, flowable):
        entry = getattr(flowable, "_toc_entry", None)
        if entry:
            level, text = entry
            key = self._key(text, level)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))
            return
        bm = getattr(flowable, "_bookmark", None)
        if bm:
            title, level = bm
            key = self._key(title, level)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=level, closed=False)


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
def flatten(story):
    """Recursively unwrap nested lists so the template sees a flat story."""
    out = []
    for item in story:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        elif item is not None:
            out.append(item)
    return out


def build(story, out_path: Path, title: str, author: str, subject: str = "",
          max_passes: int = 8) -> Path:
    global BODY_START
    BODY_START = 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = BookDoc(str(out_path), title=title, author=author, subject=subject)
    doc.multiBuild(flatten(story), maxPasses=max_passes)
    return out_path
