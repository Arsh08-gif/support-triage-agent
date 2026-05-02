
# Support Triage Agent

A terminal-based AI agent that automatically triages support tickets for HackerRank, Claude, and Visa.

## How it works

1. **Scraper** crawls the support sites and builds a local corpus
2. **Retriever** finds the most relevant documentation chunks for each ticket
3. **Agent** uses Groq (LLaMA 3.3 70B) to classify, respond, or escalate

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

| Field | Values |
|---|---|
| status | `replied`, `escalated` |
| product_area | support category |
| response | user-facing answer |
| justification | reasoning for decision |
| request_type | `product_issue`, `feature_request`, `bug`, `invalid` |

## Project structure
code/
main.py        # entry point and CLI
agent.py       # Groq API + triage logic
retriever.py   # keyword-based corpus search
scraper.py     # support site crawler
logger.py      # AGENTS.md compliant logging
corpus/        # scraped support docs (gitignored)