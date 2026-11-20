from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from hiring_trends import jev

OUT = Path("data/labels/jev_all.csv")
CHUNK = 1000
COLS = [f"jev_{q}{s}" for q in jev.QUESTIONS for s in ("", "_conf")]


def label(text):
    try:
        return jev.label_post(text)
    except Exception:
        return {}


def main():
    posts = pd.read_csv("data/processed/hn_jobs.csv")[["post_id", "text"]]
    done = pd.read_csv(OUT).dropna(subset=["jev_role"]) if OUT.exists() else pd.DataFrame(columns=["post_id"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if len(done):
        done.to_csv(OUT, index=False)
    else:
        OUT.unlink(missing_ok=True)
    todo = posts[~posts["post_id"].isin(done["post_id"])].reset_index(drop=True)
    print(f"{len(done)} already labeled, {len(todo)} to go", flush=True)

    with ThreadPoolExecutor(max_workers=8) as pool:
        for start in range(0, len(todo), CHUNK):
            chunk = todo.iloc[start:start + CHUNK].reset_index(drop=True)
            labels = pd.DataFrame(list(pool.map(label, chunk["text"])), columns=COLS)
            out = pd.concat([chunk[["post_id"]], labels], axis=1)
            out.to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
            print(f"{start + len(chunk)}/{len(todo)}", flush=True)

    failed = pd.read_csv(OUT)["jev_role"].isna().sum()
    print(f"Done. {failed} failed, rerun to retry them.")


if __name__ == "__main__":
    main()
