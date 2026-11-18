from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

from hiring_trends import features, jev

PER_YEAR = 25
SEED = 386
LOW_CONFIDENCE = 0.7
REVIEW_SIZE = 50
OUT = Path("data/labels/jev_sample.csv")
REVIEW = Path("data/labels/review.csv")


def draw_sample():
    df = pd.read_csv("data/processed/hn_jobs.csv")
    df["year"] = df["month"].str[:4]
    return df.groupby("year").sample(PER_YEAR, random_state=SEED).reset_index(drop=True)


def main():
    sample = draw_sample()
    done = pd.read_csv(OUT) if OUT.exists() else pd.DataFrame(columns=["post_id"])
    todo = sample[~sample["post_id"].isin(done["post_id"])].reset_index(drop=True)
    print(f"{len(done)} already labeled, {len(todo)} to go")

    with ThreadPoolExecutor(max_workers=8) as pool:
        labels = list(pool.map(jev.label_post, todo["text"]))
    new = pd.concat([todo, pd.DataFrame(labels)], axis=1)
    new["rule_roles"] = new["text"].map(lambda t: "; ".join(features.roles(t)))
    new["rule_ai_type"] = new["text"].map(features.ai_type)

    df = pd.concat([done, new.drop(columns="text")], ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Saved {len(df)} labels to {OUT}")

    # Rules have no "mid" or "AI product only", so those count as unspecified and none.
    role_match = df.apply(lambda r: r["jev_role"] in str(r["rule_roles"]).split("; "), axis=1)
    seniority_match = df["jev_seniority"].replace("mid", "unspecified") == df["seniority"]
    ai_match = df["jev_ai_type"].replace("AI product only", "none") == df["rule_ai_type"]
    jobs = df["jev_role"] != "not a job post"
    print(f"Not job posts: {(~jobs).mean():.0%}")
    print(f"Role match: {role_match[jobs].mean():.0%}")
    print(f"Seniority match: {seniority_match[jobs].mean():.0%}")
    print(f"AI type match: {ai_match[jobs].mean():.0%}")
    overcount = df["mentions_ai"] & df["jev_ai_type"].isin(["AI product only", "none"])
    print(f"mentions_ai but Jev says product only or none: {overcount.mean():.0%}")

    confs = df[["jev_role_conf", "jev_seniority_conf", "jev_ai_type_conf"]].min(axis=1)
    flag = ~role_match | ~seniority_match | ~ai_match | (confs < LOW_CONFIDENCE)
    cols = ["post_id", "month", "header", "rule_roles", "jev_role", "seniority", "jev_seniority",
            "rule_ai_type", "jev_ai_type", "text"]
    review = df[flag].merge(sample[["post_id", "text"]], on="post_id")[cols]
    print(f"{len(review)} posts flagged")
    review = review.sample(min(REVIEW_SIZE, len(review)), random_state=SEED)
    for name in ["my_role", "my_seniority", "my_ai_type"]:
        review[name] = ""
    review.to_csv(REVIEW, index=False)
    print(f"Saved {len(review)} to review in {REVIEW}")


if __name__ == "__main__":
    main()
