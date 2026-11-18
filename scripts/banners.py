"""Section banners: a numbered stadium sign with a lime bar that sweeps in."""
from data import SECTIONS
from svgkit import anim, caption, document, esc, write
from theme import DIM, INK, LIME, LINE, PANEL, SANS

W, H = 1200, 96


def banner(number, place, heading):
    body = (
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{PANEL}" stroke="{LINE}"/>'
        f'<text x="34" y="62" font-family="{SANS}" font-size="40" font-weight="800" fill="none" '
        f'stroke="{LIME}" stroke-width="1.4" style="{anim("fade", 0.8)}">{number}</text>'
        f'<line x1="104" y1="26" x2="104" y2="70" stroke="{LINE}"/>'
        f'<g style="{anim("rise", 0.7, 0.1)}">{caption(126, 40, place, color=LIME, size=12, spacing=3)}</g>'
        f'<text x="124" y="72" font-family="{SANS}" font-size="27" font-weight="800" fill="{INK}" '
        f'letter-spacing="-.5" style="{anim("rise", 0.7, 0.2)}">{esc(heading)}</text>'
        f'<rect x="{W - 300}" y="46" width="250" height="4" rx="2" fill="{LINE}"/>'
        f'<rect x="{W - 300}" y="46" width="250" height="4" rx="2" fill="{LIME}" '
        f'style="transform-origin:{W - 300}px 48px;{anim("grow", 1.4, 0.3)}"/>'
        f'<circle cx="{W - 38}" cy="48" r="5" fill="{LIME}" style="animation:pulse 2s ease-in-out infinite"/>'
        f'<text x="{W - 50}" y="80" text-anchor="end" font-family="{SANS}" font-size="11" fill="{DIM}">SDP42 FC</text>'
    )
    return document(W, H, f"{number} · {place}: {heading}", body)


def build():
    return [write(f"sections/{slug}.svg", banner(n, place, heading)) for slug, n, place, heading in SECTIONS]


if __name__ == "__main__":
    for path in build():
        print(path)
