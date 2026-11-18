"""The hero: a floodlit stadium at night, the name on the big screen and a
live match ticker along the bottom.

Floodlights switch on one after another as the image loads, the outlined
surname draws itself in, and the ticker scrolls forever.
"""
import math
import random

from data import PROFILE, ROLES
from svgkit import anim, caption, document, esc, write
from ticker import marquee
from theme import BG, DIM, DISPLAY, GOLD, INK, LIME, LINE, MONO, MUTE, RED, SANS, SKY

W, H = 1200, 540
CX, CY = 935, 318          # centre of the stadium bowl
RX, RY = 238, 100          # outer radii of the bowl
TICK_Y = 496               # top of the ticker strip


def sky(rng):
    stars = []
    for i in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, 250)
        r = rng.choice((0.6, 0.8, 1.0, 1.3))
        tw = f' style="animation:pulse {rng.uniform(2.5, 6):.1f}s ease-in-out {rng.uniform(0, 4):.1f}s infinite"' if i % 3 == 0 else ""
        stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{rng.uniform(.25, .8):.2f}"{tw}/>')
    return (
        f'<rect width="{W}" height="{H}" fill="url(#night)"/>'
        f'<g>{"".join(stars)}</g>'
        f'<circle cx="1105" cy="70" r="20" fill="#e9eef7" opacity=".9"/>'
        f'<circle cx="1113" cy="64" r="18" fill="#0a1222"/>'
    )


def floodlights():
    """Two pylons whose beams switch on in turn, then sway slightly."""
    beams, rigs = [], []
    for i, (x, top, lean) in enumerate(((688, 112, 1), (1182, 112, -1))):
        on = f"animation:lightson .9s steps(3,end) {0.35 + i * 0.35:.2f}s both"
        beams.append(
            f'<polygon points="{x - 14},{top + 10} {x + 14},{top + 10} '
            f'{CX + lean * 40},{CY + 40} {CX - lean * 170},{CY + 10}" fill="url(#beam)" '
            f'style="transform-origin:{x}px {top}px;{on},'
            f'sway {9 + i * 2}s ease-in-out {i * 1.5}s infinite alternate"/>'
        )
        rigs.append(
            f'<line x1="{x}" y1="{top}" x2="{x}" y2="{CY + 60}" stroke="#2a364b" stroke-width="5"/>'
            f'<line x1="{x - 12}" y1="{CY + 60}" x2="{x}" y2="{top + 60}" stroke="#222d40" stroke-width="2"/>'
            f'<line x1="{x + 12}" y1="{CY + 60}" x2="{x}" y2="{top + 60}" stroke="#222d40" stroke-width="2"/>'
            f'<rect x="{x - 22}" y="{top - 14}" width="44" height="22" rx="3" fill="#1b2433" stroke="#33415a"/>'
            f'<circle cx="{x}" cy="{top - 3}" r="46" fill="url(#halo)" style="{on}"/>'
            + "".join(
                f'<circle cx="{x - 15 + j * 10}" cy="{top - 3}" r="3.4" fill="#fffbe6" style="{on}"/>'
                for j in range(4)
            )
        )
    # cables from the pylons to the roof, cable-stayed style
    cables = "".join(
        f'<line x1="{x}" y1="130" x2="{CX + dx}" y2="{CY - RY + 14 + abs(dx) // 9}" '
        f'stroke="#3a4a66" stroke-width="1" opacity=".7"/>'
        for x, dxs in ((688, (-210, -170, -130)), (1182, (130, 170, 210)))
        for dx in dxs
    )
    return f'<g>{"".join(beams)}</g>{cables}{"".join(rigs)}'
