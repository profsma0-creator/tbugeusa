"""Build the publishable final PDF: supplied front cover + final edition interior
+ newly designed back cover. Interior pagination, folios and page labels are
preserved exactly; covers sit outside the numbering scheme.

Usage: .venv/bin/python scripts/build_publishable_edition.py
Inputs:  assets/cover/front-cover.jpg
         deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Final_Edition.pdf
Output:  deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Publishable_Final.pdf
         deliverables/final/Back_Cover.pdf (component)
"""
from pathlib import Path
import json
import pymupdf as fitz
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white

W, H = 504, 720  # 7 x 10 in trim, as the interior
BG = HexColor('#010a16')        # sampled from the supplied front-cover edges
GOLD = HexColor('#c9a44e')
PALE = HexColor('#d7e3ee')
DIM = HexColor('#9db4c6')

for name, face in [('SS', 'Regular'), ('SSB', 'Bold'), ('SSI', 'Italic')]:
    pdfmetrics.registerFont(TTFont(name, f'assets/fonts/SourceSerif4-{face}.ttf'))
pdfmetrics.registerFontFamily('SS', normal='SS', bold='SSB', italic='SSI', boldItalic='SSB')

STY = {
    'kicker': ParagraphStyle('kicker', fontName='SSB', fontSize=10, leading=13, textColor=GOLD,
                             spaceAfter=10, alignment=1),
    'title': ParagraphStyle('title', fontName='SSB', fontSize=23, leading=27, textColor=white,
                            alignment=1, spaceAfter=6),
    'sub': ParagraphStyle('sub', fontName='SSI', fontSize=12.5, leading=16, textColor=PALE,
                          alignment=1, spaceAfter=16),
    'body': ParagraphStyle('body', fontName='SS', fontSize=10.6, leading=14.6, textColor=PALE,
                           spaceAfter=10),
    'head': ParagraphStyle('head', fontName='SSB', fontSize=11, leading=14, textColor=GOLD,
                           spaceBefore=8, spaceAfter=6),
    'item': ParagraphStyle('item', fontName='SS', fontSize=10.1, leading=13.2, textColor=PALE,
                           leftIndent=14, firstLineIndent=-10, spaceAfter=3),
    'foot': ParagraphStyle('foot', fontName='SSB', fontSize=10.5, leading=14, textColor=white,
                           alignment=1, spaceBefore=6),
    'foot2': ParagraphStyle('foot2', fontName='SS', fontSize=9, leading=12, textColor=DIM,
                            alignment=1),
}

def back_cover_background(c, d):
    c.saveState()
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.rect(22, 22, W - 44, H - 44, stroke=1, fill=0)
    c.restoreState()

story = [
    Spacer(1, 8),
    Paragraph('TRT 903 &nbsp;·&nbsp; DOCTORAL TEXTBOOK', STY['kicker']),
    Paragraph('Advanced Neurobiology of Trauma', STY['title']),
    Paragraph('How threat, adversity and recovery are written into the nervous system', STY['sub']),
    HRFlowable(width='38%', thickness=0.8, color=GOLD, hAlign='CENTER', spaceAfter=16),
    Paragraph(
        'Why do some experiences leave lasting marks on the brain and body while others do not? '
        'This doctoral-level textbook follows trauma through every level of the nervous system — '
        'from molecules, synapses and genes to circuits, stress physiology, memory, sleep and '
        'social context — and asks at each step what the evidence actually shows, what it merely '
        'suggests, and what it cannot support.', STY['body']),
    Paragraph(
        'Written for critical readers, each chapter pairs concise, source-verified exposition with '
        'learning objectives, synthesis tables, composite teaching cases, review questions and '
        'research assignments. A 187-term glossary, laboratory and classroom teaching protocols, '
        'assessment checklists and blank learner worksheets support structured study and supervision.',
        STY['body']),
    Paragraph('INSIDE THIS BOOK', STY['head']),
]
for item in [
    'Foundations, functional neuroanatomy and lifespan brain development',
    'Cellular and molecular neuroscience, neurotransmission and neuroplasticity',
    'HPA-axis stress physiology, allostasis, genetics and epigenetics',
    'Threat learning, traumatic memory, emotion regulation and dissociation',
    'Neuroimmunology, neuroimaging methods and their limits',
    'Sleep and circadian rhythms, developmental and structural trauma',
    'Assessment, differential diagnosis and therapeutic translation',
    'Research methods, evidence appraisal and professional integration',
]:
    story.append(Paragraph(item, STY['item'], bulletText='•'))
story += [
    Spacer(1, 10),
    Paragraph('For doctoral students, clinicians, researchers and educators working at the '
              'interface of neuroscience and traumatic stress.', STY['body']),
    Spacer(1, 14),
    HRFlowable(width='38%', thickness=0.8, color=GOLD, hAlign='CENTER', spaceAfter=8),
    Paragraph('TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA', STY['foot']),
    Paragraph('Corporate author · © 2026', STY['foot2']),
]

back_path = Path('deliverables/final/Back_Cover.pdf')
SimpleDocTemplate(str(back_path), pagesize=(W, H), leftMargin=58, rightMargin=58,
                  topMargin=42, bottomMargin=40,
                  title='Advanced Neurobiology of Trauma — Back Cover',
                  author='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA'
                  ).build(story, onFirstPage=back_cover_background, onLaterPages=back_cover_background)
back = fitz.open(back_path)
assert len(back) == 1, len(back)

# --- Front cover page: trim-size page, artwork fitted by width on sampled background ---
front_page = fitz.open()
p = front_page.new_page(width=W, height=H)
p.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=(0.004, 0.039, 0.086))
IMG_W, IMG_H = 1086, 1448
img_h = W * IMG_H / IMG_W            # 672 pt at full width
y0 = (H - img_h) / 2                 # 24 pt bands top and bottom, filled with BG
p.insert_image(fitz.Rect(0, y0, W, y0 + img_h), filename='assets/cover/front-cover.jpg')

# --- Assemble: front cover + interior (unchanged) + back cover ---
interior = fitz.open('deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Final_Edition.pdf')
pm = json.loads(Path('deliverables/final/page-map.json').read_text())
FRONT = pm['front_matter_pages']     # 7 Roman pages inside the interior

out = fitz.open()
out.insert_pdf(front_page)
out.insert_pdf(interior)
out.insert_pdf(back)

# Page labels: covers unnumbered; Roman i.. then Arabic 1.. exactly as the interior.
out.set_page_labels([
    {'startpage': 0, 'prefix': 'Front cover', 'style': '', 'firstpagenum': 1},
    {'startpage': 1, 'prefix': '', 'style': 'r', 'firstpagenum': 1},
    {'startpage': 1 + FRONT, 'prefix': '', 'style': 'D', 'firstpagenum': 1},
    {'startpage': len(out) - 1, 'prefix': 'Back cover', 'style': '', 'firstpagenum': 1},
])

nav = [[1, 'Front cover', 1]]
nav += [[lvl, title, pg + 1] for lvl, title, pg in interior.get_toc()]
nav.append([1, 'Back cover', len(out)])
out.set_toc(nav)

out.set_metadata({
    'title': 'Advanced Neurobiology of Trauma — Doctoral Textbook (TRT 903)',
    'author': 'TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA',
    'subject': 'Publishable final edition with covers. Chapters 1–20 editorially reconstructed '
               'from verified scholarly sources; all citations checked against published '
               'records. Front cover artwork supplied by the publisher. Not independently '
               'peer-reviewed or accredited; no ISBN assigned.',
})
output = Path('deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Publishable_Final.pdf')
out.save(output, garbage=4, deflate=True)
print('Created PUBLISHABLE FINAL:', output, '| total pages:', len(out),
      '| interior pages:', len(interior))
