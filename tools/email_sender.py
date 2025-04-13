import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_compliance_email(user, message, policy, reason, action, risk_level, timestamp, incident_id):
    msg = EmailMessage()
    msg["Subject"] = f"RING RING! Compliance Review Needed | {policy} ({risk_level})"
    msg["From"] = EMAIL_USER
    msg["To"] = "izhaansalam@gmail.com"

    review_url = f"http://localhost:5000/review?incident_id={incident_id}"

    msg.set_content(f"""
🔒 Compliance Violation Flagged

User: {user}
Message: "{message}"
Policy Match: {policy}
Risk Level: {risk_level}
Timestamp: {timestamp}
Agent Recommendation: {action.upper()}

🧠 Explanation:
{reason}

Please review and confirm escalation:
👉 {review_url}
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
            print(f"✅ Sent compliance review email for user {user}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
