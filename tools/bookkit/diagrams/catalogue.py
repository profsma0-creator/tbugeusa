"""
bookkit.diagrams.catalogue — every figure in the book, as data.

Each entry declares a layout and the content for it; the renderer supplies the
geometry.  Content lives here rather than in the chapter files so that the
illustration programme of the whole book can be reviewed in one place.

Entry keys
----------
layout     which primitive composes the figure
title      small caps heading printed above the diagram
footnote   italic line printed below the diagram
caption    the numbered caption that appears on the page
source     provenance line under the caption
chapter    the chapter the figure belongs to (for the list of illustrations)
data       keyword arguments handed to the layout function
"""
from __future__ import annotations

# canvas height in inches for each layout
HEIGHT = {
    "chain": 1.72, "vchain": 2.75, "twocol": 1.95, "timeline": 1.85,
    "tree": 1.95, "cycle": 2.45, "pyramid": 2.40, "layers": 2.05,
    "matrix": 2.10, "balance": 2.25, "radial": 2.60, "stages": 2.95,
    "spectrum": 1.95, "quadrant": 2.30, "funnel": 2.35, "bridge": 2.00,
    "arch": 2.20, "before_after": 2.05,
}

# ---------------------------------------------------------------------------
# FRONT MATTER
# ---------------------------------------------------------------------------
FRONT = {
    "fig-00-1": dict(
        layout="chain", chapter=0,
        title="The architecture of generational revelation",
        data=dict(items=[
            ["REVELATION", "God speaks\ninitiative"],
            ["CUSTODY", "fathers keep\nand guard"],
            ["INTERPRETATION", "elders read\nand explain"],
            ["PREPARATION", "mentors train\nand release"],
            ["RECEPTION", "sons receive\nand obey"],
            ["FULFILMENT", "the appointed\ngeneration builds"],
        ], badges=True, tsize=6.0, bsize=5.5, gap=0.022),
        footnote="The first three movements belong to the fathers and elders; "
                 "the last three to the generation that inherits the word.",
        caption="The architecture of generational revelation: six movements "
                "through which a divine word passes from speech to fulfilment.",
        source="Author's construction."),

    "fig-00-2": dict(
        layout="layers", chapter=0,
        title="The shape of the argument",
        data=dict(x0=0.03, x1=0.97, gap=0.014, tsize=6.4,
                  rows=[
                      ["I\u2013II   The wonder", "God entrusts His word to a chain of custodians"],
                      ["III\u2013V   The pattern", "Why the young are chosen, and how the word travels"],
                      ["VI\u2013VII   The testing", "When generations collide, and how Christ models succession"],
                      ["VIII\u2013IX   The reception", "What the inheriting generation must do and avoid"],
                      ["X\u2013XI   The rebuilding", "Restoring the covenant between fathers and children"],
                  ]),
        caption="The five movements of the book's argument.",
        source="Author's construction."),

    "fig-00-3": dict(
        layout="cycle", chapter=0,
        title="The generational cycle",
        data=dict(items=[
            ["RECEIVE", "the word"],
            ["KEEP", "in the heart"],
            ["LIVE", "in the house"],
            ["DECLARE", "to the child"],
            ["ENTRUST", "to the faithful"],
            ["RELEASE", "to the next"],
        ], rx=0.31, ry=0.30, r=0.082, tsize=5.7),
        footnote="Break any link and the cycle does not slow \u2014 it stops.",
        caption="The cycle of transmission that Psalm 78 and 2 Timothy 2:2 describe.",
        source="Psalm 78:1\u20137; 2 Timothy 2:2."),
}

# ---------------------------------------------------------------------------
# PART I — THE GOD WHO SPEAKS ACROSS GENERATIONS  (ch 1\u20135)
# ---------------------------------------------------------------------------
PART1 = {
    "fig-01-1": dict(
        layout="chain", chapter=1,
        title="The custody chain of Psalm 78:1\u20137",
        data=dict(items=[
            ["HEARD", "\u201cwhich we have\nheard and known\u201d\nv. 3"],
            ["KEPT", "\u201cwe will not hide\nthem\u201d\nv. 4"],
            ["DECLARED", "\u201cdeclare them to\ntheir children\u201d\nv. 6"],
            ["HOPED", "\u201cset their hope\nin God\u201d\nv. 7"],
        ], tsize=7.0, bsize=5.6),
        footnote="Revelation survives only where hearing becomes speech.",
        caption="The custody chain of Psalm 78: hearing becomes keeping, keeping "
                "becomes declaration, and declaration becomes hope.",
        source="Drawn from Psalm 78:1\u20137."),

    "fig-01-2": dict(
        layout="chain", chapter=1,
        title="Three houses of custody",
        data=dict(items=[
            ["THE HOUSEHOLD", "Deuteronomy 6:4\u20139\n\n\u201cwhen thou sittest\nin thine house\u201d"],
            ["THE ASSEMBLY", "Psalm 78:1\u20137\n\nthe congregation\nbecomes memory"],
            ["THE SUCCESSION", "2 Timothy 1:5\n\nfaith travels through\nLois and Eunice"],
        ], tsize=7.0, bsize=5.5, gap=0.035),
        footnote="One testimony, three custodians: every generation receives it "
                 "through all three.",
        caption="The three houses through which a single testimony is transmitted "
                "and preserved.",
        source="Deuteronomy 6:4\u20139; Psalm 78:1\u20137; 2 Timothy 1:5."),

    "fig-01-3": dict(
        layout="chain", chapter=1,
        title="The four verbs of transmission",
        data=dict(items=[
            ["SHEW", "Psalm 78:4\ntell it plainly"],
            ["SPEAK", "Psalm 145:4\npraise to the next"],
            ["TEACH", "Deuteronomy 6:7\nrepeat in the ordinary"],
            ["COMMIT", "2 Timothy 2:2\nentrust to the faithful"],
        ], tsize=6.8, bsize=5.5),
        footnote="Every generation is judged by what it did with what it was given.",
        caption="The four verbs by which Scripture describes the duty of one "
                "generation to the next.",
        source="Psalm 78:4; Psalm 145:4; Deuteronomy 6:7; 2 Timothy 2:2."),

    "fig-01-4": dict(
        layout="chain", chapter=1,
        title="The daily rhythm of Deuteronomy 6",
        data=dict(items=[
            ["SITTING", "in thine house", ""],
            ["WALKING", "by the way", ""],
            ["LYING DOWN", "at the day's end", ""],
            ["RISING UP", "at the day's start", ""],
        ], tsize=6.8, bsize=5.5),
        footnote="The word is not to be scheduled but woven \u2014 attached to the "
                 "movements of an ordinary day.",
        caption="The four occasions Deuteronomy 6:7 names for instruction.",
        source="Deuteronomy 6:7."),

    "fig-01-5": dict(
        layout="funnel", chapter=5,
        title="Where a testimony is lost",
        data=dict(stages_list=[
            ["The word is spoken", "God gives revelation to a person"],
            ["The word is not declared", "the custodian keeps it privately"],
            ["The word is not heard", "the next generation never receives it"],
            ["The word is lost", "an entire generation arises that does not know"],
        ], tsize=6.4, bsize=5.4),
        footnote="Judges 2:10 describes the end of this sequence, not its beginning.",
        caption="The four stages by which a living testimony becomes a lost memory.",
        source="Judges 2:7\u201310."),

    "fig-01-6": dict(
        layout="tree", chapter=3,
        title="The eye and the hand",
        data=dict(root="DAVID \u00b7 1 Chronicles 22:5\u201319",
                  children=[
                      ["RECEIVES", "the pattern\nby the Spirit"],
                      ["GATHERS", "the material\nfor the house"],
                      ["PREPARES", "the workers\nand the plan"],
                      ["CANNOT BUILD", "he may not lay\na single stone"],
                  ], tsize=6.2, bsize=5.3),
        footnote="\u201cSolomon thy son, he shall build my house.\u201d "
                 "1 Chronicles 28:6",
        caption="What David could do and what he could not: the distinction between "
                "receiving a revelation and executing it.",
        source="1 Chronicles 22:5\u201319; 28:1\u201321; 29:1\u20135."),

    "fig-01-7": dict(
        layout="before_after", chapter=5,
        title="Inheritance and assignment",
        data=dict(before=["INHERITANCE", "What a father can hand over\n\n\u2022 a name and a place\n"
                                             "\u2022 a body of instruction\n\u2022 material provision\n"
                                             "\u2022 an introduction to God"],
                  after=["ASSIGNMENT", "What only God can give\n\n\u2022 a personal call\n"
                                        "\u2022 a personal encounter\n\u2022 a personal commission\n"
                                        "\u2022 a personal accountability"],
                  arrow_text="must be\npersonally\nentered", tsize=6.2, bsize=5.3),
        caption="Inheritance can be transferred; assignment must be personally received.",
        source="Numbers 27:18\u201323; Joshua 1:1\u20139."),

    "fig-01-8": dict(
        layout="stages", chapter=4,
        title="The name that carries a lineage",
        data=dict(items=[
            ["THE GOD OF ABRAHAM", "the promise given \u2014 Genesis 12:1\u20133"],
            ["THE GOD OF ISAAC", "the promise confirmed \u2014 Genesis 26:1\u20135"],
            ["THE GOD OF JACOB", "the promise named and carried \u2014 Genesis 28:13\u201315"],
            ["THE GOD WHO SPEAKS TO MOSES", "the promise invoked at the burning bush \u2014 Exodus 3:6, 15"],
        ], tsize=6.4, bsize=5.4),
        footnote="God will not be known only by what He did in one lifetime.",
        caption="The covenant name is itself a statement of generational continuity.",
        source="Exodus 3:6, 15; Matthew 22:31\u201332."),

    "fig-01-9": dict(
        layout="matrix", chapter=2,
        title="Unfinished assignments in Genesis",
        data=dict(col_heads=["PROMISE RECEIVED", "WHAT REMAINED"],
                  row_heads=["Abraham", "Isaac", "Jacob", "Joseph"],
                  cells=[["the land and a seed", "possessed no acre of it"],
                         ["the oath confirmed", "re-opened his\nfather's wells"],
                         ["a house and a ladder", "ended his days\nin Egypt"],
                         ["preservation\nof the line", "saved what he could\nnot bequeath"]],
                  x0=0.34, tsize=6.0, csize=5.3),
        caption="Each patriarch died holding a promise his successor had to walk into.",
        source="Genesis 12; 26; 28; 45."),

    "fig-01-10": dict(
        layout="timeline", chapter=2,
        title="Four generations, one promise",
        data=dict(points=[
            ["ABRAHAM", "called out\nGenesis 12"],
            ["ISAAC", "the oath\nrenewed\nGenesis 26"],
            ["JACOB", "the ladder\nGenesis 28"],
            ["JOSEPH", "the line\npreserved\nGenesis 45"],
        ], above=True, alt=False, tsize=6.0, bsize=5.1),
        footnote="Four lifetimes elapse between the promise and its first instalment.",
        caption="The promise of Genesis travels through four generations before it "
                "reaches a land.",
        source="Genesis 12\u201350; Exodus 1:1\u20137."),
}

# ---------------------------------------------------------------------------
# PART II — THE MYSTICS, THE FATHERS AND THE LANGUAGE OF REVELATION (6\u201312)
# ---------------------------------------------------------------------------
PART2 = {
    "fig-02-1": dict(
        layout="chain", chapter=6,
        title="The ancient school of seeing",
        data=dict(items=[
            ["THE PROPHET", "Numbers 12:6\nspeaks what God\nputs in the mouth"],
            ["THE SEER", "1 Samuel 9:9\nperceives what is\nhidden"],
            ["THE DREAMER", "Genesis 37:5\nreceives while\nnot in control"],
            ["THE INTERPRETER", "Daniel 2:19\nexplains what\nanother received"],
        ], tsize=6.6, bsize=5.3),
        footnote="Revelation is older than its terminology; the names change, "
                 "the Giver does not.",
        caption="The four offices by which Scripture describes those who perceived "
                "what others could not.",
        source="1 Samuel 9:9; Numbers 12:6; Amos 3:7; Daniel 2."),

    "fig-02-2": dict(
        layout="quadrant", chapter=7,
        title="What God conceals and what He reveals",
        data=dict(x_label="OF WHOM",
                  y_label="WHEN",
                  cells=[["REVEALED AT ONCE", "the law and the testimony\nDeuteronomy 29:29"],
                         ["REVEALED LATER", "the mystery of the Gentiles\nColossians 1:26\u201327"],
                         ["CONCEALED IN ONE AGE", "the vision sealed for a time\nDaniel 12:4, 9"],
                         ["CONCEALED UNTIL THE END", "the appointed hour\nGalatians 4:4"]],
                  x0=0.15, x1=0.97, tsize=6.2, bsize=5.2,
                  lo=("given now", "withheld")),
        caption="Concealment is not failure of revelation; it is scheduling of it.",
        source="Deuteronomy 29:29; Daniel 2:20\u201322; Colossians 1:26\u201327."),

    "fig-02-3": dict(
        layout="before_after", chapter=8,
        title="A revelation that provokes before it serves",
        data=dict(before=["THE DREAM", "Genesis 37:5\u201311\n\n\u2022 a youthful word\n"
                                          "\u2022 told to the family\n\u2022 received with hatred\n"
                                          "\u2022 provokes the brothers"],
                  after=["THE FULFILMENT", "Genesis 41:14\u201316\n\n\u2022 the same young man\n"
                                           "\u2022 in a foreign court\n\u2022 the word now serves\n"
                                           "\u2022 preserves the family"],
                  arrow_text="thirteen years,\nand a prison", tsize=6.2, bsize=5.2),
        caption="Joseph's revelation provoked the very generation it would eventually save.",
        source="Genesis 37:1\u201311; 41:14\u201316."),

    "fig-02-4": dict(
        layout="twocol", chapter=9,
        title="When the child heard what the priest could not",
        data=dict(left=["ELI", ["the accustomed ear",
                                "the lamp not yet out",
                                "a word grown rare",
                                "the one who should have heard",
                                "1 Samuel 3:2\u20133"], "#F5EFE1", "#B9AE94", "#16223A"],
                  right=["SAMUEL", ["the inexperienced ear",
                                    "lying in the same room",
                                    "a word he did not recognise",
                                    "the one who finally answered",
                                    "1 Samuel 3:4\u201310"], "#FBF7EE", "#D9BE7A", "#16223A"]),
        footnote="\u201cSpeak; for thy servant heareth.\u201d \u2014 1 Samuel 3:10",
        caption="The transition of prophetic hearing from an established priest to a child.",
        source="1 Samuel 3:1\u201321."),

    "fig-02-5": dict(
        layout="twocol", chapter=10,
        title="What the army saw and what the shepherd saw",
        data=dict(left=["THE ARMY OF ISRAEL", ["forty days of siege",
                                               "a champion, nine feet tall",
                                               "the covenant of God",
                                               "conclusion: he is too great",
                                               "1 Samuel 17:11, 24"], "#F5EFE1", "#B9AE94"],
                  right=["THE YOUNG SHEPHERD", ["one afternoon of it",
                                                "a giant who defied God",
                                                "the same covenant",
                                                "conclusion: God is greater",
                                                "1 Samuel 17:45\u201347"], "#FBF7EE", "#D9BE7A"]),
        caption="The same facts, differently weighed, produced two opposite conclusions.",
        source="1 Samuel 17:1\u201351."),

    "fig-02-6": dict(
        layout="cycle", chapter=11,
        title="What the mantle carries",
        data=dict(items=[
            ["THE CALL", "1 Kings 19:19"],
            ["THE SERVICE", "2 Kings 3:11"],
            ["THE REQUEST", "2 Kings 2:9"],
            ["THE PARTING", "2 Kings 2:11\u201312"],
            ["THE RETURN", "the Jordan crossed"],
            ["THE PROOF", "2 Kings 2:14"],
        ], rx=0.31, ry=0.29, r=0.084, tsize=5.6),
        footnote="A mantle can be picked up in a moment; the God of the mantle "
                 "must be known over years.",
        caption="The succession of Elisha: possession of the mantle preceded proof of the power.",
        source="1 Kings 19:19\u201321; 2 Kings 2:1\u201315."),

    "fig-02-7": dict(
        layout="twocol", chapter=12,
        title="Babylon's wisdom and the wisdom of God",
        data=dict(left=["THE LEARNING OF BABYLON", ["books, tongues, astronomy",
                                                    "the university of its age",
                                                    "access, patronage, salary",
                                                    "adjudged ten times better",
                                                    "Daniel 1:17\u201320"], "#F5EFE1", "#B9AE94"],
                  right=["THE WISDOM OF GOD", ["hidden and not taught",
                                                "given in the night",
                                                "prayer, not research",
                                                "adjudged worth a kingdom",
                                                "Daniel 2:19\u201323"], "#FBF7EE", "#D9BE7A"]),
        footnote="The young men did not refuse Babylon's learning; they refused to "
                 "be defined by it.",
        caption="Divine revelation did not replace imperial learning; it exceeded it.",
        source="Daniel 1:8\u201320; 2:17\u201323."),

    "fig-02-8": dict(
        layout="stages", chapter=6,
        title="How a seer is formed",
        data=dict(items=[
            ["CHOSEN", "the initiative is God's, not the candidate's \u2014 Amos 7:15"],
            ["SEPARATED", "withdrawn for a season \u2014 1 Kings 17:2\u20136"],
            ["SCHOOLED", "in Scripture before vision \u2014 1 Samuel 3:21"],
            ["SENT", "and told what to say \u2014 Jeremiah 1:7"],
            ["SUSTAINED", "through opposition \u2014 1 Kings 18:17\u201318"],
            ["SEALED", "by the fulfilment of the word \u2014 1 Samuel 3:19"],
        ], tsize=6.3, bsize=5.3),
        caption="The six movements by which Scripture describes the making of a seer.",
        source="Amos 3:7; 1 Samuel 3; Jeremiah 1."),
}

# ---------------------------------------------------------------------------
# PART III — WHY THE YOUNG? (13\u201318)
# ---------------------------------------------------------------------------
PART3 = {
    "fig-03-1": dict(
        layout="twocol", chapter=13,
        title="God's preference for the unexpected",
        data=dict(left=["WHAT HUMAN ASSESSMENT COUNTS", ["age and seniority",
                                                          "visible credentials",
                                                          "prior record",
                                                          "the approval of peers",
                                                          "1 Corinthians 1:26"], "#F5EFE1", "#B9AE94"],
                  right=["WHAT SCRIPTURE REPEATEDLY RECORDS", ["availability",
                                                                "faith before proof",
                                                                "obscurity before honour",
                                                                "the choice of God",
                                                                "1 Corinthians 1:27\u201329"], "#FBF7EE", "#D9BE7A"]),
        footnote="\u201cOut of the mouth of babes and sucklings hast thou ordained strength.\u201d "
                 "Psalm 8:2",
        caption="The contradiction between human qualification and divine selection.",
        source="Psalm 8:2; Matthew 21:15\u201316; 1 Corinthians 1:26\u201329."),

    "fig-03-2": dict(
        layout="before_after", chapter=14,
        title="The two voices over a young calling",
        data=dict(before=["\u201cI AM A CHILD\u201d", "Jeremiah 1:6\n\n\u2022 the protest of\n  inadequacy\n"
                                                   "\u2022 accurate self-assessment\n\u2022 the instinct to decline\n"
                                                   "\u2022 rooted in age"],
                  after=["\u201cSAY NOT, I AM A CHILD\u201d", "Jeremiah 1:7\u20138\n\n\u2022 the overruling word\n"
                                                              "\u2022 a command to speak\n\u2022 a promise of presence\n"
                                                              "\u2022 rooted in commission"],
                  arrow_text="the word\nof God\nintervenes", tsize=6.2, bsize=5.2),
        caption="The divine confrontation with the insecurity of youthful calling.",
        source="Jeremiah 1:4\u201310."),

    "fig-03-3": dict(
        layout="timeline", chapter=15,
        title="Josiah: the boy who found the book",
        data=dict(points=[
            ["8 YEARS OLD", "began to reign\n2 Kings 22:1"],
            ["16 YEARS OLD", "began to seek\n2 Chronicles 34:3"],
            ["20 YEARS OLD", "began to purge\n2 Chronicles 34:3"],
            ["26 YEARS OLD", "the book found\n2 Kings 22:8"],
            ["THE REFORM", "the covenant\nrenewed 2 Kings 23"],
        ], above=True, tsize=5.9, bsize=5.0),
        caption="A young king's reformation, and the recovery of a book his "
                "predecessors had neglected.",
        source="2 Kings 22:1\u201323:25; 2 Chronicles 34."),

    "fig-03-4": dict(
        layout="stages", chapter=16,
        title="What a young minister must hold",
        data=dict(items=[
            ["THE WORD", "give attendance to reading, to exhortation, to doctrine \u2014 1 Timothy 4:13"],
            ["THE GIFT", "neglect not the gift that is in thee \u2014 1 Timothy 4:14"],
            ["THE LIFE", "meditate upon these things; give thyself wholly to them \u2014 1 Timothy 4:15"],
            ["THE DOCTRINE", "take heed unto thyself, and unto the doctrine \u2014 1 Timothy 4:16"],
            ["THE EXAMPLE", "be thou an example of the believers \u2014 1 Timothy 4:12"],
            ["THE DEPOSIT", "keep that good thing committed unto thee \u2014 2 Timothy 1:14"],
        ], tsize=6.2, bsize=5.2),
        caption="Paul's charge to a young man: five things to guard and one to become.",
        source="1 Timothy 4:12\u201316; 2 Timothy 1:13\u201314."),

    "fig-03-5": dict(
        layout="chain", chapter=17,
        title="The theology of spiritual reproduction",
        data=dict(items=[
            ["PAUL", "the father in\nthe faith\nTitus 1:4"],
            ["TITUS", "the son who\nis sent\nTitus 1:5"],
            ["THE ELDERS", "appointed in\nevery city"],
            ["THE HOUSEHOLDS", "taught what is\nsound\nTitus 2:1\u20138"],
            ["THE NEXT", "a generation\nthat teaches"],
        ], tsize=6.4, bsize=5.2, gap=0.022),
        caption="Spiritual reproduction as a deliberate chain rather than an accident.",
        source="Titus 1:4\u20135; 2:1\u20138."),

    "fig-03-6": dict(
        layout="spectrum", chapter=18,
        title="What \u201clet no man despise thy youth\u201d does and does not mean",
        data=dict(left_pole="does NOT mean",
                  right_pole="DOES mean",
                  marks=[
                      ["age is irrelevant", "age is not the qualification"],
                      ["experience is worthless", "experience is not the arbiter"],
                      ["correction is rebellion", "correction is received"],
                      ["office may be seized", "office must be given"],
                  ], tsize=5.9, bsize=5.0),
        footnote="Authority is not demanded by the young; it is earned and granted.",
        caption="The boundary between rightful youthful confidence and youthful presumption.",
        source="1 Timothy 4:12; 1 Peter 5:5."),
}

# ---------------------------------------------------------------------------
# PART IV — THE FATHERS (19\u201325)
# ---------------------------------------------------------------------------
PART4 = {
    "fig-04-1": dict(
        layout="stages", chapter=19,
        title="What elders must speak",
        data=dict(items=[
            ["TESTIMONY", "what God has done \u2014 Psalm 71:17\u201318"],
            ["INSTRUCTION", "what God requires \u2014 Psalm 71:17"],
            ["PRAISE", "who God is \u2014 Psalm 145:4"],
            ["WARNING", "what destroys a generation \u2014 Judges 2:10\u201313"],
            ["BLESSING", "what is bequeathed \u2014 Genesis 49:1"],
            ["NAME", "what is inherited \u2014 Proverbs 20:7"],
        ], tsize=6.3, bsize=5.3),
        caption="The six deposits an elder is responsible to leave behind.",
        source="Psalm 71:17\u201318; Psalm 145:4; Judges 2."),

    "fig-04-2": dict(
        layout="funnel", chapter=20,
        title="The anatomy of a silent generation",
        data=dict(stages_list=[
            ["A generation that knew", "they had seen the works of God"],
            ["They gathered to their fathers", "the witnesses leave the stage"],
            ["No declaration was made", "the deeds were not rehearsed"],
            ["Another generation arose", "which knew not the Lord"],
            ["And did evil", "the vacuum filled itself"],
        ], tsize=6.2, bsize=5.2),
        footnote="\u201cThere arose another generation which knew not the Lord.\u201d "
                 "Judges 2:10",
        caption="Judges 2:10 read as a failure of transmission rather than of opportunity.",
        source="Judges 2:7\u201310; Hosea 4:6."),

    "fig-04-3": dict(
        layout="quadrant", chapter=21,
        title="Institutional failure and prophetic awakening",
        data=dict(x_label="THE INSTITUTION",
                  y_label="THE VOICE",
                  cells=[["ELI'S HOUSE", "a father who did not restrain\n1 Samuel 2:29"],
                         ["THE WORD RARE", "no open vision\n1 Samuel 3:1"],
                         ["THE FAITHFUL PRIEST", "the lamp still burning\n1 Samuel 3:3"],
                         ["THE CHILD CALLED", "a new ear opened\n1 Samuel 3:10"]],
                  x0=0.15, x1=0.97, tsize=6.2, bsize=5.2,
                  lo=("failing", "faithful")),
        footnote="God does not wait for an institution to reform before He speaks.",
        caption="A new prophetic generation emerging from within a failing order.",
        source="1 Samuel 2:27\u201336; 3:1\u201321."),

    "fig-04-4": dict(
        layout="stages", chapter=22,
        title="The last words of a father",
        data=dict(items=[
            ["\u201cBE THOU STRONG\u201d", "the charge to courage \u2014 1 Kings 2:2"],
            ["\u201cKEEP THE CHARGE OF THE LORD\u201d", "the charge to obedience \u2014 1 Kings 2:3"],
            ["\u201cTHAT THE LORD MAY CONTINUE HIS WORD\u201d", "the reason for it \u2014 1 Kings 2:4"],
            ["\u201cTHOU SHALT BRING DOWN TO THE GRAVE\u201d", "the unfinished business \u2014 1 Kings 2:5\u20139"],
            ["\u201cSO DAVID SLEPT WITH HIS FATHERS\u201d", "the end of a reign \u2014 1 Kings 2:10"],
        ], tsize=6.2, bsize=5.2),
        caption="David's final instruction: what a father leaves in his son's hands.",
        source="1 Kings 2:1\u201312."),

    "fig-04-5": dict(
        layout="chain", chapter=23,
        title="The architecture of deliberate succession",
        data=dict(items=[
            ["NUMBERED", "Moses is told\nhe shall not\npass over"],
            ["DESIGNATED", "Joshua is named\nbefore the people"],
            ["COMMISSIONED", "hands laid,\ncharge given"],
            ["ENCOURAGED", "twice: \u201cbe strong\nand of a good courage\u201d"],
            ["AUTHORISED", "the people\nobey him"],
        ], tsize=6.4, bsize=5.2, gap=0.022),
        footnote="Transition improvised under pressure is the commonest way a work "
                 "is lost; Scripture models the opposite.",
        caption="Five movements by which Moses deliberately handed over to Joshua.",
        source="Numbers 27:18\u201323; Deuteronomy 31:1\u20138, 23; Joshua 1:1\u20139."),

    "fig-04-6": dict(
        layout="bridge", chapter=24,
        title="Refusing to die with your knowledge",
        data=dict(left="PAUL\nthe apostle",
                  right="THE CHURCH\nof the next age",
                  spans=[
                      ["A DEPOSIT", "\u201cthe things that thou hast heard of me\u201d"],
                      ["A WITNESS", "committed \u201camong many witnesses\u201d"],
                      ["A RECIPIENT", "\u201cto faithful men\u201d"],
                      ["A METHOD", "\u201cwho shall be able to teach others also\u201d"],
                  ], tsize=6.2, bsize=5.4, label_size=5.6),
        caption="2 Timothy 2:2 as the apostolic mechanism for preserving revelation.",
        source="2 Timothy 2:1\u20132."),

    "fig-04-7": dict(
        layout="layers", chapter=25,
        title="The wisdom that must be spilled",
        data=dict(x0=0.03, x1=0.97, gap=0.014, tsize=6.3,
                  rows=[
                      ["HIDDEN", "wisdom retained and never spoken"],
                      ["DELAYED", "wisdom deferred to a convenient season"],
                      ["INTERRUPTED", "the teacher dies with the lesson untaught"],
                      ["LOST", "the next generation pays the price in full"],
                  ], side_labels=["the fault", "the cost"]),
        footnote="\u201cA good man leaveth an inheritance to his children's children.\u201d "
                 "Proverbs 13:22",
        caption="Four stages between possessing wisdom and losing it.",
        source="Proverbs 13:22; 20:7; Psalm 78:5\u20136."),
}

# ---------------------------------------------------------------------------
# PART V — THE HIDDEN ARCHITECTURE (26\u201332)
# ---------------------------------------------------------------------------
PART5 = {
    "fig-05-1": dict(
        layout="timeline", chapter=26,
        title="Revelation has a timeline",
        data=dict(points=[
            ["THE WORD SPOKEN", "Abraham, Genesis 12"],
            ["THE WORD WRITTEN", "Habakkuk 2:2"],
            ["THE WORD WAITED FOR", "Habakkuk 2:3"],
            ["THE SEASON APPOINTED", "Galatians 4:4"],
            ["THE WORD PERFORMED", "the fulness of time"],
        ], above=True, tsize=5.9, bsize=5.0),
        footnote="\u201cThough it tarry, wait for it; because it will surely come.\u201d "
                 "Habakkuk 2:3",
        caption="The interval between a word spoken and the generation appointed to fulfil it.",
        source="Habakkuk 2:2\u20133; Galatians 4:4."),

    "fig-05-2": dict(
        layout="cycle", chapter=27,
        title="Seed, soil and season",
        data=dict(items=[
            ["THE SEED", "Mark 4:26"],
            ["THE SOIL", "Mark 4:28"],
            ["THE BLADE", "first the blade"],
            ["THE EAR", "then the ear"],
            ["THE FULL CORN", "after that the full corn"],
            ["THE HARVEST", "immediately the sickle"],
        ], rx=0.31, ry=0.29, r=0.085, tsize=5.6),
        footnote="\u201cThe earth bringeth forth fruit of herself.\u201d Mark 4:28",
        caption="The growth of a divine purpose through successive stages, none of "
                "which can be hurried.",
        source="Genesis 8:22; Ecclesiastes 3:1\u20138; Mark 4:26\u201329."),

    "fig-05-3": dict(
        layout="vchain", chapter=28,
        title="From revelation to responsibility",
        data=dict(items=[
            ["TO ONE PERSON", "the word is given privately \u2014 Genesis 12:1"],
            ["TO A HOUSEHOLD", "the word is shared and believed \u2014 Genesis 18:19"],
            ["TO A PEOPLE", "the word becomes covenant \u2014 Exodus 19:5\u20136"],
            ["TO A GENERATION", "the word becomes commission \u2014 Joshua 1:2"],
            ["TO THE NATIONS", "the word becomes mission \u2014 Acts 1:8"],
        ], tsize=6.3, bsize=5.3),
        caption="The widening scope through which a revelation becomes a responsibility.",
        source="Isaiah 59:21; 2 Timothy 2:2."),

    "fig-05-4": dict(
        layout="twocol", chapter=29,
        title="The mantle, the message and the man",
        data=dict(left=["WHAT CAN BE TRANSMITTED", ["the mantle \u2014 an office",
                                                      "the message \u2014 a doctrine",
                                                      "the method \u2014 a practice",
                                                      "the memory \u2014 a story",
                                                      "2 Kings 2:13"], "#FBF7EE", "#D9BE7A"],
                  right=["WHAT CANNOT", ["the anointing \u2014 it is God's",
                                          "the encounter \u2014 it is personal",
                                          "the character \u2014 it is grown",
                                          "the call \u2014 it is sovereign",
                                          "1 Corinthians 3:6\u20137"], "#F5EFE1", "#B9AE94"]),
        caption="Distinguishing spiritual inheritance from personality imitation.",
        source="2 Kings 2:9\u201315; 1 Corinthians 3:4\u20137."),

    "fig-05-5": dict(
        layout="before_after", chapter=30,
        title="When the student becomes the carrier",
        data=dict(before=["THE DISCIPLE", "John 14:12\n\n\u2022 receives instruction\n"
                                          "\u2022 follows the master\n\u2022 repeats what he hears\n"
                                          "\u2022 is measured by the teacher"],
                  after=["THE APOSTLE", "Acts 2:14\n\n\u2022 gives instruction\n"
                                        "\u2022 leads the community\n\u2022 speaks with authority\n"
                                        "\u2022 is measured by the truth"],
                  arrow_text="Pentecost", tsize=6.2, bsize=5.2),
        caption="The moment a learner becomes responsible for what he has received.",
        source="John 14:12; Acts 2:14\u201321."),

    "fig-05-6": dict(
        layout="balance", chapter=31,
        title="Neither fatherless nor childless",
        data=dict(left=["THE YOUNG MUST NOT BECOME FATHERLESS",
                        "vision without\nwisdom becomes\nundisciplined"],
                  right=["THE FATHERS MUST NOT BECOME CHILDLESS",
                         "wisdom without\nvision becomes\nsterile"],
                  tsize=5.7, bsize=5.0),
        footnote="\u201cHe shall turn the heart of the fathers to the children, and the "
                 "heart of the children to their fathers.\u201d Malachi 4:6",
        caption="The equilibrium Scripture requires between the two dangers.",
        source="Malachi 4:5\u20136; Titus 2:1\u20138."),

    "fig-05-7": dict(
        layout="chain", chapter=32,
        title="Recognising what God is doing elsewhere",
        data=dict(items=[
            ["JOSHUA", "would rather\nsilence them\nNumbers 11:28"],
            ["MOSES", "would rather\nshare the Spirit\nNumbers 11:29"],
            ["THE DISCIPLE", "forbade the outsider\nMark 9:38"],
            ["CHRIST", "forbade the forbidding\nMark 9:39"],
        ], tsize=6.6, bsize=5.2),
        footnote="Envy of another's gift is the surest sign that a gift has become "
                 "an identity.",
        caption="The elder's test: can he rejoice in a work he does not control?",
        source="Numbers 11:27\u201329; Acts 21:8\u20139; Mark 9:38\u201340."),
}

# ---------------------------------------------------------------------------
# PART VI — WHEN GENERATIONS COLLIDE (33\u201338)
# ---------------------------------------------------------------------------
PART6 = {
    "fig-06-1": dict(
        layout="stages", chapter=33,
        title="How the old guard fears the new",
        data=dict(items=[
            ["THE SONG", "the women sing of David \u2014 1 Samuel 18:7"],
            ["THE COMPARISON", "Saul measures himself against a youth \u2014 18:8"],
            ["THE SUSPICION", "from that day Saul eyed David \u2014 18:9"],
            ["THE FEAR", "Saul was afraid of David \u2014 18:12"],
            ["THE MACHINERY", "the throne turns against him \u2014 18:13\u201316"],
            ["THE LOSS", "a kingdom forfeited to keep a crown \u2014 31:4"],
        ], tsize=6.2, bsize=5.2),
        caption="The progressive sequence by which insecurity hardens into opposition.",
        source="1 Samuel 18:6\u201316."),

    "fig-06-2": dict(
        layout="twocol", chapter=34,
        title="Rehoboam's two counsels",
        data=dict(left=["THE OLD MEN", ["\u201cserve them this day\u201d",
                                        "the counsel of restraint",
                                        "the memory of how the throne was won",
                                        "rejected in three days",
                                        "1 Kings 12:6\u20137"], "#FBF7EE", "#D9BE7A"],
                  right=["THE YOUNG MEN", ["\u201cmy little finger shall be thicker\u201d",
                                           "the counsel of display",
                                           "no memory of how the throne was won",
                                           "accepted at once",
                                           "1 Kings 12:8\u201311"], "#F5EFE1", "#B9AE94"]),
        footnote="Ten tribes were lost in a single afternoon of misplaced confidence.",
        caption="Two counsels, one decision, and the division of a kingdom.",
        source="1 Kings 12:1\u201319."),

    "fig-06-3": dict(
        layout="quadrant", chapter=35,
        title="Age and wisdom are not the same thing",
        data=dict(x_label="AGE",
                  y_label="COUNSEL",
                  cells=[["OLD AND FOOLISH", "experience without discernment\n1 Kings 12:6"],
                         ["OLD AND WISE", "experience tested by God\nProverbs 16:31"],
                         ["YOUNG AND FOOLISH", "confidence without knowledge\n1 Kings 12:10"],
                         ["YOUNG AND WISE", "humility with courage\n1 Timothy 4:12"]],
                  x0=0.15, x1=0.97, tsize=6.2, bsize=5.2,
                  lo=("young", "old")),
        footnote="Neither youthfulness nor grey hair is a qualification; both are "
                 "occasions for either wisdom or folly.",
        caption="Scripture refuses to equate age with wisdom, or youth with discernment.",
        source="1 Kings 12:6\u201315; Proverbs 1:7; 12:15; 16:31."),

    "fig-06-4": dict(
        layout="timeline", chapter=36,
        title="John Mark: failure and restoration",
        data=dict(points=[
            ["THE HOME", "his mother's house\nActs 12:12"],
            ["THE FIRST JOURNEY", "sent with Paul\nActs 13:5"],
            ["THE DEPARTURE", "returned to\nJerusalem Acts 13:13"],
            ["THE QUARREL", "Paul and Barnabas\npart Acts 15:39"],
            ["THE RESTORATION", "\u201che is profitable\nto me\u201d 2 Tim 4:11"],
        ], above=True, alt=True, tsize=5.8, bsize=4.9),
        footnote="Paul's last letter names the man he had once refused.",
        caption="A young worker's failure, and the twenty years that followed it.",
        source="Acts 12:12; 13:5, 13; 15:36\u201340; 2 Timothy 4:11."),

    "fig-06-5": dict(
        layout="before_after", chapter=37,
        title="Elijah's crisis and Elisha's emergence",
        data=dict(before=["THE EXHAUSTED PROPHET", "1 Kings 19:4\n\n\u2022 flees to Beersheba\n"
                                                    "\u2022 sits under a juniper\n\u2022 asks to die\n"
                                                    "\u2022 \u201cI only am left\u201d"],
                  after=["THE ANOINTED SUCCESSOR", "1 Kings 19:19\n\n\u2022 twelve yoke of oxen\n"
                                                    "\u2022 a mantle cast\n\u2022 a feast of farewell\n"
                                                    "\u2022 \u201che arose and followed\u201d"],
                  arrow_text="God's answer to\ndespair is not rest\nbut a successor",
                  tsize=6.0, bsize=5.1),
        caption="Exhaustion in one generation became the occasion for preparing another.",
        source="1 Kings 19:1\u201321."),

    "fig-06-6": dict(
        layout="twocol", chapter=38,
        title="Memory and movement",
        data=dict(left=["MEMORY KEPT RIGHTLY", ["\u201cwe will not hide them\u201d",
                                                 "the past as testimony",
                                                 "rehearsed, not idolised",
                                                 "produces hope, v. 7",
                                                 "Psalm 78:4\u20137"], "#FBF7EE", "#D9BE7A"],
                  right=["MEMORY BECOME A TRAP", ["\u201cthe former things\u201d",
                                                   "the past as possession",
                                                   "guarded, not released",
                                                   "produces stagnation",
                                                   "Isaiah 43:18\u201319"], "#F5EFE1", "#B9AE94"]),
        footnote="\u201cRemember ye not the former things \u2026 behold, I will do a new thing.\u201d "
                 "Isaiah 43:18\u201319",
        caption="The same memory can preserve a people or imprison them.",
        source="Isaiah 43:18\u201319; Philippians 3:13\u201314."),
}

# ---------------------------------------------------------------------------
# PART VII — THE CHRIST PATTERN (39\u201344)
# ---------------------------------------------------------------------------
PART7 = {
    "fig-07-1": dict(
        layout="stages", chapter=39,
        title="The Son who received",
        data=dict(items=[
            ["THE SON CAN DO NOTHING OF HIMSELF", "John 5:19 \u2014 dependence"],
            ["WHAT HE SEES THE FATHER DO, HE DOES", "John 5:19 \u2014 imitation"],
            ["THE FATHER LOVETH THE SON", "John 5:20 \u2014 affection"],
            ["AND SHEWETH HIM ALL THINGS", "John 5:20 \u2014 revelation"],
            ["I DO ALWAYS THOSE THINGS THAT PLEASE HIM", "John 8:29 \u2014 obedience"],
            ["THE FATHER THAT DWELLETH IN ME, HE DOETH THE WORKS", "John 14:10 \u2014 union"],
        ], tsize=6.1, bsize=5.1),
        footnote="Biblical succession begins in relationship, not in ambition.",
        caption="The six statements in which Christ described His own succession from the Father.",
        source="John 5:19\u201320; 8:28\u201329; 14:10."),

    "fig-07-2": dict(
        layout="chain", chapter=40,
        title="Christ's investment in an unlikely generation",
        data=dict(items=[
            ["HE CHOSE", "Mark 3:13\n\u201cthat they should\nbe with him\u201d"],
            ["HE ORDAINED", "Mark 3:14\n\u201cthat he might\nsend them forth\u201d"],
            ["HE TRAINED", "Mark 6:7\nsent two by two\nwith authority"],
            ["HE CORRECTED", "Mark 9:33\u201337\nthe argument\nabout greatness"],
            ["HE SENT", "Matthew 28:19\nto all nations\nwith all authority"],
        ], tsize=6.4, bsize=5.1, gap=0.022),
        footnote="None of the twelve was qualified at the point of calling.",
        caption="The five movements of Christ's preparation of His successors.",
        source="Mark 3:13\u201319; 6:7\u201313; Matthew 28:18\u201320."),

    "fig-07-3": dict(
        layout="spectrum", chapter=41,
        title="Reading \u201cgreater works\u201d",
        data=dict(left_pole="the narrower reading",
                  right_pole="the wider reading",
                  marks=[
                      ["greater in number", "the disciples outnumber the Master"],
                      ["greater in extent", "the gospel reaches the nations"],
                      ["greater in duration", "the work outlives the Worker"],
                      ["never greater in kind", "no work exceeds the cross"],
                  ], tsize=5.8, bsize=4.9),
        footnote="The greater works are the works of a body, not of a rival.",
        caption="What John 14:12 does and does not claim about those who follow Christ.",
        source="John 14:12; Acts 1:8."),

    "fig-07-4": dict(
        layout="twocol", chapter=42,
        title="Pentecost: one Spirit, four generations",
        data=dict(left=["JOEL'S FOUR", ["your sons shall prophesy",
                                        "your daughters shall prophesy",
                                        "your young men shall see visions",
                                        "your old men shall dream dreams",
                                        "Joel 2:28"], "#FBF7EE", "#D9BE7A"],
                  right=["PETER'S READING", ["\u201cthis is that which was spoken\u201d",
                                             "not a new promise but an old one",
                                             "one outpouring, many ages",
                                             "no generation excluded",
                                             "Acts 2:16\u201318"], "#F5EFE1", "#B9AE94"]),
        footnote="The Spirit did not come to one generation; He came to all of them at once.",
        caption="The multigenerational character of the prophetic outpouring.",
        source="Joel 2:28\u201329; Acts 2:16\u201318."),
}

# ---------------------------------------------------------------------------
# PART VIII — WHEN THE YOUNG RECEIVE (45\u201350)
# ---------------------------------------------------------------------------
PART8 = {
    "fig-08-1": dict(
        layout="before_after", chapter=45,
        title="The generation that entered",
        data=dict(before=["THE WILDERNESS GENERATION", "Numbers 14:29\u201330\n\n\u2022 left Egypt\n"
                                                        "\u2022 saw the works\n\u2022 refused the word\n"
                                                        "\u2022 died before the river"],
                  after=["THE JOSHUA GENERATION", "Joshua 1:2\n\n\u2022 born in the wilderness\n"
                                                   "\u2022 believed the word\n\u2022 crossed the river\n"
                                                   "\u2022 possessed the promise"],
                  arrow_text="the promise does not\nlapse with the\npeople who first heard it",
                  tsize=6.0, bsize=5.1),
        caption="Two generations, one promise: the second entered what the first could only approach.",
        source="Joshua 1:1\u20139; 21:43\u201345."),

    "fig-08-2": dict(
        layout="tree", chapter=46,
        title="The builders after the exile",
        data=dict(root="THE RETURN FROM BABYLON",
                  children=[
                      ["ZERUBBABEL", "the temple\nEzra 3:8"],
                      ["JESHUA", "the altar and\nthe priesthood"],
                      ["EZRA", "the law read\nand taught"],
                      ["NEHEMIAH", "the wall\nbuilt in fifty-two days"],
                  ], tsize=6.0, bsize=5.2),
        footnote="\u201cThe people had a mind to work.\u201d Nehemiah 4:6",
        caption="Four leaders, one recovery: the rebuilding of a broken inheritance.",
        source="Ezra 3:8\u201313; Nehemiah 2:17\u201320."),

    "fig-08-3": dict(
        layout="vchain", chapter=47,
        title="A fresh voice within an old institution",
        data=dict(items=[
            ["THE INSTITUTION REMAINS", "the tabernacle, the priesthood, the lamp \u2014 1 Samuel 3:3"],
            ["THE WORD GROWS RARE", "there was no open vision \u2014 1 Samuel 3:1"],
            ["THE VOICE IS RAISED", "Samuel is called by name \u2014 1 Samuel 3:10"],
            ["THE INSTITUTION IS CORRECTED", "the word is told to Eli \u2014 1 Samuel 3:18"],
            ["THE STRUCTURE IS RENEWED", "all Israel heard that Samuel was established \u2014 1 Samuel 3:20"],
        ], tsize=6.1, bsize=5.1),
        caption="Renewal that repairs a structure rather than destroying it.",
        source="1 Samuel 3:19\u201321."),

    "fig-08-4": dict(
        layout="stages", chapter=48,
        title="When the new generation finds the old book",
        data=dict(items=[
            ["THE DISCOVERY", "the book is found in the house of the Lord \u2014 2 Kings 22:8"],
            ["THE READING", "Shaphan reads it before the king \u2014 2 Kings 22:10"],
            ["THE RENDING", "the king rends his clothes \u2014 2 Kings 22:11"],
            ["THE ENQUIRY", "they ask of the Lord \u2014 2 Kings 22:13"],
            ["THE COVENANT", "the king makes a covenant \u2014 2 Kings 23:3"],
            ["THE REFORMATION", "the high places are removed \u2014 2 Kings 23:4\u201320"],
        ], tsize=6.1, bsize=5.1),
        footnote="What the older generation had neglected, the younger one restored.",
        caption="Reformation as the recovery of an inherited text.",
        source="2 Kings 22:8\u201313; 23:1\u201325."),

    "fig-08-5": dict(
        layout="radial", chapter=49,
        title="One Spirit, every kind of witness",
        data=dict(centre="THE\nOUTPOURED\nSPIRIT",
                  spokes=[
                      ["SONS", "prophesy\nJoel 2:28"],
                      ["DAUGHTERS", "prophesy\nJoel 2:28"],
                      ["OLD MEN", "dream dreams\nJoel 2:28"],
                      ["YOUNG MEN", "see visions\nJoel 2:28"],
                      ["SERVANTS", "receive the Spirit\nJoel 2:29"],
                      ["HANDMAIDS", "receive the Spirit\nJoel 2:29"],
                  ], rx=0.315, ry=0.315, r=0.085, tsize=5.4, bsize=4.8),
        footnote="The Spirit's coming dismantled the assumption that revelation "
                 "belongs to a class.",
        caption="The democratisation of prophetic witness at Pentecost.",
        source="Joel 2:28\u201329; Acts 2:17\u201318."),

    "fig-08-6": dict(
        layout="bridge", chapter=50,
        title="One sows, another reaps",
        data=dict(left="THE SOWERS\nwho did not see",
                  right="THE REAPERS\nwho did not sow",
                  spans=[
                      ["THE LABOUR", "\u201cother men laboured\u201d \u2014 John 4:38"],
                      ["THE ENTRY", "\u201cye are entered into their labours\u201d"],
                      ["THE SHARING", "\u201che that reapeth receiveth wages\u201d"],
                      ["THE JOY", "\u201cthat he that soweth and he that reapeth\nmay rejoice together\u201d"],
                  ], tsize=6.0, bsize=5.2, label_size=5.5),
        caption="Inheriting an assignment without claiming ownership of it.",
        source="John 4:34\u201338; 1 Corinthians 3:6\u20139."),
}

# ---------------------------------------------------------------------------
# PART IX — THE DANGERS ON BOTH SIDES (51\u201356)
# ---------------------------------------------------------------------------
PART9 = {
    "fig-09-1": dict(
        layout="quadrant", chapter=51,
        title="Two failures, four faces",
        data=dict(x_label="ATTITUDE TO THE PAST",
                  y_label="ATTITUDE TO AUTHORITY",
                  cells=[["THE ARROGANT YOUNG", "revelation used as a licence\nProverbs 1:7"],
                         ["THE REBELLIOUS YOUNG", "correction refused\n1 Peter 5:5"],
                         ["THE HUMBLE YOUNG", "teachable and bold\n1 Timothy 4:12"],
                         ["THE IDOLATROUS ELDER", "tradition defended as truth\nMark 7:8\u201313"]],
                  x0=0.15, x1=0.97, tsize=6.0, bsize=5.1,
                  lo=("disregarded", "revered")),
        caption="The dangers that face each generation, and the narrow path between them.",
        source="Proverbs 1:7; 12:15; Matthew 15:1\u20139; 1 Peter 5:5."),

    "fig-09-2": dict(
        layout="spectrum", chapter=53,
        title="Tradition: the servant or the master",
        data=dict(left_pole="TRADITION AS SERVANT",
                  right_pole="TRADITION AS MASTER",
                  marks=[
                      ["carries the word", "replaces the word"],
                      ["is judged by Scripture", "judges Scripture"],
                      ["is open to reform", "resists correction"],
                      ["produces worship", "produces pride"],
                  ], tsize=5.7, bsize=4.9),
        footnote="\u201cLaying aside the commandment of God, ye hold the tradition of men.\u201d "
                 "Mark 7:8",
        caption="The same word describes a faithful inheritance and a fatal substitute.",
        source="Mark 7:6\u201313."),

    "fig-09-3": dict(
        layout="stages", chapter=54,
        title="Testing a claimed revelation",
        data=dict(items=[
            ["IS IT IN SCRIPTURE?", "\u201cto the law and to the testimony\u201d \u2014 Isaiah 8:20"],
            ["IS IT SEARCHED DAILY?", "\u201cthey searched the scriptures daily\u201d \u2014 Acts 17:11"],
            ["DOES IT HONOUR CHRIST?", "every spirit that confesseth \u2014 1 John 4:2"],
            ["DOES IT PRODUCE GOOD FRUIT?", "by their fruits ye shall know them \u2014 Matthew 7:16"],
            ["DOES IT EDIFY THE BODY?", "let all things be done unto edifying \u2014 1 Corinthians 14:26"],
            ["DOES IT ENDURE EXAMINATION?", "prove all things; hold fast that which is good \u2014 1 Thessalonians 5:21"],
        ], tsize=6.0, bsize=5.0),
        caption="Six tests Scripture applies to every claim of revelation.",
        source="Isaiah 8:20; Acts 17:10\u201311; 1 Thessalonians 5:19\u201322."),

    "fig-09-4": dict(
        layout="twocol", chapter=55,
        title="Gift and character",
        data=dict(left=["WHAT GIFT CAN DO", ["open doors",
                                              "draw a crowd",
                                              "produce results",
                                              "operate instantly",
                                              "Matthew 7:22"], "#F5EFE1", "#B9AE94"],
                  right=["WHAT ONLY CHARACTER CAN DO", ["keep a door open honourably",
                                                         "sustain a crowd",
                                                         "preserve the fruit",
                                                         "grow over decades",
                                                         "Galatians 5:22\u201323"], "#FBF7EE", "#D9BE7A"]),
        footnote="\u201cMany will say to me in that day \u2026 I never knew you.\u201d "
                 "Matthew 7:22\u201323",
        caption="Why divine gifting cannot substitute for spiritual maturity.",
        source="Matthew 7:21\u201323; Galatians 5:22\u201323."),

    "fig-09-5": dict(
        layout="before_after", chapter=56,
        title="Hearing and doing",
        data=dict(before=["THE HEARER ONLY", "James 1:23\u201324\n\n\u2022 looks into the mirror\n"
                                             "\u2022 sees accurately\n\u2022 forgets immediately\n"
                                             "\u2022 is unchanged"],
                  after=["THE DOER", "James 1:25\n\n\u2022 continues in the perfect law\n"
                                      "\u2022 is not a forgetful hearer\n\u2022 acts on what is seen\n"
                                      "\u2022 is blessed in his deed"],
                  arrow_text="the mirror\nmust be obeyed\nnot admired", tsize=6.0, bsize=5.1),
        caption="The difference between preserved knowledge and embodied obedience.",
        source="James 1:22\u201325."),
}

# ---------------------------------------------------------------------------
# PART X — REBUILDING THE GENERATIONAL COVENANT (57\u201362)
# ---------------------------------------------------------------------------
PART10 = {
    "fig-10-1": dict(
        layout="twocol", chapter=57,
        title="Followers and sons",
        data=dict(left=["A FOLLOWER", ["attached to a message",
                                        "leaves when the message changes",
                                        "counts the cost of staying",
                                        "is loyal while it is convenient",
                                        "John 6:66"], "#F5EFE1", "#B9AE94"],
                  right=["A SON", ["attached to a person",
                                    "stays when the message is hard",
                                    "counts the cost of leaving",
                                    "is loyal when it is not",
                                    "John 6:68"], "#FBF7EE", "#D9BE7A"]),
        footnote="\u201cI have begotten you through the gospel.\u201d 1 Corinthians 4:15",
        caption="The difference between an audience and an inheritance.",
        source="1 Corinthians 4:14\u201317; 1 Thessalonians 2:10\u201312."),

    "fig-10-2": dict(
        layout="layers", chapter=58,
        title="Houses of transmission",
        data=dict(x0=0.03, x1=0.97, gap=0.014, tsize=6.2,
                  rows=[
                      ["THE FAMILY", "the first and irreplaceable school \u2014 Deuteronomy 6:6\u20139"],
                      ["THE CHURCH", "the assembly that remembers aloud \u2014 Psalm 78:1\u20137"],
                      ["THE SCHOOL", "instruction in the things of God \u2014 2 Timothy 3:15"],
                      ["THE INSTITUTION", "structures that outlive personalities \u2014 2 Timothy 2:2"],
                  ], side_labels=["from the\nsmallest", "to the\nlargest"]),
        caption="Four houses in which wisdom can be preserved for a generation not yet born.",
        source="Deuteronomy 6:6\u20139; 2 Timothy 1:5; 2:2."),

    "fig-10-3": dict(
        layout="chain", chapter=59,
        title="Four fathers, four methods of preparation",
        data=dict(items=[
            ["MOSES", "public appointment\nbefore the people\nNumbers 27:18\u201323"],
            ["DAVID", "private instruction\nand material provision\n1 Chronicles 22:5"],
            ["ELIJAH", "personal call\nand immediate testing\n1 Kings 19:19"],
            ["PAUL", "constant companionship\nand delegated mission\n2 Timothy 2:2"],
        ], tsize=6.4, bsize=5.1),
        footnote="The methods differ; the intention does not.",
        caption="How four leaders in Scripture deliberately prepared their successors.",
        source="Deuteronomy 31:7\u20138; 1 Kings 2:1\u20134; 2 Kings 2:9\u201315; 2 Timothy 2:2."),

    "fig-10-4": dict(
        layout="stages", chapter=60,
        title="How the young should receive",
        data=dict(items=[
            ["HONOUR", "the posture that makes learning possible \u2014 Proverbs 23:22"],
            ["DISCERNMENT", "not every word from an elder is the word of God \u2014 Acts 17:11"],
            ["QUESTIONING", "the sincere enquiry, not the challenge \u2014 Luke 2:46"],
            ["LEARNING", "the long apprenticeship that precedes authority \u2014 2 Kings 3:11"],
            ["STEWARDSHIP", "what is received must be carried further \u2014 2 Timothy 2:2"],
        ], tsize=6.2, bsize=5.2),
        caption="The five movements of a right reception.",
        source="Proverbs 23:22; Ephesians 6:1\u20133; 1 Peter 5:5."),

    "fig-10-5": dict(
        layout="cycle", chapter=61,
        title="The table where generations meet",
        data=dict(items=[
            ["THE ELDER BRINGS", "memory"],
            ["THE YOUNG BRING", "questions"],
            ["TOGETHER", "the text is opened"],
            ["THE ELDER", "interprets"],
            ["THE YOUNG", "apply"],
            ["BOTH", "obey and transmit"],
        ], rx=0.31, ry=0.29, r=0.086, tsize=5.4),
        footnote="Where one generation speaks and the other does not answer, "
                 "the table has become a pulpit.",
        caption="The mutual exchange on which a generational covenant depends.",
        source="Psalm 145:4; Acts 2:17\u201318."),

    "fig-10-6": dict(
        layout="pyramid", chapter=62,
        title="The architecture of a generational covenant",
        data=dict(tiers=[
            ["THE WORD OF GOD", "the foundation that does not change"],
            ["THE FAITHFUL PERSON", "who receives and obeys"],
            ["THE RELATIONSHIP", "in which it is handed on"],
            ["THE STRUCTURE", "which outlives both persons"],
            ["THE NEXT GENERATION", "which inherits and continues"],
        ], tsize=5.9, bsize=5.1),
        footnote="Built from the bottom: no structure will bear the weight the "
                 "foundation was not laid to carry.",
        caption="What a generational covenant is made of, and in what order it is built.",
        source="2 Timothy 2:2; Psalm 78:5\u20137."),
}

# ---------------------------------------------------------------------------
# PART XI — THE FINAL GENERATION (63\u201368)
# ---------------------------------------------------------------------------
PART11 = {
    "fig-11-1": dict(
        layout="chain", chapter=63,
        title="\u201cYour sons and your daughters shall prophesy\u201d",
        data=dict(items=[
            ["SONS", "Joel 2:28\nthe inheritors\nspeak"],
            ["DAUGHTERS", "Joel 2:28\nthe overlooked\nspeak"],
            ["YOUNG MEN", "Joel 2:28\nvisions are\ngiven"],
            ["OLD MEN", "Joel 2:28\ndreams are\ngiven"],
            ["SERVANTS", "Joel 2:29\nthe lowest\nreceive"],
        ], tsize=6.6, bsize=5.1, gap=0.022),
        footnote="The prophecy is not of a generation that replaces another, but of "
                 "one outpouring over all of them.",
        caption="The four categories Joel names, and the servants added in Joel 2:29.",
        source="Joel 2:28\u201329; Acts 2:17\u201318."),

    "fig-11-2": dict(
        layout="twocol", chapter=64,
        title="Dreams and visions",
        data=dict(left=["THE OLD MEN DREAM", ["the material is memory",
                                              "the mode is reflection",
                                              "the gift is perspective",
                                              "the risk is nostalgia",
                                              "Joel 2:28"], "#F5EFE1", "#B9AE94"],
                  right=["THE YOUNG MEN SEE VISIONS", ["the material is possibility",
                                                       "the mode is perception",
                                                       "the gift is energy",
                                                       "the risk is presumption",
                                                       "Joel 2:28"], "#FBF7EE", "#D9BE7A"]),
        footnote="Neither gift is complete without the other.",
        caption="Complementary generations rather than competing generations.",
        source="Joel 2:28."),

    "fig-11-3": dict(
        layout="before_after", chapter=65,
        title="The ministry of turning hearts",
        data=dict(before=["A HOUSE DIVIDED", "Malachi 4:6\n\n\u2022 fathers turned from children\n"
                                             "\u2022 children turned from fathers\n\u2022 tradition without transmission\n"
                                             "\u2022 the land smitten with a curse"],
                  after=["A HOUSE RECONCILED", "Luke 1:17\n\n\u2022 fathers turned to children\n"
                                               "\u2022 children turned to fathers\n\u2022 the disobedient made ready\n"
                                               "\u2022 a people prepared for the Lord"],
                  arrow_text="the work of\nElijah, repeated\nin John", tsize=5.9, bsize=5.0),
        caption="The restoration of fathers and children as part of divine preparation.",
        source="Malachi 4:5\u20136; Luke 1:16\u201317."),
}

CATALOGUE = {}
for _blk in (FRONT, PART1, PART2, PART3, PART4, PART5, PART6, PART7, PART8,
             PART9, PART10, PART11):
    CATALOGUE.update(_blk)
