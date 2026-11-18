"""Hacker News "Who is hiring?" threads from the Algolia API."""

import json
import time
from pathlib import Path

import pandas as pd
import requests

from hiring_trends import features

API_URL = "https://hn.algolia.com/api/v1"
RAW_DIR = Path("data/raw/hn")


def get_json(url, params=None):
    time.sleep(1)
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def find_hiring_threads():
    data = get_json(
        f"{API_URL}/search_by_date",
        params={"tags": "story,author_whoishiring", "hitsPerPage": 1000},
    )
    threads = [
        {"thread_id": int(hit["objectID"]), "month": hit["created_at"][:7], "title": hit["title"]}
        for hit in data["hits"]
        if hit["title"].lower().startswith("ask hn: who is hiring?")
    ]
    threads.sort(key=lambda t: t["month"])
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / "hiring_threads.json").write_text(json.dumps(threads, indent=2))
    return threads


def fetch_thread(thread_id):
    path = RAW_DIR / "jobs" / f"{thread_id}.json"
    if path.exists():
        return json.loads(path.read_text())
    data = get_json(f"{API_URL}/items/{thread_id}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))
    return data


def thread_posts(thread):
    return [c for c in thread["children"] if c.get("text")]


def jobs_table():
    threads = json.loads((RAW_DIR / "hiring_threads.json").read_text())
    rows = []
    for t in threads:
        for post in thread_posts(fetch_thread(t["thread_id"])):
            text = features.clean_html(post["text"])
            header = text.split("\n")[0]
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
    return pd.DataFrame(rows).drop_duplicates(subset=["month", "text"])
