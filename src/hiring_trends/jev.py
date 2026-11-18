"""Label job posts with Jev. Needs JEV_API_KEY and JEV_MODEL in .env."""

import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

JEV_URL = "https://api.typesafe.ai/v1/systemone"
MAX_CHARS = 4000

ROLES = {
    "frontend": "Frontend or web UI engineer.",
    "backend": "Backend, API or server engineer.",
    "full stack": "Full stack engineer, or a general software engineer covering front and back end.",
    "mobile": "iOS, Android or mobile engineer.",
    "devops/infra": "DevOps, SRE, platform or infrastructure engineer.",
    "data scientist": "Data scientist or analyst.",
    "data engineer": "Data engineer building pipelines or warehouses.",
    "ML engineer": "Machine learning engineer training or deploying models.",
    "AI engineer": "AI or LLM engineer building products on top of language models.",
    "security": "Security engineer.",
    "QA/test": "QA or test engineer.",
    "designer": "Product, UX or visual designer.",
    "product manager": "Product manager.",
    "sales/solutions": "Sales, customer success, solutions or forward deployed engineer.",
    "other": "A job that fits none of the other roles, like embedded, hardware, research or operations.",
    "not a job post": "Not a job listing, like a reply, a question or a person looking for work.",
}

SENIORITY = {
    "intern": "Internship.",
    "new grad": "New grad or entry level.",
    "junior": "Junior.",
    "mid": "Mid level, or a stated range of a few years of experience with no level named.",
    "senior": "Senior, staff, principal or lead.",
    "unspecified": "The post doesn't say.",
}

AI_TYPE = {
    "builds AI": "The job is building AI: training models, ML or LLM engineering.",
    "uses AI": "The job asks the person to work with AI coding tools like Copilot, Cursor or Claude Code, or calls itself AI-native.",
    "AI product only": "The company sells an AI product, but the job itself doesn't build AI or ask for AI tools.",
    "none": "No AI in the post.",
}

QUESTIONS = {
    "role": {
        "type": "choice",
        "instructions": "What is the main role this post is hiring for? If it lists several, pick the first or most prominent one.",
        "criteria": ROLES,
    },
    "seniority": {
        "type": "choice",
        "instructions": "What level is the job? If it hires at several levels, pick the most junior one.",
        "criteria": SENIORITY,
    },
    "ai_type": {
        "type": "choice",
        "instructions": "How does AI relate to this job?",
        "criteria": AI_TYPE,
    },
}


def label_post(text):
    body = {"model": os.environ["JEV_MODEL"], "state": text[:MAX_CHARS], "questions": QUESTIONS}
    headers = {"Authorization": f"Bearer {os.environ['JEV_API_KEY']}"}
    for attempt in range(4):
        try:
            resp = requests.post(JEV_URL, json=body, headers=headers, timeout=60)
            resp.raise_for_status()
            answers = resp.json()["answers"]
            break
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))
    labels = {}
    for name in QUESTIONS:
        labels[f"jev_{name}"] = answers[name]["choice"]
        labels[f"jev_{name}_conf"] = answers[name]["confidence"]
    return labels
