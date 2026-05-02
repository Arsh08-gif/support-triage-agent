
# Support Triage Agent

A terminal-based AI agent that reads support tickets and automatically decides
whether to reply or escalate — grounded entirely in scraped support documentation.

---
## What it does

For each ticket, the agent:
- Identifies the company (HackerRank, Claude, Visa, or infers from content)
- Retrieves the most relevant support documentation
- Classifies the issue and assesses risk
- Either replies with a grounded answer or escalates to a human
---

---

## How it works

1. **Scraper** crawls the support sites and builds a local corpus
2. **Retriever** finds the most relevant documentation chunks for each ticket
3. **Agent** uses Groq (LLaMA 3.3 70B) to classify, respond, or escalate
---


## Repository layout

```
.
├── AGENTS.md                       # Rules for AI coding tools + transcript logging
├── problem_statement.md            # Full task description and I/O schema
├── README.md                       # You are here
├── code/                           # ← Build your agent here
│   └── main.py                     #   Entry point (rename/extend as you like)
├── data/                           # Local-only support corpus (no network needed)
│   ├── hackerrank/                 #   HackerRank help center
│   ├── claude/                     #   Claude Help Center export
│   └── visa/                       #   Visa consumer + small-business support
└── support_tickets/
    ├── sample_support_tickets.csv  # Inputs + expected outputs (for development)
    ├── support_tickets.csv         # Inputs only (run your agent on these)
    └── output.csv                  # Write your agent's predictions here
```
---

---
## Architecture

support_tickets.csv
↓
main.py (CLI)
↓
retriever.py  ←  corpus/ (scraped support docs)
↓
agent.py  →  Groq API (LLaMA 3.3 70B)
↓
output.csv

**scraper.py** — crawls HackerRank, Claude, and Visa support sites and saves
content locally as text files.

**retriever.py** — given a ticket, splits the corpus into chunks and scores
them by keyword overlap to find the most relevant documentation.

**agent.py** — builds a prompt with the ticket + retrieved docs, calls the
Groq API, and returns a structured JSON response.

**main.py** — orchestrates everything, reads the input CSV, and writes results
to output.csv.

## Setup

### 1. Clone the repo
```bash
git clone <repo-url>
cd hackerrank-orchestrate-may26
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install requests beautifulsoup4 groq python-dotenv
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 5. Build the corpus (scrape support sites)
```bash
cd code
python3 scraper.py
```

### 6. Run the agent
```bash
python3 main.py --run
```

Output is written to `support_tickets/output.csv`.

## Output fields
A terminal-based agent that, for each row in `support_tickets/support_tickets.csv`, produces:

| Column         | Allowed values                                          |
| -------------- | ------------------------------------------------------- |
| `status`       | `replied`, `escalated`                                  |
| `product_area` | most relevant support category / domain area            |
| `response`     | user-facing answer grounded in the provided corpus      |
| `justification`| concise explanation of the routing/answering decision   |
| `request_type` | `product_issue`, `feature_request`, `bug`, `invalid`    |
---

## Project structure

- main.py       — entry point and CLI
- agent.py      — Groq API + triage logic  
- retriever.py  — keyword-based corpus search
- scraper.py    — support site crawler
- corpus/       — scraped support docs (gitignored)





