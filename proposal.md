# STAT 386 Final Project Proposal

Group members: Nathan McCauley, Will Westover

We want to look at how AI is changing tech hiring. Job postings are a good record of what companies actually ask for, so we plan to use them to see how hiring has changed and what it looks like now. We also want to check whether the job posts back up all the talk about AI replacing entry-level jobs.

## 1. Datasets and how we'll get them

We plan to use three sources.

Hacker News "Who is hiring?" threads. Every month since 2011, Hacker News has posted a thread where companies leave one comment per job post. The free Hacker News search API returns about 187 of these threads, and the November 2026 thread alone has about 200 job posts. We'll find the threads with the Algolia Hacker News Search API and pull each thread's posts through it or the official Hacker News API, so we'll have job posts by month going back about 15 years.

Hacker News discussion. The same API also has the site's regular stories and comments. We'll search for terms like "junior developer", "new grad", "entry level", "AI replacing" and "layoffs" and count how many posts mention them each month.

- Algolia Hacker News Search API: https://hn.algolia.com/api
- Official Hacker News API: https://github.com/HackerNews/API

Greenhouse job boards. Many tech companies post their openings through Greenhouse, which has a public API. Nathan already tested it for an earlier assignment and pulled 163 product manager postings from 15 company boards, and 71% of them listed a salary range. We'd widen that to software engineering, data and product roles at around 40 to 60 companies.

- Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html

## 2. Main questions

1. Are entry-level tech jobs changing as AI tools improve? For example, are junior and new-grad posts becoming a smaller share of all posts, and are more posts asking for AI skills?
2. Do jobs that ask for AI skills offer more money?
3. Does what people say about AI and tech jobs match what the job posts show? For example, when there's more talk about AI taking junior jobs, are there actually fewer junior posts?

The Hacker News job posts cover the first question, since they go back years. The Greenhouse data covers the second, since it has better salary information, but it only shows jobs that are open right now. The third question compares Hacker News discussion to Hacker News job posts, so we're comparing what one community says to what it actually posts.

## 3. Cleaning, analysis and visualization

Most of the cleaning is turning free text into columns. For each post we'll pull out the role type, seniority (intern, new grad, junior, senior and so on), remote or onsite, salary range, years of experience, and flags for AI-related skills and other common skills. We'll also need to drop duplicate posts and posts that aren't actually job listings. For the discussion data, we'll leave out the hiring threads, flag posts by topic (AI and jobs, entry-level, layoffs), and check a random sample by hand to make sure the keywords are working.

For analysis, we'll track the share of posts that are entry-level and the share that mention AI by month, and compare salaries for postings that ask for AI skills against those that don't, within the same role and level. For the third question, we'll plot the discussion and job post trends on the same timeline, with events like ChatGPT's release in November 2022 marked, to see whether the talk comes before, after, or along with changes in the posts. Plots will include line charts over time, bar charts of skill frequency by level, and box plots of salary. We also plan to build a dashboard where you can filter by role, level and year.

## 4. Functions in our Python package

We expect the package to include functions that:

- fetch and save Hacker News threads, stories and comments, and Greenhouse boards, with a delay between requests and saved raw files so we only pull each one once
- parse salary ranges and years of experience out of text
- assign a seniority level from a job title
- flag AI and other skill keywords in job posts and discussion posts
- build monthly trends and the main summary tables and plots

## 5. How the package helps our analysis

All three sources need the same cleaning steps, so writing them once as tested functions keeps the datasets consistent and saves us from copying code between notebooks. Using the same keyword functions everywhere means "AI" means the same thing in the job posts and the discussion, and if we change a definition, we change it in one place and rerun everything.

## 6. Dividing the work

Nathan will lead the Greenhouse data and the salary analysis. Will will lead the Hacker News data (job posts and discussion) and the analysis over time. We'll split the package functions, review each other's code through GitHub, and work on the discussion comparison, dashboard and final report together.

## 7. Potential challenges

- Hacker News posts are free text written however each company wants, so parsing salary and seniority will be messy and some posts will be missing them.
- Keyword flags can overcount. A post might mention AI just because the company sells an AI product, not because the job needs AI skills. Discussion posts have the same problem, which is why we'll check a sample by hand.
- Hacker News leans toward startups and software engineering, so it doesn't represent all tech hiring or all media. It has also grown since 2011, so we'll use monthly shares instead of raw counts.
- Even if discussion and job posts move together, one doesn't necessarily cause the other. Both could be reacting to the same things, like layoffs.
- Salary is posted more often in states with pay transparency laws, so the pay results will lean toward places like California, New York and Washington.
- Greenhouse postings disappear once jobs are filled, so we need to save everything the first time we pull it.

## 8. Why we can finish in six weeks

All the APIs are free and public, the Greenhouse pull already works, and the discussion data uses the same Hacker News API and code as the job posts. Our rough plan is to collect the data in weeks 1 and 2, build and test the package in week 3, do the analysis in week 4, build the dashboard in week 5, and finish the report in week 6. Our minimum project is the Hacker News data alone (job posts and discussion), which still answers our main questions. If Greenhouse takes longer than expected, we'll cut it back or drop it.
