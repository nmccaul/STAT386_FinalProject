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

## Layout

- `src/hiring_trends/`: the package, with one module per data source (`hn.py` for Hacker News), plus `features.py` for the text flags
- `scripts/`: scripts that run the package functions
