#!/usr/bin/env python3
"""Build a subject index from the typeset body.

Headwords are taken from the glossary (terms set in bold) and from a short
curated list of instrument names and concepts. Page numbers are located by
scanning the text layer of the body pages of the built PDF, so the index is
derived from the final text rather than from the manuscript source.
"""

import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "book")
OUT = os.path.join(ROOT, "output")

EXTRA = [
    "AUDIT", "Adult Attachment Interview", "Autism Diagnostic Observation Schedule",
    "Cattell–Horn–Cattell model", "Dyadic Adjustment Scale", "HCR-20",
    "International Test Commission", "Mini International Neuropsychiatric Interview",
    "Minnesota Multiphasic Personality Inventory", "Montreal Cognitive Assessment",
    "NEO Personality Inventory", "Personality Assessment Inventory",
    "Structured Clinical Interview for DSM-5", "Vineland Adaptive Behavior Scales",
    "Yale–Brown Obsessive Compulsive Scale",
]

STOP = {"expertise", "note", "summary"}


def glossary_terms():
    path = os.path.join(BOOK, "glossary.md")
    text = open(path, encoding="utf-8").read()
    terms = re.findall(r"^\*\*(.+?)\.\*\*", text, flags=re.M)
    return [t.strip() for t in terms]


def build_index(pdf_path, body_start_page=1):
    doc = pymupdf.open(pdf_path)
    # folio of the first page of the body, taken from the build record
    try:
        with open(os.path.join(OUT, "bookmap.json")) as fh:
            body_start = json.load(fh)["body_start"]
    except Exception:
        body_start = 1
    terms = sorted(set(glossary_terms()) | set(EXTRA))
    # find where the body ends (References begins the back matter)
    body_pages = {}
    for i in range(doc.page_count):
        body_pages[i] = " ".join(doc[i].get_text().split())
    # locate the start of References so the index does not cite back matter
    end = doc.page_count
    for i in range(doc.page_count):
        first = doc[i].get_text().strip().split("\n")[0].strip()
        if first in ("References", "REFERENCES", "Glossary", "GLOSSARY"):
            end = i
            break

    entries = []
    for term in terms:
        if term.lower() in STOP:
            continue
        pat = re.compile(r"\b" + re.escape(term) + r"s?\b", re.IGNORECASE)
        counts = {}
        for i in range(body_start - 1, end):
            n = len(pat.findall(body_pages[i]))
            if n:
                counts[i] = n
        if not counts or len(counts) > 45:
            continue
        # index the pages where the term is substantively discussed: those with
        # repeated mention, or the first mention where it occurs only once
        strong = [i for i, n in counts.items() if n >= 2]
        if not strong:
            strong = [min(counts)]
        strong = sorted(strong)[:14]
        pages = [i - body_start + 2 for i in strong]
        entries.append((term, pages))
    entries.sort(key=lambda e: e[0].lower())
    return entries, end


def format_pages(pages):
    """Collapse consecutive runs into ranges: 12, 14–16, 22."""
    if not pages:
        return ""
    pages = sorted(pages)
    runs = []
    start = prev = pages[0]
    for p in pages[1:]:
        if p == prev + 1:
            prev = p
            continue
        runs.append((start, prev))
        start = prev = p
    runs.append((start, prev))
    out = []
    for a, b in runs:
        if a == b:
            out.append(str(a))
        elif b == a + 1:
            out.append(f"{a}, {b}")
        else:
            out.append(f"{a}\u2013{b}")
    return ", ".join(out)


def main():
    pdf = os.path.join(OUT, "CPY903_Advanced_Assessment_and_Diagnosis.pdf")
    entries, end = build_index(pdf)
    payload = [{"term": t, "pages": format_pages(p)} for t, p in entries]
    with open(os.path.join(OUT, "index.json"), "w") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(f"index: {len(payload)} headwords, body ends at page {end}")


if __name__ == "__main__":
    main()
