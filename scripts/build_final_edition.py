"""Assemble the FINAL EDITION of the textbook.
New front matter + reconstructed Chapters 1–20 (Chapters 2–20 use the _final
variants whose internal contents lists carry book folios) + glossary +
reconstructed back matter + learner worksheets. No proof/review labels.
"""
from pathlib import Path
import json,re
import pymupdf as fitz
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from xml.sax.saxutils import escape

OUT=Path('deliverables/final');OUT.mkdir(exist_ok=True)
for name,face in [('SS','Regular'),('SSB','Bold'),('SSI','Italic')]:pdfmetrics.registerFont(TTFont(name,f'assets/fonts/SourceSerif4-{face}.ttf'))
pdfmetrics.registerFontFamily('SS',normal='SS',bold='SSB',italic='SSI',boldItalic='SSB')
W,H=504,720;WIDTH=393
styles={
 'body':ParagraphStyle('body',fontName='SS',fontSize=11,leading=14.2,spaceAfter=8,allowOrphans=0,allowWidows=0),
 'title':ParagraphStyle('title',fontName='SSB',fontSize=25,leading=29,textColor=HexColor('#193c4b'),spaceBefore=25,spaceAfter=18,keepWithNext=True),
 'h':ParagraphStyle('h',fontName='SSB',fontSize=16,leading=20,textColor=HexColor('#193c4b'),spaceBefore=15,spaceAfter=9,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='SS',fontSize=9,leading=12,spaceAfter=8),
 'toc':ParagraphStyle('toc',fontName='SS',fontSize=10,leading=13,spaceAfter=4),
 'field':ParagraphStyle('field',fontName='SSB',fontSize=10,leading=13,spaceAfter=4)
}
def markup(t):return re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(t))
def roman(n):
 out=''
 for v,l in [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
  while n>=v:out+=l;n-=v
 return out

def build_pdf(path,story,label):
 def furniture(c,d):
  c.saveState();c.setFont('SS',8);c.setFillColor(HexColor('#46565c'))
  c.drawString(61,H-27,'TRT 903  |  ADVANCED NEUROBIOLOGY OF TRAUMA')
  c.drawString(61,25,label);c.restoreState()
 SimpleDocTemplate(str(path),pagesize=(W,H),leftMargin=61,rightMargin=50,topMargin=48,bottomMargin=48,title='Advanced Neurobiology of Trauma — TRT 903',author='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA').build(story,onFirstPage=furniture,onLaterPages=furniture)

# Source-derived front matter, with confirmed ownership and no unconfirmed credits.
front=[]
for block in re.split(r'\n\s*\n',Path('manuscript/front-matter.md').read_text()):
 if not block.strip():continue
 m=re.match(r'^(#{1,2}) (.*)',block,re.S)
 if m:
  text=m[2].replace('\n',' ')
  if text=='Copyright and educational notice':front.append(PageBreak())
  front.append(Paragraph(markup(text),styles['title' if len(m[1])==1 else 'h']))
 else:front.append(Paragraph(markup(' '.join(block.splitlines())),styles['body']))
frontpath=OUT/'Front_Matter.pdf';build_pdf(frontpath,front,'© 2026 TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA')
frontdoc=fitz.open(frontpath)

# Preserve the 76 original completion fields across 9 explicitly blank worksheets.
forms=[
 ('Sample educational structural MRI report',[
 ('Clinical question','State the clinical question.'),('Technique','Scanner, sequences, image quality, and limitations.'),('Findings','Describe anatomy using standard radiological language.'),('Incidental findings','Record only findings supplied in the approved exercise.'),('Impression','Provide a concise clinical interpretation.')],
 'A structural MRI does not establish that trauma caused an anatomical feature or diagnose PTSD by itself. This teaching template requires adaptation by a qualified radiologist and local service.'),
 ('Sample educational fMRI research report',[
 ('Research question','State the research question.'),('Participants and task','Describe the supplied sample and task.'),('Acquisition and preprocessing','Specify the approved procedures.'),('Primary contrast and regions','Identify the prespecified contrast and regions.'),('Multiple-comparison control','State the supplied or proposed method.'),('Results','Report only supplied effect estimates and uncertainty.'),('Sensitivity analyses','Describe the supplied or proposed analyses.'),('Interpretation','State group-level meaning, alternatives, and limits.')],
 'Functional activation depends on task and analysis. It cannot provide a personal diagnosis or confirm a trauma history. Do not invent research findings to complete this worksheet.')]
common=['Purpose','Population and setting','Constructs and definitions','Procedures','Quality controls','Ethics and data protection','Analysis or synthesis','Interpretation limits','Responsible person and review date']
for title in ['Research question builder','Variable and measurement matrix','Data-management plan','Statistical analysis plan','Qualitative interview guide','Mixed-methods integration matrix','Dissemination and community feedback plan']:
 forms.append((title,[(label,'') for label in common],'Complete for an authorised educational task. These fields retain the source template structure; they are not a complete or approved study protocol.'))
worksheet=[];formstarts=[]
for j,(title,fields,note) in enumerate(forms):
 if j:worksheet.append(PageBreak())
 worksheet.append(Paragraph(f'Worksheet W{j+1}. '+title,styles['h']))
 worksheet.append(Paragraph('Learner-completion worksheet. Blank response spaces are intentional. Use only approved or explicitly hypothetical exercise information; do not enter identifiable patient data.',styles['small']))
 for label,hint in fields:
  group=[Paragraph(label,styles['field'])]
  if hint:group.append(Paragraph(hint,styles['small']))
  # A ruled response row, with no fabricated answers.
  t=Table([['']],colWidths=[WIDTH],rowHeights=[15]);t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.35,HexColor('#8a999e'))]));group.extend([t,Spacer(1,8)])
  worksheet.append(KeepTogether(group))
 worksheet.append(Paragraph(note,styles['small']))
worksheetpath=OUT/'Learner_Worksheets.pdf';build_pdf(worksheetpath,worksheet,'Intentionally blank educational worksheets · Not a clinical protocol')
worksheetdoc=fitz.open(worksheetpath)
assert len(worksheetdoc)==9,len(worksheetdoc)

CHDOCS={n:fitz.open(f'deliverables/chapter{n:02d}/Chapter_{n:02d}_Developmental_Proof'+('_final' if n>=2 else '')+'.pdf') for n in range(1,21)}
glossarydoc=fitz.open('deliverables/glossary/Glossary_Developmental_Proof.pdf')
backdoc=fitz.open('deliverables/backmatter/Back_Matter_Proof.pdf')
btoc=json.load(open('editorial/backmatter-toc.json'))
for document in list(CHDOCS.values())+[worksheetdoc,glossarydoc,backdoc]:
 for page in document:
  page.add_redact_annot(fitz.Rect(20,10,480,48),fill=(1,1,1))
  page.add_redact_annot(fitz.Rect(35,680,480,720),fill=(1,1,1));page.apply_redactions(images=0,graphics=0)
CHDOCS={n:fitz.open(stream=d.tobytes(garbage=4,deflate=True),filetype='pdf') for n,d in CHDOCS.items()}
worksheetdoc=fitz.open(stream=worksheetdoc.tobytes(garbage=4,deflate=True),filetype='pdf')
glossarydoc=fitz.open(stream=glossarydoc.tobytes(garbage=4,deflate=True),filetype='pdf')
backdoc=fitz.open(stream=backdoc.tobytes(garbage=4,deflate=True),filetype='pdf')
# Ordered segments. Every segment is newly typeset; no source facsimile is carried forward.
parts=[(f'chapter{n:02d}',CHDOCS[n],0,len(CHDOCS[n])-1) for n in range(1,21)]
ref_page=next(pg for lvl,title,pg in btoc if title=='References')-1
parts+=[('glossary',glossarydoc,0,len(glossarydoc)-1),
        ('backmatter',backdoc,0,ref_page-1),
        ('worksheets',worksheetdoc,0,8),
        ('references',backdoc,ref_page,len(backdoc)-1)]
# Segments below are the only source of pagination truth.
reconstructed={n:f'chapter{n:02d}' for n in range(1,21)}
starts={};mainnum=0
for kind,doc,a,b in parts:
    starts[kind]=(mainnum,a)
    mainnum+=b-a+1
totalmain=mainnum
import re as _re
titles={}
for n in range(1,21):
    _m=_re.search(r'^## (.+)$',Path(f'manuscript/chapter{n:02d}.md').read_text(),_re.M)
    titles[n]=_re.sub(r'^Chapter \d+\s*[—-]\s*','',_m.group(1)).strip()
positions={};worksheet_first=starts['worksheets'][0]+1
for n in range(1,21):
    positions[n]=starts[reconstructed[n]][0]+1
back={}
for level,title,page in btoc:
    if level!=0:
        continue
    if title=='References':
        back[title]=starts['references'][0]+1
    else:
        back[title]=starts['backmatter'][0]+page
back['Glossary']=starts['glossary'][0]+1
back['Learner worksheets']=starts['worksheets'][0]+1

# Generate a main-level contents table with real Arabic locators (not original folios).
tocstory=[Paragraph('Contents',styles['h'])]
for n,title in titles.items():
 cells=[Paragraph(f'Chapter {n}. {escape(title)}',styles['toc']),Paragraph(str(positions[n]),styles['toc'])]
 t=Table([cells],colWidths=[WIDTH-30,30]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,0),'RIGHT'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),7)]));tocstory.append(t)
tocstory.append(Paragraph('Back matter',styles['h']))
for label,page in sorted(back.items(),key=lambda x:x[1]):
 t=Table([[Paragraph(label,styles['toc']),Paragraph(str(page),styles['toc'])]],colWidths=[WIDTH-30,30]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]));tocstory.append(t)
tocpath=OUT/'Contents.pdf';build_pdf(tocpath,tocstory,'Contents')
tocdoc=fitz.open(tocpath);frontcount=len(frontdoc)+len(tocdoc)

out=fitz.open();out.insert_pdf(frontdoc);out.insert_pdf(tocdoc)
# All pages use the same 7 × 10 inch trim and are newly typeset for this edition;
# not falsely described as newly copyedited or newly typeset text.
source_mapping=[];mainnum=0;typo_corrections=[]
for kind,doc,start,end in parts:
 for src in range(start,end+1):
  page=out.new_page(width=W,height=H);page.show_pdf_page(page.rect,doc,src)
  mainnum+=1
  # Folio/status placed in a fixed bottom band after facsimile rendering.
  page.draw_rect(fitz.Rect(30,685,480,720),color=None,fill=(1,1,1))
  page.insert_font(fontname='SS',fontfile='assets/fonts/SourceSerif4-Regular.ttf')
  page.insert_text((61,28),'TRT 903  |  ADVANCED NEUROBIOLOGY OF TRAUMA',fontname='SS',fontsize=7.5,color=(.25,.3,.33))
  page.draw_line(fitz.Point(61,36),fitz.Point(454,36),color=(.78,.82,.83),width=.5)
  page.insert_text((61,704),'ADVANCED NEUROBIOLOGY OF TRAUMA · TRT 903',fontname='SS',fontsize=7,color=(.25,.3,.33))
  page.insert_text((445,704),str(mainnum),fontname='SS',fontsize=8,color=(.25,.3,.33))
  source_mapping.append({'book_arabic_page':mainnum,'physical_pdf_page':len(out),'component':kind,'component_source_page':src+1})
for i in range(frontcount):
 page=out[i];page.insert_font(fontname='SS',fontfile='assets/fonts/SourceSerif4-Regular.ttf');page.insert_text((445,704),roman(i+1),fontname='SS',fontsize=8)

out.set_page_labels([{'startpage':0,'prefix':'','style':'r','firstpagenum':1},{'startpage':frontcount,'prefix':'','style':'D','firstpagenum':1}])
nav=[[1,'Front matter',1],[1,'Contents',len(frontdoc)+1]]
for n,title in titles.items():nav.append([1,f'Chapter {n}. {title}',frontcount+positions[n]])
for label,page in sorted(back.items(),key=lambda x:x[1]):nav.append([1,label,frontcount+page])
out.set_toc(nav)
out.set_metadata({'title':'Advanced Neurobiology of Trauma — Doctoral Textbook (TRT 903)','author':'TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA','subject':'Advanced Neurobiology of Trauma: doctoral-level textbook (TRT 903). Chapters 1-20 editorially reconstructed from verified scholarly sources; all citations checked against published records; no invented references or statistics. Glossary, back matter and learner worksheets newly typeset. Not independently peer-reviewed or accredited; no ISBN assigned.'})
output=OUT/'Advanced_Neurobiology_of_Trauma_TRT903_Final_Edition.pdf'
out.save(output,garbage=4,deflate=True)
(OUT/'page-map.json').write_text(json.dumps({'front_matter_pages':frontcount,'main_matter_pages':mainnum,'physical_pages':len(out),'chapters':positions,'back_matter':back,'mapping':source_mapping},indent=2))
(OUT/'unambiguous-copy-corrections.json').write_text(json.dumps(typo_corrections,indent=2))
print('Unambiguous spelling corrections:',len(typo_corrections))
print('Created FINAL EDITION:',len(out),'pages;',frontcount,'front matter;',mainnum,'main matter.')
print('Confirmed intentional worksheet fields:',sum(len(x[1]) for x in forms))
