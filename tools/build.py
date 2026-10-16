#!/usr/bin/env python3
"""
build.py — assemble and typeset the whole book.

    python3 tools/build.py                 # full build
    python3 tools/build.py --only 1 2 3    # proof: front matter + chosen chapters
    python3 tools/build.py --out book.pdf

Pagination is iterative: the front matter carries a table of contents and a list
of illustrations whose content depends on the layout, and the back matter
carries indexes built from the finished pagination.  The book is therefore laid
out repeatedly until the page record stops changing.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from bookkit import document, figures, indexes, markup, openers, theme as T  # noqa: E402
from bookkit.document import (BlankPage, BodyStart, FolioSuppress,           # noqa: E402
                              HeadSuppress)
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Spacer  # noqa: E402

MANUSCRIPT = ROOT / "manuscript"
CHAPTERS = MANUSCRIPT / "chapters"
PARTS = MANUSCRIPT / "parts"
BACK = MANUSCRIPT / "back"


def load_cfg() -> dict:
    return json.loads((MANUSCRIPT / "book.json").read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def page_start(template: str, *, blank=False, no_head=False, no_folio=False,
               body_start=False) -> list:
    """Begin a new page.

    `NextPageTemplate` is handled while the *current* page is still open, so it
    must be emitted immediately before the page break that starts the new page —
    placing it after the break silently shifts every switch by one page.
    """
    out = []
    out.append(NextPageTemplate(template))
    out.append(PageBreak())
    # everything after the break is processed on the new page
    if body_start:
        out.append(BodyStart())
    if blank:
        out.append(BlankPage())
    else:
        if no_head:
            out.append(HeadSuppress())
        if no_folio:
            out.append(FolioSuppress())
    return out


# ---------------------------------------------------------------------------
# front matter
# ---------------------------------------------------------------------------
def front_matter(cfg, manifest, fig_pages, page_of) -> list:
    f = []
    cover = ROOT / "manuscript" / "cover" / "front-cover.png"
    if cover.exists():
        f += openers.cover_page(cover)

    f += page_start("blank", blank=True)
    f += openers.half_title(cfg["title"])

    f += page_start("blank", blank=True)
    f += openers.title_page(cfg["title"], cfg["subtitle"], cfg["author"],
                            cfg["place"], cfg["year"], cfg["publisher_line"])

    f += page_start("front", no_folio=True, no_head=True)
    f += openers.copyright_page(cfg)

    # dedication
    ded = read(MANUSCRIPT / "00-dedication.md").strip()
    if ded:
        f += page_start("front", no_folio=True, no_head=True)
        f += openers.dedication_page([p.strip() for p in ded.split("\n\n") if p.strip()])
        f += page_start("blank", blank=True)

    # epigraph
    epi = read(MANUSCRIPT / "00-epigraph.md").strip()
    if epi:
        blocks = [b for b in epi.split("\n\n") if b.strip()]
        text = blocks[0].strip()
        src = blocks[1].strip().lstrip("\u2014- ").strip() if len(blocks) > 1 else ""
        f += page_start("front", no_folio=True, no_head=True)
        f += openers.epigraph_page(text, src)
        f += page_start("blank", blank=True)

    # contents
    f += page_start("front", no_head=True)
    f += openers.section_head("Contents")
    f += [Spacer(1, 4)]
    f += [document.BookTOC(lambda: document.BODY_START)]

    # list of illustrations
    if fig_pages:
        f += page_start("front", no_head=True)
        f += [openers.section_head("Illustrations"), Spacer(1, 2)]
        rows = []
        for fid, meta in manifest.items():
            if fid not in fig_pages:
                continue
            pg = fig_pages[fid]
            rows.append((meta.get("label", ""), meta.get("caption", ""),
                         page_of(pg) if pg else ""))
        rows.sort(key=lambda r: (r[0] or "zz"))
        for label, caption, pg in rows:
            f.append(Paragraph(
                f"{label}\u2003{caption}\u2003<span><font color='#B08A2E'>{pg}</font></span>",
                T.STYLES["figlist"]))
            f.append(Spacer(1, 3.2))
    return f


# ---------------------------------------------------------------------------
# body
# ---------------------------------------------------------------------------
def chapter_story(cfg, ch, manifest, only=None) -> list:
    path = CHAPTERS / f"ch{ch['number']:02d}.md"
    body = read(path)
    if not body.strip():
        return []
    out = page_start("body", no_head=True)
    out += openers.chapter_opener(ch["number"], ch["title"], ch["subtitle"],
                                  ch["scriptures"])
    out += markup.parse(body, T.TEXT_W, chapter_no=ch["number"], manifest=manifest,
                        drop_cap=True)
    out += openers.chapter_end()
    return out


def part_front(part, manifest, body_start=False) -> list:
    plate = f"plate-{part['number']:02d}"
    plate = plate if plate in manifest else None
    out = page_start("body", no_head=True, body_start=body_start)
    out += openers.part_page(part["number"], part["title"],
                             part.get("standfirst", ""), plate, manifest)
    essay = read(PARTS / f"part-{part['number']:02d}.md")
    if essay.strip():
        out += page_start("body")
        out += markup.parse(essay, T.TEXT_W, manifest=manifest)
        out += [Spacer(1, 10),
                openers.decor.Ornament(space_before=6, space_after=6)]
    return out


def body_story(cfg, manifest, only=None) -> list:
    out = []
    first = True
    for part in cfg["parts"]:
        chs = part["chapters"]
        if only is not None:
            chs = [c for c in chs if c["number"] in only]
            if not chs:
                continue
        out += part_front(part, manifest, body_start=first)
        first = False
        for ch in chs:
            out += chapter_story(cfg, ch, manifest, only)
    return out


# ---------------------------------------------------------------------------
# back matter
# ---------------------------------------------------------------------------
def back_matter(cfg, manifest, index_data) -> list:
    out = [NextPageTemplate("body")]
    order = read(BACK / "order.txt")
    names = [n.strip() for n in order.splitlines() if n.strip()] if order else []

    titles = {
        "appendix-i": "Appendix I \u00b7 A Biblical Theology of Generational Revelation",
        "appendix-ii": "Appendix II \u00b7 The Generational Transitions of Scripture",
        "appendix-iii": "Appendix III \u00b7 Biblical Profiles of Young People Used by God",
        "appendix-iv": "Appendix IV \u00b7 Biblical Profiles of Fathers and Mentors",
        "appendix-v": "Appendix V \u00b7 Scriptures on Fathers, Sons, Elders and Youth",
        "appendix-vi": "Appendix VI \u00b7 A Framework for Generational Discernment",
        "appendix-vii": "Appendix VII \u00b7 Questions for Fathers, Mentors and Elders",
        "appendix-viii": "Appendix VIII \u00b7 Questions for the Young",
        "bibliography": "Bibliography",
        "about-the-author": "About the Author",
    }
    for name in names:
        path = BACK / f"{name}.md"
        text = read(path)
        if not text.strip():
            continue
        title = titles.get(name, name.replace("-", " ").title())
        out += page_start("body", no_head=True)
        out += openers.section_head(title)
        out += markup.parse(text, T.TEXT_W, manifest=manifest)

    if index_data:
        out += scripture_index(index_data["scripture"])
        out += subject_index(index_data["subject"])
    return out


def _index_paragraph(text, style):
    return Paragraph(text, style)


def scripture_index(pairs) -> list:
    if not pairs:
        return []
    from bookkit import bibleref
    grouped: dict[str, list[int]] = {}
    for ref, pages in pairs:
        grouped.setdefault(ref, []).extend(pages)
    rows = sorted(grouped.items(), key=lambda kv: bibleref.sort_key(kv[0]))
    out = page_start("body", no_head=True)
    out += openers.section_head(
        "Scripture Index",
        "References are to the Authorized (King James) Version.")
    out.append(Paragraph("Scripture Index", T.STYLES["index_letter"]))
    for ref, pages in rows:
        out.append(Paragraph(
            f"{ref}\u2003{indexes.page_list(set(pages))}", T.STYLES["index_item"]))
    return out


def subject_index(pairs) -> list:
    if not pairs:
        return []
    grouped: dict[str, list[int]] = {}
    for term, pages in pairs:
        grouped.setdefault(term, []).extend(pages)
    out = page_start("body", no_head=True)
    out += openers.section_head("Subject Index")
    current = None
    for term in sorted(grouped, key=lambda t: t.lower()):
        letter = term[0].upper()
        if letter != current:
            out.append(Paragraph(letter, T.STYLES["index_letter"]))
            current = letter
        out.append(Paragraph(
            f"{term}\u2003{indexes.page_list(set(grouped[term]))}",
            T.STYLES["index_item"]))
    return out


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def assemble(cfg, manifest, index_data, only=None) -> list:
    fig_pages = {fid: m.get("page") for fid, m in indexes.FIGURES.items()}

    def page_of(p):
        return document.label(p, document.BODY_START)

    story = []
    story += front_matter(cfg, manifest, fig_pages, page_of)
    story += body_story(cfg, manifest, only)
    if only is None:
        epi = read(MANUSCRIPT / "epilogue.md")
        if epi.strip():
            story += page_start("body", no_head=True)
            story += openers.section_head("Epilogue")
            story += [Paragraph("The Young Were Never Meant to Replace the Fathers",
                                T.STYLES["fm_sub"]), Spacer(1, 10)]
            story += markup.parse(epi, T.TEXT_W, manifest=manifest)
        story += back_matter(cfg, manifest, index_data)
    return story


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "book.pdf"))
    ap.add_argument("--only", nargs="*", type=int, default=None)
    ap.add_argument("--proof", action="store_true")
    args = ap.parse_args()

    cfg = load_cfg()
    manifest = figures.load_manifest()
    T.register_fonts()
    T.STYLES.update(T.build_styles())

    only = set(args.only) if args.only else None
    if args.proof and only is None:
        only = {1, 2}

    out = Path(args.out)
    index_data = None
    prev = None
    for it in range(1, 5):
        indexes.reset()
        story = assemble(cfg, manifest, index_data, only)
        document.build(story, out, cfg["title"], cfg["author"],
                       subject=cfg["subtitle"])
        snapshot = {
            "scripture": sorted((k, tuple(sorted(v))) for k, v in indexes.SCRIPTURE.items()),
            "subject": sorted((k, tuple(sorted(v))) for k, v in indexes.SUBJECT.items()),
            "figures": {k: v.get("page") for k, v in indexes.FIGURES.items()},
        }
        import pypdfium2 as pdfium
        n_pages = len(pdfium.PdfDocument(out))
        print(f"pass {it}: {n_pages} pages, "
              f"{len(indexes.split_postponed)} split refusals, "
              f"{len(snapshot['scripture'])} scripture refs, "
              f"{len(snapshot['subject'])} subjects, "
              f"body starts p{document.BODY_START}")
        if prev and snapshot == prev:
            print("  layout stable")
            break
        prev = snapshot
        index_data = {"scripture": snapshot["scripture"],
                      "subject": snapshot["subject"]}

    print(f"\nwrote {out}  ({out.stat().st_size/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
