# Chapter 2: editorial decisions and verification record

## What was found
The source chapter's ten numbered sections (2.1–2.10) contained no description of the structures they named. Each section held eight formulaic passages produced by inserting the section title into a fixed template ("Mechanistic analysis of X ... starts by relating Y to Z"). The chapter contained 80 such passages, drawing on a rotating pool of eight bodies of text, all closing with the identical sentence "This approach is consistent with the broader methodological caution represented by [Author] (Year), although every application requires evidence suited to the population, measure, and decision under study." Nine further sentences recur verbatim in all twenty chapters of the book.

Consequently the source chapter did not explain neuroanatomy at all. It discussed method, ethics and measurement in generic terms, then cited sources without connecting them to any anatomical claim.

## What was done
- All 80 formulaic passages were extracted and archived in `editorial/chapter02-formulaic-passages.json` before reconstruction, so no author text is silently lost.
- Sections 2.1–2.10 were rewritten as continuous anatomical prose: embryology and planes, cortical and subcortical organisation, amygdala, hippocampal formation, prefrontal cortex, insula, anterior cingulate, brainstem and periaqueductal grey, cerebellum, and large-scale networks.
- The author's genuinely distinct material was retained and edited: the professional-practice, ethics, policy, international-perspective, composite-case, worked-example, exercises and research-assignment sections. These were condensed where they repeated across chapters.
- Two figures were drawn for this chapter (levels of analysis; evidence-to-decision sequence) and are labelled as editorial schematics, not empirical data.
- Two tables were built from the chapter's own argument.

## Evidence base
Seventeen references are cited in the text and listed. Each was checked against a publisher, PubMed or PubMed Central record for authorship, year, journal, volume, pages and DOI. Seven principal sources were read in more than bibliographic detail (abstract, key points, or full text where openly available): Arnsten (2009), Craig (2009), Fenster et al. (2018), Menon (2011), Shackman et al. (2011), Stoodley & Schmahmann (2009) and the Duke neuroanatomy laboratory guide used for standard anatomical description. Page-level verification notes are in `editorial/chapter02-source-verification.md`.

## Limits that remain
- This is one editor's reconstruction, not an independent specialist review. A neuroanatomist and a trauma clinician should each read it before publication.
- Anatomical description follows standard sources; no new empirical claim, statistic or patient finding has been introduced.
- The chapter does not attempt a systematic review. Where the literature is heterogeneous, the text says so rather than selecting a convenient finding.
- Chapter-usage reconciliation with the glossary is outstanding.
