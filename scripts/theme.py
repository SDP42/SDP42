"""Design tokens shared by every generated SVG.

The palette mirrors the stadium portfolio (stadium-portfolio.vercel.app):
a floodlit night sky, lime signage, gold honours and a red LIVE light.
"""

# ── colour ───────────────────────────────────────────────────────────────────
BG = "#05080d"      # night sky behind every panel
PANEL = "#0b111b"   # card surface
PANEL_2 = "#101827" # raised surface (chips, tiles)
LINE = "#1c2636"    # hairlines and borders
INK = "#f4f6fa"     # primary text
MUTE = "#aab5c8"    # secondary text
DIM = "#6b7689"     # captions, meta
LIME = "#d4ff3a"    # signature accent
RED = "#ff2440"     # LIVE light
GOLD = "#f3c75a"    # honours
SKY = "#62c8ff"     # links, highlights
GRASS = "#123d1f"   # pitch
GRASS_2 = "#164a26" # pitch stripe

# ── type ─────────────────────────────────────────────────────────────────────
# GitHub renders README SVGs as <img>, so web fonts never load: stick to
# fonts that ship with Windows, macOS and Linux desktops.
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif"
DISPLAY = "'Arial Black','Segoe UI Black','Helvetica Neue',Impact,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
MONO_W = 0.6  # advance width of a monospace glyph, in ems

# ── motion ───────────────────────────────────────────────────────────────────
EASE = "cubic-bezier(.22,.8,.2,1)"

# Every element's resting style is its final state; animations only describe
# how it arrives. With motion turned off the image still reads correctly.
REDUCED_MOTION = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

# Entrance keyframes reused across assets.
KEYFRAMES = """
@keyframes rise{from{opacity:0;transform:translateY(14px)}}
@keyframes fade{from{opacity:0}}
@keyframes grow{from{transform:scaleX(0)}}
@keyframes pulse{50%{opacity:.25}}
@keyframes blink{50%{opacity:0}}
"""
