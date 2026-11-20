# STAT 386 Final Project Proposal

Group members: Nathan McCauley, Will Westover

Main question: what is AI actually doing to tech jobs, compared to what people say it's doing?

There's a lot of talk about AI replacing programmers, killing junior jobs and making "vibe coders" employable. Job posts are a record of what companies actually hire for and pay, so we want to compare the talk to the posts. Hacker News works well for this since it has both, it's dense, and it goes back 15 years.

## 1. Datasets and how we'll get them

Hacker News "Who is hiring?" threads. Every month since 2011, Hacker News has posted a thread where companies leave one comment per job post. We already pulled all 185 threads through the Algolia Hacker News Search API, which is about 93,000 posts from 2011 to 2026.

Hacker News discussion. The same API has the site's regular comments. We'll pull comments about AI and jobs, like ones mentioning replacing programmers, junior developers, vibe coding or layoffs, and tag which role each one is about.

- Algolia Hacker News Search API: https://hn.algolia.com/api
- Official Hacker News API: https://github.com/HackerNews/API

Greenhouse job boards. Many tech companies post their openings through Greenhouse, which has a public API. Nathan already pulled 163 product manager postings from 15 boards for an earlier assignment, and 71% listed a salary range. We'd widen that to software, data, AI and product roles at around 40 to 60 companies. This gives us good salary data for jobs open right now.

- Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html

H-1B wage filings (stretch goal). The Department of Labor publishes every H-1B application with the employer, job title and offered salary, every year back to about 2008. Big tech companies file thousands a year, so this gives us big tech salaries over time to compare against the mostly startup posts on Hacker News.

- DOL OFLC performance data: https://www.dol.gov/agencies/eta/foreign-labor/performance

## 2. Main questions

1. Which tech roles are growing or shrinking? We'll track the share of posts for each role (frontend, backend, mobile, data scientist, ML engineer, AI engineer, QA, design and so on) by month, and check which ones changed after ChatGPT came out in November 2022 compared to the trend they were already on.
2. Which roles are the hot topic? For each role, we'll measure how much Hacker News comments talk about AI replacing or changing it, and compare that to what actually happened to that role in the posts.
3. What do companies ask for now? We'll split AI jobs into two kinds: jobs that use AI (asking for tools like Copilot or Cursor, or being "AI-native") and jobs that build AI (AI and ML engineers). We'll also look at years of experience and the share of entry-level posts.
4. Does it pay? We'll compare salaries for jobs that use AI, jobs that build AI and everything else, over time on Hacker News and right now on Greenhouse. If we get to the H-1B data, we'll add big tech salaries over time.

## 3. Cleaning, analysis and visualization

Most of the cleaning is turning free text into columns. For each post we'll pull out the main role, seniority, remote or onsite, salary range, years of experience, and whether it uses AI or builds AI. We'll start with keyword rules, then label a sample with an LLM classifier (Jev) to see how often the rules are right, and have a second model check the posts where they disagree. If the rules are too loose, we'll use the classifier labels. We'll also drop duplicates and posts that aren't job listings.

For the discussion data, we'll leave out the hiring threads, tag each comment by role and topic, and count comments by month. Hacker News has grown since 2011, so we'll use shares of posts and comments instead of raw counts.

For analysis, we'll fit each role's trend before November 2022 and see how far it moved from that trend after. The main plot is one dot per role, with how much it's talked about as being replaced on one axis and how much its share of posts actually changed on the other. Roles far from the line are where the talk and the posts disagree. Other plots will include role shares over time, salary over time by AI type, and box plots of current salaries. If we have time, we'll build a dashboard where you can filter by role, level and year.

## 4. Functions in our Python package

We expect the package to include functions that:

- fetch and save Hacker News threads and comments, Greenhouse boards and H-1B files, saving raw files so we only pull each one once
- assign a role and seniority level from a job post
- flag uses-AI and builds-AI keywords in posts and comments
- parse salary ranges and years of experience out of text
- build monthly trends and the main summary tables and plots

## 5. How the package helps our analysis

All the sources need the same cleaning steps, so writing them once keeps the datasets consistent and saves us from copying code between notebooks. Using the same role and AI definitions everywhere means "AI engineer" means the same thing in the posts, the comments and the salary data, and if we change a definition we change it in one place and rerun everything.

## 6. Dividing the work

Will leads the Hacker News data and questions 1 to 3: role trends, the discussion data and what companies ask for. Nathan leads question 4: salary from Greenhouse, Hacker News and H-1B. We'll review each other's code through GitHub and work on the main plot, dashboard and report together.

## 7. Potential challenges

- Hacker News posts are free text, so parsing role, seniority and salary will be messy. Many posts list several roles, which is why we'll check the keyword rules against a labeled sample.
- Keyword flags can overcount. A post might mention AI because the company sells an AI product, not because the job needs AI skills. The uses-AI and builds-AI split is meant to help with this.
- Hacker News leans toward startups and software engineering, so it doesn't represent all tech hiring.
- Total posts dropped by about half after 2022, so overall hiring slowed at the same time AI took off. Using shares helps, but some changes could come from the slowdown and not from AI.
- Few posts listed salaries before 2023 (under 5% most years), so salary trends before then will be noisy. Salary is also posted more often in states with pay transparency laws.
- H-1B salaries only cover H-1B hires, so they don't represent everyone at a company.
- Even if the talk and the posts move together, one doesn't necessarily cause the other.

## 8. Why we can finish in six weeks

The Hacker News job posts are already downloaded and cleaned into a table, all the APIs are free and public, and the Greenhouse pull already works. The rest of the plan is to label roles and check the labels, pull the discussion data, build the trend plots, add salary, and then make the main plot and report. Our minimum project is the Hacker News data alone (questions 1 to 3), which still answers the main question. If we run short on time, we'll cut the H-1B data first, then the dashboard, then Greenhouse.
