"""Turn job post text into columns: seniority, remote, and keyword flags.

These work on any text, so the same definitions can be used for Hacker News
and Greenhouse posts.
"""

import html
import re

# Checked in this order, so a post hiring both juniors and seniors counts as junior.
SENIORITY_PATTERNS = {
    "intern": r"\bintern(s|ship|ships)?\b",
    "new grad": r"\bnew[ -]?grads?\b|\bentry[ -]level\b|\brecent grad(uate)?s?\b",
    "junior": r"\bjunior\b|\bjr\.?\b",
    "senior": r"\bsenior\b|\bsr\.?\b|\bstaff\b|\bprincipal\b|\blead\b",
}

# (?<!\.) skips domains like company.ai
AI_PATTERN = (
    r"(?<!\.)\bAI\b|\bA\.I\.|\bartificial intelligence\b|\bmachine learning\b|\bML\b"
    r"|\bdeep learning\b|\bLLMs?\b|\blarge language models?\b|\bGPT|\bgenerative\b"
)


def clean_html(text):
    """Turn HN comment HTML into plain text, keeping paragraph breaks as newlines."""
    text = text.replace("<p>", "\n")
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def seniority(text):
    """Return intern, new grad, junior, senior, or unspecified."""
    for level, pattern in SENIORITY_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            return level
    return "unspecified"


def mentions(text, pattern):
    """True if the text matches the pattern (case-insensitive)."""
    return bool(re.search(pattern, text, re.IGNORECASE))
