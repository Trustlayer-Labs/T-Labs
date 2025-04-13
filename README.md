# Trustlayer Labs

**Enterprise-Grade AI Compliance Agent for GDPR & Social Engineering Threats**

---

## 📈 Project Overview

**Trustlayer Labsl** is a stateful, multi-channel compliance monitoring system powered by the **Portia AI SDK**. It acts as an intelligent layer of protection across your organisation's internal communications — detecting policy violations, preventing sensitive data leaks, and flagging suspicious behavioural patterns such as social engineering attempts.

It not only monitors **Slack**, **meeting transcripts**, and (optionally) **email**, but also utilises powerful LLMs to provide explainable, contextual, and actionable risk analysis. The system simulates the workflow of an enterprise-grade compliance officer: observe, assess, escalate if needed — all with full transparency and human oversight.


## 🧱 Tech Stack

| Layer                 | Technology Used              |
|----------------------|------------------------------|
| Agent Framework      | Portia SDK                   |
| LLM Policy Reasoning | Gemini Pro (Google)          |
| Audio Transcription  | AssemblyAI                   |
| Communication Input  | Slack, transcripts           |
| Email Escalation     | SMTP (Gmail + App Password)  |
| Review UI            | Flask                        |
| Persistent Logs      | JSON                         |

---

## 📂 Folder Structure

```
Trustlayer-Labs/
├── run_agent.py            # Main runner (Slack + transcripts)
├── review_portal.py        # Flask portal for escalation
├── tools/                  # Modular logic (LLM, email, memory)
├── scripts/                # Generators + helpers
├── data/                   # Simulated inputs (Slack, Gmail, transcripts)
├── logs/                   # Incident log, memory snapshots
├── reports/                # Markdown summaries
├── .env                    # API keys + email secrets
├── policy_rag.json         # Internal policy rules
├── user_memory.json        # Stateful tracking file
```

---

## 🚀 Quickstart

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add credentials to `.env`:
```env
PORTIA_API_KEY=...
GEMINI_API_KEY=...
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

3. Run the pipeline:
```bash
python scripts/run_agent.py
```

4. Launch the manager portal:
```bash
python review_portal.py
```

---


## 🔮 Future Work

- Full Gmail support (with IMAP or Gmail API)
- RAG tuning from user feedback (adaptive policies)
- Live dashboard with graphs and user behaviour insights

---

## 🙌 Credits

- [Portia SDK](https://github.com/portiaAI/portia-agent-examples)
- [Google Generative AI](https://ai.google.dev/)
- [AssemblyAI](https://www.assemblyai.com/)
- [Flask](https://flask.palletsprojects.com/)
