import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from portia import Portia, Config, DefaultToolRegistry, LLMProvider, LLMModel
import sys

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools.llm_policy_checker import check_llm_policy_match

# === Load environment variables ===
load_dotenv()
api_key = os.getenv("PORTIA_API_KEY")
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

if not api_key:
    raise ValueError("PORTIA_API_KEY not found in .env file.")

config = Config(
    portia_api_key=api_key,
    llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
    llm_model_name=LLMModel.GEMINI_2_0_FLASH,
    google_api_key=GOOGLE_API_KEY
)
tools = DefaultToolRegistry(config)
portia = Portia(config=config, tools=tools)

# === Set up project structure ===
script_dir = Path(__file__).parent
root_dir = script_dir.parent
logs_dir = root_dir / "logs"
logs_dir.mkdir(exist_ok=True)

# === Slack tools ===
def fetch_slack_messages(channel_id: str, limit: int = 20):
    print(f"Fetching Slack messages from channel {channel_id}...")
    result = portia.run(
        f"Get recent messages from Slack channel {channel_id}",
        ["portia:slack:user:conversation_history"],
    )
    
    # Get the JSON string output from the portia result
    messages_str = result.model_dump_json(indent=2)
    
    # Parse the top-level JSON string into a Python object (typically a dict)
    try:
        messages = json.loads(messages_str)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return []  # Return an empty list on error
    
    # Check if the messages are wrapped in a nested structure
    if isinstance(messages, dict) and "outputs" in messages:
        conversation_info = (
            messages.get("outputs", {})
                    .get("step_outputs", {})
                    .get("$conversation_history", {})
                    .get("value")
        )
        if conversation_info:
            try:
                # Parse the conversation_info, which is a JSON string of the conversation list
                messages_list = json.loads(conversation_info)
                print("Extracted conversation messages:", type(messages_list))
                return messages_list
            except json.JSONDecodeError as e:
                print("Error decoding conversation JSON:", e)
                return []
    
    # If messages is already a list, return it directly.
    print("Structured messages loaded:", type(messages))
    return messages

def list_channel_ids():
    result = portia.run(
        "give me all the slack conversations ids",
        ["portia:slack:bot:list_conversation_ids"]
    )
    print("Available Slack Channels:")
    for c in result.get("channels", []):
        print(f"{c['name']} — {c['id']}")

if __name__ == "__main__":
    channel_id = "C08N836TP5X"

    slack_messages = fetch_slack_messages(channel_id)
    print(slack_messages, "HERE WE GO SKIBIDI")
    print(f"Loaded {len(slack_messages)} Slack messages")

    incidents = []

    # Iterate over each message (now a list of dicts)
    for msg in slack_messages:
        text = msg.get("text", "")
        if not text:
            continue

        # Call Gemini to check for policy compliance
        match = check_llm_policy_match(text)

        if match and match.get("confidence", 0) > 0.5:  # Threshold for logging incidents
            incidents.append({
                "source": "slack",
                "user": msg.get("user"),
                "message": text,
                "timestamp": msg.get("timestamp"),
                **match
            })

    # Write the incidents log to a JSON file
    incident_log_path = logs_dir / "incidents.json"
    incident_log_path.write_text(json.dumps(incidents, indent=2))
    print(f"Processed {len(incidents)} incidents.")
    print(f"Written to {incident_log_path}")
