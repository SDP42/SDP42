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


def stadium(rng):
    facade = (
        f'<path d="M{CX - RX},{CY} A{RX},{RY} 0 0 0 {CX + RX},{CY} L{CX + RX},{CY + 44} '
        f'A{RX},{RY} 0 0 1 {CX - RX},{CY + 44} Z" fill="#111a29"/>'
        f'<path d="M{CX - RX},{CY} A{RX},{RY} 0 0 0 {CX + RX},{CY} L{CX + RX},{CY + 44} '
        f'A{RX},{RY} 0 0 1 {CX - RX},{CY + 44} Z" fill="url(#windows)"/>'
    )
    band = (
        f'<ellipse cx="{CX}" cy="{CY + 6}" rx="{RX}" ry="{RY}" fill="none" stroke="{LIME}" stroke-width="3" opacity=".9">'
        f'<animate attributeName="stroke" dur="12s" repeatCount="indefinite" '
        f'values="{LIME};{SKY};{GOLD};{RED};{LIME}"/></ellipse>'
    )
    shell = f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="#0f1726" stroke="#2b3a55" stroke-width="2"/>'
    tiers = "".join(
        f'<ellipse cx="{CX}" cy="{CY + 4}" rx="{RX - k * 22}" ry="{RY - k * 9}" fill="{c}"/>'
        for k, c in enumerate(("#18233a", "#1d2a44", "#22314f", "#1a2742"), start=1)
    )
    pitch_pts = f"{CX - 112},{CY - 16} {CX + 112},{CY - 16} {CX + 142},{CY + 38} {CX - 142},{CY + 38}"
    stripes = "".join(
        f'<rect x="{CX - 150}" y="{CY - 16 + k * 6}" width="300" height="6" fill="{"#1c6b34" if k % 2 else "#1f7a3b"}"/>'
        for k in range(9)
    )
    lines = (
        f'<polygon points="{pitch_pts}" fill="none" stroke="#e8f5e9" stroke-opacity=".55" stroke-width="1.2"/>'
        f'<line x1="{CX}" y1="{CY - 16}" x2="{CX}" y2="{CY + 38}" stroke="#e8f5e9" stroke-opacity=".55"/>'
        f'<ellipse cx="{CX}" cy="{CY + 11}" rx="22" ry="8" fill="none" stroke="#e8f5e9" stroke-opacity=".55"/>'
    )
    # little players chasing the ball
    players = []
    for i in range(8):
        px, py = CX + rng.uniform(-110, 110), CY + rng.uniform(-8, 30)
        dx, dy = rng.uniform(-30, 30), rng.uniform(-6, 6)
        colour = LIME if i % 2 else RED
        players.append(
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="2.2" fill="{colour}">'
            f'<animateTransform attributeName="transform" type="translate" dur="{rng.uniform(5, 9):.1f}s" '
            f'repeatCount="indefinite" values="0 0;{dx:.0f} {dy:.0f};0 0"/></circle>'
        )
    ball = (
        f'<circle r="1.8" fill="#fff"><animateMotion dur="7s" repeatCount="indefinite" '
        f'path="M{CX - 90},{CY + 10} Q{CX - 20},{CY - 12} {CX + 60},{CY + 20} T{CX + 100},{CY} '
        f'Q{CX},{CY + 30} {CX - 90},{CY + 10}"/></circle>'
    )
    pitch = (
        f'<clipPath id="pitch"><polygon points="{pitch_pts}"/></clipPath>'
        f'<g clip-path="url(#pitch)">{stripes}</g>{lines}{"".join(players)}{ball}'
    )
    flashes = []
    for i in range(36):
        a = rng.uniform(0, 6.283)
        k = rng.uniform(0.62, 0.9)
        x, y = CX + math.cos(a) * RX * k, CY + 4 + math.sin(a) * RY * k
        flashes.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.3" fill="#fff" opacity="0" '
            f'style="animation:flash {rng.uniform(3, 7):.1f}s linear {rng.uniform(0, 6):.1f}s infinite"/>'
        )
    roof = (
        f'<ellipse cx="{CX}" cy="{CY - 2}" rx="{RX - 8}" ry="{RY - 4}" fill="none" stroke="#33445f" stroke-width="14" opacity=".85"/>'
        f'<ellipse cx="{CX}" cy="{CY - 2}" rx="{RX - 15}" ry="{RY - 7}" fill="none" stroke="#9fb3d1" stroke-width=".8" opacity=".35"/>'
    )
    towers = "".join(
        f'<g><rect x="{x - 17}" y="{CY + 8}" width="34" height="72" fill="#1a2436"/>'
        f'<ellipse cx="{x}" cy="{CY + 8}" rx="17" ry="5" fill="#26324a"/>'
        + "".join(
            f'<line x1="{x - 17}" y1="{CY + 18 + k * 13}" x2="{x + 17}" y2="{CY + 13 + k * 13}" stroke="#7fd4ff" stroke-opacity=".55" stroke-width="2"/>'
            for k in range(5)
        )
        + "</g>"
        for x in (CX - RX + 18, CX + RX - 18)
    )
    lot = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.4" fill="{GOLD}" opacity=".55"/>'
        for y in (CY + 112, CY + 132, CY + 152)
        for x in range(CX - 300 + (y % 40), CX + 290, 34)
    )
    return (
        f'<g style="{anim("rise", 1.2, 0.1)}">'
        f"{lot}{facade}{shell}{tiers}{pitch}{''.join(flashes)}{roof}{band}{towers}</g>"
    )
