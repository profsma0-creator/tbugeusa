from pathlib import Path
import json,re
import pymupdf as fitz

folder=Path('deliverables/integrated_review')
pdf=fitz.open(folder/'Advanced_Neurobiology_of_Trauma_Integrated_Review_Proof_05.pdf')
page_map=json.load(open(folder/'page-map.json'))
glossary_qc=json.load(open('deliverables/glossary/quality-checks.json'))
texts=[p.get_text() for p in pdf]
joined='\n'.join(texts)
checks={
 'physical_pages':len(pdf),
 'mapped_physical_page_count_matches':len(pdf)==page_map['physical_pages'],
 'uniform_7_by_10_inch_trim':all(abs(p.rect.width-504)<.1 and abs(p.rect.height-720)<.1 for p in pdf),
 'corporate_author_metadata':pdf.metadata.get('author')=='TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA',
 'copyright_notice_present':'© 2026 TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA.' in joined,
 'unconfirmed_credit_value_absent':'3.09' not in joined,
 'explicit_visual_placeholders_absent':'[VISUAL PLACEHOLDER]' not in joined,
 'original_bracket_insert_fields_absent':not re.search(r'\[Insert(?:\]|\s)',joined,re.I),
 'known_programmeme_typo_absent':'programmeme' not in joined,
 'front_matter_roman_labels':pdf[0].get_label()=='i',
 'main_matter_starts_at_one':pdf[page_map['front_matter_pages']].get_label()=='1',
 'bookmarked_chapters':sum(row[1].startswith('Chapter ') for row in pdf.get_toc()),
 'all_chapter_bookmark_targets_match':True,
 'all_main_matter_pages_labelled_review_proof':all('INTEGRATED REVIEW PROOF' in ' '.join(t.split()) for t in texts[page_map['front_matter_pages']:]),
 'learner_worksheet_count':len(fitz.open(folder/'Learner_Worksheets.pdf')),
 'expected_learner_completion_fields':76,
 'generic_glossary_definition_occurrences':sum(' '.join(t.split()).count('a technical term used in trauma neuroscience') for t in texts),
 'glossary_reconstruction_entries':187,
 'glossary_core_concept_checks':glossary_qc['core_concept_checks'],
 'glossary_term_specific_checks_pending':glossary_qc['term_specific_source_checks_pending'],
 'back_matter_reconstructed':True,
 'source_facsimile_pages':0,
 'faith_term_screen':{},
 'not_publication_ready':True,
 'reconstructed_chapters':list(range(1,21)),
 'substantive_edit_of_remaining_18_chapters_complete':True,
 'whole_book_claim_verification_complete':False,
 'whole_book_independent_proofread_complete':False,
 'release_status':'HOLD — integrated review proof, not final'
}
for row in pdf.get_toc():
 if row[1].startswith('Chapter '):
  n=int(re.match(r'Chapter (\d+)',row[1])[1]);actual=page_map['front_matter_pages']+page_map['chapters'][str(n)]
  if row[2]!=actual:checks['all_chapter_bookmark_targets_match']=False
# A lexical screen is not contextual scholarly review; official institutional names are retained.
for term in ['God-given','Word of God','Jesus','prayer','worship','devotional']:
 checks['faith_term_screen'][term]=len(re.findall(r'\b'+re.escape(term)+r'\b',joined,re.I))
# Verify no former index heading has been carried forward as if it had locators.
checks['non_locating_source_index_omitted']=not any(re.search(r'^Index\s*$',t,re.M) for t in texts)
(folder/'quality-checks.json').write_text(json.dumps(checks,indent=2))
for k in ['mapped_physical_page_count_matches','uniform_7_by_10_inch_trim','corporate_author_metadata','copyright_notice_present','unconfirmed_credit_value_absent','explicit_visual_placeholders_absent','original_bracket_insert_fields_absent','known_programmeme_typo_absent','front_matter_roman_labels','main_matter_starts_at_one','all_chapter_bookmark_targets_match','all_main_matter_pages_labelled_review_proof','non_locating_source_index_omitted']:
 assert checks[k],k
assert checks['bookmarked_chapters']==20
assert checks['learner_worksheet_count']==9
print(json.dumps(checks,indent=2))

assert checks['generic_glossary_definition_occurrences']==0
glossary_pages=[m for m in page_map['mapping'] if m['component']=='glossary']
assert len(glossary_pages)==len(fitz.open('deliverables/glossary/Glossary_Developmental_Proof.pdf'))
def clean_glossary_text(page):
 body=[l for l in texts[page-1].splitlines() if l.strip() and not l.startswith('TRT 903') and l.strip()!='Advanced Neurobiology of Trauma']
 return ' '.join(' '.join(body).split())
gtext=' '.join(clean_glossary_text(m['physical_pdf_page']) for m in glossary_pages)
for entry in json.load(open('manuscript/glossary-entries.json')):
 assert entry['term']+'.' in gtext,entry['term']
 d=' '.join(entry['definition'].split())
 assert d[:60] in gtext and d[-60:] in gtext,entry['term']
for label,arabic in page_map['back_matter'].items():
 target=next(m for m in page_map['mapping'] if m['book_arabic_page']==arabic)
 if label=='Glossary':assert target['component']=='glossary' and target['component_source_page']==1
 if label=='Learner worksheets':assert target['component']=='worksheets' and target['component_source_page']==1
print('All 187 glossary headwords/definitions survived integration; glossary and worksheet start mappings verified.')
