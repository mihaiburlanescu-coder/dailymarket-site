"""Graficul mic al Pick of the Day: pretul din ultimele ~40 de sesiuni, intrarea, tinta si stopul,
plus drumul pretului dupa intrare (daca exista). SVG pentru site, PNG pentru email (Gmail nu afiseaza SVG).
Fara dependinte in afara de Pillow (pentru PNG)."""
from __future__ import annotations

import io
from typing import Callable

W, H = 400, 210          # dimensiunea logica (PNG-ul se deseneaza de 2 ori mai mare)
PAD_L, PAD_R, PAD_T, PAD_B = 6, 104, 16, 10
GREEN, RED, INK, MUTED, GOLD = "#15803d", "#b91c1c", "#13223A", "#6b7280", "#D9A441"
SHOW = 30                # cate sesiuni dinainte de intrare desenam


def _geom(closes: list[float], after: list[float] | None, entry: float, target: float, stop: float, horizon: int):
    before = [float(x) for x in closes[-SHOW:]]
    aft = [float(x) for x in (after or [])][:horizon]
    vals = before + aft + [entry, target, stop]
    lo, hi = min(vals), max(vals)
    span = hi - lo or abs(hi) * 0.01 or 1.0
    lo, hi = lo - span * 0.06, hi + span * 0.06
    n = len(before) + horizon            # locul pentru urmatoarele `horizon` sesiuni ramane rezervat
    x0, x1, y0, y1 = PAD_L, W - PAD_R, PAD_T, H - PAD_B
    X = lambda i: x0 + (x1 - x0) * i / max(n - 1, 1)
    Y = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    i_e = len(before) - 1                # intrarea = ultima inchidere inainte de pick
    pts_b = [(X(i), Y(v)) for i, v in enumerate(before)]
    pts_a = [(X(i_e), Y(before[-1]))] + [(X(i_e + 1 + k), Y(v)) for k, v in enumerate(aft)] if aft else []
    return {"X": X, "Y": Y, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "i_e": i_e, "pts_b": pts_b, "pts_a": pts_a}


def _labels(entry, target, stop, Y, fmt, names):
    """Etichetele din dreapta, departate ca sa nu se suprapuna."""
    items = sorted([(Y(target), names["target"] + " " + fmt(target), GREEN), (Y(entry), names["entry"] + " " + fmt(entry), INK),
                    (Y(stop), names["stop"] + " " + fmt(stop), RED)], key=lambda t: t[0])
    gap = 18
    for k in range(1, 3):
        if items[k][0] - items[k - 1][0] < gap:
            items[k] = (items[k - 1][0] + gap, items[k][1], items[k][2])
    if items[2][0] > H - 6:
        shift = items[2][0] - (H - 6)
        items = [(y - shift, t, c) for y, t, c in items]
    return items


def chart_svg(closes: list[float], entry: float, target: float, stop: float, side: int, fmt: Callable[[float], str],
              names: dict, after: list[float] | None = None, horizon: int = 5) -> str:
    if not closes or len(closes) < 5:
        return ""
    g = _geom(closes, after, entry, target, stop, horizon)
    X, Y, x0, x1, y0, y1, i_e = g["X"], g["Y"], g["x0"], g["x1"], g["y0"], g["y1"], g["i_e"]
    xe = X(i_e)
    yt, ys, yen = Y(target), Y(stop), Y(entry)
    p = lambda pts: " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block;max-width:{W}px;height:auto" role="img" '
           f'aria-label="{names.get("aria", "")}" xmlns="http://www.w3.org/2000/svg">',
           f'<rect x="{xe:.1f}" y="{y0}" width="{x1 - xe:.1f}" height="{y1 - y0}" fill="#f3f4f6"/>',
           f'<rect x="{xe:.1f}" y="{min(yt, yen):.1f}" width="{x1 - xe:.1f}" height="{abs(yen - yt):.1f}" fill="{GREEN}" fill-opacity=".10"/>',
           f'<rect x="{xe:.1f}" y="{min(ys, yen):.1f}" width="{x1 - xe:.1f}" height="{abs(yen - ys):.1f}" fill="{RED}" fill-opacity=".08"/>',
           f'<line x1="{x0}" x2="{x1}" y1="{yt:.1f}" y2="{yt:.1f}" stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="5 4"/>',
           f'<line x1="{x0}" x2="{x1}" y1="{ys:.1f}" y2="{ys:.1f}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="5 4"/>',
           f'<line x1="{x0}" x2="{x1}" y1="{yen:.1f}" y2="{yen:.1f}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2 3"/>',
           f'<polyline points="{p(g["pts_b"])}" fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>']
    if g["pts_a"]:
        out.append(f'<polyline points="{p(g["pts_a"])}" fill="none" stroke="{GOLD}" stroke-width="2.6" stroke-linejoin="round"/>')
    out.append(f'<circle cx="{xe:.1f}" cy="{yen:.1f}" r="4" fill="{INK}"/>')
    if names.get("next"):
        out.append(f'<text x="{xe + (x1 - xe) / 2:.1f}" y="{y0 + 12}" font-size="11" fill="{MUTED}" text-anchor="middle" '
                   f'font-family="Arial,sans-serif">{names["next"]}</text>')
    for y, t, c in _labels(entry, target, stop, Y, fmt, names):
        out.append(f'<text x="{x1 + 6}" y="{y + 4:.1f}" font-size="13.5" font-weight="700" fill="{c}" font-family="Arial,sans-serif">{t}</text>')
    out.append("</svg>")
    return "".join(out)


def _font(size: int, bold: bool = False):
    from PIL import ImageFont
    for f in (["DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
              ["DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def _rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _dashed(d, x0, x1, y, color, width, dash, gap):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=color, width=width)
        x += dash + gap


def chart_png(closes: list[float], entry: float, target: float, stop: float, side: int, fmt: Callable[[float], str],
              names: dict, after: list[float] | None = None, horizon: int = 5) -> bytes | None:
    if not closes or len(closes) < 5:
        return None
    from PIL import Image, ImageDraw
    S = 2
    g = _geom(closes, after, entry, target, stop, horizon)
    X, Y, x0, x1, y0, y1, i_e = g["X"], g["Y"], g["x0"], g["x1"], g["y0"], g["y1"], g["i_e"]
    img = Image.new("RGB", (W * S, H * S), (255, 255, 255))
    d = ImageDraw.Draw(img, "RGBA")
    xe = X(i_e)
    yt, ys, yen = Y(target), Y(stop), Y(entry)
    d.rectangle([xe * S, y0 * S, x1 * S, y1 * S], fill=_rgb("#f3f4f6"))
    d.rectangle([xe * S, min(yt, yen) * S, x1 * S, max(yt, yen) * S], fill=_rgb(GREEN) + (26,))
    d.rectangle([xe * S, min(ys, yen) * S, x1 * S, max(ys, yen) * S], fill=_rgb(RED) + (20,))
    _dashed(d, x0 * S, x1 * S, yt * S, _rgb(GREEN), 3, 10, 8)
    _dashed(d, x0 * S, x1 * S, ys * S, _rgb(RED), 3, 10, 8)
    _dashed(d, x0 * S, x1 * S, yen * S, _rgb(MUTED), 2, 4, 6)
    d.line([(a * S, b * S) for a, b in g["pts_b"]], fill=_rgb(INK), width=4, joint="curve")
    if g["pts_a"]:
        d.line([(a * S, b * S) for a, b in g["pts_a"]], fill=_rgb(GOLD), width=5, joint="curve")
    r = 4 * S
    d.ellipse([xe * S - r, yen * S - r, xe * S + r, yen * S + r], fill=_rgb(INK))
    f_small, f_lab = _font(11 * S), _font(int(13.5 * S), bold=True)
    nx = names.get("next", "")
    if nx:
        tw = d.textlength(nx, font=f_small)
        d.text(((xe + (x1 - xe) / 2) * S - tw / 2, (y0 + 2) * S), nx, font=f_small, fill=_rgb(MUTED))
    for y, t, c in _labels(entry, target, stop, Y, fmt, names):
        d.text(((x1 + 6) * S, (y - 8) * S), t, font=f_lab, fill=_rgb(c))
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()
