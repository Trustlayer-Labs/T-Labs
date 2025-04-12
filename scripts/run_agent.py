import json
import re
from pathlib import Path
from datetime import datetime

# Load data
def load_json(path):
    return json.loads(Path(path).read_text())

script_dir = Path(__file__).parent
root_dir = script_dir.parent  # T-Labs directory

data_dir = root_dir / "data"
logs_dir = root_dir / "logs"
logs_dir.mkdir(exist_ok=True)

slack = load_json(data_dir / "slack_log.json")
gmail = load_json(data_dir / "gmail_log.json")
transcripts = load_json(data_dir / "transcripts.json")
policies = load_json(root_dir / "policy_rag.json")

print(f"Loaded {len(slack)} slack messages")
print(f"Loaded {len(gmail)} emails")
print(f"Loaded {len(transcripts)} transcripts")
print(f"Loaded {len(policies)} policies")

# Print first few keywords from each policy
print("\nPolicy keywords:")
for i, policy in enumerate(policies):
    keywords = policy.get("keywords", [])
    sample = keywords[:3] if keywords else []
    print(f"  Policy {i+1}: {policy.get('title')} - Sample keywords: {sample}")
    
def match_policy(text):
    if not text:
        return None
        
    for policy in policies:
        for keyword in policy.get("keywords", []):
            # Fix the regex pattern - remove extra backslash
            if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
                return {
                    "matched_policy": policy.get("title"),
                    "risk_reason": keyword,
                    "action_taken": policy.get("recommendation"),
                    "risk_level": policy.get("risk_level")
                }
    return None

# Add debugging to see the first item from each data source
if slack:
    print("\nSample slack message:", slack[0].get("text", "")[:50] + "...")
if gmail:
    print("Sample email body:", gmail[0].get("body", "")[:50] + "...")
if transcripts:
    print("Sample transcript:", transcripts[0].get("transcript", "")[:50] + "...")

incidents = []

for msg in slack:
    match = match_policy(msg.get("text", ""))
    if match:
        incidents.append({
            "source": "slack",
            "user": msg.get("user"),
            "message": msg.get("text"),
            "channel": msg.get("channel"),
            "timestamp": msg.get("timestamp"),
            **match
        })

for email in gmail:
    match = match_policy(email.get("body", ""))
    if match:
        incidents.append({
            "source": "gmail",
            "user": email.get("from"),
            "message": email.get("body"),
            "subject": email.get("subject"),
            "timestamp": email.get("timestamp"),
            **match
        })

for entry in transcripts:
    match = match_policy(entry.get("transcript", ""))
    if match:
        incidents.append({
            "source": "transcript",
            "participants": entry.get("participants"),
            "message": entry.get("transcript"),
            "timestamp": entry.get("timestamp"),
            **match
        })

Path(logs_dir / "incidents.json").write_text(json.dumps(incidents, indent=2))
print(f"\nProcessed {len(incidents)} incidents.")
