from hiring_trends import hn


def main():
    threads = hn.find_hiring_threads()
    print(f"Found {len(threads)} threads ({threads[0]['month']} to {threads[-1]['month']})")
    total = 0
    for i, t in enumerate(threads, 1):
        posts = hn.thread_posts(hn.fetch_thread(t["thread_id"]))
        total += len(posts)
        print(f"[{i}/{len(threads)}] {t['month']}: {len(posts)} posts")
    print(f"Done. {total} posts saved under {hn.RAW_DIR}/jobs/")


if __name__ == "__main__":
    main()
