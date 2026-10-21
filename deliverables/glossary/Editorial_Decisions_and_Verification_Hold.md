# Glossary reconstruction: decisions and verification hold

21 October 2026 · Developmental proof · NOT FINAL

## Scope and result

The source glossary occupies original PDF pages 1680–1703. All **187 headwords** are retained. **182 generic definitions** are replaced with term-specific working definitions; the five substantive originals (Biomarker, Neuroscience, Plasticity, Resilience and Traumatic Stress) are retained or clarified. This is authorised substantive reconstruction, not a claim that these definitions were already in the source.

The reconstruction is 19 pages including its supporting-source notes. It replaces 24 facsimile source pages in integrated proof 03. The full-book proof now contains **1,652 physical pages: six Roman-numbered front-matter pages and 1,646 Arabic-numbered main-matter pages**. The glossary begins at Arabic page 1606; acronyms begin at 1625; worksheets begin at 1630.

## Evidence boundaries

- **59 entries:** the core concept has been checked against a named supporting resource. This does **not** mean that every qualification has passed a separate claim-level check. Source access varies between page sections, institutional explanations and search excerpts; the exact limits are recorded.
- **128 entries:** newly written conventional working definitions, not yet term-specifically source-checked. They are uncoded in the proof and individually identified in the CSV/JSON register. They must not be described as verified scholarly reconstruction or approved for final publication.
- All 187 entries still need specialist review, comparison with each occurrence in the chapters, and independent proofreading. No new experiment, patient finding, numerical result, causal finding or research reference has been invented.
- Source labels are local glossary cross-references, not additions silently assigned to the original comprehensive bibliography. Full reference integration and APA consistency remain outstanding. Dates not confirmed are shown as n.d.; this is not an assertion that the resource is undated.

## Consequential editorial decisions

1. Corrected acronym capitalisation: ACTH, BOLD, DNA, EEG, fMRI, GABA, MEG, MRI, PET and PTSD. Standardised the other headwords to sentence case and British spelling.
2. Distinguished common sources of confusion: biomarkers versus diagnostic tests; predictive versus prognostic markers; reliability versus validity; correlation versus causation; mediation versus established mechanisms; and training versus independent test data.
3. Retained multiple meanings where context is indispensable: Calibration, Discrimination, Generalisation, Nucleus, Neuromodulation, State dependence, Suppression, Transcription, Translation and Validation. These entries must be reconciled with chapter usage before final release rather than choosing an undocumented meaning.
4. Avoided treating complex trauma as interchangeable with complex PTSD, or symptoms as sufficient diagnostic criteria. No checklist purporting to combine DSM and ICD requirements has been supplied.
5. Added explicit limits against common overinterpretations of BOLD, diffusion measures, polygenic scores, heritability, reconsolidation and individualised prediction. These qualifications remain subject to the same verification hold as their entries.
6. Preserved the author's substantive resilience definition. Clarified that plasticity need not be beneficial and that traumatic stress responses are not automatically PTSD; these changes are visible in the before/after register.

## Files and reproducibility

- `Glossary_Developmental_Proof.pdf`: reader-facing developmental proof.
- `Glossary_Edited_Manuscript.docx` and `.md`: editable text. The DOCX specifies Source Serif 4 but does not embed the font.
- `Glossary_Change_and_Verification_Register.csv`: each original definition, replacement, original PDF location, supporting-source codes and verification status.
- `glossary-entries.json` and `glossary-sources.json`: machine-readable entry and access records.
- `quality-checks.json`: bounded production checks, not scholarly certification.

Rebuild with `.venv/bin/python scripts/build_glossary.py`, followed by the integrated builder and checker. The builder asserts exact preservation of the normalised headword sequence, 187 unique definitions, valid source-code links and successful PDF extraction of every definition.

Representative first, middle and supporting-source pages were visually inspected. That inspection is not the independent specialist proofreading pass requested for the final book.

**Release: HOLD.** No author information is needed merely to replace these generic entries. The remaining questions concern editorial and scholarly verification; they are not missing patient data or a request for the author to fabricate material.
