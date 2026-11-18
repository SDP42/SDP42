"""Match stats on the big screen, with digits that roll like an odometer."""
from data import STATS
from svgkit import anim, caption, document, esc, write
from theme import DIM, INK, LIME, LINE, MONO, MONO_W, PANEL, PANEL_2

W, H = 1200, 190
SIZE = 54            # digit font size
STEP = SIZE * 1.15   # vertical distance between stacked digits
SPINS = 1            # full turns before settling


def odometer(value, cx, baseline, delay, uid):
    """Digits roll up from 0 and settle on `value`; other glyphs stay put."""
    adv = SIZE * MONO_W
    x = cx - len(value) * adv / 2
    out = []
    for i, ch in enumerate(value):
        if ch.isdigit():
            stack = "0123456789" * SPINS + "0123456789"
            target = SPINS * 10 + int(ch)
            column = "".join(
                f'<text x="{x:.1f}" y="{baseline + k * STEP:.1f}">{d}</text>' for k, d in enumerate(stack)
            )
            out.append(
                f'<g clip-path="url(#{uid})"><g style="transform:translateY(-{target * STEP:.1f}px);'
                f'animation:roll 1.8s cubic-bezier(.2,.9,.25,1) {delay + i * 0.12:.2f}s both">{column}</g></g>'
            )
        else:
            out.append(f'<text x="{x:.1f}" y="{baseline}">{esc(ch)}</text>')
        x += adv
    return "".join(out)


def build():
    gap = 14
    tile_w = (W - 40 - gap * (len(STATS) - 1)) / len(STATS)
    tiles, clips = [], []
    for i, (value, label) in enumerate(STATS):
        x = 20 + i * (tile_w + gap)
        uid = f"win{i}"
        clips.append(f'<clipPath id="{uid}"><rect x="{x}" y="58" width="{tile_w:.1f}" height="{STEP:.1f}"/></clipPath>')
        tiles.append(
            f'<g style="{anim("rise", 0.7, i * 0.1)}">'
            f'<rect x="{x:.1f}" y="44" width="{tile_w:.1f}" height="128" rx="16" fill="{PANEL_2}" stroke="{LINE}"/>'
            f'<g font-family="{MONO}" font-size="{SIZE}" font-weight="800" fill="{LIME}">'
            f"{odometer(value, x + tile_w / 2, 58 + SIZE * 0.95, 0.3 + i * 0.15, uid)}</g>"
            f'<text x="{x + tile_w / 2:.1f}" y="152" text-anchor="middle" font-family="{MONO}" font-size="12" '
            f'font-weight="700" letter-spacing="1.6" fill="{DIM}">{esc(label.upper())}</text></g>'
        )
    body = (
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{PANEL}" stroke="{LINE}"/>'
        + caption(24, 30, "Big screen · season so far", color=LIME, size=11.5, spacing=2.6)
        + f'<text x="{W - 24}" y="30" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{DIM}">'
        f'<tspan fill="{INK}">●</tspan> updated by hand from my repos</text>'
        + "".join(tiles)
    )
    label = "Match stats: " + ", ".join(f"{v} {l}" for v, l in STATS)
    return write("scoreboard.svg", document(W, H, label, body, "@keyframes roll{from{transform:translateY(0)}}", "".join(clips)))


if __name__ == "__main__":
    print(build())
