import json,re,csv,collections
from pathlib import Path
pages=json.load(open('editorial/source-pages.json'))
def clean(t):
 t=re.sub(r'^TRT 903 \| Advanced Neurobiology of Trauma\s*\n\d+\s*\n','',t)
 return re.sub(r'\s+',' ',t).strip()
texts=[clean(t) for t in pages]
chapters=[]
for i,t in enumerate(pages):
 m=re.search(r'\nChapter (\d+)\s*\n(.+?)(?=Central question:)',t,re.S)
 if m: chapters.append((i+1,int(m[1]),' '.join(m[2].split())))
with open('deliverables/chapter-map.csv','w') as f:
 w=csv.writer(f);w.writerow(['Chapter','Title','Source PDF start page','Source PDF end page'])
 for j,(p,n,t) in enumerate(chapters):w.writerow([n,t,p,chapters[j+1][0]-1 if j+1<len(chapters) else 1678])
rows=[]
for i,t in enumerate(texts):
 for m in re.finditer(r'\[[^\]]{1,250}\]',t):
  exact=m[0]; context=t[max(0,m.start()-200):min(len(t),m.end()+260)]
  visual=exact=='[VISUAL PLACEHOLDER]'
  rows.append([f'P{len(rows)+1:03}',i+1,exact,context,'Unfinished figure' if visual else 'Learner-completion field: provisional classification', 'Supply approved artwork or approve an editorial schematic derived only from existing content; identify sources and permissions.' if visual else 'Confirm that this is an intentionally blank teaching template rather than an incomplete worked example.', 'A caption or art brief cannot substitute for a finished figure.' if visual else 'Avoid filling learner exercises with invented clinical or research data.', 'Numbered figure file, final caption, legend, source/permission statement.' if visual else 'Retain a labelled blank field for learner use; supply data only if a completed example is intended.'])
with open('deliverables/placeholder-register.csv','w') as f:
 w=csv.writer(f);w.writerow(['ID','Source PDF page','Exact placeholder','Surrounding text','Classification','Information or decision required','Why needed','Suggested replacement format']);w.writerows(rows)
# Sentence repetition is a screening signal, not a deletion instruction.
loc=collections.defaultdict(set)
for i,t in enumerate(texts):
 for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])',t):
  if 90<=len(s)<=1800:loc[s].add(i+1)
repeats=sorted(((s,pp) for s,pp in loc.items() if len(pp)>=5),key=lambda x:-len(x[1]))
with open('deliverables/repetition-screen.csv','w') as f:
 w=csv.writer(f);w.writerow(['Exact extracted sentence','Number of source pages','Source PDF pages'])
 for s,pp in repeats:w.writerow([s,len(pp),'; '.join(map(str,sorted(pp)))])
# Functional placeholders not marked with brackets.
with open('deliverables/glossary-query-register.csv','w') as f:
 w=csv.writer(f);w.writerow(['Source PDF page','Term','Exact provisional definition','Required action'])
 for i,t in enumerate(texts):
  for m in re.finditer(r'([A-Za-z][A-Za-z -]+): (a technical term used in trauma neuroscience.*?detailed explanation\.)',t):
   w.writerow([i+1,m[1],m[2],'Replace with a term-specific definition supported by the chapter; request subject-author input if absent.'])
stats={'pdf_pages':len(pages),'raw_extracted_words':sum(len(t.split()) for t in pages),'chapter_openings':chapters,'bracketed_occurrences':len(rows),'visual_placeholders':sum(r[2]=='[VISUAL PLACEHOLDER]' for r in rows),'generic_glossary_phrase_occurrences':sum(t.count('a technical term used in trauma neuroscience') for t in texts),'repeated_sentence_groups_on_5_or_more_pages':len(repeats),'caution_formula_occurrences':sum(t.count('This approach is consistent with the broader methodological caution represented by') for t in texts),'programmeme_occurrences':sum(t.count('programmeme') for t in texts)}
Path('editorial/audit-statistics.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2));print('\nTOP REPEATS')
for s,pp in repeats[:8]:print(len(pp),s[:500])
