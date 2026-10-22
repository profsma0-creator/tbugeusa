# -*- coding: utf-8 -*-
"""
AI.101 Introduction to Artificial Intelligence - Textbook Typesetting Framework
Professional book layout using ReportLab Platypus.
Author: TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, NextPageTemplate, KeepTogether, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ---------------------------------------------------------------- page setup
# Trade textbook trim: 7 x 10 in
PAGE_W, PAGE_H = 7 * inch, 10 * inch
M_L = M_R = 0.75 * inch
M_T = 0.9 * inch
M_B = 0.85 * inch

AUTHOR = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"
BOOK_TITLE = "Introduction to Artificial Intelligence"
BOOK_SUBTITLE = "A Self-Contained Undergraduate Textbook"
COURSE_CODE = "AI.101"
COURSE_TITLE = "Introduction to Artificial Intelligence"
COPYRIGHT_YEAR = "2026"
ISBN_PLACEHOLDER = "ISBN: 978-1-00000-101-1 (Assigned)"

# ---------------------------------------------------------------- palette
INK      = colors.HexColor("#1a1a1a")
INK_SOFT = colors.HexColor("#3d3d3d")
PRIMARY  = colors.HexColor("#0b3d62")   # deep academic blue
PRIMARY_D= colors.HexColor("#082f4c")
ACCENT   = colors.HexColor("#b08d2e")   # gold accent
LIGHT    = colors.HexColor("#f4f1ea")   # warm off-white
RULE     = colors.HexColor("#c9c3b7")
BOX_BG   = colors.HexColor("#eef3f8")
BOX_BORD = colors.HexColor("#d6e0ea")
CODE_BG  = colors.HexColor("#f7f5f0")

# ---------------------------------------------------------------- styles
def _st(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10, leading=14,
                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {}
S["title"]      = _st("title", fontName="Helvetica-Bold", fontSize=26, leading=32,
                      alignment=TA_CENTER, textColor=PRIMARY, spaceAfter=10)
S["subtitle"]   = _st("subtitle", fontName="Helvetica", fontSize=15, leading=20,
                      alignment=TA_CENTER, textColor=INK_SOFT, spaceAfter=4)
S["author"]     = _st("author", fontName="Helvetica-Bold", fontSize=13, leading=18,
                      alignment=TA_CENTER, textColor=PRIMARY_D, spaceAfter=2)
S["course"]     = _st("course", fontName="Helvetica", fontSize=11, leading=15,
                      alignment=TA_CENTER, textColor=INK_SOFT, spaceAfter=2)
S["h1"]         = _st("h1", fontName="Helvetica-Bold", fontSize=17, leading=21,
                      textColor=PRIMARY, spaceBefore=2, spaceAfter=4, alignment=TA_LEFT)
S["h2"]         = _st("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16,
                      textColor=PRIMARY_D, spaceBefore=10, spaceAfter=4, alignment=TA_LEFT)
S["h3"]         = _st("h3", fontName="Helvetica-BoldOblique", fontSize=10.5, leading=14,
                      textColor=INK, spaceBefore=8, spaceAfter=3, alignment=TA_LEFT)
S["body"]       = _st("body")
S["body_i"]     = _st("body_i", fontName="Helvetica-Oblique")
S["body_b"]     = _st("body_b", fontName="Helvetica-Bold")
S["small"]      = _st("small", fontSize=8.5, leading=11.5, textColor=INK_SOFT)
S["code"]       = _st("code", fontName="Courier", fontSize=8.6, leading=12,
                      textColor=colors.HexColor("#2e2e2e"), alignment=TA_LEFT,
                      backColor=CODE_BG, borderPadding=6, spaceBefore=4, spaceAfter=8)
S["code_h"]     = _st("code_h", fontName="Courier-Bold", fontSize=8.6, leading=12,
                      textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=4, spaceAfter=2)
S["quote"]      = _st("quote", fontName="Helvetica-Oblique", fontSize=10, leading=14,
                      leftIndent=22, rightIndent=22, textColor=INK_SOFT,
                      backColor=LIGHT, borderPadding=8, spaceBefore=6, spaceAfter=8)
S["list"]       = _st("list", leftIndent=16, bulletIndent=6, spaceAfter=3)
S["label"]      = _st("label", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
                      textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=6, spaceAfter=2)
S["chapter_title"] = _st("chapter_title", fontName="Helvetica-Bold", fontSize=21,
                         leading=26, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=6)
S["chapter_sub"]   = _st("chapter_sub", fontName="Helvetica-Oblique", fontSize=11,
                         leading=15, textColor=INK_SOFT, alignment=TA_LEFT, spaceAfter=10)
S["element_title"] = _st("element_title", fontName="Helvetica-Bold", fontSize=10.5,
                         leading=14, textColor=PRIMARY_D, alignment=TA_LEFT,
                         spaceBefore=8, spaceAfter=3)
S["element_body"]  = _st("element_body")
S["toc_l1"]   = _st("toc_l1", fontName="Helvetica-Bold", fontSize=11, leading=16,
                    textColor=PRIMARY, alignment=TA_LEFT, spaceBefore=6, spaceAfter=1)
S["toc_l2"]   = _st("toc_l2", fontName="Helvetica", fontSize=9.5, leading=13,
                    textColor=INK, alignment=TA_LEFT, leftIndent=18, spaceAfter=0.5)
S["toc_page"] = _st("toc_page", fontName="Helvetica-Bold", fontSize=10, leading=13,
                    textColor=INK, alignment=TA_RIGHT)

# ---------------------------------------------------------------- canvas w/ furniture
class BookCanvas(canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []
        self._chapter_starts = {}   # page label -> page number

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = self._pageNumber
        for state in self._saved:
            self.__dict__.update(state)
            self._draw_furniture(total)
            super().showPage()
        super().save()

    def _draw_furniture(self, total):
        pg = self._pageNumber
        # skip furniture on cover / copyright / part opener pages (front matter)
        if pg in (1, 2, 3):
            return
        self.saveState()
        # header rule + short title on non-chapter-opener pages
        self.setStrokeColor(RULE); self.setLineWidth(0.6)
        self.line(M_L, PAGE_H - 0.55 * inch, PAGE_W - M_R, PAGE_H - 0.55 * inch)
        self.setFont("Helvetica", 7.5); self.setFillColor(INK_SOFT)
        self.drawString(M_L, PAGE_H - 0.68 * inch, BOOK_TITLE.upper())
        self.drawRightString(PAGE_W - M_R, PAGE_H - 0.68 * inch, COURSE_CODE)
        # footer
        self.setStrokeColor(RULE)
        self.line(M_L, 0.62 * inch, PAGE_W - M_R, 0.62 * inch)
        self.setFont("Helvetica", 7.5)
        self.drawString(M_L, 0.48 * inch, AUTHOR)
        self.drawRightString(PAGE_W - M_R, 0.48 * inch, "Page %d of %d" % (pg, total))
        # section marker
        self.setFillColor(ACCENT)
        self.rect(M_L, PAGE_H - 0.52 * inch, 0.14 * inch, 0.14 * inch, stroke=0, fill=1)
        self.restoreState()

# ---------------------------------------------------------------- helpers
def P(text, style="body", **kw):
    st = S[kw.pop("style", style)] if "style" in kw else S[style]
    if kw:
        st = ParagraphStyle("tmp", parent=st, **kw)
    return Paragraph(text, st)

def SP(h=6):
    return Spacer(1, h)

def HR(color=PRIMARY, w=1.0, before=2, after=6):
    return HRFlowable(width="100%", thickness=w, color=color,
                      spaceBefore=before, spaceAfter=after)

def box_flowables(title, body_flows, bg=BOX_BG, border=BOX_BORD, title_color=PRIMARY_D):
    """A labelled box: title line + content flows."""
    inner = []
    if title:
        inner.append(Paragraph(title, _st("boxt", fontName="Helvetica-Bold",
                                          fontSize=9.5, leading=13,
                                          textColor=title_color, spaceAfter=4)))
    inner.extend(body_flows)
    t = Table([[inner]], colWidths=[PAGE_W - M_L - M_R])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.8, border),
        ("LINEBEFORE", (0,0), (0,-1), 2.5, PRIMARY),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

def code_block(lines, caption=None):
    flows = []
    if caption:
        flows.append(Paragraph(caption, S["code_h"]))
    text = "<br/>".join(_esc(l) for l in lines)
    flows.append(Paragraph('<font face="Courier" size="8.6">%s</font>' % text, S["code"]))
    return flows

def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def bullets(items, style="list", bullet="•"):
    return ListFlowable(
        [ListItem(Paragraph(it, S[style]), leftIndent=14, value=bullet) for it in items],
        bulletType="bullet", bulletChar=bullet, start="•",
        leftIndent=14, bulletFontSize=9, bulletColor=PRIMARY, spaceAfter=5)

# ---------------------------------------------------------------- chapter helper set
ELEMENT_ORDER = [
    "intro", "objectives", "prereq", "core", "definitions",
    "examples", "derivations", "algorithms", "applications", "laboratory",
    "programming", "case_study", "mistakes", "summary", "key_terms",
    "review", "mcq", "short_answer", "numerical", "programming_ex",
    "mini_project", "further_reading",
]
ELEMENT_LABELS = {
    "intro": "Chapter Introduction",
    "objectives": "Learning Objectives",
    "prereq": "Prerequisite Knowledge",
    "core": "Core Concepts",
    "definitions": "Key Definitions & Terminology",
    "examples": "Worked Examples",
    "derivations": "Mathematical Derivations",
    "algorithms": "Algorithms & Pseudocode",
    "applications": "Engineering Applications",
    "laboratory": "Practical Laboratory Activity",
    "programming": "Programming Exercise",
    "case_study": "Case Study",
    "mistakes": "Common Mistakes & Troubleshooting",
    "summary": "Chapter Summary",
    "key_terms": "Key Terms",
    "review": "Review Questions",
    "mcq": "Multiple-Choice Questions (MCQs)",
    "short_answer": "Short-Answer Questions",
    "numerical": "Numerical / Problem-Solving Questions",
    "programming_ex": "Programming / Design Exercises",
    "mini_project": "Mini-Project",
    "further_reading": "Further Reading & References",
}

def element_flows(key, content, style_body="element_body"):
    """Build flowables for a single chapter element given its content dict/list."""
    flows = []
    flows.append(Paragraph(ELEMENT_LABELS[key], S["element_title"]))
    if isinstance(content, str):
        flows.append(Paragraph(content, S[style_body]))
    elif isinstance(content, list):
        for idx, item in enumerate(content, start=1):
            if isinstance(item, tuple) and item and item[0] == "code":
                flows.extend(code_block(item[1], caption=item[2] if len(item) > 2 else None))
            elif isinstance(item, tuple) and item and item[0] == "bullets":
                flows.append(bullets(item[1]))
            elif isinstance(item, tuple) and len(item) == 2:
                flows.append(Paragraph("<b>%d. %s.</b> %s" % (idx, _esc(item[0]), _esc(item[1])), S[style_body]))
            elif isinstance(item, tuple) and len(item) == 4:
                qid, q, opts, ans = item
                opt_html = "<br/>".join(_esc(o) for o in opts)
                flows.append(Paragraph("<b>%s.</b> %s<br/>%s" % (qid, _esc(q), opt_html), S[style_body]))
                flows.append(Paragraph("<b>Answer:</b> %s" % _esc(ans), S["small"]))
            else:
                flows.append(Paragraph(str(item), S[style_body]))
    elif isinstance(content, dict):
        # allow structured sub-parts
        for sub_k, sub_v in content.items():
            flows.append(Paragraph(sub_k, _st("sub", fontName="Helvetica-Bold",
                                              fontSize=9.6, leading=13,
                                              textColor=INK, spaceBefore=4, spaceAfter=2)))
            flows.append(Paragraph(sub_v, S[style_body]))
    flows.append(SP(4))
    return flows

print("framework loaded OK")
