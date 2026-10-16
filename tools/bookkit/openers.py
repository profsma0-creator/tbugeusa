"""
bookkit.openers — title pages, part openers and chapter openers.

Each opener is a composition of flowables rather than a single drawing, so the
TOC, bookmarks and indexes all see real text.
"""
from __future__ import annotations

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (Flowable, KeepTogether, NextPageTemplate, PageBreak,
                                Paragraph, Spacer, Table, TableStyle)

from . import decor, figures, indexes, theme as T
from .document import HeadSuppress, RunningHead

ROMAN_UPPER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT",
               "NINE", "TEN", "ELEVEN", "TWELVE"]


# ---------------------------------------------------------------------------
# front matter
# ---------------------------------------------------------------------------
class CoverArt(Flowable):
    """The approved cover art, bled to the full page, aspect preserved."""

    def __init__(self, path):
        super().__init__()
        self.path = str(path)

    def wrap(self, aw, ah):
        return (0, 0)

    def drawOn(self, canvas, x, y, _sW=0):
        # ignore the frame: this plate always occupies a whole page
        from reportlab.lib.utils import ImageReader
        canvas.saveState()
        iw, ih = ImageReader(self.path).getSize()
        scale = max(T.PAGE_W / iw, T.PAGE_H / ih)
        w, h = iw * scale, ih * scale
        dx = (T.PAGE_W - w) / 2.0
        dy = (T.PAGE_H - h) / 2.0
        p = canvas.beginPath()
        p.rect(0, 0, T.PAGE_W, T.PAGE_H)
        canvas.clipPath(p, stroke=0, fill=0)
        canvas.drawImage(self.path, dx, dy, width=w, height=h,
                         preserveAspectRatio=False, mask=None)
        canvas.restoreState()


def cover_page(cover_png) -> list:
    return [CoverArt(cover_png)]


def half_title(title: str) -> list:
    st = ParagraphStyle("ht", parent=T.STYLES["fm_title"], fontSize=15, textColor=T.INK_SOFT)
    return [Spacer(1, 2.6 * inch),
            Paragraph(title.upper(), st),
            Spacer(1, 0.2 * inch),
            decor.GoldRule(width=90, node=True, space_before=0, space_after=0)]


def title_page(title, subtitle, author, place, year, publisher_line) -> list:
    return [
        Spacer(1, 1.35 * inch),
        Paragraph(title.upper(), T.STYLES["fm_title"]),
        Spacer(1, 14),
        decor.GoldRule(width=118, node=True, space_before=0, space_after=0),
        Spacer(1, 16),
        Paragraph(subtitle, T.STYLES["fm_sub"]),
        Spacer(1, 1.5 * inch),
        Paragraph(author, T.STYLES["fm_author"]),
        Spacer(1, 8),
        Paragraph("Doctor of Philosophy", T.STYLES["fm_role"]),
        Spacer(1, 1.35 * inch),
        Paragraph(publisher_line, T.STYLES["fm_role"]),
        Spacer(1, 4),
        Paragraph(f"{place} \u00b7 {year}", T.STYLES["fm_role"]),
    ]


def copyright_page(cfg) -> list:
    s = T.STYLES["copyright"]
    c = T.STYLES["copyright_c"]
    out = [
        Spacer(1, 0.9 * inch),
        Paragraph(cfg["title"], c),
        Paragraph(cfg["subtitle"], c),
        Spacer(1, 16),
        Paragraph(f"\u00a9 {cfg['year']} {cfg['author']}. All rights reserved.", s),
        Spacer(1, 6),
        Paragraph(
            "No part of this publication may be reproduced, stored in a retrieval system, "
            "or transmitted in any form or by any means \u2014 electronic, mechanical, "
            "photocopying, recording or otherwise \u2014 without the prior written "
            "permission of the copyright holder, except for brief quotations embodied in "
            "critical articles, reviews and scholarly works, with attribution.", s),
        Paragraph(
            "Scripture quotations are taken from the Authorized (King James) Version of the "
            "Bible, which is in the public domain. References follow the conventional "
            "book\u2013chapter\u2013verse form; where a quotation spans several verses the "
            "range is given in full.", s),
        Paragraph(
            "The diagrams in this volume were prepared by the author with the assistance of "
            "computational tooling and are released with the text.", s),
        Spacer(1, 8),
        Paragraph(f"First edition, {cfg['year']}", s),
        Paragraph(f"Published in {cfg['place']}", s),
        Paragraph(f"ISBN {cfg['isbn']}", s),
        Spacer(1, 14),
        Paragraph("Typeset in EB Garamond 11/15.4 pt with Cinzel display capitals "
                  "and Lato diagram lettering.", s),
        Paragraph(
            "EB Garamond \u00a9 2017 The EB Garamond Project Authors; Cinzel \u00a9 2020 "
            "The Cinzel Project Authors; Lato \u00a9 2010\u20132014 tyPoland Lukasz "
            "Dziedzic. All three are used under the SIL Open Font Licence 1.1.", s),
        Spacer(1, 14),
        Paragraph(f"Set for {cfg['trim']} trim.", s),
    ]
    return out


def dedication_page(lines) -> list:
    out = [Spacer(1, 3.1 * inch)]
    for i, ln in enumerate(lines):
        out.append(Paragraph(ln, T.STYLES["dedication"]))
        if i < len(lines) - 1:
            out.append(Spacer(1, 13))
    return out


def epigraph_page(text, source) -> list:
    return [Spacer(1, 2.5 * inch),
            decor.Ornament(width=120, space_before=0, space_after=16),
            Paragraph(text, T.STYLES["epigraph"]),
            Spacer(1, 12),
            Paragraph(source, T.STYLES["epigraph_src"]),
            decor.Ornament(width=120, space_before=16, space_after=0)]


def section_head(text, standfirst=None) -> list:
    out = [Paragraph(text.upper(), T.STYLES["backmatter_h"]),
           decor.GoldRule(width=96, node=True, space_before=10, space_after=12)]
    if standfirst:
        out.append(Paragraph(standfirst, T.STYLES["fm_sub"]))
        out.append(Spacer(1, 10))
    return out


# ---------------------------------------------------------------------------
# part opener
# ---------------------------------------------------------------------------
def part_page(part_no: int, title: str, standfirst: str, plate_id: str | None,
              manifest: dict) -> list:
    roman = ROMAN_UPPER[part_no] if part_no < len(ROMAN_UPPER) else str(part_no)
    ptitle = Paragraph(title, T.STYLES["part_title"])
    ptitle._toc_entry = (0, f"PART {roman} \u00b7 {title}")
    ptitle._bookmark = (f"Part {roman}: {title}", 0)
    out = [HeadSuppress(), RunningHead(title), Spacer(1, 1.15 * inch),
           Paragraph(f"PART {roman}", T.STYLES["part_number"]),
           Spacer(1, 12),
           decor.GoldRule(width=132, node=True, space_before=0, space_after=16),
           ptitle,
           Spacer(1, 10)]
    if standfirst:
        out.append(Paragraph(standfirst, T.STYLES["part_standfirst"]))
    out.append(Spacer(1, 0.55 * inch))
    if plate_id:
        out.extend(figures.load_figure(plate_id, manifest, T.TEXT_W))
    return out


# ---------------------------------------------------------------------------
# chapter opener
# ---------------------------------------------------------------------------
def chapter_opener(ch_no: int, title: str, subtitle: str, scriptures: str) -> list:
    words = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX",
             7: "SEVEN", 8: "EIGHT", 9: "NINE", 10: "TEN", 11: "ELEVEN",
             12: "TWELVE", 13: "THIRTEEN", 14: "FOURTEEN", 15: "FIFTEEN",
             16: "SIXTEEN", 17: "SEVENTEEN", 18: "EIGHTEEN", 19: "NINETEEN",
             20: "TWENTY", 21: "TWENTY-ONE", 22: "TWENTY-TWO", 23: "TWENTY-THREE",
             24: "TWENTY-FOUR", 25: "TWENTY-FIVE", 26: "TWENTY-SIX",
             27: "TWENTY-SEVEN", 28: "TWENTY-EIGHT", 29: "TWENTY-NINE",
             30: "THIRTY", 31: "THIRTY-ONE", 32: "THIRTY-TWO", 33: "THIRTY-THREE",
             34: "THIRTY-FOUR", 35: "THIRTY-FIVE", 36: "THIRTY-SIX",
             37: "THIRTY-SEVEN", 38: "THIRTY-EIGHT", 39: "THIRTY-NINE",
             40: "FORTY", 41: "FORTY-ONE", 42: "FORTY-TWO", 43: "FORTY-THREE",
             44: "FORTY-FOUR", 45: "FORTY-FIVE", 46: "FORTY-SIX",
             47: "FORTY-SEVEN", 48: "FORTY-EIGHT", 49: "FORTY-NINE",
             50: "FIFTY", 51: "FIFTY-ONE", 52: "FIFTY-TWO", 53: "FIFTY-THREE",
             54: "FIFTY-FOUR", 55: "FIFTY-FIVE", 56: "FIFTY-SIX",
             57: "FIFTY-SEVEN", 58: "FIFTY-EIGHT", 59: "FIFTY-NINE",
             60: "SIXTY", 61: "SIXTY-ONE", 62: "SIXTY-TWO", 63: "SIXTY-THREE",
             64: "SIXTY-FOUR", 65: "SIXTY-FIVE", 66: "SIXTY-SIX",
             67: "SIXTY-SEVEN", 68: "SIXTY-EIGHT"}
    num = words.get(ch_no, str(ch_no))
    ch_title = Paragraph(title, T.STYLES["chapter_title"])
    ch_title._toc_entry = (1, f"{ch_no}  \u00b7  {title}")  # level 1 = chapter
    ch_title._bookmark = (f"{ch_no}. {title}", 1)
    out = [
        HeadSuppress(),
        RunningHead(f"{ch_no} \u00b7 {title}"),
        Spacer(1, 0.62 * inch),
        Paragraph(f"CHAPTER {num}", T.STYLES["chapter_number"]),
        Spacer(1, 11),
        ch_title,
        Spacer(1, 12),
        decor.GoldRule(width=104, node=True, space_before=0, space_after=13),
    ]
    if subtitle:
        out.append(Paragraph(subtitle, T.STYLES["chapter_subtitle"]))
        out.append(Spacer(1, 11))
    if scriptures:
        out.append(Paragraph("KEY SCRIPTURES", ParagraphStyle(
            "ksh", parent=T.STYLES["chapter_scriptures"], fontName="Lato-Bold",
            fontSize=7.4, textColor=T.GOLD, leading=11)))
        out.append(Paragraph(scriptures, T.STYLES["chapter_scriptures"]))
    out.append(Spacer(1, 0.30 * inch))
    out.append(decor.Ornament(width=110, space_before=0, space_after=15))
    return out


def chapter_end() -> list:
    return [Spacer(1, 12),
            decor.Ornament(width=96, space_before=0, space_after=0),
            Spacer(1, 6)]
