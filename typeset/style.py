"""Typography, colour and paragraph styles for the CPY 903 textbook.

Design brief
------------
* Trim size 6 x 9 in (152.4 x 228.6 mm), a standard academic- monograph trim.
* Body text: EB Garamond 11/15.2 pt, justified, first-line indent 14 pt.
* Display: Source Serif 4 (SemiBold) for chapter titles and part titles.
* Running heads: 8 pt letterspaced versal serif; folio centred in the foot.
* Colour is intentionally minimal: a single ink tone plus a 6 % warm grey
  for table rules and case-conference panels.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- trim & grid
PAGE_W, PAGE_H = 432.0, 648.0          # 6 x 9 in in points
M_TOP, M_BOTTOM = 58.0, 62.0
M_INNER, M_OUTER = 66.0, 52.0
TEXT_W = PAGE_W - M_INNER - M_OUTER    # 314 pt
TEXT_H = PAGE_H - M_TOP - M_BOTTOM     # 528 pt

INK = colors.HexColor("#1A1A1A")
INK_SOFT = colors.HexColor("#4A4A4A")
RULE = colors.HexColor("#8C8C8C")
RULE_LIGHT = colors.HexColor("#C9C6BE")
PANEL = colors.HexColor("#F4F2EC")
ACCENT = colors.HexColor("#3B4A54")     # muted slate, used sparingly

# ------------------------------------------------------------------- fonts
FONTS = {
    "Body": "EBGaramond-Regular.ttf",
    "Body-Italic": "EBGaramond-Italic.ttf",
    "Body-Med": "EBGaramond-Medium.ttf",
    "Body-Semi": "EBGaramond-SemiBold.ttf",
    "Body-Bold": "EBGaramond-Bold.ttf",
    "Body-SemiIt": "EBGaramond-SemiBoldItalic.ttf",
    "Disp": "SourceSerif4-Regular.ttf",
    "Disp-Semi": "SourceSerif4-SemiBold.ttf",
    "Disp-Bold": "SourceSerif4-Bold.ttf",
    "Disp-Italic": "SourceSerif4-Italic.ttf",
}


def register_fonts():
    for name, filename in FONTS.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, filename)))
    # bold is mapped to the semibold cut: EB Garamond's true bold is visually
    # too heavy against the regular at text sizes
    pdfmetrics.registerFontFamily(
        "Body",
        normal="Body",
        bold="Body-Semi",
        italic="Body-Italic",
        boldItalic="Body-SemiIt",
    )
    pdfmetrics.registerFontFamily(
        "Disp",
        normal="Disp",
        bold="Disp-Semi",
        italic="Disp-Italic",
        boldItalic="Disp-Semi",
    )


def _p(name, **kw):
    base = dict(
        fontName="Body",
        fontSize=11,
        leading=15.2,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceBefore=0,
        spaceAfter=0,
        hyphenationLang="en_GB",
        hyphenMinWord=8,
        hyphenMinPrefix=4,
        hyphenMinSuffix=4,
        uriWasteReduce=0,
        embeddedHyphenation=1,
        splitLongWords=1,
        allowWidows=0,
        allowOrphans=0,
    )
    base.update(kw)
    return ParagraphStyle(name, **base)


def build_styles():
    ss = StyleSheet1()

    # ---- body
    ss.add(_p("Body", firstLineIndent=14, spaceBefore=0, spaceAfter=0))
    ss.add(_p("BodyFirst", firstLineIndent=0, spaceBefore=0))
    ss.add(_p("BodyNoIndent", firstLineIndent=0))
    ss.add(_p("BodySmall", fontSize=9.6, leading=12.8))
    ss.add(_p("Opening", firstLineIndent=0, fontSize=11.4, leading=16.2))

    # ---- lists
    ss.add(_p("Bullet", firstLineIndent=0, leftIndent=15, bulletIndent=2,
              spaceBefore=3.2, spaceAfter=3.2, bulletFontName="Body",
              bulletFontSize=11, bulletDedent=4))
    ss.add(_p("Numbered", firstLineIndent=0, leftIndent=17, bulletIndent=2,
              spaceBefore=3.0, spaceAfter=3.0, bulletFontName="Body",
              bulletFontSize=10.4))
    ss.add(_p("RefEntry", firstLineIndent=-16, leftIndent=16, fontSize=9.6,
              leading=12.4, alignment=TA_LEFT, spaceBefore=5.0, spaceAfter=0))
    ss.add(_p("IndexEntry", firstLineIndent=-10, leftIndent=10, fontSize=8.8,
              leading=11.4, alignment=TA_LEFT, spaceBefore=1.4))
    ss.add(_p("GlossTerm", firstLineIndent=0, leftIndent=0, fontSize=9.7,
              leading=12.9, spaceBefore=5.0, alignment=TA_JUSTIFY))

    # ---- headings
    ss.add(_p("ChapterNumber", fontName="Body-Med", fontSize=9.6, leading=12,
              alignment=TA_LEFT, textColor=ACCENT, spaceAfter=6, tracking=1.4))
    ss.add(_p("ChapterTitle", fontName="Disp-Semi", fontSize=21.5, leading=25.5,
              alignment=TA_LEFT, spaceAfter=4, hyphenationLang=""))
    ss.add(_p("ChapterTitleNoHyph", fontName="Disp-Semi", fontSize=21.5,
              leading=25.5, alignment=TA_LEFT, spaceAfter=4, hyphenationLang="",
              splitLongWords=0))
    ss.add(_p("H1", fontName="Disp-Semi", fontSize=13.6, leading=16.6,
              alignment=TA_LEFT, spaceBefore=19, spaceAfter=6.5, tracking=0.15,
              hyphenationLang=""))
    ss.add(_p("H2", fontName="Disp-Semi", fontSize=11.0, leading=14.6,
              alignment=TA_LEFT, spaceBefore=15, spaceAfter=4.2, tracking=0.2,
              textColor=INK, hyphenationLang=""))
    ss.add(_p("RunIn", fontName="Body-Semi", fontSize=11, leading=15.2,
              alignment=TA_JUSTIFY, spaceBefore=8))

    # ---- figure & table furniture
    ss.add(_p("Caption", fontName="Body", fontSize=8.8, leading=11.4,
              alignment=TA_LEFT, textColor=INK, spaceBefore=5, spaceAfter=2,
              hyphenationLang=""))
    ss.add(_p("CaptionNum", fontName="Body-Semi", fontSize=8.8, leading=11.4,
              alignment=TA_LEFT, spaceBefore=5, spaceAfter=2,
              hyphenationLang=""))
    ss.add(_p("TableCaption", fontName="Body-Semi", fontSize=8.8, leading=11.4,
              alignment=TA_LEFT, spaceBefore=12, spaceAfter=4,
              hyphenationLang=""))
    ss.add(_p("TableNote", fontName="Body", fontSize=7.8, leading=10,
              alignment=TA_LEFT, textColor=INK_SOFT, spaceBefore=3, spaceAfter=6))
    ss.add(_p("TableCell", fontName="Body", fontSize=9.0, leading=11.6,
              alignment=TA_LEFT, hyphenationLang=""))
    ss.add(_p("TableHead", fontName="Body-Semi", fontSize=8.8, leading=11.2,
              alignment=TA_LEFT, hyphenationLang=""))

    # ---- panels
    ss.add(_p("Panel", fontSize=9.8, leading=13.4, bulletFontName="Body",
              bulletFontSize=9.8, alignment=TA_LEFT, hyphenationLang=""))
    ss.add(_p("PanelHead", fontName="Body-Semi", fontSize=9.8, leading=13.4,
              spaceAfter=3))
    ss.add(_p("Quote", fontSize=9.8, leading=13.4, leftIndent=18, rightIndent=14,
              firstLineIndent=0, spaceBefore=6, spaceAfter=6))

    # ---- front matter
    ss.add(_p("FMHalfTitle", fontName="Disp-Semi", fontSize=18, leading=23,
              alignment=TA_CENTER, hyphenationLang=""))
    ss.add(_p("FMTitle", fontName="Disp-Semi", fontSize=27, leading=31,
              alignment=TA_CENTER, hyphenationLang=""))
    ss.add(_p("FMSub", fontName="Disp-Italic", fontSize=12.6, leading=17,
              alignment=TA_CENTER))
    ss.add(_p("FMImprint", fontName="Body-Med", fontSize=10, leading=15,
              alignment=TA_CENTER))
    ss.add(_p("FMCopy", fontName="Body", fontSize=8.4, leading=11.4,
              alignment=TA_LEFT, hyphenationLang=""))
    ss.add(_p("FMCentre", fontName="Body", fontSize=10, leading=14,
              alignment=TA_CENTER))
    ss.add(_p("TOCLevel1", fontName="Body-Semi", fontSize=10, leading=13.4,
              alignment=TA_LEFT, spaceBefore=7))
    ss.add(_p("TOCLevel2", fontName="Body", fontSize=9.4, leading=12.2,
              alignment=TA_LEFT, leftIndent=16, firstLineIndent=-16))
    ss.add(_p("TOCPart", fontName="Disp-Semi", fontSize=11, leading=14,
              alignment=TA_LEFT, spaceBefore=12, spaceAfter=2))
    return ss


STYLES = build_styles()
