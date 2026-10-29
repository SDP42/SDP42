"""Generate the animated SVGs used by the profile README.

GitHub strips scripts and styles from README HTML, but SVG images keep their
own CSS keyframes and SMIL animations, so every moving part lives here.

The hero is a rotating 3D scatter plot. Spinning a point about the vertical
axis under a fixed camera tilt moves it along a fixed ellipse on screen, so
each data point glides along its own ellipse (cheap animateMotion) while its
size and opacity follow its depth. Text never depends on an animation, so the
page reads correctly even where animations are paused.

    python assets/build.py
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).parent

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,monospace"

INK, MUTED, FAINT = "#0F172A", "#475569", "#94A3B8"
LINE, PANEL, WHITE = "#E2E8F0", "#F8FAFC", "#FFFFFF"
INDIGO, TEAL, AMBER, ROSE = "#4F46E5", "#0D9488", "#F59E0B", "#E11D48"
EASE = "cubic-bezier(.22,.8,.2,1)"

TILT = 0.36   # camera pitch, radians
SPIN = 28     # seconds per revolution
SAMPLES = 24  # depth/position samples per revolution


def write(name, body):
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print(f"wrote {name} ({len(body) // 1024} KB)")


# ── 3D projection helpers ───────────────────────────────────────────────────
def project(cx, cy, s, X, Y, Z, a):
    """Screen position and depth (-R..R) of a point after spinning by a. +Y is down."""
    ct, st = math.cos(TILT), math.sin(TILT)
    R, th = math.hypot(X, Z), math.atan2(Z, X)
    psi = th - a
    x = cx + s * R * math.cos(psi)
    y = cy + s * (Y * ct - R * st * math.sin(psi))
    return x, y, Y * st + R * ct * math.sin(psi)


def orbit(cx, cy, s, X, Y, Z):
    """Closed elliptical path a point follows over one revolution, starting at a=0."""
    ct, st = math.cos(TILT), math.sin(TILT)
    R, th = max(math.hypot(X, Z), 0.003), math.atan2(Z, X)
    ex, ey, rx, ry = cx, cy + s * Y * ct, s * R, s * R * st

    def at(psi):
        return ex + rx * math.cos(psi), ey - ry * math.sin(psi)

    (x0, y0), (x1, y1) = at(th), at(th - math.pi)
    return (f"M{x0:.1f},{y0:.1f}A{rx:.1f},{ry:.1f} 0 1,1 {x1:.1f},{y1:.1f}"
            f"A{rx:.1f},{ry:.1f} 0 1,1 {x0:.1f},{y0:.1f}")


def anim(attr, values):
    return f'<animate attributeName="{attr}" dur="{SPIN}s" repeatCount="indefinite" values="{";".join(values)}"/>'


def point(cx, cy, s, X, Y, Z, r0, color, depth_max, stroke=None):
    depths = [project(cx, cy, s, X, Y, Z, 2 * math.pi * k / SAMPLES)[2] / depth_max for k in range(SAMPLES + 1)]
    rs = [f"{r0 * (1 + 0.35 * d):.2f}" for d in depths]
    ops = [f"{0.45 + 0.55 * (d + 1) / 2:.2f}" for d in depths]
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<circle r="{rs[0]}" fill="{color}" opacity="{ops[0]}"{st}>'
            f'<animateMotion dur="{SPIN}s" repeatCount="indefinite" path="{orbit(cx, cy, s, X, Y, Z)}"/>'
            f'{anim("r", rs)}{anim("opacity", ops)}</circle>')


def segment(cx, cy, s, p, q, **attrs):
    """A 3D line segment whose endpoints follow the rotation."""
    xs1, ys1, xs2, ys2 = [], [], [], []
    for k in range(SAMPLES + 1):
        a = 2 * math.pi * k / SAMPLES
        x1, y1, _ = project(cx, cy, s, *p, a)
        x2, y2, _ = project(cx, cy, s, *q, a)
        xs1.append(f"{x1:.1f}"); ys1.append(f"{y1:.1f}"); xs2.append(f"{x2:.1f}"); ys2.append(f"{y2:.1f}")
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return (f'<line x1="{xs1[0]}" y1="{ys1[0]}" x2="{xs2[0]}" y2="{ys2[0]}" {extra}>'
            f'{anim("x1", xs1)}{anim("y1", ys1)}{anim("x2", xs2)}{anim("y2", ys2)}</line>')


def floor(cx, cy, s, corners, fill):
    frames = []
    for k in range(SAMPLES + 1):
        a = 2 * math.pi * k / SAMPLES
        frames.append(" ".join(f"{x:.1f},{y:.1f}" for x, y, _ in (project(cx, cy, s, *c, a) for c in corners)))
    return f'<polygon points="{frames[0]}" fill="{fill}">{anim("points", frames)}</polygon>'


def label(cx, cy, s, X, Y, Z, text, color):
    return (f'<text x="0" y="0" text-anchor="middle" dy="5" style="font:700 14px {MONO};fill:{color}">{text}'
            f'<animateMotion dur="{SPIN}s" repeatCount="indefinite" path="{orbit(cx, cy, s, X, Y, Z)}"/></text>')


def scatter3d(cx, cy, s):
    rnd = random.Random(7)
    B = 1.0  # half-size of the plot cube; +Y is down on screen, floor at Y=+B
    out = [floor(cx, cy, s, [(-B, B, -B), (B, B, -B), (B, B, B), (-B, B, B)], "#EEF2FF")]
    for i in range(1, 4):
        g = -B + i * 2 * B / 4
        out.append(segment(cx, cy, s, (g, B, -B), (g, B, B), stroke="#C7D2FE", stroke_width="1"))
        out.append(segment(cx, cy, s, (-B, B, g), (B, B, g), stroke="#C7D2FE", stroke_width="1"))
    o = (-B, B, -B)
    for end, name in (((B, B, -B), "x"), ((-B, -B, -B), "y"), ((-B, B, B), "z")):
        out.append(segment(cx, cy, s, o, end, stroke=MUTED, stroke_width="2", stroke_linecap="round"))
        lx, ly, lz = (e + (e - b) * 0.12 for e, b in zip(end, o))
        out.append(label(cx, cy, s, lx, ly, lz, name, MUTED))

    clusters = [((-0.45, 0.35, -0.35), INDIGO), ((0.45, -0.1, 0.35), TEAL), ((0.1, -0.5, -0.45), AMBER)]
    pts = []
    for (mx, my, mz), color in clusters:
        for _ in range(34):
            x = max(-0.95, min(0.95, rnd.gauss(mx, 0.17)))
            y = max(-0.95, min(0.95, rnd.gauss(my, 0.17)))
            z = max(-0.95, min(0.95, rnd.gauss(mz, 0.17)))
            pts.append((x, -y, z, color))
    rmax = math.sqrt(3) * B
    out += [point(cx, cy, s, x, y, z, 5.2, c, rmax) for x, y, z, c in pts]
    out += [point(cx, cy, s, mx, -my, mz, 9, c, rmax, stroke=WHITE) for (mx, my, mz), c in clusters]
    return "".join(out)


# ── hero ────────────────────────────────────────────────────────────────────
def hero():
    W, H, KX, KY, S = 1200, 470, 905, 238, 112
    words = ["'machine learning'", "'deep learning'", "'SQL &amp; databases'",
             "'generative AI'", "'data analysis'"]
    step = 2.8
    cycle = step * len(words)
    word_svg = "".join(
        f'<text class="word{" w0" if i == 0 else ""}" x="186" y="392" style="animation-delay:{i * step}s">{w}</text>'
        for i, w in enumerate(words))

    def meta(x, icon, text):
        return f'<g transform="translate({x} 306)">{icon}<text x="24" y="5" class="meta">{text}</text></g>'

    pin = f'<path d="M8 -9a6 6 0 0 1 6 6c0 4.5-6 10-6 10s-6-5.5-6-10a6 6 0 0 1 6-6z" fill="none" stroke="{INDIGO}" stroke-width="1.8"/><circle cx="8" cy="-3" r="2" fill="{INDIGO}"/>'
    cap = f'<path d="M0 -3 L9 -8 L18 -3 L9 2 Z" fill="none" stroke="{INDIGO}" stroke-width="1.8" stroke-linejoin="round"/><path d="M4 0 v4 c3 2.5 7 2.5 10 0 v-4" fill="none" stroke="{INDIGO}" stroke-width="1.8"/>'
    chart = f'<path d="M1 7 V-7 M1 7 H17 M5 3 V-1 M9 3 V-5 M13 3 V-2" fill="none" stroke="{INDIGO}" stroke-width="1.8" stroke-linecap="round"/>'

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Swayam Panchal: data science, machine learning and generative AI">
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#CBD5E1"/></pattern>
  <radialGradient id="fade" cx="0.3" cy="0.45" r="0.75"><stop offset="0" stop-color="{WHITE}"/><stop offset="0.55" stop-color="{WHITE}" stop-opacity="0.9"/><stop offset="1" stop-color="{WHITE}" stop-opacity="0.2"/></radialGradient>
  <linearGradient id="name" gradientUnits="userSpaceOnUse" x1="320" y1="0" x2="600" y2="0"><stop offset="0" stop-color="{INDIGO}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
</defs>
<style>
  .eyebrow{{font:700 12.5px {MONO};letter-spacing:2.5px;fill:{INDIGO}}}
  .name{{font:800 74px {SANS};letter-spacing:-2.5px;fill:{INK}}}
  .lead{{font:400 21px {SANS};fill:{MUTED}}}
  .meta{{font:500 15px {SANS};fill:{MUTED}}}
  .prompt{{font:600 17px {MONO};fill:{FAINT}}}
  .word{{font:600 17px {MONO};fill:{TEAL};opacity:0;animation:word {cycle}s {EASE} infinite both}}
  .w0{{opacity:1}}
  @keyframes word{{0%{{opacity:0;transform:translateY(10px)}}{100 * 0.35 / cycle:.2f}%,{100 * (step - 0.4) / cycle:.2f}%{{opacity:1;transform:none}}{100 * step / cycle:.2f}%,100%{{opacity:0;transform:translateY(-8px)}}}}
  .blob{{animation:drift 18s ease-in-out infinite alternate}}
  .b2{{animation-duration:23s;animation-delay:-9s}}
  @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-40px,30px)}}}}
</style>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{WHITE}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <g filter="url(#soft)" opacity="0.5">
    <circle class="blob" cx="880" cy="140" r="150" fill="#E0E7FF"/>
    <circle class="blob b2" cx="1000" cy="380" r="140" fill="#CCFBF1"/>
  </g>
  {scatter3d(KX, KY, S)}

  <rect x="70" y="72" width="256" height="32" rx="16" fill="#EEF2FF"/>
  <circle cx="90" cy="88" r="4.5" fill="{INDIGO}"/>
  <text class="eyebrow" x="104" y="93">DATA SCIENCE · ML · GENAI</text>
  <text class="name" x="66" y="182">Swayam <tspan fill="url(#name)">Panchal</tspan></text>
  <text class="lead" x="70" y="228">I turn raw data into decisions: SQL and analysis,</text>
  <text class="lead" x="70" y="258">machine &amp; deep learning, and GenAI systems.</text>
  {meta(70, pin, "Mumbai, India")}
  {meta(216, cap, "B.Tech AI &amp; DS · DJSCE")}
  {meta(442, chart, "Python · SQL · PyTorch")}
  <line x1="70" y1="344" x2="600" y2="344" stroke="{LINE}"/>
  <text class="prompt" x="70" y="392">&gt;&gt;&gt; focus =</text>
  {word_svg}
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="{LINE}"/>
</svg>"""


# ── "what I do" strip ───────────────────────────────────────────────────────
def capabilities():
    W, CW, CH, GAP = 1200, 582, 318, 36
    H = 2 * CH + GAP
    rnd = random.Random(3)
    mono = f"font-family=\"{MONO}\""

    # data analysis: histogram with a density curve
    heights = [12, 22, 38, 58, 78, 92, 88, 70, 50, 32, 18, 9]
    eda = "".join(
        f'<rect class="hb" x="{40 + i * 42}" y="{112 - h}" width="30" height="{h}" rx="4" fill="{INDIGO}" fill-opacity="{0.3 + 0.05 * i:.2f}" style="animation-delay:{i * 0.06:.2f}s"/>'
        for i, h in enumerate(heights))
    eda += f'<polyline class="draw" points="{" ".join(f"{55 + i * 42},{106 - h}" for i, h in enumerate(heights))}" fill="none" stroke="{ROSE}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'

    # ML & DL: two classes, a decision boundary and a tiny network
    pts = []
    for _ in range(26):
        x, y = rnd.uniform(20, 200), rnd.uniform(12, 104)
        if y < 0.5 * x + 4:
            pts.append(f'<circle class="pp" cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="{TEAL}" style="animation-delay:{rnd.uniform(0, 2):.2f}s"/>')
    for _ in range(26):
        x, y = rnd.uniform(140, 300), rnd.uniform(12, 104)
        if y > 0.5 * x + 18:
            pts.append(f'<circle class="pp" cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="{AMBER}" style="animation-delay:{rnd.uniform(0, 2):.2f}s"/>')
    layers = [(330, 3), (390, 4), (450, 4), (505, 2)]
    net = ""
    for (x1, n1), (x2, n2) in zip(layers, layers[1:]):
        for i in range(n1):
            for j in range(n2):
                net += f'<line x1="{x1}" y1="{60 + (i - (n1 - 1) / 2) * 24}" x2="{x2}" y2="{60 + (j - (n2 - 1) / 2) * 24}" stroke="{LINE}" stroke-width="1.2"/>'
    for li, (x, n) in enumerate(layers):
        for i in range(n):
            net += f'<circle class="pp" cx="{x}" cy="{60 + (i - (n - 1) / 2) * 24}" r="7" fill="{[INDIGO, TEAL, TEAL, AMBER][li]}" style="animation-delay:{li * 0.3:.1f}s"/>'
    ml = (f'<path class="draw" d="M8 4 L 230 115" stroke="{INK}" stroke-width="2.5" fill="none"/>' + "".join(pts) + net)

    # DBMS & SQL: a query and its result
    rows = [("North", 150), ("West", 120), ("South", 92), ("East", 64)]
    sql = (f'<rect x="20" y="4" width="250" height="108" rx="10" fill="{INK}"/>'
           f'<text {mono} font-size="13" font-weight="600" fill="#93C5FD"><tspan x="36" y="30">SELECT</tspan><tspan x="100" y="30" fill="#E2E8F0">region, SUM(amt)</tspan>'
           f'<tspan x="36" y="52">FROM</tspan><tspan x="86" y="52" fill="#E2E8F0">orders JOIN users</tspan>'
           f'<tspan x="36" y="74">GROUP BY</tspan><tspan x="114" y="74" fill="#E2E8F0">region</tspan>'
           f'<tspan x="36" y="96">ORDER BY</tspan><tspan x="114" y="96" fill="#E2E8F0">2 DESC;</tspan></text>'
           + "".join(f'<text {mono} x="300" y="{24 + i * 26}" font-size="13" font-weight="600" fill="{MUTED}">{r}</text>'
                     f'<rect class="hx" x="360" y="{12 + i * 26}" width="{v}" height="16" rx="4" fill="{AMBER}" fill-opacity="{1 - i * 0.18:.2f}" style="animation-delay:{0.2 + i * 0.12:.2f}s"/>'
                     for i, (r, v) in enumerate(rows)))

    # GenAI & NLP: a question, its embedding and the routed intent
    gen = (f'<rect x="20" y="6" width="210" height="36" rx="12" fill="{WHITE}" stroke="{LINE}"/>'
           f'<text {mono} x="34" y="29" font-size="13" font-weight="600" fill="{INK}">"forecast next month?"</text>'
           + "".join(f'<rect class="hb" x="{24 + i * 24}" y="{64 + (i % 3) * 6}" width="16" height="{34 - (i % 3) * 6}" rx="3" fill="{ROSE}" fill-opacity="{0.25 + (i % 4) * 0.18:.2f}" style="animation-delay:{i * 0.07:.2f}s"/>' for i in range(9))
           + f'<text {mono} x="24" y="116" font-size="11" font-weight="700" fill="{FAINT}">EMBEDDING · 384-d</text>'
           f'<path class="draw" d="M250 80 C 280 80, 290 50, 320 50" fill="none" stroke="#CBD5E1" stroke-width="2"/>'
           f'<rect x="322" y="18" width="200" height="86" rx="14" fill="{INDIGO}"/>'
           f'<text {mono} font-size="13" font-weight="600" fill="{WHITE}"><tspan x="340" y="46">intent: forecast</tspan><tspan x="340" y="68">confidence 0.91 ✓</tspan><tspan x="340" y="90" fill="#C7D2FE">→ /forecast API</tspan></text>')

    cards = [
        ("Data science &amp; analytics", INDIGO, eda,
         ["Cleaning, EDA and hypothesis testing", "Forecasting and clear reporting"]),
        ("Machine &amp; deep learning", TEAL, ml,
         ["Ensembles, time series, SHAP explanations", "GRU / CNN models in PyTorch, YOLO for vision"]),
        ("DBMS &amp; SQL", AMBER, sql,
         ["PostgreSQL, PL/pgSQL, SQLite full-text search", "Schema design, SQLAlchemy and Alembic"]),
        ("Generative AI &amp; NLP", ROSE, gen,
         ["LLM apps with Gemini and Groq", "Embeddings, intent models, knowledge graphs"]),
    ]
    body = []
    for i, (title, color, chart, bullets) in enumerate(cards):
        x, y = (i % 2) * (CW + GAP), (i // 2) * (CH + GAP)
        items = "".join(
            f'<circle cx="{x + 30}" cy="{y + 248 + j * 28}" r="3.5" fill="{color}"/><text x="{x + 44}" y="{y + 253 + j * 28}" class="b">{b}</text>'
            for j, b in enumerate(bullets))
        body.append(f"""
<g>
  <rect x="{x + 0.5}" y="{y + 0.5}" width="{CW - 1}" height="{CH - 1}" rx="20" fill="{WHITE}" stroke="{LINE}"/>
  <rect x="{x + 22}" y="{y + 22}" width="{CW - 44}" height="140" rx="14" fill="{PANEL}"/>
  <g transform="translate({x + 22} {y + 34})">{chart}</g>
  <rect x="{x + 24}" y="{y + 186}" width="28" height="4" rx="2" fill="{color}"/>
  <text x="{x + 24}" y="{y + 218}" class="h">{title}</text>
  {items}
</g>""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="What I do: data science and analytics, machine and deep learning, DBMS and SQL, generative AI and NLP">
<style>
  .h{{font:700 23px {SANS};fill:{INK};letter-spacing:-.3px}}
  .b{{font:400 16px {SANS};fill:{MUTED}}}
  .hb{{transform-box:fill-box;transform-origin:bottom;animation:grow 6s {EASE} infinite both}}
  @keyframes grow{{0%{{transform:scaleY(.08)}}25%,80%{{transform:scaleY(1)}}100%{{transform:scaleY(.08)}}}}
  .hx{{transform-box:fill-box;transform-origin:left;animation:growx 6s {EASE} infinite both}}
  @keyframes growx{{0%{{transform:scaleX(.05)}}25%,80%{{transform:scaleX(1)}}100%{{transform:scaleX(.05)}}}}
  .draw{{stroke-dasharray:640;animation:draw 6s {EASE} infinite both}}
  @keyframes draw{{0%,8%{{stroke-dashoffset:640}}40%,85%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:640}}}}
  .pp{{transform-box:fill-box;transform-origin:center;animation:pop 3s ease-in-out infinite}}
  @keyframes pop{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.25)}}}}
</style>
{''.join(body)}
</svg>"""


def footer():
    W, H = 1200, 110
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Let's turn data into decisions.">
<defs>
  <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{INDIGO}" stop-opacity="0"/><stop offset=".3" stop-color="{INDIGO}"/><stop offset=".7" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>
  <radialGradient id="spark"><stop offset="0" stop-color="{WHITE}"/><stop offset=".35" stop-color="{INDIGO}" stop-opacity=".6"/><stop offset="1" stop-color="{INDIGO}" stop-opacity="0"/></radialGradient>
</defs>
<style>
  .s{{animation:run 6s cubic-bezier(.45,0,.55,1) infinite}}
  @keyframes run{{0%,100%{{transform:translateX(140px)}}50%{{transform:translateX({W - 140}px)}}}}
  .t{{font:700 22px {SANS};fill:{INK};text-anchor:middle;letter-spacing:-.3px}}
  .m{{font:500 13px {MONO};fill:{FAINT};text-anchor:middle;letter-spacing:1.5px}}
</style>
<rect x="0" y="16" width="{W}" height="1.5" fill="url(#l)"/>
<ellipse class="s" cx="0" cy="16.7" rx="70" ry="8" fill="url(#spark)"/>
<text class="t" x="{W/2}" y="64">Let's turn data into decisions.</text>
<text class="m" x="{W/2}" y="92">OPEN TO DATA SCIENCE, ML &amp; DATA ANALYST OPPORTUNITIES · MUMBAI</text>
</svg>"""


if __name__ == "__main__":
    for old in OUT.glob("*-dark.svg"):
        old.unlink()
    for old in OUT.glob("*-light.svg"):
        old.unlink()
    write("hero.svg", hero())
    write("what-i-do.svg", capabilities())
    write("footer.svg", footer())
