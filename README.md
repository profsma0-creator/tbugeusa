# Advanced Neurobiology of Trauma — editorial workspace

## Current status: FINAL EDITION RELEASED

The final edition is:

`deliverables/final/Advanced_Neurobiology_of_Trauma_TRT903_Final_Edition.pdf`

**272 pages (seven Roman + 265 Arabic)**, 7 × 10 in trim, no blank pages, 34 bookmarks. It contains new secular front matter, all twenty chapters reconstructed from verified scholarly sources, seven original vector figures, a 187-entry glossary, fully rewritten back matter (acronyms, four appendices, research resources, teaching protocols, professional standards, annotated further reading), nine learner worksheets (76 completion fields, blank by design), and a consolidated 47-entry APA 7 reference list. There are no proof/review labels and no source-facsimile pages anywhere in the file.

Read `deliverables/final/Final_Edition_Certification_and_QC_Report.md` for the editorial certification, chapter map, QC results and disclosed limitations. `deliverables/integrated_review/Publication_Readiness_Status.md` records how each former release blocker was resolved. Earlier proofs remain for auditability.

## Author decisions confirmed

- Corporate author and 2026 copyright holder: **TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION, USA**.
- Doctoral positioning; retain TRT 903; omit credit hours.
- Reconstruction from verifiable scholarly sources authorised; significant changes documented.
- Blank research/imaging fields are intentional learner-completion worksheets.
- Original figure creation authorised where needed.

See `editorial/author-decisions.json`.

## Disclosed limitations

No independent external peer review, accreditation, or ISBN is claimed (the front matter states this). No index — the source index had no reliable locators. Chapters 3–20 are concise doctoral-level treatments (1,682–2,630 words each) with an annotated Further reading list for depth. Glossary verification depth is recorded in `deliverables/glossary/Glossary_Change_and_Verification_Register.csv`.

## Rebuilding the final edition

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-editorial.txt
# Pass 1: components (run chapter typesetters twice so contents caches converge)
.venv/bin/python scripts/typeset_chapter.py            # Chapter 1 (run twice)
for ch in $(seq 2 20); do .venv/bin/python scripts/typeset_volume_chapter.py $ch 0; done
.venv/bin/python scripts/build_glossary.py
.venv/bin/python scripts/typeset_backmatter.py
.venv/bin/python scripts/build_integrated_proof.py     # fixes the definitive page map
# Pass 2: offset variants so each chapter's internal contents carries book folios
.venv/bin/python - <<'EOF'
import json, subprocess
pm = json.load(open('deliverables/integrated_review/page-map.json'))
for n in range(2, 21):
    subprocess.run(['.venv/bin/python', 'scripts/typeset_volume_chapter.py',
                    str(n), str(pm['chapters'][str(n)] - 1), '_final'], check=True)
EOF
.venv/bin/python scripts/build_final_edition.py
.venv/bin/python scripts/check_final_edition.py
.venv/bin/python scripts/check_chapters.py
```

Editable inputs are in `manuscript/`; fonts (OFL) in `assets/fonts/`; audit material in `editorial/`.
