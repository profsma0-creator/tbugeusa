"""Typeset one reconstructed volume chapter to a bounded editorial proof.

Usage: .venv/bin/python scripts/typeset_volume_chapter.py 2
Reads manuscript/chapterNN.md and manuscript/chapterNN-references.json.
The proof is an editorial working document, not a certification of scientific accuracy.
"""
from pathlib import Path
import json, re, sys
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Table, TableStyle, Flowable, KeepTogether, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pymupdf as fitz

CH = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OFFSET = int(sys.argv[2]) if len(sys.argv) > 2 else 0
SUFFIX = sys.argv[3] if len(sys.argv) > 3 else ''
SRC = Path(f'manuscript/chapter{CH:02d}.md')
REFS = json.load(open(f'manuscript/chapter{CH:02d}-references.json'))
OUT = Path(f'deliverables/chapter{CH:02d}'); OUT.mkdir(parents=True, exist_ok=True)
TOC_CACHE = Path(f'editorial/chapter{CH:02d}-toc.json')
CAPTURED = []

for name, face in [('SS', 'Regular'), ('SSB', 'Bold'), ('SSI', 'Italic')]:
    pdfmetrics.registerFont(TTFont(name, f'assets/fonts/SourceSerif4-{face}.ttf'))
pdfmetrics.registerFontFamily('SS', normal='SS', bold='SSB', italic='SSI', boldItalic='SSB')
NAVY = HexColor('#193c4b'); TEAL = HexColor('#216b72'); LIGHT = HexColor('#edf4f4'); GREY = HexColor('#46565c')
W, H = 504, 720; WIDTH = 393
STY = {
    'body': ParagraphStyle('body', fontName='SS', fontSize=11, leading=14.2, spaceAfter=7.5, allowWidows=0, allowOrphans=0),
    'title': ParagraphStyle('title', fontName='SSB', fontSize=24, leading=28.5, spaceBefore=10, spaceAfter=16, textColor=NAVY, keepWithNext=True),
    'h1': ParagraphStyle('h1', fontName='SSB', fontSize=15.5, leading=19.5, spaceBefore=15, spaceAfter=8, textColor=NAVY),
    'h2': ParagraphStyle('h2', fontName='SSB', fontSize=12.3, leading=15.8, spaceBefore=12, spaceAfter=6, textColor=NAVY),
    'quote': ParagraphStyle('quote', fontName='SSI', fontSize=10.5, leading=13.6, leftIndent=14, rightIndent=8, spaceBefore=6, spaceAfter=9),
    'small': ParagraphStyle('small', fontName='SS', fontSize=9, leading=11.7, spaceAfter=6, allowWidows=0, allowOrphans=0),
    'cell': ParagraphStyle('cell', fontName='SS', fontSize=8.8, leading=11.1),
    'cellhead': ParagraphStyle('cellhead', fontName='SSB', fontSize=8.8, leading=11.1, textColor=white),
    'caption': ParagraphStyle('caption', fontName='SSB', fontSize=9.8, leading=12.6, spaceBefore=9, spaceAfter=6, keepWithNext=True),
    'item': ParagraphStyle('item', fontName='SS', fontSize=11, leading=14.2, leftIndent=14, firstLineIndent=-12, spaceAfter=5.5, allowWidows=0, allowOrphans=0),
    'toc0': ParagraphStyle('toc0', fontName='SS', fontSize=10, leading=13, spaceAfter=2),
    'toc1': ParagraphStyle('toc1', fontName='SS', fontSize=9, leading=12, leftIndent=10, spaceAfter=1),
    'tocpage': ParagraphStyle('tocpage', fontName='SS', fontSize=10, leading=13, alignment=2),
    'ref': ParagraphStyle('ref', fontName='SS', fontSize=9.8, leading=12, leftIndent=14, firstLineIndent=-14, spaceAfter=5),
}

def markup(t):
    t = escape(t)
    t = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', t)

def drawpara(c, text, x, y, w, style):
    p = Paragraph(markup(text), style); _, h = p.wrap(w, 1000); p.drawOn(c, x, y - h); return h

class Diagram(Flowable):
    def __init__(self, kind):
        super().__init__(); self.kind = kind; self.width = WIDTH; self.height = 360 if kind in (3, 4) else (330 if kind in (1, 2) else 320)

    def box(self, c, x, y, w, h, head, body=None):
        c.setFillColor(LIGHT); c.roundRect(x, y - h, w, h, 3, fill=1, stroke=0)
        drawpara(c, head, x + 8, y - 6, w - 16, STY['caption'])
        if body:
            drawpara(c, body, x + 8, y - 25, w - 16, STY['small'])

    def arrow(self, c, x1, y1, x2, y2, dash=False):
        c.setStrokeColor(TEAL); c.setLineWidth(.9)
        if dash:
            c.setDash(2, 2)
        c.line(x1, y1, x2, y2); c.setDash()
        if abs(x2 - x1) < 2:
            d = 1 if y2 > y1 else -1
            c.line(x2, y2, x2 - 3, y2 - 5 * d); c.line(x2, y2, x2 + 3, y2 - 5 * d)
        else:
            d = 1 if x2 > x1 else -1
            c.line(x2, y2, x2 - 5 * d, y2 - 3); c.line(x2, y2, x2 - 5 * d, y2 + 3)

    def draw(self):
        c = self.canv; w = self.width; h = self.height
        if self.kind == 1:
            levels = [('Society and context', 'services, culture, law, resources, inequality'),
                      ('Behaviour and function', 'sleep, avoidance, performance, relationships'),
                      ('Brain systems', 'networks, prefrontal-limbic circuits, interoception'),
                      ('Cells and synapses', 'neurons, glia, receptors, plasticity'),
                      ('Molecules and genes', 'transmitters, hormones, gene expression')]
            for i, (head, body) in enumerate(levels):
                y = h - 12 - i * 62; shrink = i * 18
                c.setFillColor(LIGHT); c.roundRect(shrink, y - 50, w - 2 * shrink, 50, 3, fill=1, stroke=0)
                drawpara(c, head, shrink + 10, y - 6, w - 2 * shrink - 20, STY['caption'])
                drawpara(c, body, shrink + 10, y - 25, w - 2 * shrink - 20, STY['small'])
                if i < 4:
                    c.setStrokeColor(TEAL); c.line(w / 2, y - 52, w / 2, y - 60)
                    c.line(w / 2, y - 60, w / 2 - 3, y - 56); c.line(w / 2, y - 60, w / 2 + 3, y - 56)
        elif self.kind == 2:
            steps = [('State the question', 'Exposure, outcome, population, timing, intended decision'),
                     ('Identify the design', 'Cross-sectional, longitudinal, experimental, qualitative'),
                     ('Audit measurement', 'Construct, instrument, reliability, validity, error'),
                     ('List alternatives', 'Confounders, reverse causation, selection, comorbidity'),
                     ('Weigh uncertainty', 'Effect size, confidence, replication, heterogeneity'),
                     ('State a bounded conclusion', 'What is supported, what is not, what would reduce doubt')]
            for i, (head, body) in enumerate(steps):
                y = h - i * 55
                c.setFillColor(LIGHT if i % 2 == 0 else HexColor('#e3eeee'))
                c.roundRect(0, y - 46, w, 46, 3, fill=1, stroke=0)
                drawpara(c, f'{i+1}.  {head}', 10, y - 6, w - 20, STY['caption'])
                drawpara(c, body, 10, y - 24, w - 20, STY['small'])
                if i < 5:
                    c.setStrokeColor(TEAL); c.line(w / 2, y - 48, w / 2, y - 53)
        elif self.kind == 3:
            x, bw, bh = 82, 230, 56
            ys = [h - 8, h - 92, h - 176, h - 260]
            self.box(c, x, ys[0], bw, bh, 'Hypothalamus (paraventricular nucleus)', 'secretes CRH into the portal circulation')
            self.box(c, x, ys[1], bw, bh, 'Anterior pituitary', 'secretes ACTH into the systemic circulation')
            self.box(c, x, ys[2], bw, bh, 'Adrenal cortex', 'secretes cortisol; the main glucocorticoid in humans')
            self.box(c, x, ys[3], bw, bh, 'Brain and pituitary', 'cortisol feeds back on hippocampus, prefrontal cortex and hypothalamus')
            for i in range(3):
                self.arrow(c, x + bw / 2, ys[i] - bh, x + bw / 2, ys[i + 1] + 2)
            c.setStrokeColor(TEAL); c.setLineWidth(.9); c.setDash(2, 2)
            y4 = ys[3] - bh / 2
            c.line(x + bw, y4, x + bw + 42, y4)
            c.line(x + bw + 42, y4, x + bw + 42, ys[0] - bh / 2)
            c.line(x + bw + 42, ys[0] - bh / 2, x + bw + 4, ys[0] - bh / 2)
            c.setDash()
            c.line(x + bw + 4, ys[0] - bh / 2, x + bw + 9, ys[0] - bh / 2 - 3)
            c.line(x + bw + 4, ys[0] - bh / 2, x + bw + 9, ys[0] - bh / 2 + 3)
            drawpara(c, 'negative feedback', x + bw + 4, ys[2] + 44, 74, STY['small'])
        elif self.kind == 4:
            self.box(c, 6, h - 6, 180, 52, 'Threat cue (CS)', 'sensory thalamus and cortex')
            self.box(c, 207, h - 6, 180, 52, 'Aversive event (US)', 'somatosensory and brainstem pathways')
            self.box(c, 6, h - 104, 381, 56, 'Lateral amygdala', 'convergence of cue and event information; synaptic plasticity')
            self.box(c, 6, h - 196, 180, 62, 'Central amygdala', 'output nucleus')
            self.box(c, 207, h - 196, 180, 62, 'Defensive output', 'freezing, autonomic arousal, cortisol release')
            self.box(c, 6, h - 306, 381, 52, 'Regulation and context', 'vmPFC restrains output; hippocampus encodes the context')
            self.arrow(c, 96, h - 58, 96, h - 102)
            self.arrow(c, 297, h - 58, 297, h - 102)
            self.arrow(c, 96, h - 160, 96, h - 194)
            self.arrow(c, 297, h - 160, 297, h - 194)
            c.setStrokeColor(TEAL); c.setLineWidth(.9); c.setDash(2, 2)
            c.line(96, h - 258, 96, h - 304)
            c.setDash()
            c.line(96, h - 304, 96, h - 309); c.line(96, h - 304, 93, h - 299); c.line(96, h - 304, 99, h - 299)
            drawpara(c, 'dashed: contextual and inhibitory input', 104, h - 274, 280, STY['small'])
        else:
            self.box(c, 96, h - 6, 200, 46, 'Memory', None)
            self.box(c, 0, h - 96, 178, 76, 'Declarative', 'medial temporal lobe, especially hippocampus')
            self.box(c, 215, h - 96, 178, 76, 'Non-declarative', 'basal ganglia, cerebellum, amygdala')
            self.box(c, 0, h - 236, 178, 120, 'Examples', 'episodic: events and their context\nsemantic: facts and concepts')
            self.box(c, 215, h - 236, 178, 120, 'Examples', 'skills and habits\nconditioned responses\nemotional learning')
            self.arrow(c, 196, h - 52, 89, h - 94)
            self.arrow(c, 196, h - 52, 304, h - 94)
            self.arrow(c, 89, h - 172, 89, h - 234)
            self.arrow(c, 304, h - 172, 304, h - 234)

class ProofDoc(BaseDocTemplate):
    def __init__(self, path):
        super().__init__(str(path), pagesize=(W, H),
            title=f'Advanced Neurobiology of Trauma — Chapter {CH} Developmental Proof',
            author='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA',
            leftMargin=61, rightMargin=50, topMargin=48, bottomMargin=48)
        self.addPageTemplates([
            PageTemplate(id='Odd', frames=[Frame(61, 48, WIDTH, 624, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                         onPage=self.furniture, autoNextPageTemplate='Even'),
            PageTemplate(id='Even', frames=[Frame(50, 48, WIDTH, 624, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
                         onPage=self.furniture, autoNextPageTemplate='Odd')])
    def furniture(self, c, d):
        c.saveState(); left = 61 if d.page % 2 else 50
        c.setFont('SS', 8); c.setFillColor(GREY)
        c.drawString(left, H - 28, f'TRT 903  |  CHAPTER {CH}  |  DEVELOPMENTAL PROOF')
        c.setStrokeColor(HexColor('#c7d1d4')); c.line(left, H - 34, left + WIDTH, H - 34)
        c.drawString(left, 25, 'Not approved for publication · 21 October 2026')
        c.drawRightString(left + WIDTH, 25, str(d.page)); c.restoreState()
    def afterFlowable(self, flow):
        if isinstance(flow, Paragraph) and hasattr(flow, 'outline'):
            level, key, title = flow.outline
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(title, key, level=level, closed=False)
            CAPTURED.append([level, title, self.page])

def heading(text, style, level, key):
    p = Paragraph(markup(text), STY[style])
    if level is not None: p.outline = (level, key, text)
    return p

text = SRC.read_text()
story = []
doc = Document(); sec = doc.sections[0]
sec.page_width = Inches(7); sec.page_height = Inches(10)
sec.top_margin = sec.bottom_margin = Inches(2 / 3); sec.left_margin = Inches(.85); sec.right_margin = Inches(.7)
for name in ['Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3']:
    doc.styles[name].font.name = 'Source Serif 4'
doc.styles['Normal'].font.size = Pt(11)
doc.styles['Normal'].paragraph_format.line_spacing = Pt(14.2)
doc.styles['Normal'].paragraph_format.space_after = Pt(7)
for name, size in [('Title', 24), ('Heading 1', 15.5), ('Heading 2', 12.3), ('Heading 3', 11.5)]:
    doc.styles[name].font.size = Pt(size)
hdr = sec.header.paragraphs[0]; hdr.text = f'TRT 903  |  CHAPTER {CH}  |  DEVELOPMENTAL PROOF'; hdr.style = 'Caption'
ftr = sec.footer.paragraphs[0]; ftr.text = 'Not approved for publication · '
fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE'); ftr._p.append(fld)

def add_doc(s, style=None):
    p = doc.add_paragraph(style=style)
    for i, part in enumerate(re.split(r'\*\*(.*?)\*\*', s)):
        for j, sub in enumerate(re.split(r'(?<!\*)\*([^*]+)\*(?!\*)', part)):
            r = p.add_run(sub); r.bold = bool(i % 2); r.italic = bool(j % 2)
    return p

def contents():
    story.append(Spacer(1, 10))
    story.append(Paragraph('In this chapter', STY['h2']))
    if TOC_CACHE.exists():
        rows = json.loads(TOC_CACHE.read_text())
        data = []
        for level, title, page in rows[1:]:
            indent = '' if level == 0 else '\u2003'
            data.append([Paragraph(markup(indent + title), STY['toc0' if level == 0 else 'toc1']),
                         Paragraph(str(page + OFFSET), STY['tocpage'])])
        t = Table(data, colWidths=[WIDTH - 26, 26], hAlign='LEFT')
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
        story.append(t)
    else:
        toc = TableOfContents()
        toc.levelStyles = [ParagraphStyle('toc0', fontName='SS', fontSize=10, leading=13, spaceBefore=5, rightIndent=20),
                           ParagraphStyle('toc1', fontName='SS', fontSize=9, leading=12, leftIndent=12, rightIndent=20, spaceBefore=2)]
        story.append(toc)
    story.append(PageBreak())
    doc.add_page_break(); doc.add_heading('Chapter contents', 1)
    p = doc.add_paragraph(); f = OxmlElement('w:fldSimple'); f.set(qn('w:instr'), 'TOC \\o "1-2" \\h \\z \\u'); p._p.append(f)
    doc.add_paragraph('The PDF contains generated contents and page numbers. Refresh the contents field in Word after editing.', style='Caption')
    doc.add_page_break()

def split_table(block):
    rows = [r.strip().strip('|').split('|') for r in block.strip().splitlines()]
    rows = [[c.strip() for c in r] for r in rows]
    if len(rows) > 1 and all(set(c) <= {'-', ':', ' '} for c in rows[1]):
        rows = [rows[0]] + rows[2:]
    return rows

def fit_table(rows):
    n = len(rows[0])
    longest = [[max((r[j] or ' ').split(), key=len) for j in range(n)] for r in rows if len(r) == n]
    caps = [max(len(r[j]) for r in rows if j < len(r)) for j in range(n)]
    lw = [max(len(w[j]) for w in longest) for j in range(n)]
    chosen = None
    for fs in (8.8, 8.5, 8.2, 7.9, 7.6, 7.3, 7.0):
        need = [max(pdfmetrics.stringWidth(w[j], 'SS', fs) for w in longest) + 11 for j in range(n)]
        if sum(need) <= WIDTH:
            chosen = (fs, need)
            break
    if chosen is None:
        fs = 7.0
        need = [max(pdfmetrics.stringWidth(w[j], 'SS', fs) for w in longest) + 8 for j in range(n)]
        scale = WIDTH / sum(need)
        return fs, [x * scale for x in need]
    fs, need = chosen
    wts = [max(1, caps[j] - lw[j] + 1) for j in range(n)]
    s = sum(wts)
    extra = WIDTH - sum(need)
    return fs, [need[j] + extra * wts[j] / s for j in range(n)]

blocks = [b.strip() for b in re.split(r'\n\s*\n', text) if b.strip()]
first_h2 = True; idx = 0; fig = 0
while idx < len(blocks):
    block = blocks[idx]; idx += 1
    if block.startswith('[FIGURE:'):
        fid = re.search(r'\[FIGURE:([\d.]+)\]', block)[1]
        fig += 1
        KIND = {'2.1': 4, '7.1': 5, '8.1': 3}
        kind = KIND.get(fid, 1 if fig == 1 else 2)
        CAPS = {
            1: ('Levels of analysis in trauma neurobiology',
                'The levels interact reciprocally. Arrows indicate influence, not anatomical containment; '
                'a finding at one level cannot be substituted for a finding at another.'),
            2: ('From evidence to a defensible conclusion',
                'The sequence is an educational reasoning aid, not a validated clinical algorithm or a claim of causation.'),
            3: ('The hypothalamic–pituitary–adrenal axis and glucocorticoid feedback',
                'CRH, corticotrophin-releasing hormone; ACTH, adrenocorticotrophic hormone. Solid arrows indicate stimulation; '
                'the dashed arrow indicates negative feedback. The diagram is schematic and omits many inputs and timescales.'),
            4: ('A simplified threat-learning circuit',
                'CS, conditioned stimulus; US, unconditioned stimulus; vmPFC, ventromedial prefrontal cortex. '
                'Connections are simplified: the amygdala is treated as a functional unit and many parallel routes are omitted.'),
            5: ('Memory systems relevant to trauma',
                'The taxonomy follows the declarative/non-declarative distinction. Real tasks usually engage more than one system, '
                'and the boundaries between systems are debated.'),
        }
        title, note = CAPS[kind]
        cap = f'Figure {fid}. {title}'
        story.extend([Paragraph(cap, STY['caption']), Diagram(kind), Paragraph(note, STY['small']), Spacer(1, 8)])
        from reportlab.pdfgen.canvas import Canvas
        dg = Diagram(kind); asset = OUT / f'Figure_{CH}_{fig}_edited.pdf'
        cv = Canvas(str(asset), pagesize=(WIDTH, dg.height)); dg.canv = cv; dg.draw(); cv.save()
        d = fitz.open(asset); d[0].get_pixmap(matrix=fitz.Matrix(2, 2)).save(str(OUT / f'Figure_{CH}_{fig}_edited.png')); d.close()
        add_doc(cap, 'Caption'); doc.add_picture(str(OUT / f'Figure_{CH}_{fig}_edited.png'), width=Inches(WIDTH / 72)); add_doc(note, 'Caption')
    elif re.match(r'^Table \d+\.\d+\.', block) and idx < len(blocks) and blocks[idx].startswith('|'):
        cap = block; rows = split_table(blocks[idx]); idx += 1
        story.append(Paragraph(markup(cap), STY['caption']))
        fs, widths = fit_table(rows)
        headst = ParagraphStyle('ch', parent=STY['cellhead'], fontSize=fs, leading=fs * 1.26)
        cellst = ParagraphStyle('cc', parent=STY['cell'], fontSize=fs, leading=fs * 1.26)
        data = [[Paragraph(markup(x), headst) for x in rows[0]]] + \
               [[Paragraph(markup(x), cellst) for x in r] for r in rows[1:]]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT]),
            ('LINEBELOW', (0, 0), (-1, 0), .7, TEAL), ('LINEBELOW', (0, -1), (-1, -1), .6, TEAL)]))
        story.extend([t, Spacer(1, 8)])
        add_doc(cap, 'Caption')
        dt = doc.add_table(rows=1, cols=len(rows[0])); dt.style = 'Light Shading Accent 1'
        for c, s in zip(dt.rows[0].cells, rows[0]): c.text = s
        trpr = dt.rows[0]._tr.get_or_add_trPr(); trpr.append(OxmlElement('w:tblHeader'))
        for row in rows[1:]:
            for c, s in zip(dt.add_row().cells, row): c.text = s
        for row in dt.rows:
            row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs: r.font.size = Pt(9)
        doc.add_paragraph('')
    elif block == '[PAGEBREAK]':
        story.append(PageBreak()); doc.add_page_break()
    elif block.startswith('> '):
        s = ' '.join(line.lstrip('> ').strip() for line in block.splitlines())
        story.append(Paragraph(markup(s), STY['quote'])); add_doc(s, 'Quote')
    elif block == '[BIBLIOGRAPHY]':
        for s in sorted(REFS, key=str.casefold):
            story.append(Paragraph(markup(s), STY['ref']))
            p = add_doc(s); p.paragraph_format.left_indent = Pt(14); p.paragraph_format.first_line_indent = Pt(-14)
    elif block.startswith('#'):
        lines = [l for l in block.splitlines() if l.strip()]
        for line in lines:
            m = re.match(r'^(#{1,4}) (.*)', line, re.S)
            if not m: continue
            level = len(m[1]); s = m[2].replace('\n', ' ').strip()
            if level == 1: continue
            if level == 2 and first_h2:
                first_h2 = False
                story.append(heading(s, 'title', 0, f't-{idx}'))
                doc.add_heading(s, 0)
                story.append(Paragraph(f'Chapter {CH}', STY['small']))
                doc.add_paragraph(f'Chapter {CH}', style='Caption')
                contents()
                continue
            style = 'h1' if level == 2 else 'h2'
            story.append(CondPageBreak(66 if level == 2 else 52))
            story.append(heading(s, style, 0 if level == 2 else 1, f'h-{idx}-{level}'))
            doc.add_heading(s, 1 if level == 2 else 2)
    elif all(re.match(r'^(?:- |\d+\. )', x) for x in block.splitlines()):
        for line in block.splitlines():
            bullet = line.startswith('- ')
            s = re.sub(r'^(?:- |\d+\. )', '', line)
            st = ParagraphStyle('b', parent=STY['item'], firstLineIndent=0, bulletIndent=0,
                                bulletFontName='SS', bulletFontSize=10) if bullet else STY['item']
            story.append(Paragraph(markup(s), st, bulletText='•') if bullet else Paragraph(markup(s), st))
            add_doc(('• ' if bullet else '') + s)
    else:
        s = ' '.join(block.splitlines())
        story.append(Paragraph(markup(s), STY['body'])); add_doc(s)

pdf = OUT / f'Chapter_{CH:02d}_Developmental_Proof{SUFFIX}.pdf'
ProofDoc(pdf).multiBuild(story)
doc.save(OUT / f'Chapter_{CH:02d}_Edited_Manuscript{SUFFIX}.docx')
readable = text.replace('[BIBLIOGRAPHY]', '\n\n'.join(sorted(REFS, key=str.casefold)))
(OUT / f'Chapter_{CH:02d}_Edited_Manuscript{SUFFIX}.md').write_text(readable)
TOC_CACHE.parent.mkdir(exist_ok=True)
if not SUFFIX: TOC_CACHE.write_text(json.dumps(CAPTURED, indent=2))
print('Created', pdf, 'pages:', len(fitz.open(pdf)), '| references:', len(REFS), '| toc entries:', len(CAPTURED))
