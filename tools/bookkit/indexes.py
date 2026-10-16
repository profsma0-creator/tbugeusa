"""
bookkit.indexes — page-accurate back-of-book indexes built during typesetting.

`IndexedParagraph` reports the page on which it is drawn, so the Scripture
Index, Subject Index and List of Illustrations are generated from the real
typographic pagination rather than from guesswork.
"""
from __future__ import annotations

import re
from collections import defaultdict

from reportlab.platypus import Flowable, Paragraph

from . import bibleref

SCRIPTURE: dict[str, set[int]] = defaultdict(set)
SUBJECT: dict[str, set[int]] = defaultdict(set)
FIGURES: dict[str, dict] = {}
NOTES: dict[str, list] = {}

# --------------------------------------------------------------------------
# subject vocabulary — terms worth indexing in a work on generational
# revelation.  Matched on word boundaries, case-insensitively.
# --------------------------------------------------------------------------
SUBJECT_TERMS: dict[str, str] = {}


def _add(term: str, *aliases: str) -> None:
    for a in (term,) + aliases:
        SUBJECT_TERMS[a.lower()] = term


_add("Aaron", )
_add("Abraham", "Abram")
_add("adoption")
_add("apostles", "apostleship")
_add("anointing")
_add("authority")
_add("baptism", "baptism of the Spirit")
_add("Barnabas")
_add("blessing", "blessings")
_add("Boaz")
_add("calling", "callings", "divine calling")
_add("character")
_add("charisma", "charismatic gift", "spiritual gift", "spiritual gifts")
_add("Christ", "Jesus", "Christ Jesus", "Messiah")
_add("commissioning")
_add("consecration")
_add("continuity")
_add("covenant", "covenants")
_add("Daniel")
_add("David")
_add("Deborah")
_add("discernment")
_add("discipleship", "disciple", "disciples")
_add("Eli")
_add("Elijah")
_add("Elisha")
_add("elders", "elder", "eldership")
_add("Esther")
_add("evangelism")
_add("faith")
_add("faithfulness")
_add("family", "families")
_add("fathers", "father", "fatherhood")
_add("fear of the Lord")
_add("fruit of the Spirit")
_add("generation", "generations", "generational")
_add("gift", "gifts", "gifting")
_add("glory")
_add("grace")
_add("hearing", "hearing God")
_add("heart", "hearts")
_add("heritage")
_add("Holy Spirit", "Spirit of God", "Spirit")
_add("honour", "honor")
_add("household", "households")
_add("humility")
_add("inheritance")
_add("instruction", "instructions")
_add("intercession")
_add("Isaac")
_add("Israel")
_add("Jacob")
_add("Jeremiah")
_add("Jerusalem")
_add("Jesus")
_add("John the Baptist", "John the Baptizer")
_add("Joseph")
_add("Joshua")
_add("Josiah")
_add("judgment")
_add("kingdom", "kingdom of God")
_add("knowledge", "knowledge of God")
_add("law", "law of Moses")
_add("leadership", "leader", "leaders")
_add("Levi", "Levites")
_add("love")
_add("Mary")
_add("mentor", "mentors", "mentorship", "mentoring")
_add("mercy")
_add("ministry", "ministries")
_add("mission", "missions")
_add("Moses")
_add("mothers", "mother", "motherhood")
_add("mystery", "mysteries")
_add("mystic", "mystics", "mysticism")
_add("Nehemiah")
_add("obedience")
_add("ordination")
_add("parents", "parent", "parenthood")
_add("passing the mantle")
_add("Paul")
_add("Pentecost")
_add("perseverance")
_add("Peter")
_add("power")
_add("prayer")
_add("preaching")
_add("priest", "priesthood", "priests")
_add("promise", "promises")
_add("prophecy", "prophecies")
_add("prophet", "prophets", "prophetic")
_add("provision")
_add("psalm", "psalms", "psalter")
_add("rebuke")
_add("reformation", "renewal", "revival")
_add("remnant")
_add("repentance")
_add("revelation", "revelations")
_add("reward")
_add("righteousness")
_add("Samuel")
_add("Saul")
_add("Scripture", "Scriptures", "the Word")
_add("seer", "seers", "seeing")
_add("service", "servanthood")
_add("Shepherd", "shepherding")
_add("signs and wonders")
_add("Solomon")
_add("sons", "sonship", "son")
_add("Spirit")
_add("stewardship")
_add("succession")
_add("suffering")
_add("teaching", "doctrine")
_add("temple")
_add("testimony", "testimonies")
_add("Timothy")
_add("Titus")
_add("tradition", "traditions")
_add("transference", "transmission")
_add("trust")
_add("truth")
_add("vineyard")
_add("vision", "visions")
_add("vocation")
_add("watchfulness")
_add("wealth")
_add("wilderness")
_add("wisdom")
_add("witness", "witnesses")
_add("worship")
_add("youth", "youthfulness", "young people", "young man", "young men")
_add("Zerubbabel")

_SUBJECT_RE = {
    term: re.compile(r"(?<![\w])" + re.escape(alias) + r"s?(?![\w])", re.I)
    for alias, term in SUBJECT_TERMS.items()
}


def reset() -> None:
    SCRIPTURE.clear()
    SUBJECT.clear()
    FIGURES.clear()
    NOTES.clear()


def find_subjects(text: str) -> list[str]:
    plain = re.sub(r"<[^>]+>", " ", text)
    hits = set()
    for term, rx in _SUBJECT_RE.items():
        if rx.search(plain):
            hits.add(term)
    return sorted(hits)


class IndexedParagraph(Paragraph):
    """A paragraph that notes its own page in the indexes as it is drawn."""

    def __init__(self, text, style, index_scripture=True, index_subject=True,
                 figure=None, **kw):
        # reportlab re-instantiates paragraphs with text=None when splitting
        if text:
            self._refs = bibleref.find_refs(text) if index_scripture else []
            self._subjects = find_subjects(text) if index_subject else []
        else:
            self._refs, self._subjects = [], []
        self._figure = figure
        super().__init__(text, style, **kw)

    def split(self, availWidth, availHeight):
        """reportlab draws the *first split part*, not the original flowable,
        so the indexing metadata has to travel with it."""
        parts = super().split(availWidth, availHeight)
        if parts:
            first = parts[0]
            if isinstance(first, IndexedParagraph) and first is not self:
                first._refs = self._refs
                first._subjects = self._subjects
                first._figure = self._figure
        return parts

    def draw(self):
        page = self.canv.getPageNumber()
        for r in self._refs:
            SCRIPTURE[r].add(page)
        for s in self._subjects:
            SUBJECT[s].add(page)
        if self._figure:
            entry = FIGURES.setdefault(self._figure, {})
            entry["page"] = page
        super().draw()


class FigureMarker(Flowable):
    """Zero-height carrier used to record the page a figure falls on."""

    def __init__(self, fig_id):
        super().__init__()
        self._figure = fig_id

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        entry = FIGURES.setdefault(self._figure, {})
        entry.setdefault("page", self.canv.getPageNumber())


def page_list(pages) -> str:
    """Collapse a set of page numbers into a readable index run."""
    ps = sorted(p for p in pages if p and p > 0)
    if not ps:
        return ""
    runs, start, prev = [], ps[0], ps[0]
    for p in ps[1:]:
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
