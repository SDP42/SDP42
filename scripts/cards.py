"""Project cards for the Starting XI, styled like matchday player cards.

Each card is its own SVG so the README can wrap it in a link to the repo.
A spark of light runs around the border; the content rises in on load.
"""
from data import SQUAD
from svgkit import anim, caption, chips, document, esc, wrap, write
from theme import DIM, DISPLAY, GOLD, INK, LIME, LINE, MONO, MUTE, PANEL, SANS, SKY

W, H = 590, 340
PAD = 30


def perimeter(w, h, r=18):
    """Length of a rounded rectangle's outline."""
    return int(2 * (w + h) - 8 * r + 2 * 3.1416 * r)


def border(w, h, delay=0.0):
    """A hairline frame with a short lime spark travelling around it."""
    length = perimeter(w, h)
    return (
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>'
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="none" stroke="{LIME}" stroke-width="2" '
        f'stroke-linecap="round" stroke-dasharray="70 {length - 70}" opacity=".85" '
        f'style="animation:orbit 9s linear {delay:.1f}s infinite"/>'
    )


ORBIT = "@keyframes orbit{to{stroke-dashoffset:-%d}}"
