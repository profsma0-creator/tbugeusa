"""
bookkit.decor — the visual furniture of the book: rules, flourishes, scripture
blocks, excursus boxes, pull quotes, drop caps and ornamental dividers.
"""
from __future__ import annotations

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable, KeepTogether, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable

from . import indexes, theme as T


# ---------------------------------------------------------------------------
# simple rules and ornaments
# ---------------------------------------------------------------------------
class GoldRule(Flowable):
    """A centred horizontal rule, optionally with a diamond node in the middle."""

    def __init__(self, width=None, thickness=0.7, color=None, space_before=8,
                 space_after=8, node=False, inset=0.0, align="center"):
        super().__init__()
        self.rule_w = width
        self.t = thickness
        self.color = color or T.GOLD
        self.sb = space_before
        self.sa = space_after
        self.node = node
        self.inset = inset
        self.align = align

    def wrap(self, aw, ah):
        self.avail = aw
        self.width = self.rule_w if self.rule_w else aw - 2 * self.inset
        self.height = self.t + self.sb + self.sa
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setFillColor(self.color)
        c.setLineWidth(self.t)
        y = self.sa + self.t / 2.0
        w = self.width
        if self.align == "left":
            x0, x1 = self.inset, self.inset + w
        elif self.align == "center":
            x0 = (self.avail - w) / 2.0
            x1 = x0 + w
        else:
            x0, x1 = self.avail - self.inset - w, self.avail - self.inset
        if self.node:
            gap = 11.0
            mid = (x0 + x1) / 2.0
            c.line(x0, y, mid - gap, y)
            c.line(mid + gap, y, x1, y)
            r = 2.3
            c.saveState()
            c.translate(mid, y)
            c.rotate(45)
            c.rect(-r, -r, 2 * r, 2 * r, stroke=0, fill=1)
            c.restoreState()
        else:
            c.line(x0, y, x1, y)


class Ornament(Flowable):
    """A centred typographic flourish: rule — fleuron — rule."""

    def __init__(self, width=None, space_before=13, space_after=13, color=None):
        super().__init__()
        self.w = width
        self.sb = space_before
        self.sa = space_after
        self.color = color or T.GOLD

    def wrap(self, aw, ah):
        self.avail = aw
        self.width = self.w or min(aw * 0.44, 150)
        self.height = self.sb + self.sa + 8
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setFillColor(self.color)
        w = self.width
        x0 = (self.avail - w) / 2.0
        y = self.sa + 4
        c.setLineWidth(0.6)
        c.line(x0, y, x0 + w * 0.34, y)
        c.line(x0 + w * 0.66, y, x0 + w, y)
        c.saveState()
        c.translate(x0 + w * 0.5, y)
        for dx, r in ((-7.5, 1.5), (0, 2.6), (7.5, 1.5)):
            c.saveState()
            c.translate(dx, 0)
            c.rotate(45)
            c.rect(-r, -r, 2 * r, 2 * r, stroke=0, fill=1)
            c.restoreState()
        c.restoreState()


class SectionMark(Flowable):
    """Small gold rule placed under a section heading."""

    def __init__(self, width=34, thickness=0.9):
        super().__init__()
        self.width = width
        self.height = thickness + 3

    def wrap(self, aw, ah):
        self.avail = aw
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(T.GOLD)
        self.canv.setLineWidth(0.9)
        self.canv.line(0, 2, self.width, 2)


# ---------------------------------------------------------------------------
# drop caps
# ---------------------------------------------------------------------------
DROP_CAP_SIZE = 43.0
DROP_CAP_LEADING = 27.0
DROP_CAP_RAISE = 5.6     # pt of space inserted above the cap so caps align


def drop_cap_paragraph(first: str, rest_html: str, style: ParagraphStyle,
                       size=None, leading=None):
    """First paragraph of a chapter: an oversized gold initial with the text
    flowing beside it, then the remainder of the paragraph full width."""
    size = size or DROP_CAP_SIZE
    leading = leading or DROP_CAP_LEADING
    cap_style = ParagraphStyle(
        "dc", fontName="Cinzel-Bold", fontSize=size, leading=leading,
        textColor=T.GOLD, alignment=TA_CENTER, spaceBefore=0, allowance=0,
    )
    cap_para = indexes.IndexedParagraph(first, cap_style, index_subject=False)
    w = pdfmetrics.stringWidth(first, "Cinzel-Bold", size) + 7.0
    # the cap and the opening lines sit side by side; the tail flows underneath
    lead = Table([[cap_para, indexes.IndexedParagraph(rest_html, style)]],
                 colWidths=[w, None], spaceBefore=DROP_CAP_RAISE)
    lead.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return lead


# ---------------------------------------------------------------------------
# scripture / quotation blocks
# ---------------------------------------------------------------------------
def scripture_block(verse_paras, attribution) -> Table:
    """Cream panel with a gold bar down the left edge."""
    inner = list(verse_paras)
    if attribution:
        inner.append(indexes.IndexedParagraph(attribution, T.STYLES["verse_attrib"],
                                             index_subject=False))
    t = Table([[inner]], colWidths=[T.TEXT_W - 20])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), T.CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, T.GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def excursus_box(title: str, body_paras) -> Table:
    """Boxed aside used for excursus material, definitions and case studies."""
    inner = []
    if title:
        inner.append(Paragraph(title, T.STYLES["note_title"]))
        inner.append(HRFlowable(width="100%", thickness=0.5, color=T.RULE,
                                spaceBefore=1, spaceAfter=6))
    inner.extend(body_paras)
    t = Table([[inner]], colWidths=[T.TEXT_W - 20])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), T.CREAM_DARK),
        ("BOX", (0, 0), (-1, -1), 0.6, T.RULE_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def keypoints_box(items) -> Table:
    """‘At a glance’ panel of summary points."""
    inner = [Paragraph("At a glance", T.STYLES["note_title"]),
             HRFlowable(width="100%", thickness=0.5, color=T.RULE,
                        spaceBefore=1, spaceAfter=6)]
    for it in items:
        inner.append(Paragraph(it, T.STYLES["kp_item"], bulletText="\u25C6"))
    t = Table([[inner]], colWidths=[T.TEXT_W - 20])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), T.CREAM),
        ("BOX", (0, 0), (-1, -1), 0.6, T.GOLD_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def pull_quote(body_paras, attribution=None):
    """Displayed quotation set large and centred between gold flourishes."""
    out = [GoldRule(width=52, node=True, space_before=4, space_after=9)]
    out.extend(body_paras)
    if attribution:
        out.append(Paragraph(attribution, T.STYLES["pull_attrib"]))
    out.append(GoldRule(width=52, node=True, space_before=9, space_after=4))
    return KeepTogether(out)
