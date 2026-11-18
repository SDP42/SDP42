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
