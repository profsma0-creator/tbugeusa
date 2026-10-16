"""
bookkit.theme — physical book format, colour palette, fonts and the stylesheet.

Trim 6 x 9 in (trade hardback / paperback), EB Garamond body, Cinzel display,
Lato for diagram labels and captions.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent.parent
FONT_DIR = ROOT / "assets" / "fonts"

# --------------------------------------------------------------------------
# page geometry
# --------------------------------------------------------------------------
PAGE_W = 6.0 * inch          # 432 pt
PAGE_H = 9.0 * inch          # 648 pt
MARGIN_INSIDE = 0.875 * inch
MARGIN_OUTSIDE = 0.75 * inch
MARGIN_TOP = 0.80 * inch
MARGIN_BOTTOM = 0.85 * inch
TEXT_W = PAGE_W - MARGIN_INSIDE - MARGIN_OUTSIDE      # 315 pt
TEXT_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM          # 529.2 pt
HEAD_BASELINE = PAGE_H - 0.58 * inch                   # running-head baseline

# --------------------------------------------------------------------------
# palette — sampled from the front cover
# --------------------------------------------------------------------------
INK = HexColor("#16223A")          # deep navy, primary text
INK_SOFT = HexColor("#2E3A50")     # secondary text
NAVY_DEEP = HexColor("#0E1729")
GOLD = HexColor("#B08A2E")
GOLD_LIGHT = HexColor("#D9BE7A")
GOLD_PALE = HexColor("#F0E6CC")
CREAM = HexColor("#FBF7EE")
CREAM_DARK = HexColor("#F5EFE1")
WARM_GRAY = HexColor("#6E6A63")
RULE = HexColor("#D8CEB8")
RULE_DARK = HexColor("#B9AE94")
WHITE = HexColor("#FFFFFF")
BLACK = HexColor("#111111")

# --------------------------------------------------------------------------
# fonts
# --------------------------------------------------------------------------
FONTS = {
    "Garamond": "EBGaramond-Regular.ttf",
    "Garamond-It": "EBGaramond-Italic.ttf",
    "Garamond-SB": "EBGaramond-SemiBold.ttf",
    "Garamond-SBIt": "EBGaramond-SemiBoldItalic.ttf",
    "Garamond-Bold": "EBGaramond-Bold.ttf",
    "Cinzel": "Cinzel-Regular.ttf",
    "Cinzel-SB": "Cinzel-SemiBold.ttf",
    "Cinzel-Bold": "Cinzel-Bold.ttf",
    "Cinzel-XB": "Cinzel-ExtraBold.ttf",
    "Lato": "Lato-Regular.ttf",
    "Lato-Bold": "Lato-Bold.ttf",
    "Lato-It": "Lato-Italic.ttf",
    "Lato-Black": "Lato-Black.ttf",
    "Lato-Med": "Lato-Medium.ttf",
}

FAMILY = {
    "body": "Garamond",
    "body-it": "Garamond-It",
    "body-sb": "Garamond-SB",
    "body-sbit": "Garamond-SBIt",
    "display": "Cinzel",
    "display-sb": "Cinzel-SB",
    "display-b": "Cinzel-Bold",
    "sans": "Lato",
    "sans-b": "Lato-Bold",
    "sans-it": "Lato-It",
}


def register_fonts() -> None:
    missing = []
    for name, fname in FONTS.items():
        path = FONT_DIR / fname
        if not path.exists():
            missing.append(str(path))
            continue
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(path)))
    if missing:
        raise SystemExit(
            "Font files missing:\n  " + "\n  ".join(missing) +
            "\n\nRun tools/bootstrap.sh to fetch and instantiate them."
        )
    # register the body family so <b> and <i> work inside paragraphs
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily(
        "Garamond",
        normal="Garamond", bold="Garamond-SB",
        italic="Garamond-It", boldItalic="Garamond-SBIt",
    )
    registerFontFamily(
        "Lato", normal="Lato", bold="Lato-Bold",
        italic="Lato-It", boldItalic="Lato-It",
    )
    registerFontFamily(
        "Cinzel", normal="Cinzel", bold="Cinzel-Bold",
        italic="Cinzel", boldItalic="Cinzel-Bold",
    )


# --------------------------------------------------------------------------
# stylesheet
# --------------------------------------------------------------------------
def build_styles() -> dict[str, ParagraphStyle]:
    s: dict[str, ParagraphStyle] = {}

    # ---- body copy -------------------------------------------------------
    s["body"] = ParagraphStyle(
        "body", fontName="Garamond", fontSize=11.0, leading=15.4,
        textColor=INK, alignment=TA_JUSTIFY, firstLineIndent=0,
        spaceBefore=0, spaceAfter=0, hyphenationLang="en_GB",
        embeddedHyphenation=1, splitLongWords=0,
    )
    s["body_first"] = ParagraphStyle("body_first", parent=s["body"])
    # subsequent paragraphs get a first-line indent, the classic novel/book rule
    s["body_ind"] = ParagraphStyle(
        "body_ind", parent=s["body"], firstLineIndent=13,
    )
    s["body_center"] = ParagraphStyle(
        "body_center", parent=s["body"], alignment=TA_CENTER,
    )

    # ---- chapter / part furniture ---------------------------------------
    s["part_number"] = ParagraphStyle(
        "part_number", fontName="Cinzel", fontSize=13, leading=20,
        textColor=GOLD, alignment=TA_CENTER, tracking=3,
    )
    s["part_title"] = ParagraphStyle(
        "part_title", fontName="Cinzel-Bold", fontSize=25, leading=31,
        textColor=INK, alignment=TA_CENTER, tracking=1.2,
    )
    s["part_standfirst"] = ParagraphStyle(
        "part_standfirst", fontName="Garamond-It", fontSize=12.5, leading=18,
        textColor=INK_SOFT, alignment=TA_CENTER, spaceBefore=6,
    )
    s["chapter_number"] = ParagraphStyle(
        "chapter_number", fontName="Cinzel", fontSize=11.5, leading=18,
        textColor=GOLD, alignment=TA_CENTER, tracking=2.6,
    )
    s["chapter_title"] = ParagraphStyle(
        "chapter_title", fontName="Cinzel-Bold", fontSize=19.5, leading=25,
        textColor=INK, alignment=TA_CENTER, tracking=0.8,
    )
    s["chapter_subtitle"] = ParagraphStyle(
        "chapter_subtitle", fontName="Garamond-It", fontSize=11.6, leading=16.4,
        textColor=INK_SOFT, alignment=TA_CENTER, spaceBefore=7,
    )
    s["chapter_scriptures"] = ParagraphStyle(
        "chapter_scriptures", fontName="Lato", fontSize=8.2, leading=12.4,
        textColor=WARM_GRAY, alignment=TA_CENTER, spaceBefore=2,
    )

    # ---- section headings -----------------------------------------------
    s["h2"] = ParagraphStyle(
        "h2", fontName="Cinzel-Bold", fontSize=12.2, leading=17,
        textColor=INK, alignment=TA_LEFT, tracking=0.7,
        spaceBefore=19, spaceAfter=7, keepWithNext=1,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="Cinzel-SB", fontSize=10.4, leading=15,
        textColor=GOLD, alignment=TA_LEFT, tracking=0.7,
        spaceBefore=14, spaceAfter=5, keepWithNext=1,
    )
    s["h4"] = ParagraphStyle(
        "h4", fontName="Garamond-SBIt", fontSize=11.0, leading=15,
        textColor=INK_SOFT, alignment=TA_LEFT,
        spaceBefore=10, spaceAfter=3, keepWithNext=1,
    )

    # ---- scripture / quotation ------------------------------------------
    s["verse_text"] = ParagraphStyle(
        "verse_text", fontName="Garamond-It", fontSize=10.6, leading=15,
        textColor=INK, alignment=TA_JUSTIFY, leftIndent=13, rightIndent=9,
    )
    s["verse_attrib"] = ParagraphStyle(
        "verse_attrib", fontName="Lato", fontSize=8.4, leading=12,
        textColor=GOLD, alignment=TA_RIGHT, rightIndent=9, spaceBefore=4,
        tracking=0.4,
    )
    s["quote_text"] = ParagraphStyle(
        "quote_text", parent=s["verse_text"], fontName="Garamond",
    )
    s["pull_text"] = ParagraphStyle(
        "pull_text", fontName="Garamond-It", fontSize=14.5, leading=21,
        textColor=INK, alignment=TA_CENTER,
    )
    s["pull_attrib"] = ParagraphStyle(
        "pull_attrib", fontName="Lato", fontSize=8.6, leading=12,
        textColor=GOLD, alignment=TA_CENTER, spaceBefore=7, tracking=0.5,
    )

    # ---- boxes ------------------------------------------------------------
    s["note_title"] = ParagraphStyle(
        "note_title", fontName="Cinzel-SB", fontSize=9.8, leading=14,
        textColor=INK, alignment=TA_LEFT, tracking=0.6, spaceAfter=5,
    )
    s["note_body"] = ParagraphStyle(
        "note_body", fontName="Garamond", fontSize=10.2, leading=14.2,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=5,
    )
    s["note_body_ind"] = ParagraphStyle(
        "note_body_ind", parent=s["note_body"], firstLineIndent=11,
    )
    s["kp_item"] = ParagraphStyle(
        "kp_item", fontName="Garamond", fontSize=10.3, leading=14.4,
        textColor=INK, alignment=TA_LEFT, leftIndent=15, bulletIndent=3,
        spaceAfter=3.5,
    )

    # ---- lists -------------------------------------------------------------
    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"], leftIndent=17, bulletIndent=4,
        spaceAfter=3.2, alignment=TA_LEFT,
    )
    s["numbered"] = ParagraphStyle(
        "numbered", parent=s["bullet"], leftIndent=19, bulletIndent=2,
    )

    # ---- figures ------------------------------------------------------------
    s["fig_caption"] = ParagraphStyle(
        "fig_caption", fontName="Lato", fontSize=8.3, leading=12.2,
        textColor=WARM_GRAY, alignment=TA_LEFT,
    )
    s["fig_number"] = ParagraphStyle(
        "fig_number", fontName="Lato-Bold", fontSize=7.6, leading=11,
        textColor=GOLD, alignment=TA_LEFT, tracking=0.6, spaceAfter=1.5,
    )
    s["fig_source"] = ParagraphStyle(
        "fig_source", fontName="Lato-It", fontSize=7.4, leading=10.6,
        textColor=RULE_DARK, alignment=TA_LEFT, spaceBefore=2.5,
    )

    # ---- tables -------------------------------------------------------------
    s["tbl_head"] = ParagraphStyle(
        "tbl_head", fontName="Lato-Bold", fontSize=8.6, leading=12.2,
        textColor=INK, alignment=TA_LEFT,
    )
    s["tbl_head_c"] = ParagraphStyle("tbl_head_c", parent=s["tbl_head"], alignment=TA_CENTER)
    s["tbl_cell"] = ParagraphStyle(
        "tbl_cell", fontName="Garamond", fontSize=10.0, leading=13.6,
        textColor=INK, alignment=TA_LEFT,
    )
    s["tbl_cell_it"] = ParagraphStyle("tbl_cell_it", parent=s["tbl_cell"],
                                      fontName="Garamond-It")
    s["tbl_caption"] = ParagraphStyle(
        "tbl_caption", fontName="Lato-Bold", fontSize=7.6, leading=11,
        textColor=GOLD, alignment=TA_LEFT, tracking=0.6,
    )

    # ---- front / back matter -------------------------------------------------
    s["fm_title"] = ParagraphStyle(
        "fm_title", fontName="Cinzel-Bold", fontSize=21, leading=29,
        textColor=INK, alignment=TA_CENTER, tracking=0.8,
    )
    s["fm_sub"] = ParagraphStyle(
        "fm_sub", fontName="Garamond-It", fontSize=12.5, leading=18,
        textColor=INK_SOFT, alignment=TA_CENTER, spaceBefore=8,
    )
    s["fm_author"] = ParagraphStyle(
        "fm_author", fontName="Cinzel", fontSize=11, leading=17,
        textColor=INK, alignment=TA_CENTER, tracking=2.2,
    )
    s["fm_role"] = ParagraphStyle(
        "fm_role", fontName="Lato", fontSize=8.4, leading=12.6,
        textColor=WARM_GRAY, alignment=TA_CENTER,
    )
    s["copyright"] = ParagraphStyle(
        "copyright", fontName="Garamond", fontSize=8.4, leading=12.6,
        textColor=INK_SOFT, alignment=TA_LEFT, spaceAfter=5,
    )
    s["copyright_c"] = ParagraphStyle("copyright_c", parent=s["copyright"], alignment=TA_CENTER)
    s["dedication"] = ParagraphStyle(
        "dedication", fontName="Garamond-It", fontSize=12, leading=19,
        textColor=INK_SOFT, alignment=TA_CENTER,
    )
    s["epigraph"] = ParagraphStyle(
        "epigraph", fontName="Garamond-It", fontSize=11.5, leading=17.5,
        textColor=INK, alignment=TA_CENTER,
    )
    s["epigraph_src"] = ParagraphStyle(
        "epigraph_src", fontName="Lato", fontSize=8.3, leading=12,
        textColor=GOLD, alignment=TA_CENTER, spaceBefore=6, tracking=0.4,
    )
    s["toc_entry"] = ParagraphStyle(
        "toc_entry", fontName="Garamond", fontSize=9.6, leading=14.4,
        textColor=INK, alignment=TA_LEFT,
    )
    s["toc_part"] = ParagraphStyle(
        "toc_part", fontName="Cinzel-Bold", fontSize=9.2, leading=14.6,
        textColor=INK, alignment=TA_CENTER, tracking=0.7,
        spaceBefore=11, spaceAfter=3,
    )
    s["toc_part_rule"] = ParagraphStyle("toc_part_rule", parent=s["toc_part"])
    s["figlist"] = ParagraphStyle(
        "figlist", fontName="Garamond", fontSize=9.4, leading=14,
        textColor=INK, alignment=TA_LEFT,
    )
    s["backmatter_h"] = ParagraphStyle(
        "backmatter_h", fontName="Cinzel-Bold", fontSize=17, leading=23,
        textColor=INK, alignment=TA_CENTER, tracking=0.9,
    )
    s["index_item"] = ParagraphStyle(
        "index_item", fontName="Garamond", fontSize=8.7, leading=11.9,
        textColor=INK, alignment=TA_LEFT, leftIndent=11, firstLineIndent=-11,
    )
    s["index_letter"] = ParagraphStyle(
        "index_letter", fontName="Cinzel-Bold", fontSize=10.4, leading=17,
        textColor=GOLD, alignment=TA_LEFT, spaceBefore=7, spaceAfter=1.5,
    )
    s["biblio"] = ParagraphStyle(
        "biblio", fontName="Garamond", fontSize=9.5, leading=13.4,
        textColor=INK, alignment=TA_LEFT, leftIndent=15, firstLineIndent=-15,
        spaceAfter=5.5,
    )
    s["biblio_h"] = ParagraphStyle(
        "biblio_h", fontName="Cinzel-SB", fontSize=10.4, leading=15,
        textColor=GOLD, alignment=TA_LEFT, tracking=0.7,
        spaceBefore=15, spaceAfter=6,
    )
    return s


STYLES: dict[str, ParagraphStyle] = {}
