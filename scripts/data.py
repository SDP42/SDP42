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
