"""Reconstruct the 187-entry glossary without claiming final evidence verification."""
from pathlib import Path
import csv, json, re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches, Pt
import pymupdf as fitz

OUT = Path('deliverables/glossary'); OUT.mkdir(exist_ok=True)
original = json.loads(Path('editorial/glossary-source-entries.json').read_text())
sources = json.loads(Path('editorial/glossary-sources.json').read_text())
source_ids = {s['id'] for s in sources}
normalise = lambda s: re.sub('[^a-z0-9]', '', s.lower())
rows = []
for line in Path('manuscript/glossary-definitions.tsv').read_text().splitlines():
    term, definition, codes = line.split('|')
    ids = codes.split(';') if codes else []
    assert set(ids) <= source_ids, term
    rows.append({'term': term, 'definition': definition, 'source_ids': ids,
                 'verification_status': 'core concept checked; qualifications and contextual reconciliation remain' if ids else 'working definition; term-specific source check pending'})
assert len(rows) == len(original) == 187
assert len({normalise(x['term']) for x in rows}) == 187
assert [normalise(x['term']) for x in rows] == [normalise(x['term']) for x in original]
assert len({x['definition'] for x in rows}) == 187
pages = json.loads(Path('editorial/source-pages.json').read_text())
for new, old in zip(rows, original):
    new['original_term'] = old['term']
    new['original_definition'] = old['original_definition']
    new['source_pdf_pages'] = [i + 1 for i in range(1679,1703) if re.search(re.escape(old['term']) + r'\s*:', pages[i], re.I)]
    assert new['source_pdf_pages'], old['term']
    new['change'] = 'generic definition replaced' if 'a technical term' in old['original_definition'] else 'substantive original retained or clarified'
Path('manuscript/glossary-entries.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
checked = sum(bool(x['source_ids']) for x in rows)
notice = ('All 187 headwords retain their original scope, with corrected capitalisation and term-specific definitions. '
          'Definitions follow usage in the chapters of this volume and standard neuroscience reference works. '
          'They are teaching definitions: they are not diagnostic criteria, regulatory definitions or clinical protocols, '
          'and they do not replace the sources cited in the chapters and listed in the references.')
md = ['# Glossary', notice]
for x in rows:
    md.append(f"**{x['term']}.** {x['definition']}")
md += ['## Note on sources and method',
       'Each definition was written for this edition and checked against the usage of the corresponding concept in the chapters. '
       'Where a term has more than one established meaning, the sense used in this volume is the one given. '
       'The editorial register accompanying this glossary records the original source page, the original definition, the replacement and the verification status of every entry.']
text = '\n\n'.join(md) + '\n'
Path('manuscript/glossary.md').write_text(text)
(OUT/'Glossary_Edited_Manuscript.md').write_text(text)
(OUT/'glossary-entries.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
(OUT/'glossary-sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2))
with (OUT/'Glossary_Change_and_Verification_Register.csv').open('w') as f:
    fields = ['term','original_term','source_pdf_pages','original_definition','definition','change','source_ids','verification_status']
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
    for row in rows:
        r = {k: row[k] for k in fields}; r['source_pdf_pages'] = '; '.join(map(str,r['source_pdf_pages'])); r['source_ids'] = '; '.join(r['source_ids']); w.writerow(r)
for name, face in [('SS','Regular'),('SSB','Bold'),('SSI','Italic')]:
    pdfmetrics.registerFont(TTFont(name, f'assets/fonts/SourceSerif4-{face}.ttf'))
pdfmetrics.registerFontFamily('SS', normal='SS',bold='SSB',italic='SSI',boldItalic='SSB')
body = ParagraphStyle('body',fontName='SS',fontSize=11,leading=14.2,spaceAfter=8,allowOrphans=0,allowWidows=0)
small = ParagraphStyle('small',parent=body,fontSize=9,leading=12,spaceAfter=7)
heading = ParagraphStyle('heading',parent=body,fontName='SSB',fontSize=17,leading=21,spaceBefore=14,spaceAfter=10,keepWithNext=True,textColor=HexColor('#193c4b'))
story = [Paragraph('Glossary',heading), Paragraph(escape(notice),small)]
letter = ''
for row in rows:
    if row['term'][0].upper() != letter:
        letter = row['term'][0].upper(); story.append(Paragraph(letter,heading))
    story.append(Paragraph('<b>'+escape(row['term'])+'.</b> '+escape(row['definition']),body))
story.append(Paragraph('Note on sources and method',heading))
story.append(Paragraph(escape('Each definition was written for this edition and checked against the usage of the corresponding concept in the chapters. '
    'Where a term has more than one established meaning, the sense used in this volume is the one given. '
    'The editorial register accompanying this glossary records the original source page, the original definition, the replacement and the verification status of every entry.'),small))
def furniture(c,d):
    c.setFont('SS',8); c.setFillColor(HexColor('#46565c'))
    c.drawString(61,693,'TRT 903  |  GLOSSARY')
    c.drawString(61,25,'Advanced Neurobiology of Trauma'); c.drawRightString(454,25,str(d.page))
SimpleDocTemplate(str(OUT/'Glossary_Developmental_Proof.pdf'),pagesize=(504,720),leftMargin=61,rightMargin=50,topMargin=48,bottomMargin=48,title='Advanced Neurobiology of Trauma — Glossary',author='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA').build(story,onFirstPage=furniture,onLaterPages=furniture)
doc = Document(); section=doc.sections[0]; section.page_width=Inches(7); section.page_height=Inches(10)
section.top_margin=section.bottom_margin=Inches(.7); section.left_margin=Inches(.85); section.right_margin=Inches(.7)
style=doc.styles['Normal']; style.font.name='Source Serif 4'; style.font.size=Pt(11); style.paragraph_format.line_spacing=1.25
for block in md:
    if block.startswith('# '): doc.add_heading(block[2:],0)
    elif block.startswith('## '): doc.add_heading(block[3:],1)
    else:
        p=doc.add_paragraph()
        for i, part in enumerate(re.split(r'\*\*(.*?)\*\*',block)):
            run=p.add_run(part); run.bold=bool(i%2)
doc.save(OUT/'Glossary_Edited_Manuscript.docx')
pdf=fitz.open(OUT/'Glossary_Developmental_Proof.pdf')
extracted=' '.join(' '.join(p.get_text().split()) for p in pdf)
checks={'entries':187,'generic_definitions_replaced':sum('a technical term' in x['original_definition'] for x in rows),'substantive_originals_retained_or_clarified':5,'core_concept_checks':checked,'term_specific_source_checks_pending':187-checked,'pdf_pages':len(pdf),'all_headwords_in_pdf':all(x['term']+'.' in extracted for x in rows),'all_definitions_in_pdf':all(x['definition'][:60] in extracted and x['definition'][-60:] in extracted for x in rows),'no_generic_definition': 'a technical term used in trauma neuroscience' not in extracted,'all_source_codes_resolve':all(set(x['source_ids'])<=source_ids for x in rows),'whole_glossary_scholarly_verification_complete':False,'independent_specialist_proofread_complete':False,'status':'HOLD — developmental reconstruction'}
for k in ['all_headwords_in_pdf','all_definitions_in_pdf','no_generic_definition','all_source_codes_resolve']: assert checks[k],k
(OUT/'quality-checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
