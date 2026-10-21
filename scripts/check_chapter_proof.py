"""Deterministic QC of a bounded proof. Does not verify scientific accuracy."""
from pathlib import Path
import json,re,collections
import pymupdf as fitz
from docx import Document

folder=Path('deliverables/chapter01')
pdf=fitz.open(folder/'Chapter_01_Developmental_Proof.pdf')
text='\n'.join(p.get_text() for p in pdf)
checks={};issues=[]
checks['page_count']=len(pdf)
checks['two_vector_figures_present']=all(f'Figure 1.{i}.' in text for i in (1,2))
checks['two_tables_present']=all(f'Table 1.{i}.' in text for i in (1,2))
checks['no_internal_assembly_tokens']=not any(x in text for x in ['[FIGURE:','[TABLE:','[BIBLIOGRAPHY]','[VISUAL PLACEHOLDER]'])
checks['corporate_author_present']='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA' in text
checks['all_pages_labelled_not_approved']=all('Not approved for publication' in p.get_text() for p in pdf)
checks['outline_present']=len(pdf.get_toc())>20
checks['contents_links_present']=sum(len(p.get_links()) for p in pdf)>20
checks['no_out_of_page_text']=True
fonts=set()
for i,p in enumerate(pdf):
 for b in p.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for s in l['spans']:
    if not s['text'].strip():continue
    fonts.add(s['font'])
    x0,y0,x1,y1=s['bbox']
    if x0<-.5 or y0<-.5 or x1>p.rect.width+.5 or y1>p.rect.height+.5:
     checks['no_out_of_page_text']=False;issues.append({'page':i+1,'text':s['text'],'bbox':s['bbox']})
checks['actual_text_fonts']=sorted(fonts)
checks['all_actual_text_uses_source_serif']=all('SourceSerif4' in x for x in fonts)
embedded=set()
for p in pdf:
 for font in p.get_fonts():
  xref=font[0]
  try:
   name,ext,typ,data=pdf.extract_font(xref)
   if data:embedded.add(font[3].split('+')[-1])
  except Exception:pass
checks['all_used_font_faces_embedded']=all(f in embedded for f in fonts)

refs=json.load(open('manuscript/chapter01-verified-references.json'))
def norm(s):return re.sub(r'\W+','',s,flags=re.UNICODE).casefold()
body_text='\n'.join('\n'.join(line for line in page.get_text().splitlines() if not line.startswith(('TRT 903  |', 'Not approved for publication')) and not re.fullmatch(r'\d+',line.strip())) for page in pdf)
normal=norm(body_text)
checks['seven_reconstruction_references_rendered']=len(refs)==7 and all(norm(r) in normal for r in refs)
checks['twenty_original_reference_entries_archived']=len(json.load(open('manuscript/chapter01-source-bibliography.json')))==20
# Compare every prose/list/heading block with rendered text, excluding layout instructions.
source=Path('manuscript/chapter01.md').read_text();missing=[]
for block in re.split(r'\n\s*\n',source):
 if block.startswith('['):continue
 for line in block.splitlines() if all(re.match(r'^(?:- |\d+\. )',l) for l in block.splitlines()) else [' '.join(block.splitlines())]:
  line=re.sub(r'^#{1,3} ','',line);line=re.sub(r'^- ','',line).replace('**','')
  if line and norm(line) not in normal:missing.append(line)
checks['edited_prose_coverage']=not missing
checks['missing_prose_blocks']=missing
word=Document(folder/'Chapter_01_Edited_Manuscript.docx')
checks['docx_has_two_tables']=len(word.tables)==2
checks['docx_has_two_figures']=len(word.inline_shapes)==2
checks['source_bibliography_entries']=len(refs)
checks['visual_layout_inspection']='Representative title, contents, table and figure pages inspected; not a complete independent proofread.'
checks['scientific_accuracy_verified']=False
checks['selective_source_verification']='Seven records checked with bounded support documented in Source_Verification_Register.md; not a full chapter or whole-book evidence audit.'
checks['full_book_edited']=False
checks['release_status']='HOLD — selective reconstruction checked; remaining manuscript and independent subject review outstanding'
checks['layout_issues']=issues
(folder/'quality-checks.json').write_text(json.dumps(checks,indent=2))
required=['two_vector_figures_present','two_tables_present','no_internal_assembly_tokens','corporate_author_present','all_pages_labelled_not_approved','outline_present','contents_links_present','no_out_of_page_text','all_actual_text_uses_source_serif','all_used_font_faces_embedded','seven_reconstruction_references_rendered','edited_prose_coverage','docx_has_two_tables','docx_has_two_figures']
failed=[k for k in required if not checks[k]]
print(json.dumps(checks,indent=2))
if failed:raise SystemExit('FAILED: '+', '.join(failed))
