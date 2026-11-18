"""Keyword rules for job post text."""

import html
import re

# Checked in order, so a post hiring juniors and seniors counts as junior.
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

ROLE_PATTERNS = {
    "frontend": r"front[- ]?end|\breact\b",
    "backend": r"back[- ]?end",
    "full stack": r"full[- ]?stack",
    "mobile": r"\bios\b|android|mobile",
    "devops/infra": r"devops|\bsre\b|site reliability|infrastructure",
    "data scientist": r"data scien",
    "data engineer": r"data engineer",
    "ML engineer": r"machine learning engineer|\bml engineer|mlops",
    "AI engineer": r"\bai engineer|llm engineer|applied ai|ai/ml engineer",
    "security": r"security engineer|appsec|infosec",
    "QA/test": r"\bqa\b|quality assurance|test engineer|sdet",
    "designer": r"designer|\bux\b",
    "product manager": r"product manager",
    "sales/solutions": r"account executive|\bsales\b|customer success|solutions engineer|forward[- ]deployed",
}

BUILDS_AI_PATTERN = ROLE_PATTERNS["ML engineer"] + "|" + ROLE_PATTERNS["AI engineer"]
USES_AI_PATTERN = (
    r"\bcursor\b|copilot|claude code|\bcodex\b|windsurf|ai[- ]native|ai[- ]first|vibe[- ]?cod"
)


def clean_html(text):
    text = text.replace("<p>", "\n")
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def mentions(text, pattern):
    return bool(re.search(pattern, text, re.IGNORECASE))


def seniority(text):
    for level, pattern in SENIORITY_PATTERNS.items():
        if mentions(text, pattern):
            return level
    return "unspecified"


def roles(text):
    return [role for role, pattern in ROLE_PATTERNS.items() if mentions(text, pattern)]


def ai_type(text):
    if mentions(text, BUILDS_AI_PATTERN):
        return "builds AI"
    if mentions(text, USES_AI_PATTERN):
        return "uses AI"
    return "none"
