"""Calls to action: the portfolio banner and the full-time footer."""
import random

from data import PORTFOLIO
from svgkit import anim, caption, document, write
from theme import BG, DIM, DISPLAY, GOLD, INK, LIME, LINE, MONO, MUTE, PANEL, RED, SANS, SKY

W = 1200


def button(x, y, label, w=270, h=52):
    """A lime pill with a ring that keeps pulsing outwards."""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="none" stroke="{LIME}" stroke-width="2" '
        f'style="transform-origin:{x + w / 2}px {y + h / 2}px;animation:ring 2.4s ease-out infinite"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{LIME}"/>'
        f'<text x="{x + w / 2}" y="{y + h / 2 + 5.5}" text-anchor="middle" font-family="{SANS}" font-size="16" '
        f'font-weight="800" fill="#0b1205">{label}</text>'
    )


RING = "@keyframes ring{from{opacity:.8;transform:scale(1)}to{opacity:0;transform:scale(1.18,1.5)}}"


def mini_stadium(cx, cy):
    rings = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{150 - k * 22}" ry="{62 - k * 9}" fill="{c}"/>'
        for k, c in enumerate(("#141e31", "#1a2640", "#20304f", "#1a2742"))
    )
    return (
        f'<ellipse cx="{cx}" cy="{cy + 18}" rx="150" ry="62" fill="#0d1420"/>'
        f"{rings}"
        f'<rect x="{cx - 52}" y="{cy - 16}" width="104" height="32" rx="2" fill="#1f7a3b" transform="skewX(-12)" '
        f'style="transform-origin:{cx}px {cy}px"/>'
        f'<ellipse cx="{cx}" cy="{cy}" rx="150" ry="62" fill="none" stroke="{LIME}" stroke-width="2.5">'
        f'<animate attributeName="stroke" dur="10s" repeatCount="indefinite" values="{LIME};{SKY};{GOLD};{LIME}"/></ellipse>'
        f'<circle r="5" fill="#fffbe6"><animateMotion dur="6s" repeatCount="indefinite" '
        f'path="M{cx - 150},{cy} a150,62 0 1,0 300,0 a150,62 0 1,0 -300,0"/></circle>'
    )


def portfolio():
    h = 230
    host = PORTFOLIO.split("//", 1)[1]
    body = (
        f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="22" fill="{PANEL}" stroke="{LINE}"/>'
        f'<g style="{anim("rise", 0.8)}">'
        + caption(40, 54, "The full matchday experience", color=LIME, size=12, spacing=3)
        + f'<text x="38" y="102" font-family="{SANS}" font-size="36" font-weight="800" fill="{INK}" letter-spacing="-1">'
        f"Walk into my 3D stadium portfolio</text>"
        f'<text x="40" y="134" font-family="{SANS}" font-size="16" fill="{MUTE}">'
        f"Floodlights, a live match, a penalty shootout and a project document for every player.</text></g>"
        f'<g style="{anim("rise", 0.8, 0.3)}">{button(40, 156, "Enter the stadium  →")}'
        f'<text x="330" y="188" font-family="{MONO}" font-size="14" fill="{DIM}">{host}</text></g>'
        f'<g style="{anim("fade", 1.2, 0.4)}">{mini_stadium(980, 116)}</g>'
    )
    return write("portfolio.svg", document(W, h, f"Visit my 3D stadium portfolio at {host}", body, RING))


def footer():
    h = 250
    rng = random.Random(7)
    crowd = []
    for i in range(96):
        x = 14 + i * 12.3
        colour = rng.choice((LIME, SKY, GOLD, RED, INK, INK, "#5b6b86"))
        delay = i * 0.04
        crowd.append(
            f'<circle cx="{x:.1f}" cy="{h - 26}" r="4" fill="{colour}" opacity=".85" '
            f'style="animation:wave 4.5s ease-in-out {delay:.2f}s infinite"/>'
        )
    body = (
        f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="22" fill="{BG}" stroke="{LINE}"/>'
        f'<g style="{anim("rise", 0.8)}">'
        f'<rect x="{W / 2 - 160}" y="34" width="320" height="58" rx="10" fill="#070b12" stroke="{LINE}"/>'
        f'<text x="{W / 2 - 128}" y="70" font-family="{MONO}" font-size="14" font-weight="800" fill="{RED}">FT</text>'
        f'<text x="{W / 2 - 92}" y="70" font-family="{MONO}" font-size="16" font-weight="800" fill="{INK}">SDP42</text>'
        f'<text x="{W / 2 + 6}" y="72" text-anchor="middle" font-family="{DISPLAY}" font-size="24" fill="{LIME}">1 – 0</text>'
        f'<text x="{W / 2 + 54}" y="70" font-family="{MONO}" font-size="16" font-weight="800" fill="{INK}">BUGS</text>'
        f'<text x="{W / 2}" y="140" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="800" fill="{INK}" letter-spacing="-.6">'
        f"Thanks for visiting the stadium.</text>"
        f'<text x="{W / 2}" y="172" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTE}">'
        f"Let's turn raw data into decisions, together.</text></g>"
        f'<g>{"".join(crowd)}</g>'
    )
    style = "@keyframes wave{0%,30%,100%{transform:translateY(0)}12%{transform:translateY(-16px)}}"
    return write("footer.svg", document(W, h, "Full time: SDP42 1, Bugs 0. Thanks for visiting the stadium.", body, style))


def build():
    return [portfolio(), footer()]


if __name__ == "__main__":
    for path in build():
        print(path)
