# T-Labs



compliance-sentinel/
├── agent.yml                         # Core Portia agent config (main brain)
├── policy_rag.json                   # Policy definitions (GDPR, SocEng) used for RAG
├── roles.json                        # Role-based access mapping
├── user_memory.json                  # Tracks flag history per user
├── .env                              # API keys (GEMINI, SMTP, etc.)
├── requirements.txt                  # Python deps (portia, dotenv, etc.)

├── data/                             # Input simulation data
│   ├── slack_log.json                # Simulated Slack messages
│   ├── gmail_log.json                # Simulated emails
│   └── transcripts.json              # Simulated voice transcript payloads

├── logs/                             # Auto-generated logs
│   └── incidents.json                # All actions (redact, escalate, etc.)

├── scripts/                          # Runners + testing + reporting
│   ├── run_agent.py                  # Load input → run agent → log actions
│   ├── test_inputs.py                # Feed simulated messages (Slack/Gmail/etc.)
│   └── generate_report.py            # Daily markdown summary from logs

├── tools/                            # Optional custom tools (e.g. for SMTP)
│   └── email_sender.py               # (if using custom SMTP logic)

├── reports/                          # Markdown/JSON reports (if CLI dashboard)
│   └── daily_summary.md

├── .github/workflows/                # GitHub Actions (optional automation)
│   └── run-agent.yml                 # Run agent + email report + log cleanup etc.

├── README.md                         # Setup instructions + demo flow
└── conversation_config.yaml          # (Optional) For future podcast-style summaries




























### 1. Set Up the Environment
Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file using the template:
```bash
cp .env.example .env
```
Edit `.env` and fill in your credentials:
```
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret
PORTIA_API_KEY=your-portia-key
```