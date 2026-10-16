"""
bookkit.diagrams.engine — drawing primitives sized for the printed page.

Conventions
-----------
Coordinates run 0..1 in both axes within the figure canvas.

Vertical limits are always expressed as **(bottom, top)**.  The helper `band()`
returns the strip available to a diagram once the heading rule above and the
footnote below have been reserved, and every layout centres its content in that
strip, so a diagram can never drift into the heading or float in dead space.

Figures are designed at the width they will occupy on the page (the text
measure, 4.02 in), so a 6 pt label in a source file is a 6 pt label in print.
All output is vector SVG with text converted to outlines.
"""
from __future__ import annotations

import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import (Circle, FancyArrowPatch, FancyBboxPatch, Polygon,
                                Rectangle, Wedge)

# ---------------------------------------------------------------------------
# palette (mirrors bookkit.theme)
# ---------------------------------------------------------------------------
INK = "#16223A"
INK_SOFT = "#2E3A50"
GOLD = "#B08A2E"
GOLD_L = "#D9BE7A"
GOLD_P = "#F0E6CC"
CREAM = "#FBF7EE"
CREAM_D = "#F5EFE1"
GRAY = "#6E6A63"
RULE = "#D8CEB8"
RULE_D = "#B9AE94"
PAPER = "#FFFFFF"
NAVY = "#0E1729"

matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["figure.dpi"] = 100

PRINT_W = 4.02          # inches — the book's text measure
HEAD_Y = 0.965
RULE_Y = 0.925
NOTE_Y = 0.035

_fonts_ready = False


def setup_fonts(font_dir):
    global _fonts_ready
    if _fonts_ready:
        return
    for name in ("Lato-Regular.ttf", "Lato-Bold.ttf", "Lato-Italic.ttf",
                 "Lato-Black.ttf", "Lato-Medium.ttf", "EBGaramond-Regular.ttf",
                 "EBGaramond-Italic.ttf", "EBGaramond-SemiBold.ttf"):
        p = font_dir / name
        if p.exists():
            font_manager.fontManager.addfont(str(p))
    matplotlib.rcParams["font.family"] = "Lato"
    _fonts_ready = True


# ---------------------------------------------------------------------------
# canvas
# ---------------------------------------------------------------------------
def canvas(h=3.0, w=PRINT_W, pad=0.02):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig._book_pad = pad
    return fig, ax


def finalize(ax, fig, pad=None):
    """Crop to the drawn art so no dead margin survives into the page."""
    pad = pad if pad is not None else getattr(fig, "_book_pad", 0.02)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    xs, ys = [], []
    for art in ax.get_children():
        if not art.get_visible():
            continue
        try:
            bb = art.get_window_extent(renderer=r)
        except Exception:
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        xs += [x0, x1]
        ys += [y0, y1]
    if not xs:
        return
    dx, dy = max(xs) - min(xs), max(ys) - min(ys)
    if dx > 0:
        ax.set_xlim(min(xs) - pad * dx, max(xs) + pad * dx)
    if dy > 0:
        ax.set_ylim(min(ys) - pad * dy, max(ys) + pad * dy)


def save(fig, ax, name, out_dir, pad=None):
    finalize(ax, fig, pad)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.svg"
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.015,
                transparent=True)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------
def _extent(ax, fig, artist):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bb = artist.get_window_extent(renderer=r)
    inv = ax.transData.inverted()
    (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    return abs(x1 - x0), abs(y1 - y0)


def measure(ax, fig, text, size, weight="normal", style="normal", lines=1):
    """Rendered size of a text in data units: (width, height)."""
    t = ax.text(0.5, 0.5, text, fontsize=size, fontweight=weight,
                fontstyle=style, alpha=0)
    w, h = _extent(ax, fig, t)
    t.remove()
    return w, h * max(1, lines)


def fit(text, ax, fig, max_w, size, weight="normal", style="normal", floor=3.2):
    """Largest size <= `size` at which `text` fits inside `max_w`."""
    if fig is None:
        return size
    w, _ = measure(ax, fig, text, size, weight, style)
    if w <= 0:
        return size
    return max(floor, size * min(1.0, max_w / w))


def fit_lines(lines, ax, fig, max_w, size, **kw):
    return min(fit(l, ax, fig, max_w, size, **kw) for l in lines)


# ---------------------------------------------------------------------------
# the content band
# ---------------------------------------------------------------------------
def band(has_title: bool = True, has_note: bool = True):
    """Vertical strip open to the diagram, as (bottom, top)."""
    top = (RULE_Y - 0.022) if has_title else 0.975
    bottom = (NOTE_Y + 0.075) if has_note else 0.03
    return bottom, top


def centre(b, h):
    """Bottom coordinate that centres a block of height h in band b."""
    bb, bt = b
    return bb + max(0.0, (bt - bb - h)) / 2.0


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------
def _pair(item):
    """Items may be a bare string, (title, body) or (title, body, note)."""
    if isinstance(item, (tuple, list)):
        parts = list(item)
        while len(parts) < 2:
            parts.append("")
        return parts[0], parts[1]
    return item, ""


def panel(ax, x, y, w, h, fc=CREAM, ec=RULE, lw=0.8, r=0.02, z=1, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z,
                       linestyle=ls)
    ax.add_patch(p)
    return p


def box(ax, x, y, w, h, title, body="", fig=None, fc=CREAM, ec=GOLD_L, tc=INK,
        bc=GRAY, tsize=7.0, bsize=6.0, lw=0.8, r=0.02, z=2, weight="bold",
        title_at=0.70, body_at=0.32):
    """Rounded panel with a centred title and optional body text.

    Both strings shrink to fit the panel; body lines are stacked from the
    vertical centre so two- and three-line bodies sit consistently.
    """
    panel(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, r=r, z=z)
    inner = w * 0.88
    cx = x + w / 2.0
    lines = body.split("\n") if body else []
    if body:
        # pick a size that satisfies both the widest line and the height
        bsz = fit_lines(lines, ax, fig, inner, bsize) if fig else bsize
        if fig:
            _, lh = measure(ax, fig, "Ag", bsz)
            while len(lines) * lh * 1.45 > h * 0.52 and bsz > 3.4:
                bsz -= 0.2
                _, lh = measure(ax, fig, "Ag", bsz)
        block_h = len(lines) * (measure(ax, fig, "Ag", bsz)[1] * 1.45 if fig else 0.05)
        tsz = fit(title, ax, fig, inner, tsize, weight=weight) if fig else tsize
        ty = y + h - max(0.035, h * 0.24)
        ax.text(cx, ty, title, ha="center", va="center", color=tc,
                fontsize=tsz, fontweight=weight, zorder=z + 1)
        by = ty - 0.020 - block_h / 2.0
        ax.text(cx, by, body, ha="center", va="center", color=bc,
                fontsize=bsz, zorder=z + 1, linespacing=1.45)
    else:
        tsz = fit(title, ax, fig, inner, tsize, weight=weight) if fig else tsize
        ax.text(cx, y + h / 2.0, title, ha="center", va="center", color=tc,
                fontsize=tsz, fontweight=weight, zorder=z + 1)
    return (x, y, w, h)


def label(ax, x, y, text, size=5.6, color=GRAY, weight="normal", ha="center",
          va="center", z=6, style="normal", linespacing=1.4):
    return ax.text(x, y, text, ha=ha, va=va, color=color, fontsize=size,
                   fontweight=weight, fontstyle=style, zorder=z,
                   linespacing=linespacing)


def arrow(ax, x1, y1, x2, y2, color=GOLD, lw=1.1, style="-|>", ms=6.5,
          rad=0.0, z=3, ls="-", alpha=1.0):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                        color=color, linewidth=lw, zorder=z, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0,
                        alpha=alpha)
    ax.add_patch(a)
    return a


def hrule(ax, x1, x2, y, color=RULE, lw=0.7, z=2, ls="-"):
    ax.plot([x1, x2], [y, y], color=color, lw=lw, zorder=z,
            solid_capstyle="round", linestyle=ls)


def vrule(ax, x, y1, y2, color=RULE, lw=0.7, z=2, ls="-"):
    ax.plot([x, x], [y1, y2], color=color, lw=lw, zorder=z,
            solid_capstyle="round", linestyle=ls)


def badge(ax, cx, cy, n, r=0.021, fc=GOLD, tc="white", size=5.6, z=6):
    ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor="none", zorder=z))
    ax.text(cx, cy, str(n), ha="center", va="center", color=tc,
            fontsize=size, fontweight="bold", zorder=z + 1)


def heading(ax, text, y=HEAD_Y, size=7.2, color=INK, rule_y=RULE_Y):
    ax.text(0.5, y, text.upper(), ha="center", va="center", color=color,
            fontsize=size, fontweight="bold")
    hrule(ax, 0.015, 0.985, rule_y, color=GOLD_L, lw=0.7)


def footnote(ax, text, y=NOTE_Y, size=5.8, color=INK_SOFT, style="italic"):
    ax.text(0.5, y, text, ha="center", va="center", color=color, fontsize=size,
            fontstyle=style)


# ---------------------------------------------------------------------------
# relationships
# ---------------------------------------------------------------------------
def chain(ax, items, band_b, h=None, fig=None, x0=0.015, x1=0.985, gap=0.028,
          fc=CREAM, ec=GOLD_L, tsize=7.0, bsize=5.8, badges=False,
          badge_above=0.045):
    """Left-to-right boxes joined by arrows."""
    n = len(items)
    bb, bt = band_b
    h = h or min(0.44, (bt - bb) * 0.68)
    y = centre(band_b, h + (badge_above if badges else 0))
    w = ((x1 - x0) - gap * (n - 1)) / n
    out = []
    for i, item in enumerate(items):
        title, body = _pair(item)
        x = x0 + i * (w + gap)
        out.append(box(ax, x, y, w, h, title, body, fig=fig, fc=fc, ec=ec,
                       tsize=tsize, bsize=bsize))
        if i:
            px = x - gap
            arrow(ax, px + gap * 0.10, y + h / 2, px + gap * 0.90, y + h / 2)
        if badges:
            badge(ax, x + w / 2, y + h + badge_above, i + 1)
    return out, w, gap


def vchain(ax, items, band_b, x=0.08, w=0.88, fig=None, gap=0.030, fc=CREAM,
           ec=GOLD_L, tsize=6.6, bsize=5.6):
    """Top-to-bottom boxes joined by downward arrows."""
    bb, bt = band_b
    n = len(items)
    h = ((bt - bb) - gap * (n - 1)) / n
    out = []
    for i, item in enumerate(items):
        title, body = _pair(item)
        y = bt - h - i * (h + gap)
        out.append(box(ax, x, y, w, h, title, body, fig=fig, fc=fc, ec=ec,
                       tsize=tsize, bsize=bsize))
        if i:
            top = y + h + gap
            arrow(ax, x + w / 2, top, x + w / 2, y + h + gap * 0.18)
    return out, h, gap


def two_col(ax, left, right, band_b, fig=None, h=None, head_size=7.0,
            body_size=5.8, gap=0.05):
    """Two contrasted panels with headings \u2014 the workhorse for comparisons."""
    bb, bt = band_b
    h = h or (bt - bb) * 0.86
    y = centre(band_b, h)
    w = (1.0 - 0.03 - gap) / 2
    panels = []
    for i, spec in enumerate((left, right)):
        head, lines = spec[0], spec[1]
        fc = spec[2] if len(spec) > 2 else CREAM_D
        ec = spec[3] if len(spec) > 3 else GOLD_L
        tc = spec[4] if len(spec) > 4 else INK
        x = 0.015 + i * (w + gap)
        panel(ax, x, y, w, h, fc=fc, ec=ec, lw=0.9)
        hsz = fit(head, ax, fig, w * 0.90, head_size, weight="bold") if fig else head_size
        hy = y + h - 0.045
        ax.text(x + w / 2, hy, head, ha="center", va="top", color=tc,
                fontsize=hsz, fontweight="bold", zorder=4)
        hrule(ax, x + 0.025, x + w - 0.025, hy - 0.038, color=ec, lw=0.7)
        ty = hy - 0.055
        for ln in lines:
            if not ln:
                ty -= 0.022
                continue
            sz = fit(ln, ax, fig, w * 0.90, body_size) if fig else body_size
            ax.text(x + 0.018, ty, ln, ha="left", va="top", color=GRAY,
                    fontsize=sz, zorder=4, linespacing=1.4)
            ty -= 0.046 if len(ln) < 36 else 0.078
        panels.append((x, y, w, h))
    return panels


# ---------------------------------------------------------------------------
# the band
# ---------------------------------------------------------------------------
def timeline(ax, points, band_b, fig=None, axis_x0=0.035, axis_x1=0.965,
             above=True, alt=False, tsize=6.1, bsize=5.4, dot_size=0.013):
    """Horizontal axis with stems; the label stack is centred in the band."""
    bb, bt = band_b
    n = len(points)
    slot = (axis_x1 - axis_x0) / max(1, n)
    stem = 0.058
    # measure the deepest stack so the whole assembly can be centred
    need = 0.0
    for pt in points:
        _, body = _pair(pt)
        lines = body.split("\n") if body else []
        _, lh = measure(ax, fig, "Ag", bsize)
        _, th = measure(ax, fig, "Ag", tsize)
        need = max(need, stem + 0.012 + len(lines) * lh * 1.45 + th + 0.012)
    span_above = need if above and not alt else need
    y = bb + max(0.0, (bt - bb - need)) / 2.0 + (stem + 0.02)
    hrule(ax, axis_x0, axis_x1, y, color=GOLD, lw=1.1)
    for i, pt in enumerate(points):
        title, body = _pair(pt)
        x = axis_x0 + slot * (i + 0.5)
        ax.add_patch(Circle((x, y), dot_size, facecolor=GOLD,
                            edgecolor=PAPER, linewidth=0.8, zorder=5))
        up = above if not alt else (i % 2 == 0)
        sign = 1 if up else -1
        va = "bottom" if up else "top"
        lines = body.split("\n") if body else []
        _, lh = measure(ax, fig, "Ag", bsize)
        bh = len(lines) * lh * 1.45
        vrule(ax, x, y + sign * 0.012, y + sign * stem,
              color=RULE_D, lw=0.6, ls=(0, (1, 1.4)))
        by = y + sign * (stem + 0.008)
        ty = by + sign * bh
        if lines:
            bsz = fit_lines(lines, ax, fig, slot * 0.95, bsize)
            ax.text(x, by, body, ha="center", va=va, color=GRAY, fontsize=bsz,
                    zorder=6, linespacing=1.45)
        tsz = fit(title, ax, fig, slot * 0.95, tsize, weight="bold")
        ax.text(x, ty, title, ha="center", va=va, color=INK, fontsize=tsz,
                fontweight="bold", zorder=6)


def tree(ax, root, children, band_b, fig=None, tsize=6.4, bsize=5.4,
         root_w=0.34, child_gap=0.022):
    """One parent box branching to a row of descendants."""
    bb, bt = band_b
    rh = 0.14
    ch = min(0.24, (bt - bb) * 0.34)
    y_top = bt - rh
    y_bot = bb
    rx = 0.5 - root_w / 2
    box(ax, rx, y_top, root_w, rh, root, "", fig=fig, tsize=tsize, fc=CREAM_D)
    n = len(children)
    cw = ((0.97 - 0.03) - child_gap * (n - 1)) / n
    cxs = []
    for i, ch_item in enumerate(children):
        title, body = _pair(ch_item)
        x = 0.03 + i * (cw + child_gap)
        box(ax, x, y_bot, cw, ch, title, body, fig=fig, tsize=tsize, bsize=bsize)
        cxs.append(x + cw / 2)
    stem_y = y_bot + ch + (y_top - y_bot - ch) * 0.42
    vrule(ax, 0.5, y_top, stem_y, color=GOLD_L, lw=0.9)
    hrule(ax, cxs[0], cxs[-1], stem_y, color=GOLD_L, lw=0.9)
    for cx in cxs:
        arrow(ax, cx, stem_y, cx, y_bot + ch + 0.006, lw=0.9, ms=5.5)
    return cxs


def cycle(ax, items, band_b, fig=None, cx=0.5, rx=0.305, ry=None, r=0.088,
          tsize=5.9, bsize=5.1, start=90):
    """Items on an ellipse, each arrowed to the next."""
    bb, bt = band_b
    cy = (bb + bt) / 2.0
    ry = ry if ry is not None else (bt - bb) / 2.0 - r - 0.035
    n = len(items)
    pos = [(cx + rx * math.cos(math.radians(start + 360.0 * i / n)),
            cy + ry * math.sin(math.radians(start + 360.0 * i / n)))
           for i in range(n)]
    for i in range(n):
        x1, y1 = pos[i]
        x2, y2 = pos[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        shrink = r + 0.030
        arrow(ax, x1 + dx / d * shrink, y1 + dy / d * shrink,
              x2 - dx / d * shrink, y2 - dy / d * shrink,
              color=GOLD_L, lw=0.9, ms=6, rad=-0.20)
    for i, it in enumerate(items):
        title, body = _pair(it)
        x, y = pos[i]
        ax.add_patch(Circle((x, y), r, facecolor=CREAM, edgecolor=GOLD_L,
                            linewidth=0.9, zorder=5))
        chord = r * 1.62          # usable width inside the circle
        tsz = fit(title, ax, fig, chord, tsize, weight="bold")
        if body:
            bsz = fit(body, ax, fig, chord, bsize)
            _, th = measure(ax, fig, "Ag", tsz)
            _, bh = measure(ax, fig, "Ag", bsz)
            ax.text(x, y + (bh / 2 + 0.006), title, ha="center", va="center",
                    color=INK, fontsize=tsz, fontweight="bold", zorder=6)
            ax.text(x, y - (th / 2 + 0.006), body, ha="center", va="center",
                    color=GRAY, fontsize=bsz, zorder=6)
        else:
            ax.text(x, y, title, ha="center", va="center", color=INK,
                    fontsize=tsz, fontweight="bold", zorder=6)
    return pos


def pyramid(ax, tiers, band_b, fig=None, x0=0.05, x1=0.95, tsize=6.3,
            bsize=5.4, fc_list=None):
    """Stacked tiers, widest at the base, first item at the base."""
    bb, bt = band_b
    n = len(tiers)
    th = (bt - bb) / n
    out = []
    cx = (x0 + x1) / 2
    half = (x1 - x0) / 2
    for i, tier in enumerate(tiers):
        title, body = _pair(tier)
        f_lo = 1.0 if i == 0 else 0.46 + 0.54 * (n - i) / n
        f_hi = 0.46 + 0.54 * (n - i - 1) / n
        yb = bb + i * th
        yt = yb + th
        pts = [(cx - half * f_lo, yb), (cx + half * f_lo, yb),
               (cx + half * f_hi, yt), (cx - half * f_hi, yt)]
        fc = (fc_list or [CREAM, CREAM_D] * n)[i]
        ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=GOLD_L,
                             linewidth=0.8, zorder=2))
        inner = half * min(f_lo, f_hi) * 1.85
        tsz = fit(title, ax, fig, inner, tsize, weight="bold")
        ax.text(cx, yb + th * (0.62 if body else 0.5), title, ha="center",
                va="center", color=INK, fontsize=tsz, fontweight="bold", zorder=4)
        if body:
            bsz = fit(body, ax, fig, inner, bsize)
            ax.text(cx, yb + th * 0.27, body, ha="center", va="center",
                    color=GRAY, fontsize=bsz, zorder=4)
        out.append((cx, yb, th))
    return out


def layers(ax, rows, band_b, fig=None, x0=0.05, x1=0.95, gap=0.016,
           tsize=6.3, bsize=5.4, side_labels=None):
    """Horizontal strata; first item at the top."""
    bb, bt = band_b
    n = len(rows)
    h = ((bt - bb) - gap * (n - 1)) / n
    out = []
    for i, row in enumerate(rows):
        title, body = _pair(row)
        y = bt - h - i * (h + gap)
        fc = CREAM if i % 2 == 0 else CREAM_D
        panel(ax, x0, y, x1 - x0, h, fc=fc, ec=GOLD_L, lw=0.8)
        tsz = fit(title, ax, fig, (x1 - x0) * 0.44, tsize, weight="bold")
        ax.text(x0 + 0.018, y + h / 2, title, ha="left", va="center",
                color=INK, fontsize=tsz, fontweight="bold", zorder=4)
        if body:
            bsz = fit(body, ax, fig, (x1 - x0) * 0.58, bsize)
            ax.text(x1 - 0.018, y + h / 2, body, ha="right", va="center",
                    color=GRAY, fontsize=bsz, zorder=4)
        out.append((y, h))
    if side_labels:
        for i, lab in enumerate(side_labels):
            if i >= n:
                break
            y = bt - h - i * (h + gap) + h / 2
            ax.text(x0 - 0.012, y, lab, ha="right", va="center", color=GOLD,
                    fontsize=bsize - 0.6, fontweight="bold", zorder=4,
                    linespacing=1.3)
    return out


def matrix(ax, col_heads, row_heads, cells, band_b, fig=None, x0=0.30, x1=0.97,
           tsize=5.9, csize=5.4):
    """Grid with row and column headings."""
    bb, bt = band_b
    nc, nr = len(col_heads), len(row_heads)
    y1 = bt - 0.055
    y0 = bb
    cw = (x1 - x0) / nc
    rh = (y1 - y0) / nr
    for j, ch in enumerate(col_heads):
        hsz = fit(ch, ax, fig, cw * 0.92, tsize, weight="bold")
        ax.text(x0 + cw * (j + 0.5), y1 + 0.026, ch, ha="center", va="bottom",
                color=INK, fontsize=hsz, fontweight="bold", zorder=4)
    for i, rhead in enumerate(row_heads):
        rsz = fit(rhead, ax, fig, (x0 - 0.035), tsize, weight="bold")
        ax.text(x0 - 0.014, y1 - rh * (i + 0.5), rhead, ha="right", va="center",
                color=INK, fontsize=rsz, fontweight="bold", zorder=4)
        for j in range(nc):
            txt = cells[i][j] if i < len(cells) and j < len(cells[i]) else ""
            yy = y1 - rh * (i + 1)
            fc = CREAM if (i + j) % 2 == 0 else CREAM_D
            panel(ax, x0 + cw * j, yy, cw, rh, fc=fc, ec=RULE, lw=0.6)
            if txt:
                lines = txt.split("\n")
                sz = fit_lines(lines, ax, fig, cw * 0.86, csize)
                ax.text(x0 + cw * (j + 0.5), yy + rh / 2, txt, ha="center",
                        va="center", color=INK_SOFT, fontsize=sz, zorder=4,
                        linespacing=1.35)


def balance(ax, left, right, band_b, fig=None, tsize=5.9, bsize=5.1):
    """Two pans on a beam in equilibrium \u2014 complementary, not opposed."""
    bb, bt = band_b
    beam_y = bt - 0.055
    pivot_y = beam_y - 0.040
    cx = 0.5
    ax.add_patch(Polygon([(cx - 0.030, pivot_y), (cx + 0.030, pivot_y),
                          (cx, pivot_y - 0.062)], closed=True,
                         facecolor=CREAM_D, edgecolor=GOLD_L, linewidth=0.8,
                         zorder=2))
    tilt = 0.030
    spread = 0.235
    arm_l = (cx - spread, beam_y + tilt)
    arm_r = (cx + spread, beam_y - tilt)
    ax.plot([arm_l[0] - 0.05, arm_r[0] + 0.05], [arm_l[1], arm_r[1]],
            color=GOLD, lw=1.5, zorder=3, solid_capstyle="round")
    bw = 0.462
    top = beam_y - tilt - 0.028
    for (title, body), (px, ay) in ((left, arm_l), (right, arm_r)):
        vrule(ax, px, ay, top, color=GOLD_L, lw=0.7)
        box(ax, px - bw / 2, bb, bw, top - bb, title, body, fig=fig,
            tsize=tsize, bsize=bsize)


def radial(ax, centre, spokes, band_b, fig=None, cx=0.5, rx=0.285, ry=0.285,
           r=0.082, tsize=5.9, bsize=5.1, start=90):
    """A hub with labelled spokes."""
    bb, bt = band_b
    cy = (bb + bt) / 2.0
    ax.add_patch(Circle((cx, cy), r, facecolor=CREAM_D, edgecolor=GOLD,
                        linewidth=1.0, zorder=5))
    lines = centre.split("\n")
    csz = fit_lines(lines, ax, fig, r * 1.45, tsize, weight="bold")
    ax.text(cx, cy, centre, ha="center", va="center", color=INK, fontsize=csz,
            fontweight="bold", zorder=6, linespacing=1.3)
    n = len(spokes)
    for i, sp in enumerate(spokes):
        title, body = _pair(sp)
        a = math.radians(start + 360.0 * i / n)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy) or 1
        arrow(ax, cx + dx / d * (r + 0.012), cy + dy / d * (r + 0.012),
              x - dx / d * 0.055, y - dy / d * 0.055, color=GOLD_L, lw=0.9,
              ms=5.5)
        w, bh = 0.268, 0.135
        box(ax, x - w / 2, y - bh / 2, w, bh, title, body, fig=fig,
            tsize=tsize - 0.5, bsize=bsize - 0.4)
