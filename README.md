# Compliance Sentinel 🔒

**AI-powered Compliance Monitoring for GDPR and Social Engineering Risks**

---

## 📈 Overview

**Compliance Sentinel** is a multi-channel AI compliance agent that detects GDPR violations and social engineering attempts across workplace communication platforms. Built on top of the **Portia SDK**, the system leverages powerful LLM reasoning, role-based permissions, and human-in-the-loop workflows to ensure data protection and responsible internal communications.

---

## 📄 Features

### 🔍 Intelligent Policy Monitoring
- Detects violations of:
  - GDPR Article 4 (Personal Data)
  - GDPR Article 28 (Third-party Disclosure)
  - GDPR Article 32 (Security of Processing)
  - Social engineering and phishing behaviour

### 🧠 Risk Analysis Engine
- Uses **Gemini 1.5 Pro** (via Google Generative AI API) to:
  - Interpret natural language messages
  - Match internal policies using structured RAG logic
  - Assign confidence scores and risk levels
  - Recommend actions (escalate, redact, ignore)
  - Provide human-readable violation explanations

### 🧳️ User Behaviour Tracking
- Tracks policy flags per user
- Detects repeat offenders and auto-escalates
- Implements cooldown periods ("Ignore similar messages for 24h")

### 🔧 Incident Management & Logging
- All violations stored in structured JSON logs
- Escalates high-risk incidents via SMTP email
- Managers can confirm or dismiss cases via a review portal

### 🌐 Multi-Channel Monitoring
- ✅ Slack messages (via Portia Slack integration)
- ✅ Transcribed meeting audio (AssemblyAI + parser)
- ⏳ Gmail support in progress

---

## 🛡️ Portia SDK Feature Usage

| Portia Feature         | Implemented | Description                                      |
|------------------------|-------------|--------------------------------------------------|
| Planning               | ✅           | Agent declares intended actions beforehand        |
| Clarification          | ✅           | Agent requests input from humans where required   |
| Human-in-the-loop      | ✅           | Review portal confirms high-risk escalations      |
| Stateful Memory        | ✅           | Tracks user flags, decisions, ignore states       |
| Explainability         | ✅           | Violation summary + reason shown to end users     |
| Multi-modal Input      | ✅           | Slack and voice transcripts                       |

---

## 🚀 Workflow Summary

```plaintext
Slack message or transcript ➔ Gemini LLM analysis
➔ Matches GDPR policy ➔ Generates summary, explanation, risk score
➔ Agent decides: escalate, redact, ignore
➔ High-risk cases trigger email to compliance manager
➔ Manager confirms via review portal (Flask)
➔ Incident logged to persistent JSON system
```

---

## 🧱 Tech Stack

| Layer                 | Technology Used              |
|----------------------|------------------------------|
| Agent Framework      | Portia SDK                   |
| LLM Integration      | Gemini (Google Gen AI)       |
| Audio Transcription  | AssemblyAI                   |
| Messaging Platform   | Slack                        |
| Email Escalation     | Gmail SMTP (App Password)    |
| Review UI            | Flask                        |
| Data Storage         | JSON (logs, memory, policies)|

---

## 📂 Project Structure

```bash
compliance-sentinel/
├── run_agent.py            # Main execution file (agent pipeline)
├── review_portal.py        # Manager review portal
├── tools/
│   ├── llm_policy_checker.py
│   ├── user_memory.py
│   └── email_sender.py
├── policy_rag.json         # GDPR and social engineering rules
├── user_memory.json        # Per-user flag tracking
├── logs/incidents.json     # Main incident log
├── data/transcripts.json   # Meeting transcripts
├── .env                    # API and email credentials
```

---

## 🔧 How to Run

1. Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your environment variables to `.env`:
```env
PORTIA_API_KEY=...
GEMINI_API_KEY=...
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

3. Run the main agent pipeline:
```bash
python run_agent.py
```

4. Launch the manager review portal:
```bash
python review_portal.py
```

---

## 🌟 Why This Project Wins

- **Solves a real-world pain point**: internal data leaks & compliance fines
- **Uses Portia as intended**: showcases every SDK strength (planning, memory, clarification)
- **Extremely demoable**: input a Slack message, get real-time alert + human review
- **Production-style design**: modular, maintainable, role-aware, and secure

---

## 📝 Future Improvements
- Add Gmail parsing (emails as policy triggers)
- Build visual dashboard for flag trends and user risk scores
- Implement feedback loop into policy tuning (auto-learn false positives)

---

## 🙌 Built With
- [Portia SDK](https://github.com/portiaAI/portia-agent-examples)
- [Google Generative AI](https://ai.google.dev/)
- [AssemblyAI](https://www.assemblyai.com/)
- [Flask](https://flask.palletsprojects.com/)
