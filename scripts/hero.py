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


def headline():
    cycle = 3.2 * len(ROLES)
    share = 100 / len(ROLES)
    words = "".join(
        f'<text class="word" x="180" y="372" style="opacity:{1 if i == 0 else 0};'
        f'animation:word{i} {cycle}s infinite">{esc(w)}</text>'
        for i, w in enumerate(ROLES)
    )
    frames = "".join(
        f"@keyframes word{i}{{0%,{max(i * share - 0.01, 0):.2f}%{{opacity:0}}"
        f"{i * share + 2:.2f}%,{(i + 1) * share - 3:.2f}%{{opacity:1}}"
        f"{(i + 1) * share:.2f}%,100%{{opacity:0}}}}"
        for i in range(len(ROLES))
    )
    text = (
        f'<circle cx="56" cy="74" r="6" fill="{RED}" style="animation:pulse 1.4s ease-in-out infinite"/>'
        f'<circle cx="56" cy="74" r="11" fill="none" stroke="{RED}" stroke-opacity=".5"/>'
        + caption(74, 79, "Live from Mumbai", color=RED, size=13, spacing=3)
        + f'<text x="46" y="196" font-family="{DISPLAY}" font-size="104" font-weight="900" fill="{INK}" '
        f'textLength="560" lengthAdjust="spacingAndGlyphs" style="{anim("rise", 0.9, 0.15)}">{PROFILE["first"]}</text>'
        f'<text class="outline" x="46" y="300" font-family="{DISPLAY}" font-size="104" font-weight="900" '
        f'textLength="560" lengthAdjust="spacingAndGlyphs">{PROFILE["last"]}</text>'
        f'<g font-family="{MONO}" font-size="19" font-weight="600">'
        f'<text x="48" y="372" fill="{DIM}">&gt; building</text>{words}'
        '</g>'
        f'<text x="48" y="418" font-family="{SANS}" font-size="18" fill="{MUTE}" style="{anim("rise", 0.8, 0.9)}">'
        f'AI &amp; Data Science undergrad at DJSCE · CGPA 9.70 · 5× hackathon winner.</text>'
        f'<text x="48" y="444" font-family="{SANS}" font-size="18" fill="{MUTE}" style="{anim("rise", 0.8, 1.0)}">'
        f"{esc(PROFILE['summary'])} This is my stadium.</text>"
    )
    return text, frames


def ticker():
    left = 330
    marquee_markup, frames = marquee(left, TICK_Y, W - left, H - TICK_Y, name="hero-tick")
    board = (
        f'<rect x="0" y="{TICK_Y}" width="{W}" height="{H - TICK_Y}" fill="#070b12"/>'
        f'<line x1="0" y1="{TICK_Y}" x2="{W}" y2="{TICK_Y}" stroke="{LINE}"/>'
        f'<rect x="18" y="{TICK_Y + 10}" width="52" height="24" rx="4" fill="{RED}"/>'
        + caption(44, TICK_Y + 27, "Live", color="#fff", size=12, spacing=1.5, anchor="middle")
        + f'<text x="84" y="{TICK_Y + 27}" font-family="{MONO}" font-size="13" font-weight="700" fill="{INK}">SDP42</text>'
        f'<rect x="136" y="{TICK_Y + 9}" width="24" height="26" rx="4" fill="{INK}"/>'
        f'<text x="148" y="{TICK_Y + 27}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="800" fill="{BG}">1</text>'
        f'<text x="170" y="{TICK_Y + 27}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{DIM}">–</text>'
        f'<rect x="180" y="{TICK_Y + 9}" width="24" height="26" rx="4" fill="{INK}"/>'
        f'<text x="192" y="{TICK_Y + 27}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="800" fill="{BG}">0</text>'
        f'<text x="214" y="{TICK_Y + 27}" font-family="{MONO}" font-size="13" font-weight="700" fill="{INK}">BUGS</text>'
        f'<text x="262" y="{TICK_Y + 27}" font-family="{MONO}" font-size="13" font-weight="700" fill="{LIME}">90+<tspan style="animation:blink 1s steps(1) infinite">\'</tspan></text>'
        f'<line x1="{left}" y1="{TICK_Y + 8}" x2="{left}" y2="{H - 8}" stroke="{LINE}"/>'
    )
    return board + marquee_markup, frames


def build():
    rng = random.Random(42)
    text, word_frames = headline()
    strip, marquee_frames = ticker()
    defs = (
        f'<linearGradient id="night" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#0a1222"/><stop offset=".6" stop-color="{BG}"/><stop offset="1" stop-color="#03050a"/></linearGradient>'
        f'<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#fffbe6" stop-opacity=".55"/><stop offset="1" stop-color="#fffbe6" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="halo"><stop offset="0" stop-color="#fffbe6" stop-opacity=".7"/><stop offset="1" stop-color="#fffbe6" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="vignette" cx=".28" cy=".5" r=".7"><stop offset="0" stop-color="{BG}" stop-opacity=".92"/>'
        f'<stop offset=".55" stop-color="{BG}" stop-opacity=".55"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>'
        f'<pattern id="windows" width="9" height="11" patternUnits="userSpaceOnUse">'
        f'<rect x="2" y="3" width="4" height="6" fill="{GOLD}" opacity=".35"/></pattern>'
        f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
    )
    style = (
        f".word{{fill:{LIME}}}"
        f".outline{{fill:none;stroke:{LIME};stroke-width:2.4;stroke-dasharray:1600;stroke-dashoffset:0;"
        f"animation:draw 2.6s {'cubic-bezier(.65,0,.35,1)'} .5s both}}"
        "@keyframes draw{from{stroke-dashoffset:1600}}"
        "@keyframes lightson{from{opacity:0}}"
        "@keyframes sway{to{transform:rotate(2.5deg)}}"
        "@keyframes flash{0%,92%,100%{opacity:0}95%{opacity:1}}"
        + word_frames
        + marquee_frames
    )
    body = (
        f'<g clip-path="url(#frame)">{sky(rng)}{floodlights()}{stadium(rng)}'
        f'<rect width="760" height="{TICK_Y}" fill="url(#vignette)"/>{text}{strip}</g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="{LINE}"/>'
    )
    label = f"{PROFILE['name']}: {PROFILE['role']}. {PROFILE['summary']}"
    return write("hero.svg", document(W, H, label, body, style, defs))


if __name__ == "__main__":
    print(build())
