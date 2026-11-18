"""The trophy cabinet: three honours with a light sweeping across the glass."""
from data import HONOURS
from svgkit import anim, caption, document, esc, wrap, write
from theme import DIM, GOLD, INK, LINE, MUTE, PANEL, PANEL_2, SANS

W, H = 1200, 220
GAP, PAD = 14, 20


def build():
    tile_w = (W - PAD * 2 - GAP * (len(HONOURS) - 1)) / len(HONOURS)
    tiles = []
    for i, h in enumerate(HONOURS):
        x = PAD + i * (tile_w + GAP)
        note = "".join(
            f'<text x="{x + 28:.1f}" y="{150 + j * 19}" font-family="{SANS}" font-size="13.5" fill="{MUTE}">{esc(line)}</text>'
            for j, line in enumerate(wrap(h["note"], 46))
        )
        tiles.append(
            f'<g style="{anim("rise", 0.8, 0.15 * i)}">'
            f'<rect x="{x:.1f}" y="{PAD}" width="{tile_w:.1f}" height="{H - PAD * 2}" rx="16" fill="{PANEL_2}" stroke="{LINE}"/>'
            + caption(x + 28, 52, f"Honour 0{i + 1}", color=DIM, size=11, spacing=2.4)
            + f'<text x="{x + 26:.1f}" y="110" font-family="{SANS}" font-size="50" font-weight="900" fill="{GOLD}">{esc(h["big"])}</text>'
            f'<text x="{x + tile_w - 26:.1f}" y="108" text-anchor="end" font-family="{SANS}" font-size="17" '
            f'font-weight="800" fill="{INK}">{esc(h["label"])}</text>'
            f"{note}</g>"
        )
    sweep = (
        f'<rect x="-300" y="0" width="160" height="{H}" fill="url(#shine)" transform="skewX(-20)" '
        f'style="animation:shine 6s ease-in-out 1s infinite"/>'
    )
    defs = (
        '<linearGradient id="shine" x1="0" x2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="cabinet"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
    )
    body = (
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{PANEL}" stroke="{LINE}"/>'
        + "".join(tiles)
        + f'<g clip-path="url(#cabinet)">{sweep}</g>'
    )
    style = "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}40%,100%{transform:skewX(-20deg) translateX(1700px)}}"
    label = "Honours: " + "; ".join(f'{h["big"]} {h["label"]}' for h in HONOURS)
    return write("honours.svg", document(W, H, label, body, style, defs))


if __name__ == "__main__":
    print(build())
