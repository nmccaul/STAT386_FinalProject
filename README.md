# STAT 386 Final Project: AI and Tech Hiring

Nathan McCauley and Will Westover. See `proposal.md` for the plan.

## Setup

You need [uv](https://docs.astral.sh/uv/). No API keys are needed.

```bash
git clone https://github.com/nmccaul/STAT386_FinalProject.git
cd STAT386_FinalProject
uv sync
```

## Collecting data

Hacker News "Who is hiring?" threads:

```bash
uv run python scripts/collect_hn_jobs.py
```

This saves the thread list to `data/raw/hn/hiring_threads.json` and each thread to `data/raw/hn/jobs/<thread_id>.json`. Threads already saved are skipped, so you can stop and rerun it. Raw data isn't committed.

Then build the job post table:

```bash
uv run python scripts/clean_hn_jobs.py
```

This writes `data/processed/hn_jobs.csv` with one row per post: month, company, the header line, remote, seniority (intern, new grad, junior, senior or unspecified), whether it mentions AI, and the full text. The keyword definitions are in `src/hiring_trends/features.py`.

## Checking the keyword rules

We label a random sample of 400 posts (25 per year) with Jev, an LLM classifier, and compare its labels to the keyword rules. The labels are committed in `data/labels/`, so you only need this step if you want to relabel. It needs `JEV_API_KEY` and `JEV_MODEL` in a `.env` file at the project root.

```bash
uv run python scripts/label_sample.py
```

This saves `data/labels/jev_sample.csv`, prints how often Jev and the rules agree, and writes `data/labels/review.csv`, 50 posts where they disagree to check.

Jev labels for every post are in `data/labels/jev_all.csv`. To relabel them (about 30 minutes, resumes if stopped):

```bash
uv run python scripts/label_all.py
```

## Role shares over time

```bash
uv run python scripts/role_shares.py
```

This joins the Jev role labels to the job posts, drops posts Jev marked as not a job post, and writes `data/processed/role_shares.csv` with the share of each role by year and the post count. 2026 is a partial year.

## Hacker News talk counts

```bash
uv run python scripts/collect_hn_talk.py
```

This counts Hacker News comments each month that match a few search terms (LLM, replace programmers, junior developers, vibe coding, layoffs), plus the number of new Hacker News items that month (from item IDs) so we can use shares. It saves `data/raw/hn/talk_counts.csv` and skips months already saved. It takes about 20 minutes. The terms are in `TALK_TERMS` in `src/hiring_trends/hn.py`. The counts come from Algolia search, so they're close but not exact. 2026-11 is a partial month.

## Layout

- `src/hiring_trends/`: the package, with one module per data source (`hn.py` for Hacker News), plus `features.py` for the text flags
- `scripts/`: scripts that run the package functions
