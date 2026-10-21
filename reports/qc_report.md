# Quality-Control Report

**Book:** *Advanced Assessment and Diagnosis: A Doctoral-Level Textbook in Counselling Psychology* (CPY 903)
**File:** `output/CPY903_Advanced_Assessment_and_Diagnosis.pdf`
**Extent:** 359 pages — front matter i–xxiv, body 1–308, references 309–314, glossary 315–320, appendices 321–330, about the author 331, index 333–335
**Body text:** 74,448 words
**Date of this pass:** 21 October 2026

---

## 1. Verdict

The interior file is structurally correct, typographically consistent and free of unresolved production errors. It is **not yet final**, because five author/publisher placeholders remain on the page (see §6) and because the text itself is an editorial rebuild that the author has not yet approved.

Everything in §2–§5 was checked mechanically against the built PDF, not against the source files, so the checks describe the book a reader will actually hold.

---

## 2. Checks performed and results

| # | Check | Method | Result |
|---|---|---|---|
| 1 | Contents matches the headings | Every contents entry re-read from the final PDF and compared with the page it names | All 327 entries correct; every heading in the book appears in the contents, and no entry points to an empty page |
| 2 | Chapter, part and back-matter openers fall on recto pages | Page number recorded for all 28 openers at build time and re-verified in the final file | 28/28 on recto; 0 on verso |
| 3 | Intentional blank pages carry no folio, no running head and no text | Text layer extracted for every page | 15 blank pages, all empty, each caused by an opener that would otherwise have fallen on a verso |
| 4 | Roman front-matter folios | Contents entries compared with the printed folios | Correct (i–xxiv) and continuous |
| 5 | Arabic body folios | Every page checked for head and folio presence outside chapter openers | Continuous 1–308, then 309–335 across the back matter |
| 6 | Index accuracy | For all 79 headwords, every cited page opened and searched for the term | 79 headwords, 0 incorrect page references |
| 7 | Index scope | Checked that no back-matter page is cited | Index cites body pages only (highest folio cited: 304) |
| 8 | List of Figures / List of Tables | Every listed page opened and checked that the figure or table is on it | 17 figures and 10 tables listed; 0 mismatches |
| 9 | Figures and tables referred to in the text | Each float's label searched in the chapter text | 27/27 referred to; 21 cross-reference sentences were added in this pass and merged into the paragraph that introduces each exhibit |
| 10 | Figure and table numbering | Sequence checked within each chapter | Continuous per chapter (1.1–16.1; 1.1–8.1); no duplicates, no gaps |
| 11 | Running heads | Every body page inspected | Correct verso/recto heads; suppressed on chapter openers and blanks |
| 12 | Widows and orphans | Paragraph-level settings plus a scan for headings stranded at a page foot | Widow/orphan control is on; 0 stranded headings after the conditional breaks were raised |
| 13 | Fonts | Font resources enumerated on every page | Exactly six embedded faces: EB Garamond Regular, Italic, Medium, SemiBold and Source Serif 4 Italic, SemiBold. No base-14 font is referenced |
| 14 | Placeholders | Pattern search of the whole text (`[…]`, TBD, XXX, lorem, INSERT, "to be supplied/confirmed/assigned") | 5 live placeholders, all intentional and listed in §6; no hidden ones |
| 15 | Faith-based material | Whole-text search for devotional vocabulary and manual reading of every religious passage | None. The 7 religious passages are academic and neutral (see `substantive_issues.md` §3) |
| 16 | Spelling convention | Variant counts across the body | British English throughout: 259 *-ise/-isation* forms; the only *-ize/-ization* forms are inside quoted reference titles or the name "World Health Organization"; *judgement* 57, *judgment* 0; *colour/behaviour* consistent; *behaviour* is the only spelling used outside instrument names |
| 17 | Repetition | Sentence-level comparison of the built text | No repeated sentence; no recycled paragraph; no duplicated reference entry |
| 18 | References | 67 entries parsed; duplicates and format checked; each checked against the text and the Further Reading lists | 67 unique entries, APA 7, no duplicates; 63 cited in the text, 4 listed only in Further Reading; no entry lacks an author, year or title |
| 19 | Cross-references | Every "Chapter N" and "Section N.N" reference followed | All resolve to an existing chapter or section; no orphan references |
| 20 | Tables | Every table inspected for header repetition on continuation, column balance and hyphenation | 10/10 break with repeating headers where they split; no table exceeds the measure; no fragmented data |
| 21 | Convergence of pagination | Contents, lists and index regenerated after every text change until stable | Build converged in 2 passes after the final edit; the file shipped is the converged build |

---

## 3. Typography and page design

| Element | Specification |
|---|---|
| Trim | 152 × 229 mm (6 × 9 in), portrait |
| Margins | top 20.5 mm, bottom 21.9 mm, inner 23.3 mm, outer 18.3 mm; text measure 111 mm |
| Body | EB Garamond 11/15.2 pt, justified, first line indented 5 mm, hyphenation en-GB with a 4-letter minimum |
| Chapter number | EB Garamond Medium 9.6 pt, letter-spaced, accent colour |
| Chapter title | Source Serif 4 SemiBold 21.5/25.5 pt, unjustified, no hyphenation |
| Section heading (H1) | Source Serif 4 SemiBold 13.6/16.6 pt, no hyphenation |
| Subheading (H2) | Source Serif 4 SemiBold 11/14.6 pt |
| Reference entries | 9.6/12.4 pt with a true APA hanging indent (16 pt) |
| Glossary | 9.7/12.9 pt, justified, term in bold |
| Tables | 9 pt cells, 8.8 pt headers, left-aligned, no hyphenation, rules above/below the header and at the foot |
| Captions | 8.8/11.4 pt, left-aligned, no hyphenation |
| Running heads | 7.1 pt letter-spaced small caps effect, verso title / recto chapter, suppressed on openers |
| Folios | centred at the foot, 9.5 pt |

Chapter openers carry the chapter number, title, rule, a learning-objectives panel and the key terms, and alone occupy the first page of the chapter. Part titles are display pages in the same display face.

---

## 4. Editorial checks specific to this manuscript

- **Article and agreement errors** of the source type ("a employee", "a acute") do not occur in the built text. Every "a" before a vowel letter was checked individually and is correct by sound (*a useful*, *a university*, *a unidimensional*, *a euthymic*).
- **Numbering** runs CHAPTER 1–16, sections N.1–N.12, figures N.1–N.2, tables N.1–N.2 without a gap or a duplicate.
- **Terminology** is stable: *assessment* and *testing* are distinguished in Chapter 1 and used consistently thereafter; *diagnosis*, *formulation*, *case conceptualisation* and *treatment plan* carry the glossary senses throughout; *client* is used except where a medical setting is quoted.
- **Tone**: no rhetorical questions in body prose (the only question marks are in Review and Discussion Questions), no devotional or promotional language, no second-person address outside the instructional "How to Use This Book".
- **Paragraphing**: no paragraph exceeds 200 words. A residue of short single-sentence paragraphs remains, principally topic statements opening a section and one-line items inside panels; none was left as a fragment of a longer argument.
- **Worked examples**: the two numerical illustrations (predictive values in Chapter 1 and Figure 3.2; the confidence interval in Chapter 3) were recomputed and are arithmetically correct.

---

## 5. Production state of the file

- Single PDF, 0.73 MB, produced with embedded subset fonts and compressed streams; no external references, no JavaScript, no transparency artefacts.
- Bookmarks: a two-level outline (parts, chapters and front/back-matter sections at level 1; numbered sections at level 2) matches the contents.
- Document properties: title, author, subject, creator and keywords are set; the author field carries the corporate author, Triune Biblical University Global Extension, USA, and no metadata field contains a placeholder.
- PDF is searchable and text-selectable throughout; the index and contents folios are live text, not images.

---

## 6. Outstanding items before the file is final

| Item | Where | Owner |
|---|---|---|
| Copyright year and rights holder | copyright page (p. 3) | Publisher |
| ISBN | copyright page (p. 3) | Publisher |
| Institutional note on the corporate author | About the Author, folio 331 (PDF p. 355) | Publisher |
| Month and year of the preface signature (optional) | preface, folio xxi | Publisher |
| Approval of the rebuilt text | whole book | Academic lead |
| Decisions B1–B12 in `author_information_required.md` | front matter and apparatus | Publisher / academic lead |

Until these are closed the file should be described as a **final proof**, not as a final book.

---

## 7. What was not done, and why

- No index entry was created for a term that is not discussed on the cited page; headwords were restricted to the glossary and a curated list of instruments and concepts, and 45-page-wide scatter was excluded as unhelpful.
- No citation was supplied for a claim the source left unsupported; those claims are listed for the author in `substantive_issues.md` §5.
- No permission research was undertaken for DSM-5-TR or ICD-11 material; the copyright page carries the attribution and the publisher must confirm the permissions position.
- No cover, jacket copy or CIP data was produced; these are outside the interior file.
