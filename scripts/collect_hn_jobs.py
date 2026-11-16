"""Download every Hacker News "Who is hiring?" thread to data/raw/hn/.

Threads already on disk are skipped, so this can be rerun safely.
Run with: uv run python scripts/collect_hn_jobs.py
"""

from hiring_trends import hn


def main():
    threads = hn.find_hiring_threads()
    print(f"Found {len(threads)} hiring threads "
          f"({threads[0]['month']} to {threads[-1]['month']})")

    total = 0
    for i, t in enumerate(threads, 1):
        posts = hn.thread_posts(hn.fetch_thread(t["thread_id"]))
        total += len(posts)
        print(f"[{i}/{len(threads)}] {t['month']}: {len(posts)} posts")

    print(f"Done. {total} job posts saved under {hn.RAW_DIR}/jobs/")


if __name__ == "__main__":
    main()
