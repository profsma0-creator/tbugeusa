# -*- coding: utf-8 -*-
"""
Build the AI.101 "Introduction to Artificial Intelligence" final PDF textbook.
Professional book layout: cover, front matter, body (12 chapters), back matter.
Author: TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, NextPageTemplate, Table, TableStyle, HRFlowable, Flowable,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas as canvas_module
import chapters as CH

from framework import (
    BookCanvas, PAGE_W, PAGE_H, M_L, M_R, M_T, M_B,
    AUTHOR, BOOK_TITLE, BOOK_SUBTITLE, COURSE_CODE, COURSE_TITLE,
    COPYRIGHT_YEAR, ISBN_PLACEHOLDER,
    INK, INK_SOFT, PRIMARY, PRIMARY_D, ACCENT, LIGHT, RULE,
    S, P, SP, element_flows, ELEMENT_ORDER,
)

OUT = "AI.101-Introduction-to-Artificial-Intelligence_Final.pdf"

CHAPTER_TITLES = [
    ("Foundations and History of Artificial Intelligence",
     "What AI is, its milestones, and its place in engineering"),
    ("Intelligent Agents and Environments",
     "PEAS, rationality, and agent architectures"),
    ("Problem Formulation and State-Space Search",
     "Turning tasks into search problems"),
    ("Uninformed Search Algorithms",
     "BFS, DFS, UCS, and iterative deepening"),
    ("Informed Search Algorithms",
     "Heuristics, greedy best-first, and A*"),
    ("Adversarial Search",
     "Minimax and alpha-beta pruning"),
    ("Knowledge Representation and Logic",
     "Propositional and first-order logic, inference"),
    ("Reasoning Under Uncertainty and Bayesian AI",
     "Probability, Bayes\u2019 theorem, decision-making"),
    ("Expert Systems",
     "Rule-based diagnosis and the match-resolve-act cycle"),
    ("Machine Learning and Neural Networks Overview",
     "Supervised learning, classification, overfitting"),
    ("Natural Language Processing and Computer Vision",
     "Chatbots, pixels, edges, and image understanding"),
    ("Robotics, Generative AI, Responsible AI, and the Future",
     "Integration, emerging tech, ethics, and final project"),
]

for ch, (t, s) in zip(CH.CHAPTERS, CHAPTER_TITLES):
    ch["_title"] = t
    ch["_subtitle"] = s


def _st(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10, leading=14,
                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


def hrule(color=PRIMARY, w=1.0, before=0, after=8):
    return HRFlowable(width="100%", thickness=w, color=color,
                      spaceBefore=before, spaceAfter=after)


def chapter_opener(num, title, subtitle):
    flows = []
    flows.append(NextPageTemplate("body"))
    flows.append(PageBreak())
    flows.append(Paragraph("CHAPTER %d" % num, _st("ck", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=6)))
    flows.append(Paragraph(title, S["chapter_title"]))
    flows.append(Paragraph(subtitle, S["chapter_sub"]))
    flows.append(HRFlowable(width="100%", thickness=1.6, color=PRIMARY,
                            spaceBefore=4, spaceAfter=10))
    chip = Table([["%02d" % num]], colWidths=[0.9*inch], rowHeights=[0.9*inch])
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.white),
        ("FONTSIZE", (0,0), (-1,-1), 22),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
    ]))
    flows.append(Spacer(1, 14))
    return flows


class TOCNotify(Flowable):
    """Zero-size flowable that registers a TOC entry at the current page."""
    def __init__(self, level, text, doc_ref):
        self.level = level
        self.text = text
        self.doc_ref = doc_ref
    def wrap(self, aw, ah):
        return (0, 0)
    def draw(self):
        self.doc_ref.notify('TOCEntry', (self.level, self.text, self.doc_ref.page))


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=(PAGE_W, PAGE_H),
        leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
        title=BOOK_TITLE, author=AUTHOR,
        subject="AI.101 Introduction to Artificial Intelligence",
        creator="TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA",
    )

    cover_frame = Frame(M_L, M_B, PAGE_W-M_L-M_R, PAGE_H-M_T-M_B, id="cover")
    front_frame = Frame(M_L, M_B, PAGE_W-M_L-M_R, PAGE_H-M_T-M_B, id="front")
    chap_frame  = Frame(M_L, M_B, PAGE_W-M_L-M_R, PAGE_H-M_T-0.9*inch, id="chap")
    body_frame  = Frame(M_L, M_B, PAGE_W-M_L-M_R, PAGE_H-M_T-M_B, id="body")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame]),
        PageTemplate(id="front", frames=[front_frame]),
        PageTemplate(id="chapter", frames=[chap_frame]),
        PageTemplate(id="body",  frames=[body_frame]),
    ])

    story = []

    # ------------------------------------------------------------- COVER
    story.append(Spacer(1, 0.9*inch))
    story.append(Paragraph("TRIUNE BIBLICAL UNIVERSITY", _st("covk", fontName="Helvetica-Bold",
        fontSize=14, leading=18, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph("GLOBAL EXTENSION USA", _st("covk2", fontName="Helvetica-Bold",
        fontSize=14, leading=18, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=24)))
    story.append(HRFlowable(width="55%", thickness=1.2, color=PRIMARY,
                            hAlign="CENTER", spaceBefore=2, spaceAfter=26))
    story.append(Paragraph(BOOK_TITLE, S["title"]))
    story.append(Paragraph(BOOK_SUBTITLE, S["subtitle"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph("%s<br/>%s" % (COURSE_CODE, COURSE_TITLE), S["course"]))
    story.append(Paragraph(CH.BOOK_META["year_semester"], _st("covy", fontName="Helvetica",
        fontSize=11, leading=15, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=26)))
    story.append(HRFlowable(width="55%", thickness=0.8, color=RULE, hAlign="CENTER",
                            spaceBefore=2, spaceAfter=22))
    story.append(Paragraph(AUTHOR, S["author"]))
    story.append(Spacer(1, 18))
    story.append(Paragraph(ISBN_PLACEHOLDER, _st("covi", fontName="Helvetica", fontSize=9.5,
        leading=13, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("%s \u00a9 %s" % (AUTHOR, COPYRIGHT_YEAR), _st("covi2", fontName="Helvetica",
        fontSize=9.5, leading=13, textColor=INK_SOFT, alignment=TA_CENTER)))

    # ------------------------------------------------------------- COPYRIGHT
    story.append(NextPageTemplate("front"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph("Copyright and Publication Information", _st("cr", fontName="Helvetica-Bold",
        fontSize=13, leading=17, textColor=PRIMARY_D, alignment=TA_LEFT, spaceAfter=10)))
    story.append(hrule(PRIMARY, 1.2, 0, 10))
    copyright_text = (
        "<b>%s</b><br/>%s<br/>%s<br/><br/>"
        "%s \u00a9 %s. All rights reserved.<br/>"
        "No part of this publication may be reproduced, stored in a retrieval system, or "
        "transmitted, in any form or by any means, electronic, mechanical, photocopying, "
        "recording, or otherwise, without the prior written permission of the publisher.<br/><br/>"
        "Published by TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA.<br/>"
        "%s<br/>"
        "This textbook is produced for the Bachelor of Artificial Intelligence and Robotics "
        "Engineering programme, course %s %s.<br/><br/>"
        "Textbook Production Standard: each chapter is self-contained and includes learning "
        "objectives, prerequisite knowledge, core concepts, definitions, worked examples, "
        "mathematical derivations, algorithms and pseudocode, engineering applications, "
        "practical laboratory activities, programming exercises, case studies, review questions, "
        "MCQs, short-answer questions, numerical problems, programming/design exercises, a "
        "mini-project, and further reading."
    ) % (BOOK_TITLE, AUTHOR, COURSE_CODE, AUTHOR, COPYRIGHT_YEAR, ISBN_PLACEHOLDER,
         COURSE_CODE, COURSE_TITLE)
    story.append(Paragraph(copyright_text, S["small"]))
    story.append(Spacer(1, 26))
    story.append(Paragraph("Version 1.0 \u2014 Final Edition", _st("crv", fontName="Helvetica-Oblique",
        fontSize=9, leading=12, textColor=INK_SOFT, alignment=TA_LEFT)))

    # ------------------------------------------------------------- CONTENTS
    toc = TableOfContents()
    toc.levelStyles = [
        _st("toc1", fontName="Helvetica-Bold", fontSize=11, leading=16,
            textColor=PRIMARY, alignment=TA_LEFT, leftIndent=6, spaceBefore=8, spaceAfter=1),
        _st("toc2", fontName="Helvetica", fontSize=9.5, leading=13,
            textColor=INK, alignment=TA_LEFT, leftIndent=22, spaceAfter=0.5),
    ]
    toc.dotsMinLevel = 1

    story.append(NextPageTemplate("front"))
    story.append(PageBreak())
    story.append(Paragraph("Contents", _st("toch", fontName="Helvetica-Bold", fontSize=17,
        leading=21, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=10)))
    story.append(hrule(PRIMARY, 1.4, 0, 14))
    story.append(toc)
    story.append(Spacer(1, 16))
    story.append(Paragraph("Final Integrated Project", S["toc_l1"]))
    story.append(Paragraph("Autonomous Delivery Agent \u2014 end-of-course capstone", S["toc_l2"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Back Matter", _st("tocb", fontName="Helvetica-Bold", fontSize=12,
        leading=16, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=8, spaceAfter=4)))
    for lab in ["Glossary", "Bibliography", "Subject Index",
                "Practical-Laboratory Index", "Recommended Software and Hardware Tools"]:
        story.append(Paragraph(lab, S["toc_l2"]))

    # ------------------------------------------------------------- BODY
    story.append(NextPageTemplate("chapter"))
    story.append(PageBreak())
    for i, ch in enumerate(CH.CHAPTERS, start=1):
        story.extend(chapter_opener(i, ch["_title"], ch["_subtitle"]))
        story.append(TOCNotify(0, ch["_title"], doc))
        for key in CH.ELEMENT_ORDER:
            val = ch.get(key)
            if val is None:
                continue
            story.extend(element_flows(key, val))

    # Final integrated project
    story.append(NextPageTemplate("chapter"))
    story.append(PageBreak())
    story.append(Paragraph("PART IV", _st("ck", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=6)))
    story.append(Paragraph("Final Integrated Course Project", S["chapter_title"]))
    story.append(Paragraph(CH.FINAL_PROJECT["title"], S["chapter_sub"]))
    story.append(hrule(PRIMARY, 1.6, 4, 10))
    story.append(TOCNotify(0, CH.FINAL_PROJECT["title"], doc))
    story.append(Paragraph(CH.FINAL_PROJECT["description"], S["body"]))
    story.append(SP(8))
    story.append(Paragraph("Project Phases", _st("el", fontName="Helvetica-Bold", fontSize=10.5,
        leading=14, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=4, spaceAfter=3)))
    story.append(CH.FINAL_PROJECT["phases"])
    story.append(SP(6))
    story.append(Paragraph("Assessment Rubric", _st("el2", fontName="Helvetica-Bold", fontSize=10.5,
        leading=14, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=4, spaceAfter=3)))
    story.append(CH.FINAL_PROJECT["rubric"])

    # ------------------------------------------------------------- BACK MATTER
    story.append(NextPageTemplate("chapter"))
    story.append(PageBreak())
    story.append(Paragraph("Back Matter", _st("bm", fontName="Helvetica-Bold", fontSize=17,
        leading=21, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=10)))
    story.append(hrule(PRIMARY, 1.4, 0, 14))
    story.append(TOCNotify(0, "Back Matter", doc))

    # Glossary
    story.append(Paragraph("Glossary", _st("el", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=8, spaceAfter=8)))
    story.append(TOCNotify(1, "Glossary", doc))
    gloss_rows = [[Paragraph("<b>Term</b>", S["body"]), Paragraph("<b>Definition</b>", S["body"])]]
    for term, definition in CH.GLOSSARY_ENTRIES:
        gloss_rows.append([Paragraph("<b>%s</b>" % term, _st("gt", fontName="Helvetica-Bold",
            fontSize=9.5, leading=13, textColor=INK, alignment=TA_LEFT)),
                            Paragraph(definition, _st("gd", fontSize=9.5, leading=13,
                                textColor=INK, alignment=TA_JUSTIFY))])
    gt = Table(gloss_rows, colWidths=[1.7*inch, PAGE_W-M_L-M_R-1.7*inch], repeatRows=1)
    gt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("GRID", (0,0), (-1,-1), 0.4, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(gt)

    # Bibliography
    story.append(PageBreak())
    story.append(Paragraph("Bibliography", _st("el", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=8, spaceAfter=8)))
    story.append(TOCNotify(1, "Bibliography", doc))
    story.append(hrule(PRIMARY, 1.2, 0, 8))
    for i, ref in enumerate(CH.BIBLIOGRAPHY, start=1):
        story.append(Paragraph("<b>[%d]</b>&nbsp;%s" % (i, ref), _st("br", fontSize=9.5,
            leading=13.5, textColor=INK, alignment=TA_JUSTIFY, leftIndent=16,
            firstLineIndent=-16, spaceAfter=4)))

    # Subject index
    story.append(PageBreak())
    story.append(Paragraph("Subject Index", _st("el", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=8, spaceAfter=8)))
    story.append(TOCNotify(1, "Subject Index", doc))
    story.append(hrule(PRIMARY, 1.2, 0, 8))
    idx_rows = []
    for i in range(0, len(CH.SUBJECT_INDEX), 2):
        pair = CH.SUBJECT_INDEX[i:i+2]
        cells = []
        for term, pages in pair:
            cells.append(Paragraph("<b>%s</b>&hellip;&nbsp;%s" % (term, pages), _st("ix", fontSize=9.5,
                leading=13, textColor=INK, alignment=TA_LEFT)))
        while len(cells) < 2:
            cells.append("")
        idx_rows.append(cells)
    it = Table(idx_rows, colWidths=[(PAGE_W-M_L-M_R)/2.0]*2)
    it.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    story.append(it)

    # Practical-laboratory index
    story.append(PageBreak())
    story.append(Paragraph("Practical-Laboratory Index", _st("el", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=8, spaceAfter=8)))
    story.append(TOCNotify(1, "Practical-Laboratory Index", doc))
    story.append(hrule(PRIMARY, 1.2, 0, 8))
    lab_rows = [[Paragraph("<b>Laboratory Activity</b>", S["body"]), Paragraph("<b>Chapter</b>", S["body"])]]
    for lab, chap in CH.LAB_INDEX:
        lab_rows.append([Paragraph(lab, _st("lt", fontSize=9.5, leading=13, textColor=INK,
                             alignment=TA_LEFT)),
                         Paragraph(chap, _st("lc", fontSize=9.5, leading=13, textColor=INK,
                             alignment=TA_LEFT))])
    lt = Table(lab_rows, colWidths=[PAGE_W-M_L-M_R-1.0*inch, 1.0*inch], repeatRows=1)
    lt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("GRID", (0,0), (-1,-1), 0.4, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(lt)

    # Recommended tools
    story.append(PageBreak())
    story.append(Paragraph("Recommended Software and Hardware Tools", _st("el", fontName="Helvetica-Bold",
        fontSize=13, leading=17, textColor=PRIMARY_D, alignment=TA_LEFT, spaceBefore=8, spaceAfter=8)))
    story.append(TOCNotify(1, "Recommended Software and Hardware Tools", doc))
    story.append(hrule(PRIMARY, 1.2, 0, 8))
    tool_rows = [[Paragraph("<b>Category</b>", S["body"]), Paragraph("<b>Tools</b>", S["body"])]]
    for cat, tools in CH.TOOLS:
        tool_rows.append([Paragraph("<b>%s</b>" % cat, _st("tt", fontSize=9.5, leading=13,
            textColor=INK, alignment=TA_LEFT)), Paragraph(tools, _st("td", fontSize=9.5, leading=13,
            textColor=INK, alignment=TA_LEFT))])
    tt = Table(tool_rows, colWidths=[1.9*inch, PAGE_W-M_L-M_R-1.9*inch], repeatRows=1)
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("GRID", (0,0), (-1,-1), 0.4, RULE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(tt)
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceBefore=6, spaceAfter=8))
    story.append(Paragraph("End of textbook \u2014 %s \u00a9 %s" % (AUTHOR, COPYRIGHT_YEAR),
        _st("end", fontName="Helvetica-Oblique", fontSize=9, leading=12,
            textColor=INK_SOFT, alignment=TA_CENTER)))

    doc.multiBuild(story, canvasmaker=BookCanvas)
    print("PDF written:", OUT)
    return OUT


if __name__ == "__main__":
    build()
