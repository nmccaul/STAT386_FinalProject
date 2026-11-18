from pathlib import Path

from hiring_trends import hn

OUT = Path("data/processed/hn_jobs.csv")


def main():
    df = hn.jobs_table()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Saved {len(df)} posts to {OUT}")

    df["year"] = df["month"].str[:4]
    df["entry_level"] = df["seniority"].isin(["intern", "new grad", "junior"])
    summary = df.groupby("year")[["entry_level", "mentions_ai", "remote"]].mean()
    print((summary * 100).round(1).to_string())


if __name__ == "__main__":
    main()
