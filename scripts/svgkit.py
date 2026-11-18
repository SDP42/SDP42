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
