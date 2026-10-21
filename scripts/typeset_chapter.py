"""Typeset a bounded editorial proof; does not certify scientific validity.
Run from repository root with .venv/bin/python scripts/typeset_chapter.py.
"""
from pathlib import Path
import re,json
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,
    PageBreak,Table,TableStyle,Flowable,KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from docx import Document
from docx.shared import Inches,Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pymupdf as fitz

OUT=Path('deliverables/chapter01');OUT.mkdir(exist_ok=True)
for name,file in [('SS','Regular'),('SSB','Bold'),('SSI','Italic')]:
 pdfmetrics.registerFont(TTFont(name,f'assets/fonts/SourceSerif4-{file}.ttf'))
pdfmetrics.registerFontFamily('SS',normal='SS',bold='SSB',italic='SSI',boldItalic='SSB')
NAVY=HexColor('#193c4b');TEAL=HexColor('#216b72');LIGHT=HexColor('#edf4f4');GREY=HexColor('#46565c')
W,H=504,720;WIDTH=393
styles={
 'body':ParagraphStyle('body',fontName='SS',fontSize=11,leading=14.2,spaceAfter=7,allowWidows=0,allowOrphans=0),
 'title':ParagraphStyle('title',fontName='SSB',fontSize=25,leading=29,spaceBefore=14,spaceAfter=15,textColor=NAVY,keepWithNext=True),
 'h1':ParagraphStyle('h1',fontName='SSB',fontSize=16,leading=20,spaceBefore=15,spaceAfter=9,textColor=NAVY,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='SSB',fontSize=13,leading=16.5,spaceBefore=13,spaceAfter=7,textColor=NAVY,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SSB',fontSize=11.5,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='SS',fontSize=9,leading=11.6,spaceAfter=6,allowWidows=0,allowOrphans=0),
 'cell':ParagraphStyle('cell',fontName='SS',fontSize=9,leading=11.3),
 'cellhead':ParagraphStyle('cellhead',fontName='SSB',fontSize=9,leading=11.3,textColor=white),
 'caption':ParagraphStyle('caption',fontName='SSB',fontSize=10,leading=13,spaceBefore=9,spaceAfter=7,keepWithNext=True),
 'item':ParagraphStyle('item',fontName='SS',fontSize=11,leading=14.2,leftIndent=12,firstLineIndent=-10,spaceAfter=6,allowWidows=0,allowOrphans=0),
 'reference':ParagraphStyle('reference',fontName='SS',fontSize=10,leading=12,leftIndent=14,firstLineIndent=-14,spaceAfter=5,allowWidows=0,allowOrphans=0),
}
def markup(text):
 text=escape(text);text=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',text)
 return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)

def drawpara(c,text,x,y,w,style):
 p=Paragraph(markup(text),style);_,h=p.wrap(w,1000);p.drawOn(c,x,y-h);return h

class TeachingFigure(Flowable):
 def __init__(self,kind):
  super().__init__();self.kind=kind;self.width=WIDTH;self.height=310 if kind==1 else 365
 def draw(self):
  c=self.canv;w=self.width;h=self.height
  if self.kind==1:
   labels=['1.1 Scope of neuroscience','1.2 Meaning of trauma in biological research','1.3 History of stress science','1.4 Early lesion and behavioural studies','1.5 Rise of psychophysiology','1.6 Development of neuroendocrinology','1.7 Growth of brain imaging','1.8 Translation from laboratory to clinic','1.9 Limits of biological reductionism','1.10 Integrative contemporary models']
   for i,label in enumerate(labels):
    x=(w/2+5)*(i%2);y=h-(i//2)*49
    c.setFillColor(LIGHT);c.roundRect(x,y-43,w/2-5,43,4,fill=1,stroke=0)
    drawpara(c,label,x+9,y-8,w/2-23,styles['small'])
   drawpara(c,'Shared interpretative framework',0,52,w,styles['caption'])
   drawpara(c,'Define the question • Examine evidence • Consider alternatives • Apply proportionately • Review',0,30,w,styles['small'])
  else:
   steps=[('Define the question and context','Exposure, population, timing, and intended decision'),('Examine the evidence','Biological level, method, measurement, and uncertainty'),('Consider outcomes and alternatives','Symptoms, function, safety, context, and competing explanations'),('Select a proportionate action','Professional scope, resources, responsibilities, and limits'),('Monitor and review','Outcomes, adverse effects, new information, and revision')]
   for i,(head,body) in enumerate(steps):
    y=h-i*73
    c.setFillColor(LIGHT);c.roundRect(0,y-58,w,58,4,fill=1,stroke=0)
    drawpara(c,f'{i+1}  {head}',10,y-8,w-20,styles['caption'])
    drawpara(c,body,10,y-30,w-20,styles['small'])
    if i<4:
     x=w/2;c.setStrokeColor(TEAL);c.line(x,y-60,x,y-70);c.line(x,y-70,x-3,y-66);c.line(x,y-70,x+3,y-66)

class ProofDoc(BaseDocTemplate):
 def __init__(self,path):
  super().__init__(str(path),pagesize=(W,H),title='Advanced Neurobiology of Trauma — Chapter 1 Developmental Proof',author='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA',leftMargin=61,rightMargin=50,topMargin=48,bottomMargin=48)
  self.addPageTemplates([
   PageTemplate(id='Odd',frames=[Frame(61,48,WIDTH,624,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.furniture,autoNextPageTemplate='Even'),
   PageTemplate(id='Even',frames=[Frame(50,48,WIDTH,624,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.furniture,autoNextPageTemplate='Odd')])
 def furniture(self,c,d):
  c.saveState();left=61 if d.page%2 else 50
  c.setFont('SS',8);c.setFillColor(GREY)
  c.drawString(left,H-28,'TRT 903  |  CHAPTER 1  |  DEVELOPMENTAL PROOF')
  c.setStrokeColor(HexColor('#c7d1d4'));c.line(left,H-34,left+WIDTH,H-34)
  c.drawString(left,25,'Not approved for publication · 21 October 2026')
  c.drawRightString(left+WIDTH,25,str(d.page));c.restoreState()
 def afterFlowable(self,flow):
  if isinstance(flow,Paragraph) and hasattr(flow,'outline'):
   level,key,title=flow.outline
   self.canv.bookmarkPage(key)
   self.canv.addOutlineEntry(title,key,level=level,closed=False)
   if not getattr(flow,'tocskip',False):
    self.notify('TOCEntry',(level,title,self.page,key));CAPTURED.append([level,title,self.page])

def heading(text,level,key):
 p=Paragraph(markup(text),styles[{1:'title',2:'h2',3:'h3'}[level]])
 if level in (2,3):p.outline=(level-2,key,text)
 return p

text=Path('manuscript/chapter01.md').read_text()
refs=json.load(open('manuscript/chapter01-verified-references.json'))
tables={x['id']:x for x in json.load(open('manuscript/chapter01-tables.json'))}
story=[];doc=Document();sec=doc.sections[0]
sec.page_width=Inches(7);sec.page_height=Inches(10)
sec.top_margin=sec.bottom_margin=Inches(2/3);sec.left_margin=Inches(.85);sec.right_margin=Inches(.7)
for name in ['Normal','Title','Heading 1','Heading 2','Heading 3']:
 doc.styles[name].font.name='Source Serif 4'
doc.styles['Normal'].font.size=Pt(11)
doc.styles['Normal'].paragraph_format.line_spacing=Pt(14.2)
doc.styles['Normal'].paragraph_format.space_after=Pt(7)
for name,size in [('Title',25),('Heading 1',16),('Heading 2',13),('Heading 3',11.5)]:doc.styles[name].font.size=Pt(size)
header=sec.header.paragraphs[0];header.text='TRT 903  |  CHAPTER 1  |  DEVELOPMENTAL PROOF';header.style='Caption'
footer=sec.footer.paragraphs[0];footer.text='Not approved for publication · '
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
settings=doc.settings.element;update=OxmlElement('w:updateFields');update.set(qn('w:val'),'true');settings.append(update)

def add_doc_para(s,style=None):
 p=doc.add_paragraph(style=style)
 for i,part in enumerate(re.split(r'\*\*(.*?)\*\*',s)):
  
  for j,subpart in enumerate(re.split(r'(?<!\*)\*([^*]+)\*(?!\*)',part)):
   r=p.add_run(subpart);r.bold=bool(i%2);r.italic=bool(j%2)
 return p

def insert_contents():
 story.append(Spacer(1,10));story.append(Paragraph('In this chapter',ParagraphStyle('itch',parent=styles['h2'],keepWithNext=False)))
 if TOC_CACHE.exists():
  _rows=json.loads(TOC_CACHE.read_text())
  _t0=ParagraphStyle('toc0',fontName='SS',fontSize=10.5,leading=13.5)
  _t1=ParagraphStyle('toc1',fontName='SS',fontSize=9.6,leading=12.6)
  _tp=ParagraphStyle('tocpage',fontName='SS',fontSize=9.6,leading=12.6,alignment=2)
  _data=[[Paragraph(markup((' ' if _l else '')+_t),_t0 if _l==0 else _t1),Paragraph(str(_pg),_tp)] for _l,_t,_pg in _rows]
  _tab=Table(_data,colWidths=[WIDTH-26,26],hAlign='LEFT')
  _tab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,-1),'RIGHT'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),2.6),('BOTTOMPADDING',(0,0),(-1,-1),2.6)]))
  story.append(_tab);story.append(PageBreak())
 else:
  toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='SS',fontSize=10,leading=13,spaceBefore=5,rightIndent=20),ParagraphStyle('toc1',fontName='SS',fontSize=9,leading=12,leftIndent=12,rightIndent=20,spaceBefore=2)]
  story.append(toc);story.append(PageBreak())
 doc.add_heading('In this chapter',2)
 p=doc.add_paragraph();field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'TOC \\o "1-2" \\h \\z \\u');p._p.append(field)
 doc.add_paragraph('The PDF contains the generated contents and page numbers. Refresh the contents field in Word after editing.',style='Caption');doc.add_page_break()

SEEN_TITLE=[False]
CAPTURED=[];TOC_CACHE=Path('editorial/chapter01-toc.json')
for idx,block in enumerate(re.split(r'\n\s*\n',text)):
 block=block.strip()
 if not block:continue
 if block.startswith('[FIGURE:'):
  fid=re.search(r'\[FIGURE:([\d.]+)\]',block)[1];kind=int(fid.split('.')[1])
  cap=f'Figure {fid}. '+('Chapter topics and interpretative framework' if kind==1 else 'Evidence-to-practice reasoning')
  note=('Boxes identify the ten main topics in the source outline; their placement does not imply anatomy or causation.' if kind==1 else 'Arrows show an educational decision sequence, not biological causation or a validated clinical algorithm.')+' Original editorial schematic derived from the supplied chapter; no empirical data are plotted.'
  story.extend([Paragraph(cap,styles['caption']),TeachingFigure(kind),Paragraph(note,styles['small']),Spacer(1,8)])
  # Export the same vector diagram and create an embedded Word image.
  from reportlab.pdfgen.canvas import Canvas
  fig=TeachingFigure(kind);asset=OUT/f'Figure_1_{kind}_edited.pdf'
  cv=Canvas(str(asset),pagesize=(WIDTH,fig.height));fig.canv=cv;fig.draw();cv.save()
  d=fitz.open(asset);d[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(str(OUT/f'Figure_1_{kind}_edited.png'));d.close()
  add_doc_para(cap,'Caption');doc.add_picture(str(OUT/f'Figure_1_{kind}_edited.png'),width=Inches(WIDTH/72));add_doc_para(note,'Caption')
 elif block.startswith('[TABLE:'):
  tid=re.search(r'\[TABLE:([\d.]+)\]',block)[1];t=tables[tid];cap=f'Table {tid}. '+t['title']
  story.append(Paragraph(cap,styles['caption']))
  data=[[Paragraph(markup(x),styles['cellhead']) for x in t['columns']]]+[[Paragraph(markup(x),styles['cell']) for x in row] for row in t['rows']]
  table=Table(data,colWidths=[84,99,104,106],repeatRows=1,hAlign='LEFT')
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT]),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,-1),(-1,-1),.6,TEAL)]))
  story.extend([table,Spacer(1,6),Paragraph(t['note'],styles['small'])])
  add_doc_para(cap,'Caption');dt=doc.add_table(rows=1,cols=4);dt.style='Light Shading Accent 1'
  for c,s in zip(dt.rows[0].cells,t['columns']):c.text=s
  trpr=dt.rows[0]._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');trpr.append(repeat)
  for row in t['rows']:
   cells=dt.add_row().cells
   for cell,s in zip(cells,row):cell.text=s
  for row in dt.rows:
   pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
   for c in row.cells:
    for p in c.paragraphs:
     for r in p.runs:r.font.size=Pt(9)
  add_doc_para(t['note'],'Caption')
 elif block=='[BIBLIOGRAPHY]':
  for s in sorted(refs,key=str.casefold):
   story.append(Paragraph(markup(s),styles['reference']));p=add_doc_para(s);p.paragraph_format.left_indent=Pt(14);p.paragraph_format.first_line_indent=Pt(-14)
 else:
  match=re.match(r'^(#{1,3}) (.*)',block,re.S)
  if match:
   level=len(match[1]);s=match[2].replace('\n',' ')
   if level==1:continue  # '# Chapter 1' locator line; chapter title follows as the first ## heading.
   if level==2 and s=='Learning objectives':insert_contents()
   if level==2 and not SEEN_TITLE[0]:
    SEEN_TITLE[0]=True
    _p=Paragraph(markup(s),styles['title']);_p.outline=(0,f'h-{idx}',s);_p.tocskip=True;story.append(_p)
    story.append(Paragraph('Chapter 1',styles['small']));doc.add_heading(s,0);doc.add_paragraph('Chapter 1',style='Caption')
   else:
    story.append(heading(s,level,f'h-{idx}'));doc.add_heading(s,level-1)
  elif all(re.match(r'^(?:- |\d+\. )',x) for x in block.splitlines()):
   for line in block.splitlines():
    is_bullet=line.startswith('- ')
    line=re.sub(r'^- ','',line)
    if is_bullet:
     st=ParagraphStyle('bullet',parent=styles['item'],firstLineIndent=0,bulletIndent=0,bulletFontName='SS',bulletFontSize=11)
     story.append(Paragraph(markup(line),st,bulletText='•'));add_doc_para('• '+line)
    else:
     story.append(Paragraph(markup(line),styles['item']));add_doc_para(line)
  else:
   s=' '.join(block.splitlines());story.append(Paragraph(markup(s),styles['body']));add_doc_para(s)

pdf=OUT/'Chapter_01_Developmental_Proof.pdf'
ProofDoc(pdf).multiBuild(story)
TOC_CACHE.write_text(json.dumps(CAPTURED,indent=2))
doc.save(OUT/'Chapter_01_Edited_Manuscript.docx')
# Deliver the readable text with actual references and table data separately.
readable=text.replace('[BIBLIOGRAPHY]','\n\n'.join(sorted(refs,key=str.casefold)))
(OUT/'Chapter_01_Edited_Manuscript.md').write_text(readable)
print('Created',pdf)
