"""Download Hacker News "Who is hiring?" threads from the Algolia HN API.

The API is free and needs no key. Each thread is saved to disk so it's only
downloaded once.
"""

import json
import time
from pathlib import Path

import requests

API_URL = "https://hn.algolia.com/api/v1"
RAW_DIR = Path("data/raw/hn")


def get_json(url, params=None):
    """GET a URL and return the JSON. Waits 1 second first to go easy on the API."""
    time.sleep(1)
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def find_hiring_threads():
    """Return every "Who is hiring?" thread, oldest first, and save the list."""
    data = get_json(
        f"{API_URL}/search_by_date",
        params={"tags": "story,author_whoishiring", "hitsPerPage": 1000},
    )
    threads = [
        {
            "thread_id": int(hit["objectID"]),
            "month": hit["created_at"][:7],  # threads go up on the 1st or 2nd
            "title": hit["title"],
        }
        for hit in data["hits"]
        # older titles capitalize it differently ("Who is Hiring?", "Who Is Hiring?")
        if hit["title"].lower().startswith("ask hn: who is hiring?")
    ]
    threads.sort(key=lambda t: t["month"])

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / "hiring_threads.json").write_text(json.dumps(threads, indent=2))
    return threads


def fetch_thread(thread_id):
    """Return a thread with all its comments. Downloads it only if it isn't saved yet."""
    path = RAW_DIR / "jobs" / f"{thread_id}.json"
    if path.exists():
        return json.loads(path.read_text())

    data = get_json(f"{API_URL}/items/{thread_id}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))
    return data


def thread_posts(thread):
    """Return the job posts in a thread: top-level comments that weren't deleted."""
    return [c for c in thread["children"] if c.get("text")]


def jobs_table():
    """Build one row per job post from the saved threads.

    Run scripts/collect_hn_jobs.py first. Exact duplicate posts within a
    month are dropped.
    """
    import pandas as pd

    from hiring_trends import features

    threads = json.loads((RAW_DIR / "hiring_threads.json").read_text())
    rows = []
    for t in threads:
        for post in thread_posts(fetch_thread(t["thread_id"])):
            text = features.clean_html(post["text"])
            header = text.split("\n")[0]  # "Company | Role | Location | ..."
            rows.append({
                "post_id": post["id"],
                "month": t["month"],
                "company": header.split("|")[0].strip() if "|" in header else None,
                "header": header,
                "remote": features.mentions(header, r"\bremote\b"),
                "seniority": features.seniority(header),
                "mentions_ai": features.mentions(text, features.AI_PATTERN),
                "text": text,
            })

    df = pd.DataFrame(rows)
    return df.drop_duplicates(subset=["month", "text"])
