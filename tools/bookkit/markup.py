"""
bookkit.markup — the manuscript dialect.

Blocks
------
    ## Heading            section head        ### Sub-head       #### Run-in head
    plain text            paragraph (auto first-line indent after the first)
    > lines               quotation panel, last line "— Source" becomes attribution
    - item / 1. item      bulleted and numbered lists
    | a | b |             pipe table, optional :::table caption above it

Fenced blocks
-------------
    :::verse ... :::            scripture panel (cream, gold bar)
    :::quote ... :::            plain block quotation
    :::pull ... :::             displayed pull quote
    :::note Title ... :::       excursus / case-study box
    :::keypoints ... :::        "At a glance" summary panel
    :::figure fig-01-1          place a managed figure
    :::table Caption ... :::    pipe table with a numbered caption

Inline
------
    **bold**   *italic*   ^{sup}   ~{sub}   [^1]   —  (n-dash: write the character)
"""
from __future__ import annotations

import re

from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak,
                                Paragraph, Spacer, Table, TableStyle)

from . import decor, figures, indexes, theme as T

FENCE = re.compile(r"^:::\s*(?P<kind>[\w-]+)?\s*(?P<arg>.*?)\s*$")
BULLET = re.compile(r"^\s*[-*\u2022]\s+(?P<txt>.*)$")
NUMBER = re.compile(r"^\s*(?P<n>\d{1,2})[.)]\s+(?P<txt>.*)$")
PIPE = re.compile(r"^\s*\|.*\|\s*$")
PIPE_SEP = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")
ATTR = re.compile(r"^\s*[\u2014\u2013-]{1,2}\s*(?P<src>.+?)\s*$")


# ---------------------------------------------------------------------------
# inline
# ---------------------------------------------------------------------------
def esc(s: str) -> str:
    return re.sub(r"&(?!(?:amp|lt|gt|nbsp|quot|apos|#\d+);)", "&amp;", s)


_IT = r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"


def _bold(m: re.Match) -> str:
    """**bold**, allowing a single-asterisk italic inside the span."""
    inner = re.sub(_IT, r"<i>\1</i>", m.group(1))
    return "<b>" + inner + "</b>"


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", s)
    s = re.sub(r"\*\*(.+?)\*\*(?!\*)", _bold, s)
    s = re.sub(_IT, r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<i>\1</i>", s)
    s = re.sub(r"\^\{([^}]+)\}", r"<super>\1</super>", s)
    s = re.sub(r"~\{([^}]+)\}", r"<sub>\1</sub>", s)
    s = re.sub(r"\[\^([\w]+)\]", r"<super>\1</super>", s)
    # soft hyphen hints: "gene\-era\-tion" -> reportlab shy
    return s


# ---------------------------------------------------------------------------
# table helper
# ---------------------------------------------------------------------------
def _cells(line: str) -> list[str]:
    parts = line.strip().strip("|").split("|")
    return [p.strip() for p in parts]


def _make_table(rows: list[list[str]], caption: str | None, label: str | None,
                text_width: float):
    header = None
    body = rows
    if len(rows) >= 2 and all(set(c) <= set("-: ") and c for c in rows[1]):
        header, body = rows[0], rows[2:]
    elif rows and rows[0] and rows[0][0].isupper() and len(rows) > 2 and _looks_like_header(rows):
        header, body = rows[0], rows[1:]

    ncol = max(len(r) for r in rows)
    ncol = max(2, min(ncol, 4))
    # proportional column widths from content length
    weights = []
    for c in range(ncol):
        lengths = [len(_strip_markup(r[c])) if c < len(r) else 0 for r in rows]
        weights.append(max(8, sum(lengths) / max(1, len(lengths))))
    total = sum(weights)
    widths = [text_width * w / total for w in weights]
    # keep the widest column from dominating
    lo = text_width * 0.16
    widths = [max(lo, w) for w in widths]
    scale = text_width / sum(widths)
    widths = [w * scale for w in widths]

    data = []
    for r in body:
        row = []
        for c in range(ncol):
            txt = r[c] if c < len(r) else ""
            row.append(Paragraph(inline(txt), T.STYLES["tbl_cell"]))
        data.append(row)

    tbl = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [T.WHITE, T.CREAM]),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, T.RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, T.RULE_DARK),
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, T.GOLD),
    ]
    if header:
        hrow = [Paragraph(inline(c), T.STYLES["tbl_head"]) for c in header]
        data.insert(0, hrow)
        tbl = Table(data, colWidths=widths, repeatRows=1)
        style = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, 0), T.CREAM_DARK),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, 0), 1.0, T.GOLD),
            ("LINEBELOW", (0, 1), (-1, -2), 0.35, T.RULE),
            ("LINEBELOW", (0, -1), (-1, -1), 0.9, T.RULE_DARK),
        ]
    tbl.setStyle(TableStyle(style))
    out = []
    if caption:
        out.append(Paragraph((label + " " if label else "") + inline(caption).upper()
                             if False else
                             (f"{label} \u00b7 " if label else "") + inline(caption),
                             T.STYLES["tbl_caption"]))
        out.append(Spacer(1, 3.5))
    out.append(tbl)
    return out


def _strip_markup(s: str) -> str:
    return re.sub(r"[*_`]", "", s)


def _looks_like_header(rows) -> bool:
    return False


# ---------------------------------------------------------------------------
# main parser
# ---------------------------------------------------------------------------
class Parser:
    def __init__(self, text_width: float, chapter_no: int | None = None,
                 manifest: dict | None = None, drop_cap: bool = False,
                 first_heading_space: bool = False):
        self.tw = text_width
        self.chapter_no = chapter_no
        self.manifest = manifest or {}
        self.drop_cap = drop_cap
        self.flows: list = []
        self.para_count = 0
        self.table_no = 0
        self._pending_space = first_heading_space

    # -- helpers ---------------------------------------------------------
    def para(self, txt: str, style_key: str | None = None):
        if not txt.strip():
            return
        self.para_count += 1
        if self.drop_cap and self.para_count == 1 and len(txt) > 60:
            m = re.match(r"^(?:<[^>]+>|\*\*?)?(\w)(.*)$", txt, re.S)
            if m:
                letter, rest = m.group(1), m.group(2)
                rest = re.sub(r"^(\*\*|\*)", "", rest)
                self.flows.append(
                    decor.drop_cap_paragraph(letter, inline(rest), T.STYLES["body_first"]))
                self.flows.append(Spacer(1, 4))
                return
        if style_key:
            key = style_key
        elif self.para_count == 1:
            key = "body_first"
        else:
            key = "body_ind"
        self.flows.append(indexes.IndexedParagraph(inline(txt), T.STYLES[key]))

    def heading(self, level: int, txt: str):
        key = {2: "h2", 3: "h3", 4: "h4"}[level]
        st = T.STYLES[key]
        p = indexes.IndexedParagraph(inline(txt), st)
        if level == 2:
            # section heads appear in the PDF outline but not in the printed
            # contents, which lists parts and chapters only
            p._bookmark = (_strip_markup(txt), 2)
            self.flows.append(p)
            self.flows.append(decor.SectionMark())
            self.flows.append(Spacer(1, 3))
        else:
            self.flows.append(p)
        self.para_count = 0

    # -- top level -------------------------------------------------------
    def parse(self, src: str):
        lines = src.replace("\r\n", "\n").split("\n")
        i = 0
        buf: list[str] = []

        def flush():
            if not buf:
                return
            block = " ".join(l.strip() for l in buf).strip()
            buf.clear()
            if block:
                self.para(block)

        while i < len(lines):
            raw = lines[i]
            line = raw.rstrip()
            stripped = line.strip()

            if not stripped:
                flush()
                i += 1
                continue

            # fenced block
            m = FENCE.match(stripped)
            if m and stripped == ":::":
                flush()
                i += 1
                continue
            if m:
                flush()
                kind = (m.group("kind") or "").lower()
                arg = m.group("arg").strip()
                body, i = self._collect(lines, i + 1)
                self._emit_block(kind, arg, body)
                continue

            # heading
            hm = re.match(r"^(#{2,4})\s+(.*)$", stripped)
            if hm:
                flush()
                self.heading(len(hm.group(1)), hm.group(2).strip())
                i += 1
                continue

            # block quote
            if stripped.startswith(">"):
                flush()
                q = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    q.append(lines[i].strip().lstrip(">").strip())
                    i += 1
                self._emit_quote(q)
                continue

            # pipe table
            if PIPE.match(stripped):
                flush()
                rows = []
                while i < len(lines) and PIPE.match(lines[i].strip()):
                    if not PIPE_SEP.match(lines[i]):
                        rows.append(_cells(lines[i]))
                    else:
                        rows.append(["---"] * len(_cells(lines[i])))
                    i += 1
                self.table_no += 1
                label = (f"Table {self.chapter_no}.{self.table_no}"
                         if self.chapter_no else None)
                self.flows.extend(_make_table(rows, None, label, self.tw))
                self.flows.append(Spacer(1, 8))
                continue

            # lists
            bm = BULLET.match(line)
            nm = NUMBER.match(line)
            if bm or nm:
                flush()
                items, numbered = [], bool(nm)
                while i < len(lines):
                    ln = lines[i]
                    if not ln.strip():
                        break
                    mb = BULLET.match(ln)
                    mn = NUMBER.match(ln)
                    if not (mb or mn):
                        break
                    mm = mb or mn
                    items.append(mm.group("txt"))
                    i += 1
                    # continuation lines (indented)
                    while i < len(lines) and lines[i].strip() and \
                            not BULLET.match(lines[i]) and not NUMBER.match(lines[i]) \
                            and lines[i].startswith(("   ", "\t")) \
                            and not lines[i].strip().startswith(("|", ">", "#", ":::")):
                        items[-1] += " " + lines[i].strip()
                        i += 1
                self._emit_list(items, numbered)
                continue

            buf.append(line)
            i += 1

        flush()
        return self.flows

    def _collect(self, lines, i):
        body = []
        while i < len(lines) and lines[i].strip() != ":::":
            body.append(lines[i])
            i += 1
        return body, i + 1

    # -- block emitters ---------------------------------------------------
    def _split_attrib(self, text: str):
        lines = [l for l in text.split("\n") if l.strip()]
        attrib = None
        if lines and ATTR.match(lines[-1].strip()) and len(lines[-1].strip()) < 120:
            attrib = ATTR.match(lines[-1].strip()).group("src")
            lines = lines[:-1]
        body = " ".join(l.strip() for l in lines).strip()
        return body, attrib

    def _emit_quote(self, q_lines):
        txt, attrib = self._split_attrib("\n".join(q_lines))
        paras = [indexes.IndexedParagraph(inline(txt), T.STYLES["quote_text"])]
        self.flows.append(Spacer(1, 5))
        self.flows.append(KeepTogether([decor.scripture_block(paras, attrib)]))
        self.flows.append(Spacer(1, 9))

    def _emit_block(self, kind, arg, body_lines):
        text = "\n".join(body_lines)
        if kind == "figure":
            self.flows.extend(figures.build_figure(arg, self.manifest, self.tw))
            return
        if kind in ("plate", "illustration"):
            self.flows.extend(figures.build_figure(arg, self.manifest, self.tw))
            return
        if kind == "verse":
            txt, attrib = self._split_attrib(text)
            paras = [indexes.IndexedParagraph(inline(txt), T.STYLES["verse_text"])]
            blk = decor.scripture_block(paras, attrib)
            self.flows.append(Spacer(1, 5))
            self.flows.append(KeepTogether([blk]))
            self.flows.append(Spacer(1, 9))
            return
        if kind == "quote":
            txt, attrib = self._split_attrib(text)
            paras = [indexes.IndexedParagraph(inline(txt), T.STYLES["quote_text"])]
            self.flows.append(Spacer(1, 5))
            self.flows.append(KeepTogether([decor.scripture_block(paras, attrib)]))
            self.flows.append(Spacer(1, 9))
            return
        if kind == "pull":
            txt, attrib = self._split_attrib(text)
            paras = [indexes.IndexedParagraph(inline(txt), T.STYLES["pull_text"])]
            self.flows.append(Spacer(1, 8))
            self.flows.append(decor.pull_quote(paras, attrib))
            self.flows.append(Spacer(1, 10))
            return
        if kind in ("note", "excursus", "box"):
            title = arg or None
            paras, cur = [], []
            for ln in text.split("\n"):
                if not ln.strip():
                    if cur:
                        paras.append(indexes.IndexedParagraph(
                            inline(" ".join(cur)), T.STYLES["note_body"]))
                        cur = []
                    continue
                if ln.strip().startswith("- "):
                    if cur:
                        paras.append(indexes.IndexedParagraph(
                            inline(" ".join(cur)), T.STYLES["note_body"]))
                        cur = []
                    paras.append(indexes.IndexedParagraph(
                        inline(ln.strip()[2:]), T.STYLES["kp_item"], bulletText="\u25C6"))
                    continue
                cur.append(ln.strip())
            if cur:
                paras.append(indexes.IndexedParagraph(
                    inline(" ".join(cur)), T.STYLES["note_body"]))
            self.flows.append(Spacer(1, 6))
            self.flows.append(decor.excursus_box(title, paras))
            self.flows.append(Spacer(1, 10))
            return
        if kind in ("keypoints", "takeaways", "summary"):
            items = []
            for ln in text.split("\n"):
                s = ln.strip()
                if not s:
                    continue
                s = re.sub(r"^[-*\u2022]\s+", "", s)
                s = re.sub(r"^\d+[.)]\s+", "", s)
                items.append(inline(s))
            self.flows.append(Spacer(1, 6))
            self.flows.append(decor.keypoints_box(items))
            self.flows.append(Spacer(1, 10))
            return
        if kind in ("table",):
            rows, cap = [], arg or None
            for ln in text.split("\n"):
                if PIPE.match(ln.strip()):
                    rows.append(_cells(ln) if not PIPE_SEP.match(ln)
                                else ["---"] * len(_cells(ln)))
            self.table_no += 1
            label = f"Table {self.chapter_no}.{self.table_no}" if self.chapter_no else None
            self.flows.extend(_make_table(rows, cap, label, self.tw))
            self.flows.append(Spacer(1, 9))
            return
        if kind in ("list", "bullets"):
            items = [re.sub(r"^[-*\u2022]\s+", "", l.strip())
                     for l in text.split("\n") if l.strip()]
            self._emit_list(items, False)
            return
        if kind in ("notes", "endnotes"):
            items = [l.strip() for l in text.split("\n") if l.strip()]
            self.flows.append(Spacer(1, 12))
            self.flows.append(decor.GoldRule(width=70, space_before=0, space_after=6,
                                             color=T.RULE_DARK))
            self.flows.append(Paragraph("NOTES", T.STYLES["note_title"]))
            for it in items:
                it = re.sub(r"^(\d+)[.)]?\s*", r"\1.\u2002", it)
                self.flows.append(Paragraph(inline(it), T.STYLES["numbered"]))
            self.flows.append(Spacer(1, 6))
            return
        # unknown fence: treat as ordinary paragraphs
        for para_txt in re.split(r"\n\s*\n", text):
            self.para(" ".join(para_txt.split()))

    def _emit_list(self, items, numbered):
        flows = []
        for n, it in enumerate(items, 1):
            st = T.STYLES["numbered" if numbered else "bullet"]
            flows.append(indexes.IndexedParagraph(
                inline(it), st, bulletText=(f"{n}." if numbered else "\u25AA")))
        lf = ListFlowable(
            [ListItem(f).__class__ and f for f in flows],
            bulletType="bullet", start="\u25AA", leftIndent=0, spaceBefore=2,
            spaceAfter=2,
        )
        # ListFlowable adds its own bullets; simpler to emit flat list paragraphs
        for f in flows:
            self.flows.append(f)
        self.flows.append(Spacer(1, 4))


def parse(text: str, text_width: float, chapter_no: int | None = None,
          manifest: dict | None = None, drop_cap: bool = False):
    return Parser(text_width, chapter_no, manifest, drop_cap).parse(text)
