"""Small helpers for writing hand-tuned SVG as strings."""
from html import escape
from pathlib import Path

from theme import DIM, EASE, INK, KEYFRAMES, LINE, MONO, MONO_W, PANEL_2, REDUCED_MOTION

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def esc(text):
    """Escape text for use inside SVG markup."""
    return escape(str(text), quote=True)


def document(width, height, label, body, style="", defs=""):
    """Wrap a body in a standalone, accessible SVG document."""
    css = KEYFRAMES + style + REDUCED_MOTION
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{esc(label)}">\n'
        f"<title>{esc(label)}</title>\n"
        f"<defs>{defs}</defs>\n"
        f"<style>{' '.join(css.split())}</style>\n"
        f"{body}\n</svg>\n"
    )


def write(name, svg):
    """Write an SVG into assets/ and report its size."""
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return path


def anim(name, duration, delay=0.0, extra=""):
    """Inline style for a one-shot entrance animation."""
    return f"animation:{name} {duration}s {EASE} {delay:.2f}s both{extra}"


def mono_width(text, size):
    """Rendered width of monospace text."""
    return len(text) * size * MONO_W


def wrap(text, limit):
    """Greedy word wrap to at most `limit` characters per line."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if len(trial) > limit and line:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def chip(x, y, label, color=INK, size=12, pad=10, fill=PANEL_2, stroke=LINE):
    """A rounded monospace tag. Returns (markup, width)."""
    w = mono_width(label, size) + pad * 2
    h = size + 12
    markup = (
        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
        f'fill="{fill}" stroke="{stroke}"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" '
        f'font-family="{MONO}" font-size="{size}" font-weight="600" fill="{color}">{esc(label)}</text>'
    )
    return markup, w


def chips(x, y, labels, max_x, gap=8, **kw):
    """Lay out chips left to right, dropping any that would overflow max_x."""
    out = []
    for label in labels:
        markup, w = chip(x, y, label, **kw)
        if x + w > max_x:
            break
        out.append(markup)
        x += w + gap
    return "".join(out)
