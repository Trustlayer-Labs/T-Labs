# Trustlayer Labs
---
![Alt text](../TL%20LABS%202.png)
![Alt text](../TL%20LABS%201.png)


*Enterprise-Grade AI Compliance Agent for GDPR & Social Engineering Threats*

---
### 📂 Links

<a href="https://github.com/Trustlayer-Labs/T-Labs" style="font-weight: bold; color: blue; font-size: 1.2em;">Project Repo</a>

<a href="https://youtu.be/apnxMRFoUbw" style="font-weight: bold; color: blue; font-size: 1.2em;">Video Demo</a>

## 📈 Project Overview


**Trustlayer Labsl** is a stateful, multi-channel compliance monitoring system powered by the **Portia AI SDK**. It acts as an intelligent layer of protection across your organisation's internal communications — detecting policy violations, preventing sensitive data leaks, and flagging suspicious behavioural patterns such as social engineering attempts.

It not only monitors **Slack**, **meeting transcripts**, and (optionally) **email**, but also utilises powerful LLMs to provide explainable, contextual, and actionable risk analysis. The system simulates the workflow of an enterprise-grade compliance officer: observe, assess, escalate if needed — all with full transparency and human oversight.

---

## 📄 Key Features

### 🔍 Intelligent Policy Violation Detection
- Applies company policy rules (GDPR + Social Engineering) via structured RAG
- Scans Slack conversations and meeting transcripts in real time
- Detects:
  - Personal data exposure (GDPR Article 4)
  - Unauthorised data sharing (GDPR Article 28)
  - Poor data protection practices (GDPR Article 32)
  - Social engineering risk phrases and tactics

### 🧠 LLM Risk Engine with Explanation
- Uses **Gemini 1.5 Pro** (Google Generative AI)
- Returns structured reasoning in JSON format:
  - Matched policy clause
  - Confidence score
  - Risk level (low/medium/high)
  - Recommended action (ignore, redact, escalate)
  - Natural-language explanation of what was risky and why

### 🧳 Stateful Memory for Users
- Tracks number of violations per user
- Automatically escalates after repeated offences
- Implements per-user ignore timers ("Ignore for 24 hours")

### 📬 Email Escalation & Manager Review
- High-risk violations generate real-time email to compliance manager
- Email includes:
  - Violation context
  - Explanation
  - Call-to-action link for escalation confirmation
- Flask-based portal for managers to confirm or dismiss escalations

### 🧠 Human-in-the-Loop
- Manager actions recorded in logs
- Supports full audit trail for traceability and accountability

---

## 🌐 Multi-Channel Coverage

| Channel         | Status | Notes                                  |
|----------------|--------|----------------------------------------|
| Slack           | ✅      | Fully integrated via Portia SDK         |
| Meeting Audio   | ✅      | Transcribed via AssemblyAI, processed   |
| Gmail (Optional)| 🔜      | API placeholder ready, coming soon      |

---

## 🛡️ Portia SDK Highlights

| Portia Feature     | Used | Description                                    |
|--------------------|------|------------------------------------------------|
| Planning           | ✅    | Agent declares intentions before acting       |
| Clarification      | ✅    | Manager confirmation for sensitive actions     |
| Human-in-the-loop  | ✅    | Portal + email approvals                      |
| Stateful memory    | ✅    | Tracks user history and cooldown state        |
| Multi-modal input  | ✅    | Slack + transcript support                    |
| Explanation layer  | ✅    | Reason shown to end-user and manager          |

---

## 🧠 Workflow Summary

1. Fetch new Slack messages or transcripts  
2. For each message:
   - Check against internal policy via Gemini + RAG
   - Log result, explanation, and confidence
   - If severe or repeated: escalate  
3. Send email to compliance officer  
4. Portal UI: review, confirm or reject  
5. Save final incident state  

---

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
