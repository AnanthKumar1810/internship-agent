"""
Central config: keywords, sources, email settings.
Edit KEYWORDS to tune what counts as a match.
"""

import os

# Keywords used to filter listing titles/descriptions.
# Matching is case-insensitive substring match (see filters.py) — keep it broad,
# filters.py does the smarter scoring.
KEYWORDS = [
    "machine learning", "ml intern", "ai intern", "artificial intelligence",
    "deep learning", "computer vision", "cv intern", "opencv",
    "iot", "internet of things", "embedded", "edge ai", "edge computing",
    "tinyml", "tflite", "onnx", "robotics", "nlp", "data science intern",
]

# Naukri search query (space -> %20 handled by requests params)
NAUKRI_SEARCH_KEYWORDS = "AI ML Intern"
NAUKRI_LOCATION = ""  # leave blank for all-India

# Internshala category slugs to check (public listing pages)
INTERNSHALA_CATEGORIES = [
    "machine-learning-internship",
    "artificial-intelligence-internship",
    "internet-of-things-internship",
    "computer-vision-internship",
    "data-science-internship",
]

# LinkedIn public job search (no login) — query string built per keyword
LINKEDIN_KEYWORDS = ["AI ML Intern", "Computer Vision Intern", "IoT Intern", "Edge AI Intern"]
LINKEDIN_LOCATION = "India"

# Where dedup state is persisted (relative to repo root; GitHub Actions will
# commit this file back so state survives between runs)
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "seen_listings.json")

# Email (set these as GitHub Actions secrets, read via env vars)
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")

# Politeness
REQUEST_TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
DELAY_BETWEEN_REQUESTS_SEC = 2
