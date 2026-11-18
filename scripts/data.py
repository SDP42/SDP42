"""Profile content. Facts mirror the stadium portfolio and the repositories on
github.com/SDP42, so the README and the portfolio never disagree."""

PORTFOLIO = "https://stadium-portfolio.vercel.app"
GITHUB = "https://github.com/SDP42"


def gh(repo):
    return f"{GITHUB}/{repo}"


# ── profile ──────────────────────────────────────────────────────────────────
PROFILE = {
    "name": "Swayam Panchal",
    "first": "SWAYAM",
    "last": "PANCHAL",
    "role": "Data Science · Machine Learning · Generative AI",
    "degree": "B.Tech, Artificial Intelligence & Data Science",
    "college": "Dwarkadas J. Sanghvi College of Engineering",
    "location": "Mumbai, India",
    "summary": "I build ML and GenAI systems that turn raw data into decisions.",
}

# Words cycled by the hero's typing line: "> building ___"
ROLES = [
    "ML systems that hold up",
    "GenAI products people use",
    "explainable models",
    "data pipelines end to end",
]

# ── honours ──────────────────────────────────────────────────────────────────
HONOURS = [
    {"big": "5×", "label": "Hackathon winner", "note": "Working AI, data and full-stack products built against the clock."},
    {"big": "2×", "label": "Ideathon winner", "note": "Problem framing and solution design that won the room."},
    {"big": "JPMC", "label": "Code for Good", "note": "J.P. Morgan Chase & Co. hackathon building tech for non-profits."},
]

# Scrolling ticker along the bottom of the hero and between sections.
TICKER = [
    "SDP42 FC TAKE THE FIELD",
    "CGPA 9.70 / 10",
    "5× HACKATHON WINNER",
    "2× IDEATHON WINNER",
    "JPMC CODE FOR GOOD",
    "SECRETARY · DJS NSDC × INFOMATRIX",
    "MIRAGE: 41/42 LAUNDERED VOICE DEEPFAKES CAUGHT",
    "LEARNOVA: 700+ TESTS",
    "ELEVATE 1.0: 700+ REGISTRATIONS",
    "OPSDESK: 472 COMMITS",
    "MERIDIAN: SIXTEEN AGENTS, FIVE DEFENCE LAYERS",
    "TRANSFER WINDOW: OPEN",
]

# ── scoreboard ───────────────────────────────────────────────────────────────
# (value, label) pairs rendered as rolling odometer digits.
STATS = [
    ("9.70", "CGPA / 10"),
    ("5", "Hackathon wins"),
    ("2", "Ideathon wins"),
    ("11", "Projects in the XI"),
    ("1,392", "Commits across the XI"),
]
