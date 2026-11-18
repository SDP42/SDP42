"""The Starting XI on a pitch in a 4-3-3.

The ball is played out from the keeper through midfield to the striker and
into the net. Each player lights up as the ball reaches them.
"""
import math

from data import PASSING_ORDER, SQUAD
from svgkit import caption, document, esc, write
from theme import BG, DIM, GOLD, GRASS, GRASS_2, INK, LIME, LINE, MONO, SANS

W, H = 1200, 620
X0, Y0, PW, PH = 70, 74, 1060, 476   # pitch rectangle on screen
SX, SY = PW / 105, PH / 68           # pixels per metre
CYCLE = 12.0                          # seconds for one passing move


def at(x, z):
    """Pitch metres (origin at the centre spot) to screen pixels."""
    return X0 + PW / 2 + x * SX, Y0 + PH / 2 + z * SY


def markings():
    line = 'fill="none" stroke="#e8f5e9" stroke-opacity=".6" stroke-width="2"'
    cx, cy = at(0, 0)
    out = [
        f'<rect x="{X0}" y="{Y0}" width="{PW}" height="{PH}" {line}/>',
        f'<line x1="{cx}" y1="{Y0}" x2="{cx}" y2="{Y0 + PH}" {line}/>',
        f'<ellipse cx="{cx}" cy="{cy}" rx="{9.15 * SX:.1f}" ry="{9.15 * SY:.1f}" {line}/>',
        f'<circle cx="{cx}" cy="{cy}" r="3" fill="#e8f5e9" fill-opacity=".7"/>',
    ]
    for side in (-1, 1):
        goal_line = 52.5 * side
        for depth, width in ((16.5, 40.3), (5.5, 18.3)):
            x1, y1 = at(goal_line - depth * side, -width / 2)
            x2, y2 = at(goal_line, width / 2)
            out.append(f'<rect x="{min(x1, x2):.1f}" y="{y1:.1f}" width="{abs(x2 - x1):.1f}" height="{y2 - y1:.1f}" {line}/>')
        sx, sy = at(goal_line - 11 * side, 0)
        out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.5" fill="#e8f5e9" fill-opacity=".7"/>')
        gx, gy1 = at(goal_line, -3.66)
        _, gy2 = at(goal_line, 3.66)
        depth = 2.4 * SX * side
        out.append(
            f'<rect x="{min(gx, gx + depth):.1f}" y="{gy1:.1f}" width="{abs(depth):.1f}" height="{gy2 - gy1:.1f}" '
            f'fill="url(#net)" stroke="#e8f5e9" stroke-opacity=".8" stroke-width="2"/>'
        )
    return "".join(out)


def grass():
    bands = 14
    width = PW / bands
    stripes = "".join(
        f'<rect x="{X0 + i * width:.1f}" y="{Y0}" width="{width + .5:.1f}" height="{PH}" fill="{GRASS if i % 2 else GRASS_2}"/>'
        for i in range(bands)
    )
    return f'<rect x="{X0 - 30}" y="{Y0 - 30}" width="{PW + 60}" height="{PH + 60}" rx="10" fill="#0f3219"/>{stripes}'


def route():
    """Screen points the ball visits and the fraction of the cycle at each."""
    by_no = {p["no"]: p for p in SQUAD}
    points = [at(*by_no[n]["at"]) for n in PASSING_ORDER]
    goal = at(52.5 + 1.5, 1.2)
    points.append(goal)
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    total = sum(lengths)
    play = 0.86  # share of the cycle the ball is moving; the rest is the celebration
    arrive, run = [0.0], 0.0
    for seg in lengths:
        run += seg
        arrive.append(run / total * play)
    return points, arrive, play


def players(arrivals):
    out = []
    for p in SQUAD:
        x, y = at(*p["at"])
        captain = p.get("captain")
        ring = GOLD if captain else LIME
        t = arrivals.get(p["no"])
        glow = ""
        if t is not None:
            start = t * 100
            glow = (
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="22" fill="none" stroke="{ring}" stroke-width="3" opacity="0" '
                f'style="transform-origin:{x:.1f}px {y:.1f}px;animation:touch{p["no"]} {CYCLE}s linear infinite"/>'
            )
            out.append(
                f'<style>@keyframes touch{p["no"]}{{0%,{max(start - 0.5, 0):.2f}%{{opacity:0;transform:scale(1)}}'
                f'{start + 0.5:.2f}%{{opacity:1;transform:scale(1)}}{start + 8:.2f}%,100%{{opacity:0;transform:scale(2.2)}}}}</style>'
            )
        name = esc(p["title"])
        label_w = len(p["title"]) * 7.6 + 22
        out.append(
            f'<g>{glow}'
            f'<circle cx="{x:.1f}" cy="{y + 3:.1f}" r="21" fill="#000" opacity=".35"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="20" fill="{BG}" stroke="{ring}" stroke-width="2.5"/>'
            f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" font-family="{SANS}" font-size="17" '
            f'font-weight="800" fill="{INK}">{p["no"]}</text>'
            f'<rect x="{x - label_w / 2:.1f}" y="{y + 27:.1f}" width="{label_w:.1f}" height="22" rx="11" fill="{BG}" fill-opacity=".82"/>'
            f'<text x="{x:.1f}" y="{y + 42:.1f}" text-anchor="middle" font-family="{SANS}" font-size="12.5" '
            f'font-weight="700" fill="{INK}">{name}</text>'
            f'<text x="{x:.1f}" y="{y - 28:.1f}" text-anchor="middle" font-family="{MONO}" font-size="10" '
            f'font-weight="700" letter-spacing="1.5" fill="{ring}">{p["pos"]}</text>'
            + (
                f'<rect x="{x + 11:.1f}" y="{y - 21:.1f}" width="14" height="14" rx="3" fill="{GOLD}"/>'
                f'<text x="{x + 18:.1f}" y="{y - 10:.1f}" text-anchor="middle" font-family="{SANS}" font-size="10" '
                f'font-weight="900" fill="#1a1405">C</text>'
                if captain else ""
            )
            + "</g>"
        )
    return "".join(out)


def build():
    points, arrive, play = route()
    arrivals = dict(zip(PASSING_ORDER, arrive))
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)
    key_times = ";".join(f"{t:.4f}" for t in arrive) + ";1"
    key_points = ";".join(f"{t / play:.4f}" for t in arrive) + ";1"
    ball = (
        f'<path d="{path}" fill="none" stroke="{LIME}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 8"/>'
        f'<g><circle r="7" fill="#fff" stroke="#111" stroke-width="1.5"/>'
        f'<circle r="2.5" fill="#111"/>'
        f'<animateMotion dur="{CYCLE}s" repeatCount="indefinite" calcMode="linear" path="{path}" '
        f'keyPoints="{key_points}" keyTimes="{key_times}"/></g>'
    )
    cx, cy = at(0, 0)
    goal = (
        f'<text x="{cx}" y="{cy + 26}" text-anchor="middle" font-family="{SANS}" font-size="84" font-weight="900" '
        f'fill="{LIME}" letter-spacing="6" opacity="0" style="animation:goal {CYCLE}s linear infinite">GOAL!</text>'
    )
    head = (
        caption(X0 - 30, 40, "4-3-3 · build-up from the keeper", color=LIME, size=12, spacing=2.5)
        + f'<text x="{X0 + PW + 30}" y="40" text-anchor="end" font-family="{MONO}" font-size="12" fill="{DIM}">'
        f'attacking →</text>'
        + f'<text x="{W / 2}" y="{H - 14}" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{DIM}">'
        f'Every player is a project. Cards with details and links are below.</text>'
    )
    defs = (
        '<pattern id="net" width="6" height="6" patternUnits="userSpaceOnUse">'
        '<path d="M0 0L6 6M6 0L0 6" stroke="#e8f5e9" stroke-opacity=".35" stroke-width=".8"/></pattern>'
        f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
    )
    end = play * 100
    style = f"@keyframes goal{{0%,{end:.1f}%{{opacity:0}}{end + 2:.1f}%,{end + 10:.1f}%{{opacity:1}}100%{{opacity:0}}}}"
    body = (
        f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{BG}"/>'
        f"{grass()}{markings()}{ball}{players(arrivals)}{goal}{head}</g>"
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="{LINE}"/>'
    )
    label = "The Starting XI: eleven projects on a football pitch in a 4-3-3 formation"
    return write("pitch.svg", document(W, H, label, body, style, defs))


if __name__ == "__main__":
    print(build())
