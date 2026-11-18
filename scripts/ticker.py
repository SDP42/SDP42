"""A scrolling stadium ticker, used in the hero and as a section divider."""
from data import TICKER
from svgkit import caption, document, esc, mono_width, write
from theme import INK, LIME, LINE, MONO

SEP = "   ◆   "
SPEED = 70  # pixels per second


def marquee(x, y, width, height, items=TICKER, size=13, color=INK, name="marquee"):
    """Markup and keyframes for an endlessly scrolling line of text.

    Two copies of the run sit side by side; sliding left by exactly one run
    length and repeating makes the loop seamless.
    """
    run = SEP.join(items) + SEP
    length = mono_width(run, size)
    clip = f"{name}-clip"
    markup = (
        f'<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{width}" height="{height}"/></clipPath>'
        f'<g clip-path="url(#{clip})"><g style="animation:{name} {length / SPEED:.1f}s linear infinite">'
        + "".join(
            f'<text x="{x + 16 + k * length:.1f}" y="{y + height / 2 + size * 0.36:.1f}" font-family="{MONO}" '
            f'font-size="{size}" font-weight="700" fill="{color}" xml:space="preserve">{esc(run)}</text>'
            for k in range(2)
        )
        + "</g></g>"
    )
    keyframes = f"@keyframes {name}{{to{{transform:translateX(-{length:.1f}px)}}}}"
    return markup, keyframes


def build():
    w, h = 1200, 46
    strip, frames = marquee(150, 0, w - 150, h)
    body = (
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="#070b12" stroke="{LINE}"/>'
        f'<rect x="10" y="10" width="124" height="26" rx="6" fill="{LIME}"/>'
        + caption(72, 28, "Honours", color="#0b1205", size=11.5, spacing=2.2, anchor="middle")
        + strip
    )
    return write("ticker.svg", document(w, h, "Honours: " + "; ".join(TICKER), body, frames))


if __name__ == "__main__":
    print(build())
