"""Vector figures for the textbook, drawn with ReportLab primitives.

Every chapter opens with one conceptual map (Figure n.1). The maps are drawn
from the same specification so that the visual language of the book stays
consistent: numbered nodes on a two-column ladder joined by elbow connectors,
ending in the integrative outcome of the chapter.
"""

import math

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable

from style import ACCENT, INK, PANEL, RULE_LIGHT, TEXT_W


def wrap(text, font, size, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class ConceptualMap(Flowable):
    """A numbered ladder of conceptual steps.

    ``nodes`` is a list of short phrases (two to six words each); the final
    node is drawn as the integrative outcome of the sequence.
    """

    BOX_W = 148.0
    BOX_H = 46.0
    GAP_Y = 20.0
    ROW_H = BOX_H + GAP_Y
    PAD = 2.0

    def __init__(self, nodes, width=TEXT_W):
        Flowable.__init__(self)
        self.nodes = nodes
        self.width = width
        self._compute_height()

    def _compute_height(self):
        rows = math.ceil(len(self.nodes) / 2.0)
        self.height = rows * self.ROW_H - self.GAP_Y + 2 * self.PAD + 8

    # ------------------------------------------------------------------ draw
    def draw(self):
        c = self.canv
        c.saveState()
        n = len(self.nodes)
        box_w, box_h = self.BOX_W, self.BOX_H
        left_x = 0.0
        right_x = self.width - box_w
        y_top = self.height - self.PAD

        centres = []
        for idx, label in enumerate(self.nodes):
            row = idx // 2
            col = idx % 2
            x = left_x if col == 0 else right_x
            y = y_top - box_h - row * self.ROW_H
            centres.append((x + box_w / 2.0, y, x, y))
            final = idx == n - 1
            self._node(c, x, y, box_w, box_h, idx + 1, label, final)

        # connectors
        for i in range(n - 1):
            x1, y1, _, _ = centres[i]
            x2, y2, _, _ = centres[i + 1]
            self._elbow(c, x1, y1, x2, y2 + box_h)
        c.restoreState()

    # --------------------------------------------------------------- helpers
    def _node(self, c, x, y, w, h, number, label, final):
        c.setLineWidth(0.55)
        c.setStrokeColor(ACCENT if final else colors.HexColor("#3F3F3F"))
        c.setFillColor(colors.white)
        c.rect(x, y, w, h, stroke=1, fill=1)

        # roundel with the step number
        cx, cy, r = x, y + h / 2.0, 8.0
        c.setFillColor(ACCENT if final else colors.white)
        c.setStrokeColor(ACCENT if final else colors.HexColor("#3F3F3F"))
        c.circle(cx, cy, r, stroke=1, fill=1)
        c.setFillColor(colors.white if final else ACCENT)
        c.setFont("Body-Semi", 7.4)
        c.drawCentredString(cx, cy - 2.6, str(number))

        # label
        font = "Body-Med" if final else "Body"
        c.setFillColor(INK)
        c.setFont(font, 8.3)
        lines = wrap(label, font, 8.3, w - 26)
        total = len(lines) * 9.8
        ty = y + h / 2.0 + total / 2.0 - 7.6
        for ln in lines:
            c.drawString(x + 17, ty, ln)
            ty -= 9.8

    def _elbow(self, c, x1, y1, x2, y2):
        """Connector from bottom of node i to top of node i+1."""
        c.setStrokeColor(colors.HexColor("#5A5A5A"))
        c.setLineWidth(0.55)
        p = c.beginPath()
        if abs(x1 - x2) < 0.5:
            p.moveTo(x1, y1)
            p.lineTo(x2, y2 + 5)
        else:
            mid = (y1 + y2) / 2.0
            p.moveTo(x1, y1)
            p.lineTo(x1, mid)
            p.lineTo(x2, mid)
            p.lineTo(x2, y2 + 5)
        c.drawPath(p)
        # arrowhead
        c.setFillColor(colors.HexColor("#5A5A5A"))
        c.setStrokeColor(colors.HexColor("#5A5A5A"))
        ah = 4.6
        c.line(x2 - 2.6, y2 + 1.2, x2, y2 - 0.4)
        c.line(x2 + 2.6, y2 + 1.2, x2, y2 - 0.4)


class CurveFigure(Flowable):
    """Small companion figure: predictive values as a function of prevalence.

    Used in Chapter 3 to show that a test's positive predictive value depends
    on base rate. The curves are computed from Bayes' theorem with fixed
    sensitivity and specificity, stated in the caption.
    """

    def __init__(self, sens, spec, width=TEXT_W * 0.86, height=150):
        Flowable.__init__(self)
        self.sens, self.spec = sens, spec
        self.width, self.height = width, height

    def draw(self):
        c = self.canv
        c.saveState()
        pad_l, pad_b, pad_r, pad_t = 34, 26, 12, 12
        w = self.width - pad_l - pad_r
        h = self.height - pad_b - pad_t
        ox, oy = pad_l, pad_b

        # axes
        c.setStrokeColor(colors.HexColor("#4A4A4A"))
        c.setLineWidth(0.55)
        c.line(ox, oy, ox, oy + h)
        c.line(ox, oy, ox + w, oy)

        # gridlines
        c.setStrokeColor(RULE_LIGHT)
        c.setLineWidth(0.35)
        c.setDash(1.2, 2.4)
        for frac in (0.25, 0.5, 0.75, 1.0):
            y = oy + h * frac
            c.line(ox, y, ox + w, y)
            c.setFont("Body", 6.6)
            c.setFillColor(colors.HexColor("#4A4A4A"))
            c.drawRightString(ox - 3, y - 2.2, f"{int(frac*100)}")
        for frac in (0, 0.25, 0.5, 0.75, 1.0):
            x = ox + w * frac
            c.line(x, oy, x, oy + h)
            c.drawCentredString(x, oy - 9, f"{int(frac*100)}")
        c.setDash()

        # PPV and NPV curves
        for label, fn, colour, dash in (
            ("PPV", lambda p: (self.sens * p) / (self.sens * p + (1 - self.spec) * (1 - p)), ACCENT, None),
            ("NPV", lambda p: (self.spec * (1 - p)) / (self.spec * (1 - p) + (1 - self.sens) * p), colors.HexColor("#8A5A44"), (3, 2)),
        ):
            c.setStrokeColor(colour)
            c.setLineWidth(0.9)
            if dash:
                c.setDash(*dash)
            p = c.beginPath()
            first = True
            for i in range(0, 101):
                prev = i / 100.0
                val = fn(prev)
                x = ox + w * prev
                y = oy + h * val
                if first:
                    p.moveTo(x, y)
                    first = False
                else:
                    p.lineTo(x, y)
            c.drawPath(p)
            c.setDash()

        # axis labels
        c.setFillColor(INK)
        c.setFont("Body", 7.4)
        c.drawCentredString(ox + w / 2.0, oy - 19, "Prevalence of the condition in the setting (%)")
        c.saveState()
        c.translate(12, oy + h / 2.0)
        c.rotate(90)
        c.drawCentredString(0, 0, "Posterior probability (%)")
        c.restoreState()

        # legend
        c.setFont("Body", 7.2)
        lx, ly = ox + w - 62, oy + h - 12
        c.setStrokeColor(ACCENT)
        c.setLineWidth(0.9)
        c.line(lx, ly + 2.4, lx + 14, ly + 2.4)
        c.setFillColor(INK)
        c.drawString(lx + 17, ly, "Positive predictive value")
        c.setStrokeColor(colors.HexColor("#8A5A44"))
        c.setDash(3, 2)
        c.line(lx, ly - 8.2, lx + 14, ly - 8.2)
        c.setDash()
        c.setFillColor(INK)
        c.drawString(lx + 17, ly - 10.6, "Negative predictive value")
        c.restoreState()
