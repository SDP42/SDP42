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

# ── starting XI ──────────────────────────────────────────────────────────────
# A 4-3-3. `at` is (x, z) in metres on a 105 × 68 pitch, attacking +x.
SQUAD = [
    {
        "no": 1, "pos": "GK", "pos_name": "Goalkeeper", "at": (-46, 0), "slug": "elevate",
        "title": "Elevate 1.0", "repo": gh("Elevate1.0"), "live": "https://elevate1-0.vercel.app",
        "commits": 145, "event": "24-hour national hackathon",
        "tagline": "The official platform that ran a 24-hour national hackathon.",
        "points": [
            "2,500+ views, 700+ registrations, 115+ participants in 32 teams",
            "Role-based portals on Neon PostgreSQL with JWT cookies and bcrypt",
            "Scores stay hidden until approved; exports never leak passwords",
        ],
        "stack": ["React", "Node.js", "PostgreSQL", "PL/pgSQL", "JWT"],
    },
    {
        "no": 2, "pos": "RB", "pos_name": "Right back", "at": (-30, 24), "slug": "namaste",
        "title": "NAMASTE × ICD-11", "repo": gh("SIH_PS_10"),
        "commits": 40, "event": "Smart India Hackathon",
        "tagline": "A FHIR R4 service linking traditional and modern medical codes.",
        "points": [
            "468 curated mappings stored in SQLite with FTS5 full-text search",
            "Terminology lookups in under 100 ms behind a FastAPI service",
            "FHIR R4-compliant resources served to a React front end",
        ],
        "stack": ["FastAPI", "SQLite FTS5", "FHIR R4", "React"],
    },
    {
        "no": 4, "pos": "CB", "pos_name": "Centre back", "at": (-32, 9), "slug": "ohmen",
        "title": "OHMEN", "repo": gh("ohmen"),
        "commits": 62, "event": "D3COY · PS 03",
        "tagline": "See the cascade before it happens, across critical systems.",
        "points": [
            "Consequence-based risk scoring instead of raw CVE counts",
            "Attack-path simulation across operational dependencies",
            "Mitigation optimiser that ranks fixes cutting the most risk",
        ],
        "stack": ["Python", "TypeScript", "Graph analytics", "Digital twin"],
    },
    {
        "no": 5, "pos": "CB", "pos_name": "Centre back", "at": (-32, -9), "slug": "datapilot",
        "title": "DataPilot", "repo": gh("datapilot"),
        "commits": 71, "event": "Long-running build",
        "tagline": "An autonomous data scientist that explains every step.",
        "points": [
            "Profiling, data-quality analysis and approval-gated cleaning",
            "Filesystem dataset versioning with full lineage validation",
            "Deterministic EDA and statistics layer, then problem framing",
        ],
        "stack": ["Python", "Pandas", "Statistics", "React"],
    },
    {
        "no": 3, "pos": "LB", "pos_name": "Left back", "at": (-30, -24), "slug": "freight",
        "title": "East Coast Freight Desk", "repo": gh("east-coast-freight-desk"),
        "live": "https://east-coast-freight-desk.vercel.app",
        "commits": 34, "event": "Smart India Hackathon 2026",
        "tagline": "Freight forecasts and chartering calls for SAIL's coal imports.",
        "points": [
            "Four models compared walk-forward with Wilcoxon tests",
            "ARIMA + XGBoost ensemble, each forecast explained by SHAP",
            "86.9% intent model and a PostgreSQL back end for the desk",
        ],
        "stack": ["PyTorch", "XGBoost", "SHAP", "PostgreSQL", "FastAPI"],
    },
    {
        "no": 6, "pos": "CDM", "pos_name": "Defensive midfield", "at": (-14, 0), "slug": "brainmap",
        "title": "BrainMapAI", "repo": gh("BrainMapAI"),
        "commits": 58, "event": "Open source",
        "tagline": "Turns PDFs and research papers into navigable knowledge graphs.",
        "points": [
            "spaCy parsing and KeyBERT keyphrase extraction per document",
            "Entity-relation graphs you can explore and validate visually",
            "Python back end with an interactive TypeScript front end",
        ],
        "stack": ["Python", "spaCy", "KeyBERT", "NLP"],
    },
    {
        "no": 8, "pos": "CM", "pos_name": "Central midfield", "at": (-4, 15), "slug": "learnova",
        "title": "Learnova V2", "repo": gh("LearnovaV2"),
        "commits": 185, "event": "IEEE & Springer LNCS papers",
        "tagline": "Rebuilds lecture PDFs into illustrated, interactive decks.",
        "points": [
            "Gemini + Groq with a FastAPI + React app and PPTX export",
            "700+ automated tests keep the generation pipeline dependable",
            "Visuals picked per idea, step-by-step explainers and a tutor",
        ],
        "stack": ["FastAPI", "React", "Gemini", "Groq", "Docker"],
    },
    {
        "no": 10, "pos": "CAM", "pos_name": "Playmaker", "at": (-2, -15), "slug": "opsdesk",
        "title": "OpsDesk", "repo": gh("OpsDesk"),
        "commits": 472, "event": "Team Outliers · travel ops for TBO",
        "tagline": "Every ticket is a flight: a travel-ops desk run like a tower.",
        "points": [
            "Gradient-boosted Ghost Flights flag bookings likely to fail",
            "Monte Carlo breach forecasts and a routing what-if simulator",
            "FastAPI + Next.js 15, a 3D case map and 12 e2e journeys",
        ],
        "stack": ["FastAPI", "Next.js", "scikit-learn", "SQLAlchemy"],
    },
    {
        "no": 7, "pos": "RW", "pos_name": "Right wing", "at": (22, 24), "slug": "meridian",
        "title": "MERIDIAN", "repo": gh("agentx"),
        "commits": 116, "event": "PS-02 · Agentic trading bot",
        "tagline": "Speak the market, trust every trade: an agentic paper desk.",
        "points": [
            "Sixteen agents, from a NIFTY 500 scanner to a kill switch",
            "Every order needs a Risk PASS fingerprinted to that order",
            "Backtests against buy-and-hold and NIFTY 50; 117 pytest checks",
        ],
        "stack": ["FastAPI", "TypeScript", "faster-whisper", "Ollama"],
    },
    {
        "no": 11, "pos": "LW", "pos_name": "Left wing", "at": (22, -24), "slug": "worldcup",
        "title": "WorldCupAI 2026", "repo": gh("WorldCupAI-2026"),
        "commits": 8, "event": "Sports analytics",
        "tagline": "Predicts the complete FIFA World Cup 2026 knockout bracket.",
        "points": [
            "Machine learning and deep learning models as ensembles",
            "Monte Carlo simulation of the full knockout bracket",
            "SHAP explanations of each prediction in Streamlit",
        ],
        "stack": ["scikit-learn", "TensorFlow", "SHAP", "Streamlit"],
    },
    {
        "no": 9, "pos": "ST", "pos_name": "Striker", "at": (31, 0), "slug": "mirage", "captain": True,
        "title": "MIRAGE", "repo": gh("isacaps2"),
        "commits": 201, "event": "D3COY 1.0 · DJS ISACA · PS 02",
        "subtitle": "Multimodal Impersonation & Request-Aware Guard Engine",
        "tagline": "Seeing is no longer believing. Is it really safe to act on this?",
        "numbers": [("201", "commits"), ("1.87%", "voice EER"), ("41/42", "voice fakes caught"), ("15/15", "image fakes caught")],
        "deep": [
            ("Detect", "Five witnesses (voice, face, provenance, words, identity) built on published deepfake detectors."),
            ("Explain", "Every claim cites numbered exhibits tied to waveform seconds, words, frames and OCR boxes."),
            ("Cure", "A live response per scam type: hold the money, challenge questions and pre-filled reports."),
            ("Shield", "Voice check, live call shield and a Chrome extension. English, Hindi and Hinglish."),
        ],
        "points": [
            "Five detector witnesses; voice detection at 1.87% EER",
            "Red-team lab: 41/42 voice and 15/15 image fakes caught",
            "Cites numbered evidence, then runs the cure: hold, verify, report",
        ],
        "stack": ["PyTorch", "FastAPI", "TypeScript", "Chrome extension"],
    },
]

# Build-up play, keeper to striker: the order the ball travels on the pitch.
PASSING_ORDER = [1, 4, 6, 8, 10, 7, 9]

# ── the bench ────────────────────────────────────────────────────────────────
BENCH = [
    {"title": "Stratify", "url": "https://dombivli-hackathon-s6vb.vercel.app", "tagline": "Algorithmic trading platform with a Pandas and NumPy strategy backtester.", "stack": ["Python", "React", "SQL"]},
    {"title": "Medical AI · Chest X-ray", "url": None, "tagline": "YOLOv9 and DenseNet-121 diagnosis on 2,000+ chest X-rays, explained with Grad-CAM.", "stack": ["PyTorch", "YOLOv9", "Grad-CAM"]},
    {"title": "Parallel", "url": gh("parallel"), "tagline": "Attention digital twin that shows both futures of a notification before you tap.", "stack": ["TypeScript", "Python", "Causal ML"]},
    {"title": "Smart Resort 360", "url": gh("guestexperience"), "tagline": "Guest portal with a live 3D twin of a 130-suite resort and a trilingual concierge.", "stack": ["Next.js", "three.js", "RAG"]},
    {"title": "DriftWard", "url": gh("driftward"), "tagline": "Behavioural identity layer that contains hijacked AI agents with valid tokens.", "stack": ["FastAPI", "three.js", "CUSUM"]},
    {"title": "CityPulse AI", "url": gh("citypulse-ai"), "tagline": "Local-first civic evidence workbench: every number traces back to source rows.", "stack": ["FastAPI", "SQLite", "H3"]},
    {"title": "Learnova IPD", "url": gh("LearnovaIPD"), "tagline": "The original engine behind Learnova, turning text-heavy decks into visual slides.", "stack": ["Python", "Groq", "Gemini"]},
    {"title": "Football Analytics", "url": gh("Football-Analytics"), "tagline": "Tactical football analytics platform, in research and architecture phase.", "stack": ["Python", "ML", "CV"]},
    {"title": "HackNova L5614", "url": gh("HackNova-L5614"), "tagline": "A logistics platform built against the clock at the HackNova L5614 hackathon.", "stack": ["JavaScript", "Python", "Docker"]},
]

# ── sections ─────────────────────────────────────────────────────────────────
# (file slug, number, stadium location, heading) for each section banner.
SECTIONS = [
    ("tunnel", "01", "Players' tunnel", "About me"),
    ("scoreboard", "02", "Big screen", "Match stats"),
    ("captain", "03", "The armband", "Captain's project"),
    ("pitch", "04", "The pitch", "Starting XI"),
    ("bench", "05", "The dugout", "On the bench"),
    ("honours", "06", "Centre spot", "Honours & roles"),
    ("toolkit", "07", "Kit room", "Toolkit"),
    ("activity", "08", "Training ground", "GitHub activity"),
    ("press", "09", "Press box", "Get in touch"),
]
