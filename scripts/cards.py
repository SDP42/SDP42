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


def card(player):
    no, pos = player["no"], player["pos"]
    head = (
        f'<text x="{W - PAD}" y="96" text-anchor="end" font-family="{DISPLAY}" font-size="96" font-weight="900" '
        f'fill="none" stroke="{LIME}" stroke-opacity=".9" stroke-width="1.5" style="{anim("fade", 1.2, 0.2)}">{no}</text>'
        + caption(PAD, 44, f"{pos} · {player['pos_name']}", color=LIME, size=11, spacing=2.5)
        + f'<text x="{PAD}" y="84" font-family="{SANS}" font-size="29" font-weight="800" fill="{INK}" '
        f'letter-spacing="-.6">{esc(player["title"])}</text>'
        + f'<text x="{PAD}" y="108" font-family="{MONO}" font-size="11.5" fill="{DIM}">{esc(player["event"])}</text>'
    )
    tagline = "".join(
        f'<text x="{PAD}" y="{142 + i * 21}" font-family="{SANS}" font-size="15.5" fill="{MUTE}">{esc(line)}</text>'
        for i, line in enumerate(wrap(player["tagline"], 62))
    )
    points = "".join(
        f'<g style="{anim("rise", 0.7, 0.35 + i * 0.12)}">'
        f'<path d="M{PAD} {181 + i * 27}l7 5-7 5z" fill="{LIME}"/>'
        f'<text x="{PAD + 16}" y="{191 + i * 27}" font-family="{SANS}" font-size="13.5" fill="{INK}">{esc(p)}</text></g>'
        for i, p in enumerate(player["points"])
    )
    foot_y = H - 54
    footer = (
        f'<line x1="{PAD}" y1="{foot_y - 14}" x2="{W - PAD}" y2="{foot_y - 14}" stroke="{LINE}"/>'
        + chips(PAD, foot_y, player["stack"], W - 170, size=11, pad=9)
        + f'<text x="{W - PAD}" y="{foot_y + 17}" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}">'
        f'{player["commits"]}<tspan fill="{DIM}" font-weight="400"> commits</tspan></text>'
    )
    if player.get("live"):
        footer += (
            f'<circle cx="{W - PAD - 82}" cy="120" r="4" fill="{SKY}" style="animation:pulse 1.6s ease-in-out infinite"/>'
            + caption(W - PAD, 124, "Live demo", color=SKY, size=10.5, spacing=1.6, anchor="end")
        )
    if player.get("captain"):
        footer += (
            f'<rect x="{W - 150}" y="28" width="22" height="22" rx="5" fill="{GOLD}"/>'
            f'<text x="{W - 139}" y="44" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="900" fill="#1a1405">C</text>'
        )
    body = (
        border(W, H, delay=no * 0.7)
        + f'<g style="{anim("rise", 0.8)}">{head}{tagline}</g>{points}'
        + f'<g style="{anim("fade", 1, 0.8)}">{footer}</g>'
    )
    label = f"#{no} {player['title']} ({player['pos_name']}): {player['tagline']}"
    return document(W, H, label, body, ORBIT % perimeter(W, H))


def build():
    return [write(f"cards/{p['no']:02d}-{p['slug']}.svg", card(p)) for p in SQUAD]


if __name__ == "__main__":
    for path in build():
        print(path)
