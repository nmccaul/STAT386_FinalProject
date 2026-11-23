from pathlib import Path

import pandas as pd

OUT = Path("data/processed/role_shares.csv")


def main():
    posts = pd.read_csv("data/processed/hn_jobs.csv", usecols=["post_id", "month"])
    labels = pd.read_csv("data/labels/jev_all.csv", usecols=["post_id", "jev_role"])
    df = posts.merge(labels, on="post_id")
    df = df[df["jev_role"] != "not a job post"]
    df["year"] = df["month"].str[:4].astype(int)

    shares = pd.crosstab(df["year"], df["jev_role"], normalize="index").round(3)
    shares.insert(0, "posts", df.groupby("year").size())
    shares.to_csv(OUT)
    print(shares.to_string())


if __name__ == "__main__":
    main()
