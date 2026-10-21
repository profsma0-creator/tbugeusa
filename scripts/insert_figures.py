"""Build source-derived teaching plates and a clearly labelled working PDF.
No empirical data, biological pathways or source citations are generated.
"""
from pathlib import Path
import json,re,csv
import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from xml.sax.saxutils import escape

OUT=Path('deliverables/figure_revision');OUT.mkdir(exist_ok=True)
pages=json.load(open('editorial/source-pages.json'))
stats=json.load(open('editorial/audit-statistics.json'))
chapters={n:(p,title) for p,n,title in stats['chapter_openings']}
contents='\n'.join(pages[30:41])
navy=HexColor('#173e50');teal=HexColor('#176b73');pale=HexColor('#eff5f6');grey=HexColor('#40535b')
W,H=595.32,841.92
style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=15,textColor=navy)
small=ParagraphStyle('small',parent=style,fontSize=9,leading=12,textColor=grey)
title_style=ParagraphStyle('title',fontName='Times-Bold',fontSize=21,leading=25,textColor=navy)
def para(c,text,x,y,w,st=style):
 p=Paragraph(escape(text),st);_,h=p.wrap(w,1000);p.drawOn(c,x,y-h);return h

def sentence_case(s):
 s=s.strip();s=s[0].upper()+s[1:].lower()
 for a in ['GABA','HPA','PTSD','MRI','fMRI','EEG','MEG','PET','AI','DNA']:
  s=re.sub(r'\b'+a.lower()+r'\b',a,s,flags=re.I)
 return s

def plate(n,k,path):
 title=chapters[n][1];items=re.findall(rf'^{n}\.(\d+)\s+([^\n]+)',contents,re.M)
 assert len(items)==10
 c=canvas.Canvas(str(path),pagesize=(W,H));c.setTitle(f'Figure {n}.{k} — {title}')
 c.setAuthor('TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA')
 c.setFillColor(navy);c.rect(0,H-12,W,12,fill=1,stroke=0)
 para(c,f'TRT 903  /  CHAPTER {n}  /  EDITORIAL TEACHING SCHEMATIC',44,H-38,W-88,small)
 caption=f'Figure {n}.{k}. '+('Integrated Concept Map: ' if k==1 else 'Evidence-to-Practice Pathway: ')+title
 h=para(c,caption,44,H-76,W-88,title_style);top=H-76-h-22
 if k==1:
  para(c,'Chapter topics and a reading framework',44,top,W-88);top-=32
  for idx,(num,label) in enumerate(items):
   row=idx//2;col=idx%2;x=44+col*260;y=top-row*66
   c.setFillColor(pale);c.roundRect(x,y-58,247,58,6,fill=1,stroke=0)
   para(c,f'{n}.{num}  {sentence_case(label)}',x+12,y-12,223)
  bottom=top-5*66-12
  para(c,'Read across levels',44,bottom,W-88)
  para(c,'Neural • endocrine • immune • cognitive • developmental • social',44,bottom-25,W-88)
  para(c,'For each topic: define the construct, examine the method, interpret uncertainty, and consider the decision or application.',44,bottom-54,W-88)
  note='Boxes index the chapter’s existing section headings. Position is for navigation, not anatomical location or causal order. No connecting arrows are used because the outline alone cannot establish biological pathways.'
 else:
  steps=[('1  Define the question and context','Specify the exposure, population, timing, and decision. Distinguish the question from the explanation.'),('2  Specify the process and evidence','Identify the relevant biological level and the method used to study it. Separate observation from inference.'),('3  Assess outcomes and alternatives','Consider symptoms, function, safety, context, and competing explanations. Group findings do not determine an individual diagnosis.'),('4  Select a proportionate action','Relate evidence to assessment, education, supervised practice, or research. Record limits and responsibilities.'),('5  Monitor and review','Review outcomes, uncertainty, adverse effects, and new information. Revise the interpretation when warranted.')]
  for j,(head,body) in enumerate(steps):
   y=top-j*91
   c.setFillColor(pale);c.roundRect(44,y-75,W-88,75,6,fill=1,stroke=0)
   para(c,head,57,y-10,W-114)
   para(c,body,57,y-32,W-114,small)
   if j<4:
    c.setStrokeColor(teal);c.setLineWidth(1.2);x=W/2
    c.line(x,y-77,x,y-88);c.line(x,y-88,x-3,y-84);c.line(x,y-88,x+3,y-84)
  note='Arrows show an educational decision sequence, not biological causation or a validated clinical algorithm. Apply this framework to the chapter topics; it does not prescribe treatment or establish diagnostic accuracy.'
 para(c,note,44,194,W-88,small)
 para(c,f'Source: Chapter {n}, section outline and existing discussion of evidence, interpretation, application, and review. Original editorial schematic; no empirical data are plotted. Subject-author review remains required.',44,133,W-88,small)
 c.setStrokeColor(teal);c.line(44,62,W-44,62)
 para(c,f'WORKING MANUSCRIPT  •  Plate {n}.{k}  •  Not a final page proof',44,49,W-88,small)
 c.save()

source=fitz.open('/tmp/arena-coding-uploads/TRT_903_Advanced_Neurobiology_of_Trauma_Complete_Textbook.pdf')
# Explicit author role is added without assigning copyright ownership.
source[18].insert_textbox(fitz.Rect(120,409,478,457),'Author\nTRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA',fontname='hebo',fontsize=10,align=1,color=(.09,.24,.31))
source[2].insert_textbox(fitz.Rect(90,350,505,410),'Author\nTRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA',fontname='hebo',fontsize=11,align=1,color=(.09,.24,.31))
insertions={};log=[]
for i,text in enumerate(pages):
 if '[VISUAL PLACEHOLDER]' not in text:continue
 matches=list(re.finditer(r'Figure\s+(\d+)\.(\d+)\.',text))
 # Captions occur on the same source page as every explicit placeholder.
 targets=source[i].search_for('[VISUAL PLACEHOLDER]')
 assert len(matches)==len(targets),(i,len(matches),len(targets))
 for match,rect in zip(matches,targets):
  n,k=map(int,match.groups());path=OUT/f'Figure_{n:02}_{k}.pdf';plate(n,k,path)
  insertions.setdefault(i,[]).append(path)
  source[i].add_redact_annot(rect,fill=(1,1,1))
  log.append({'figure':f'{n}.{k}','source_pdf_page':i+1,'asset':path.name,'kind':'Chapter topic map' if k==1 else 'Educational decision framework','status':'Created and inserted; subject-author review pending'})
 source[i].apply_redactions(images=0,graphics=0)
 for match,rect in zip(matches,targets):
  n,k=map(int,match.groups())
  source[i].insert_text((rect.x0,rect.y1-3),f'See inserted teaching plate {n}.{k} immediately after this source page.',fontname='helv',fontsize=9,color=(.09,.24,.31))

out=fitz.open();nav=[]
for i in range(len(source)):
 out.insert_pdf(source,from_page=i,to_page=i)
 for path in insertions.get(i,[]):
  p=fitz.open(path);out.insert_pdf(p);p.close()
  fig=re.search(r'Figure_(\d+)_(\d+)',path.name);n,k=map(int,fig.groups())
  next(r for r in log if r['figure']==f'{n}.{k}')['working_pdf_page']=len(out)
  nav.append([2,f'Figure {n}.{k}',len(out)])
# Retain source folios, add a discreet digital-draft status, and use real PDF page labels.
labels=[]
plate_pages={r['working_pdf_page']-1:r['figure'] for r in log}
srcnum=0
for i,page in enumerate(out):
 if i in plate_pages:labels.append({'startpage':i,'prefix':f'Plate {plate_pages[i]}','style':''})
 else:
  srcnum+=1;labels.append({'startpage':i,'prefix':'Source ','style':'D','firstpagenum':srcnum})
  page.insert_text((36,23),'WORKING FIGURE REVISION — NOT FINAL',fontsize=7,fontname='helv',color=(.35,.35,.35))
out.set_page_labels(labels)
out.set_metadata({'title':'Advanced Neurobiology of Trauma — Working Figure Revision','author':'TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA','subject':'40 source-derived teaching schematics inserted; wider editorial review outstanding'})
toc=[];offset=0
for p,n,title in stats['chapter_openings']:
 actual=p+sum(len(v) for idx,v in insertions.items() if idx<p-1)
 toc.append([1,f'Chapter {n}: {title}',actual])
 for r in log:
  if r['figure'].split('.')[0]==str(n):toc.append([2,'Figure '+r['figure'],r['working_pdf_page']])
out.set_toc(toc)
output=OUT/'Advanced_Neurobiology_of_Trauma_Working_Figure_Revision.pdf'
out.save(output,garbage=4,deflate=True)
with open(OUT/'figure-revision-log.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(log[0]));w.writeheader();w.writerows(log)
assert len(log)==40 and len(out)==1762
print('Created',len(log),'plates; working PDF pages',len(out))
# Verify all explicit visual tokens were replaced; verify author text and figure labels.
check=fitz.open(output)
assert not any('[VISUAL PLACEHOLDER]' in p.get_text() for p in check)
assert 'Author' in check[18].get_text()
for r in log:
 assert 'Figure '+r['figure']+'.' in check[r['working_pdf_page']-1].get_text()
check[log[2]['working_pdf_page']-1].get_pixmap(matrix=fitz.Matrix(1,1)).save('editorial/figure-preview.png')
print('Checks passed: figure count, placeholder removal, corporate-author label, and plate insertion.')
