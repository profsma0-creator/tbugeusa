"""Typeset the reconstructed back matter (acronyms, appendices, resources,
teaching protocols, professional standards, further reading, references).

Usage: .venv/bin/python scripts/typeset_backmatter.py
Reads manuscript/backmatter.md and the per-chapter reference lists.
Writes deliverables/backmatter/Back_Matter_Proof.pdf and editorial/backmatter-toc.json.
"""
from pathlib import Path
import json, re
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Table, TableStyle, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
import pymupdf as fitz

for name, face in [('SS', 'Regular'), ('SSB', 'Bold'), ('SSI', 'Italic')]:
    pdfmetrics.registerFont(TTFont(name, f'assets/fonts/SourceSerif4-{face}.ttf'))
pdfmetrics.registerFontFamily('SS', normal='SS', bold='SSB', italic='SSI', boldItalic='SSB')

NAVY = HexColor('#193c4b'); TEAL = HexColor('#216b72'); LIGHT = HexColor('#edf4f4'); GREY = HexColor('#46565c')
W, H = 504, 720; WIDTH = 393
OUT = Path('deliverables/backmatter'); OUT.mkdir(parents=True, exist_ok=True)
CAPTURED = []

STY = {
    'title': ParagraphStyle('title', fontName='SSB', fontSize=22, leading=26, textColor=NAVY, spaceBefore=6, spaceAfter=14, keepWithNext=True),
    'h1': ParagraphStyle('h1', fontName='SSB', fontSize=15, leading=19, textColor=NAVY, spaceBefore=16, spaceAfter=7, keepWithNext=True),
    'h2': ParagraphStyle('h2', fontName='SSB', fontSize=11.8, leading=15, textColor=NAVY, spaceBefore=12, spaceAfter=5, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='SS', fontSize=10.6, leading=14, spaceAfter=7, allowWidows=0, allowOrphans=0),
    'item': ParagraphStyle('item', fontName='SS', fontSize=10.6, leading=14, leftIndent=14, firstLineIndent=-11, spaceAfter=4.5),
    'cell': ParagraphStyle('cell', fontName='SS', fontSize=8.8, leading=11.2),
    'cellhead': ParagraphStyle('cellhead', fontName='SSB', fontSize=8.8, leading=11.2, textColor=white),
    'ref': ParagraphStyle('ref', fontName='SS', fontSize=9.3, leading=11.8, leftIndent=14, firstLineIndent=-14, spaceAfter=4.5),
}


def markup(t):
    t = escape(t)
    t = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', t)


class Doc(BaseDocTemplate):
    def __init__(self, path):
        super().__init__(str(path), pagesize=(W, H),
            title='Advanced Neurobiology of Trauma — Back Matter',
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
        c.drawString(left, H - 28, 'TRT 903  |  BACK MATTER')
        c.setStrokeColor(HexColor('#c7d1d4')); c.line(left, H - 34, left + WIDTH, H - 34)
        c.drawString(left, 25, 'Not approved for publication · 21 October 2026')
        c.drawRightString(left + WIDTH, 25, str(d.page))
        c.restoreState()

    def afterFlowable(self, flow):
        if isinstance(flow, Paragraph) and hasattr(flow, 'outline'):
            level, key, title = flow.outline
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(title, key, level=level, closed=False)
            CAPTURED.append([level, title, self.page])


def fit_widths(rows):
    n = len(rows[0])
    longest = [[max((r[j] or ' ').split(), key=len) for j in range(n)] for r in rows if len(r) == n]
    caps = [max(len(r[j]) for r in rows if j < len(r)) for j in range(n)]
    lw = [max(len(w[j]) for w in longest) for j in range(n)]
    for fs in (8.8, 8.5, 8.2, 7.9, 7.6):
        need = [max(pdfmetrics.stringWidth(w[j], 'SS', fs) for w in longest) + 11 for j in range(n)]
        if sum(need) <= WIDTH:
            wts = [max(1, caps[j] - lw[j] + 1) for j in range(n)]
            s = sum(wts); extra = WIDTH - sum(need)
            return fs, [need[j] + extra * wts[j] / s for j in range(n)]
    need = [max(pdfmetrics.stringWidth(w[j], 'SS', 7.6) for w in longest) + 8 for j in range(n)]
    scale = WIDTH / sum(need)
    return 7.6, [x * scale for x in need]


def split_table(block):
    rows = [r.strip().strip('|').split('|') for r in block.strip().splitlines()]
    rows = [[c.strip() for c in r] for r in rows]
    if len(rows) > 1 and all(set(c) <= {'-', ':', ' '} for c in rows[1]):
        rows = [rows[0]] + rows[2:]
    return rows


refs = []
for name in ['manuscript/chapter01-verified-references.json', 'manuscript/chapter02-references.json'] + \
            [f'manuscript/chapter{n:02d}-references.json' for n in range(3, 21)]:
    for r in json.loads(Path(name).read_text()):
        if r not in refs:
            refs.append(r)
refs = sorted(refs, key=str.casefold)

text = Path('manuscript/backmatter.md').read_text()
story = []
blocks = [b.strip() for b in re.split(r'\n\s*\n', text) if b.strip()]
idx = 0; seen_title = False
for block in blocks:
    idx += 1
    if block.startswith('# ') and not block.startswith('## '):
        story.append(Paragraph(markup(block[2:].strip()), STY['title']))
        continue
    if block == '[REFERENCES]':
        for r in refs:
            story.append(Paragraph(markup(r), STY['ref']))
        continue
    if block.startswith('### '):
        s = block[4:].strip()
        p = Paragraph(markup(s), STY['h2']); p.outline = (1, f'b-{idx}', s)
        story.append(p); continue
    if block.startswith('## '):
        if seen_title or story:
            story.append(PageBreak())
        seen_title = True
        s = block[3:].strip()
        p = Paragraph(markup(s), STY['h1']); p.outline = (0, f'b-{idx}', s)
        story.append(p); continue
    if block.startswith('|'):
        rows = split_table(block)
        fs, widths = fit_widths(rows)
        headst = ParagraphStyle('ch', parent=STY['cellhead'], fontSize=fs, leading=fs * 1.27)
        cellst = ParagraphStyle('cc', parent=STY['cell'], fontSize=fs, leading=fs * 1.27)
        data = [[Paragraph(markup(x), headst) for x in rows[0]]] + \
               [[Paragraph(markup(x), cellst) for x in r] for r in rows[1:]]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT]),
            ('LINEBELOW', (0, 0), (-1, 0), .7, TEAL), ('LINEBELOW', (0, -1), (-1, -1), .6, TEAL)]))
        story.extend([t, Spacer(1, 8)]); continue
    if all(re.match(r'^- ', x) for x in block.splitlines()):
        for line in block.splitlines():
            story.append(Paragraph(markup(line[2:].strip()), STY['item'], bulletText='•'))
        continue
    story.append(Paragraph(markup(' '.join(block.splitlines())), STY['body']))

pdf = OUT / 'Back_Matter_Proof.pdf'
Doc(pdf).multiBuild(story)
Path('editorial/backmatter-toc.json').write_text(json.dumps(CAPTURED, indent=2))
print('Created', pdf, 'pages:', len(fitz.open(pdf)), '| references:', len(refs), '| sections:', len(CAPTURED))
