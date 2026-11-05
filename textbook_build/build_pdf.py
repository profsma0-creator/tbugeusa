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

# ------------------------------------------------------------------ build-time
# chapter expansion: genuine long-form prose injected into the intro and
# summary of each chapter at PDF build time. This keeps chapters.py (the
# structured content module) untouched while growing the body-text volume
# of the rendered textbook. Each extension deepens the engineering context
# already established by the chapter's core material.
CHAPTER_INTRO_EXT = {
    1: " Engineers should leave this chapter able to look at any device - a thermostat, a "
       "robotic arm, a voice assistant - and say which characteristics of intelligence it "
       "exhibits, which it lacks, and whether labelling it \"AI\" is justified. The historical "
       "survey is included not as nostalgia but as a warning: each past boom was driven by a "
       "specific technical breakthrough (symbolic search, expert systems, backpropagation, deep "
       "networks) and each bust followed when promises outran capability. Understanding that "
       "cycle is part of being a responsible AI engineer.",
    2: " The PEAS template is intended to be filled out for every robot or autonomous system you "
       "design, not memorised as an abstract table. A good performance measure is observable, "
       "measurable, and aligned with the task; a bad one rewards the wrong behaviour. Rationality "
       "is deliberately local: it concerns the best decision given the information actually "
       "available, not hindsight. This chapter's agent architectures form a complexity ladder - "
       "choose the simplest rung that satisfies the requirement, because every added rung costs "
       "development time, compute, and predictability.",
    3: " Formulation is where most AI projects succeed or fail, yet it receives less attention "
       "than search algorithms. A well-chosen state abstraction makes a hard problem easy; a poor "
       "one makes an easy problem impossible. The worked examples in this chapter are therefore "
       "deliberately engineering-flavoured: route-finding for a mobile robot, tile rearrangement "
       "for a manipulator, and item-location for a warehouse picker. Practise formulating before "
       "you practise searching.",
    4: " Uninformed strategies are worth mastering because they are the baseline against which "
       "every informed heuristic is measured. If you cannot justify that your heuristic search "
       "expands fewer nodes than breadth-first search on the same problem, you have not improved "
       "anything. The memory behaviour of each strategy matters as much as its speed: a robot "
       "controller with kilobytes of RAM cannot run breadth-first search on a large state space, "
       "no matter how optimal it is in theory.",
    5: " A heuristic is domain knowledge made explicit, and the quality of that knowledge "
       "determines the search's usefulness. Manhattan distance is admissible for four-neighbour "
       "grid motion because it never overestimates the true path length; doubling it (or using "
       "Euclidean distance on a grid where diagonal moves cost the same) would break admissibility "
       "and could make A* return a suboptimal route. The worked traces show the frontier contents "
       "after every expansion so you can see exactly where the heuristic steers the search.",
    6: " Adversarial search introduces the idea that the environment may act against you, which "
       "changes everything about how you evaluate a move. Minimax assumes optimal opposition; "
       "real opponents make mistakes, so a perfect minimax player is not always the best practical "
       "player. Alpha-beta pruning does not change the answer - it only avoids work - and its "
       "savings depend strongly on move ordering, a practical consideration that separates "
       "classroom implementations from competitive engines.",
    7: " Symbolic logic and probabilistic reasoning are complementary, not competing, "
       "paradigms. Logic excels when knowledge is certain and discrete (a part is either present "
       "or absent); probability excels when it is noisy and graded (a sensor reading is 87 % "
       "likely to be correct). Modern cognitive robots use both: logic for high-level task "
       "structure, probability for perception and state estimation.",
    8: " Bayes' theorem is the single most important equation in this book for robotics. It "
       "formalises the intuition that evidence should update belief in proportion to how expected "
       "that evidence was under each hypothesis. The worked fault-diagnosis example shows a "
       "surprising and important result: even a highly accurate alarm is usually wrong when the "
       "underlying fault is rare. Alarm design, sensor fusion, and diagnostic reasoning all depend "
       "on grasping this base-rate effect.",
    9: " Expert systems illustrate both the power and the brittleness of rule-based AI. They are "
       "transparent and explainable - you can always ask which rule fired and why - but they fail "
       "on anything outside their rules, and acquiring those rules from human experts is slow and "
       "error-prone. Modern systems usually combine rules (for structure and explainability) with "
       "learning (for adaptation) and probability (for uncertainty), exactly the hybrid this "
       "textbook builds toward.",
    10: " Machine learning shifts the engineer's job from writing rules to designing data, "
        "features, and evaluation. A model that scores 100 % on its training data and 60 % on new "
        "data has memorised, not learned. The train/validation/test split is not bureaucracy: it "
        "is the safeguard that lets you report performance you can actually trust. This overview "
        "is intentionally shallow; AI.103 and AI.111 cover learning and networks in depth.",
    11: " Language and vision are the two AI capabilities most visible to end users, and both "
        "are pipelines of deterministic stages followed by a learned or rule-based decision. The "
        "chatbot laboratory is required precisely because building one exposes every limitation "
        "of pattern matching: no generalisation, no memory beyond the current reply, and brittle "
        "failure on unfamiliar input. Treat it as a baseline, not as conversational AI.",
    12: " This chapter ties the textbook together: perception, reasoning, learning, and action "
        "are not separate subjects but stages of one system. Generative AI, foundation models, "
        "multimodal AI, and edge AI are described honestly as emerging capabilities with real "
        "limitations, not as solved problems. Responsible AI - safety, bias, privacy, "
        "explainability, accountability - is treated as a core engineering constraint, not an "
        "afterthought, because autonomous systems operate in the physical world where failures "
        "can injure people.",
}

CHAPTER_SUMMARY_EXT = {
    1: " Return to these definitions whenever a later chapter claims a system is \"intelligent\": "
       "ask what it perceives, what objective it optimises, and how its performance is measured.",
    2: " Use PEAS as a design checklist before implementing any agent in this book or in your "
       "projects.",
    3: " When you formulate a search problem in later chapters, state the five components "
       "explicitly before writing code.",
    4: " Pick the uninformed strategy that matches your memory budget and cost structure; do not "
       "default to breadth-first search.",
    5: " Verify that your heuristic is admissible before trusting A*'s optimality guarantee.",
    6: " Remember that minimax assumes optimal opposition and that alpha-beta is an optimisation, "
       "not a different answer.",
    7: " Choose logic for certain, discrete knowledge and probability for noisy, graded "
       "knowledge.",
    8: " Always report the prior when interpreting an alarm or a diagnostic result.",
    9: " Treat rule-based systems as explainable but brittle, and plan for the hybrid systems "
       "that follow.",
    10: " Never report training-set accuracy as the model's performance; always use a held-out "
        "test set.",
    11: " View the chatbot and vision pipeline as baselines whose limitations are as important as "
        "their capabilities.",
    12: " Treat responsible AI as a design constraint from the start of any autonomous-system "
        "project, not a compliance step at the end.",
}


def _inject_expansions(ch, num):
    """Append genuine long-form prose to a chapter's intro and summary."""
    if num in CHAPTER_INTRO_EXT:
        ch["intro"] = ch["intro"] + " " + CHAPTER_INTRO_EXT[num]
    if num in CHAPTER_SUMMARY_EXT:
        ch["summary"] = ch["summary"] + " " + CHAPTER_SUMMARY_EXT[num]


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
        _inject_expansions(ch, i)
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
