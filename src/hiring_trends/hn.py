"""Hacker News "Who is hiring?" threads from the Algolia API."""

import json
import time
from pathlib import Path

import pandas as pd
import requests

from hiring_trends import features

API_URL = "https://hn.algolia.com/api/v1"
RAW_DIR = Path("data/raw/hn")


def get_json(url, params=None, tries=5):
    for i in range(tries):
        time.sleep(1)
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            if i == tries - 1:
                raise
            time.sleep(30)


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


TALK_TERMS = ["LLM", "replace programmers", "junior developers", "vibe coding", "layoffs"]


def last_item_before(t):
    data = get_json(
        f"{API_URL}/search_by_date",
        params={"hitsPerPage": 1, "numericFilters": f"created_at_i<{int(t.timestamp())}"},
    )
    return int(data["hits"][0]["objectID"])


def comment_count(query, start, end):
    data = get_json(
        f"{API_URL}/search_by_date",
        params={
            "query": query,
            "tags": "comment",
            "hitsPerPage": 0,
            "typoTolerance": "false",
            "numericFilters": f"created_at_i>={int(start.timestamp())},created_at_i<{int(end.timestamp())}",
        },
    )
    return data["nbHits"]


def talk_counts():
    # Algolia's total for an empty query is a rough estimate, so the monthly
    # total is the jump in item IDs (stories and comments) instead.
    path = RAW_DIR / "talk_counts.csv"
    done = pd.read_csv(path) if path.exists() else pd.DataFrame(columns=["month"])
    months = pd.date_range("2011-04-01", pd.Timestamp.today().to_period("M").to_timestamp(), freq="MS")
    for start in months:
        month = start.strftime("%Y-%m")
        if month in done["month"].values:
            continue
        end = min(start + pd.offsets.MonthBegin(), pd.Timestamp.today())
        row = {"month": month, "hn_items": last_item_before(end) - last_item_before(start)}
        for term in TALK_TERMS:
            row[term] = comment_count(term, start, end)
        pd.DataFrame([row]).to_csv(path, mode="a", header=not path.exists(), index=False)
        print(row, flush=True)
    return pd.read_csv(path)
