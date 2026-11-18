"""The captain's project: a wide feature card for MIRAGE with its headline
numbers and the four stages of the system."""
from cards import ORBIT, border, perimeter
from data import SQUAD
from svgkit import anim, caption, chips, document, esc, wrap, write
from theme import DIM, DISPLAY, GOLD, INK, LIME, LINE, MONO, MUTE, PANEL_2, SANS

W, H = 1200, 430
PAD = 40


def build():
    p = next(player for player in SQUAD if player.get("captain"))
    head = (
        f'<rect x="{PAD}" y="34" width="26" height="26" rx="6" fill="{GOLD}"/>'
        f'<text x="{PAD + 13}" y="53" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="900" fill="#1a1405">C</text>'
        + caption(PAD + 40, 52, f"Captain · #{p['no']} {p['pos_name']} · {p['event']}", color=GOLD, size=12, spacing=2.5)
        + f'<text x="{PAD - 3}" y="128" font-family="{DISPLAY}" font-size="72" font-weight="900" fill="{INK}" '
        f'letter-spacing="2">{esc(p["title"])}</text>'
        f'<text x="{PAD}" y="160" font-family="{MONO}" font-size="14" fill="{LIME}">{esc(p["subtitle"])}</text>'
        f'<text x="{PAD}" y="192" font-family="{SANS}" font-size="18" fill="{MUTE}">{esc(p["tagline"])}</text>'
    )
    numbers = []
    tile_w = 128
    for i, (value, label) in enumerate(p["numbers"]):
        x = W - PAD - (4 - i) * (tile_w + 10) + 10
        numbers.append(
            f'<g style="{anim("rise", 0.8, 0.3 + i * 0.15)}">'
            f'<rect x="{x}" y="40" width="{tile_w}" height="104" rx="14" fill="{PANEL_2}" stroke="{LINE}"/>'
            f'<text x="{x + tile_w / 2}" y="98" text-anchor="middle" font-family="{SANS}" font-size="30" '
            f'font-weight="800" fill="{LIME}">{esc(value)}</text>'
            f'<text x="{x + tile_w / 2}" y="124" text-anchor="middle" font-family="{SANS}" font-size="12" '
            f'fill="{DIM}">{esc(label)}</text></g>'
        )
    stages = []
    col_w = (W - PAD * 2 - 30) / 4
    for i, (name, text) in enumerate(p["deep"]):
        x = PAD + i * (col_w + 10)
        lines = "".join(
            f'<text x="{x + 20}" y="{284 + j * 20}" font-family="{SANS}" font-size="13.5" fill="{MUTE}">{esc(line)}</text>'
            for j, line in enumerate(wrap(text, 36))
        )
        stages.append(
            f'<g style="{anim("rise", 0.8, 0.8 + i * 0.18)}">'
            f'<rect x="{x}" y="222" width="{col_w:.1f}" height="140" rx="14" fill="{PANEL_2}" stroke="{LINE}"/>'
            f'<text x="{x + 20}" y="256" font-family="{MONO}" font-size="12" font-weight="700" fill="{DIM}">0{i + 1}</text>'
            f'<text x="{x + 48}" y="256" font-family="{SANS}" font-size="17" font-weight="800" fill="{INK}">{esc(name)}</text>'
            f"{lines}</g>"
        )
        if i < 3:
            stages.append(
                f'<path d="M{x + col_w - 2:.1f} 292l10 0" stroke="{LIME}" stroke-width="2" '
                f'style="animation:pulse 1.8s ease-in-out {i * 0.3:.1f}s infinite"/>'
            )
    foot = (
        chips(PAD, 382, p["stack"], 760, size=11.5)
        + f'<text x="{W - PAD}" y="400" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}">'
        f'github.com/SDP42/isacaps2 <tspan fill="{LIME}">↗</tspan></text>'
    )
    body = border(W, H) + f'<g style="{anim("rise", 0.8)}">{head}</g>{"".join(numbers)}{"".join(stages)}' + (
        f'<g style="{anim("fade", 1, 1.4)}">{foot}</g>'
    )
    label = f"Captain's project — {p['title']}: {p['subtitle']}. {p['tagline']}"
    return write("captain.svg", document(W, H, label, body, ORBIT % perimeter(W, H)))


if __name__ == "__main__":
    print(build())
