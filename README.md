# 🛡️ Compliance Sentinel – T-Labs

A Portia-powered compliance and risk monitoring agent that detects GDPR violations and social engineering in Slack messages, Gmail emails, and meeting transcripts. Designed for enterprises to proactively flag risks, redact sensitive data, and generate daily audit summaries.

---

## 📁 Project Structure

```
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
```

---

## ⚙️ 1. Set Up the Environment

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 2. Configure Environment Variables

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

---

## 🚀 3. Run the Agent

To run the compliance agent on test inputs:

```bash
python scripts/run_agent.py
```

This will process all available logs in the `data/` folder and record actions in `logs/incidents.json`.

---

## 🧪 4. Test with Simulated Inputs

Use `test_inputs.py` to inject new simulated data:

```bash
python scripts/test_inputs.py
```

You can add new Slack messages, emails, or transcripts to the respective JSON files in `data/`.

---

## 📊 5. Generate Reports

Create a markdown summary of flagged incidents:

```bash
python scripts/generate_report.py
```

The output will be saved to `reports/daily_summary.md`.

---

## 🛠️ Optional: GitHub Actions Automation

Automatically run the agent and email a report daily with the workflow in:

```
.github/workflows/run-agent.yml
```

---

## 🤖 Powered By

- [Portia SDK](https://www.portia.ai/)
- [OpenAI / Gemini APIs](https://deepmind.google/technologies/gemini/)
- Python, dotenv, and your config of choice.

---

## 📬 Contact

For questions, reach out to the **T-Labs** team or open an issue.

