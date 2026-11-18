"""The substitutes' bench: projects that did not make the Starting XI."""
from data import BENCH
from svgkit import anim, chips, document, esc, wrap, write
from theme import DIM, INK, LIME, LINE, MONO, MUTE, PANEL, PANEL_2, SANS

W = 1200
COLS, GAP, PAD = 3, 14, 20
TILE_H = 132


def build():
    rows = -(-len(BENCH) // COLS)
    h = PAD * 2 + rows * TILE_H + (rows - 1) * GAP
    tile_w = (W - PAD * 2 - GAP * (COLS - 1)) / COLS
    tiles = []
    for i, item in enumerate(BENCH):
        col, row = i % COLS, i // COLS
        x, y = PAD + col * (tile_w + GAP), PAD + row * (TILE_H + GAP)
        lines = "".join(
            f'<text x="{x + 20:.1f}" y="{y + 64 + j * 18}" font-family="{SANS}" font-size="13" fill="{MUTE}">{esc(line)}</text>'
            for j, line in enumerate(wrap(item["tagline"], 52)[:2])
        )
        tiles.append(
            f'<g style="{anim("rise", 0.7, 0.08 * i)}">'
            f'<rect x="{x:.1f}" y="{y}" width="{tile_w:.1f}" height="{TILE_H}" rx="14" fill="{PANEL_2}" stroke="{LINE}"/>'
            f'<text x="{x + 20:.1f}" y="{y + 36}" font-family="{SANS}" font-size="17" font-weight="800" fill="{INK}">{esc(item["title"])}</text>'
            f'<text x="{x + tile_w - 18:.1f}" y="{y + 34}" text-anchor="end" font-family="{MONO}" font-size="10.5" '
            f'font-weight="700" letter-spacing="1.4" fill="{LIME if item["url"] else DIM}">'
            f'{"SUB ↑" if item["url"] else "PRIVATE"}</text>'
            f"{lines}"
            + chips(x + 20, y + TILE_H - 36, item["stack"], x + tile_w - 16, size=10.5, pad=8, fill=PANEL)
            + "</g>"
        )
    body = f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="20" fill="{PANEL}" stroke="{LINE}"/>' + "".join(tiles)
    label = "On the bench: " + ", ".join(b["title"] for b in BENCH)
    return write("bench.svg", document(W, h, label, body))


if __name__ == "__main__":
    print(build())
