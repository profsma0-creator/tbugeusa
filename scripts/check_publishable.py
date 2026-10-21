"""QC for the publishable final PDF (covers + final-edition interior)."""
from pathlib import Path
import json
import pymupdf as fitz

fin = fitz.open('deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Publishable_Final.pdf')
src = fitz.open('deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Final_Edition.pdf')
pm = json.loads(Path('deliverables/final/page-map.json').read_text())
F = pm['front_matter_pages']

checks = {}
checks['total_pages'] = len(fin)
checks['expected_pages_interior_plus_2_covers'] = (len(fin) == len(src) + 2)
checks['uniform_7_by_10_inch_trim'] = all(abs(p.rect.width - 504) < .1 and abs(p.rect.height - 720) < .1 for p in fin)
checks['front_cover_is_full_page_image'] = len(fin[0].get_images(full=True)) >= 1
img = fin[0].get_images(full=True)[0]
pix = fitz.Pixmap(fin, img[0])
checks['front_cover_image_pixels'] = [pix.width, pix.height]
checks['front_cover_label'] = fin[0].get_label()
checks['interior_still_starts_at_i'] = fin[1].get_label() == 'i'
checks['chapter1_still_page_1'] = fin[1 + F].get_label() == '1'
checks['back_cover_label'] = fin[-1].get_label()

# Interior text must be byte-identical page-by-page (covers only added).
mismatch = [i + 1 for i in range(len(src)) if fin[i + 1].get_text() != src[i].get_text()]
checks['interior_text_identical_to_final_edition'] = (mismatch == [])
checks['interior_mismatch_pages'] = mismatch[:5]

nav = fin.get_toc()
checks['bookmarks'] = len(nav)
checks['cover_bookmarks'] = [nav[0][1], nav[-1][1]]
ch_mismatch = []
for lvl, title, pg in nav:
    if title.startswith('Chapter '):
        n = int(title.split()[1].rstrip('.'))
        if pg != 1 + F + pm['chapters'][str(n)]:
            ch_mismatch.append(title)
checks['chapter_bookmarks_on_mapped_folios'] = (ch_mismatch == [])

joined = '\n'.join(p.get_text() for p in fin)
checks['no_proof_or_review_labels'] = not any(
    x in joined for x in ['NOT FINAL', 'Not approved', 'INTEGRATED REVIEW PROOF', 'DEVELOPMENTAL PROOF'])
checks['corporate_author_metadata'] = fin.metadata.get('author') == 'TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA'
checks['back_cover_has_no_fabricated_isbn'] = 'ISBN' not in fin[-1].get_text()

Path('deliverables/final/publishable-quality-checks.json').write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
for k in ['expected_pages_interior_plus_2_covers', 'uniform_7_by_10_inch_trim', 'front_cover_is_full_page_image',
          'interior_still_starts_at_i', 'chapter1_still_page_1', 'interior_text_identical_to_final_edition',
          'chapter_bookmarks_on_mapped_folios', 'no_proof_or_review_labels', 'corporate_author_metadata',
          'back_cover_has_no_fabricated_isbn']:
    assert checks[k], k
print('Publishable edition checks: ALL PASS')
