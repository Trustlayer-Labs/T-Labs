import json
from pathlib import Path
from datetime import datetime, timedelta

MEMORY_PATH = Path("data/user_memory.json")
MEMORY_EXPIRATION_DAYS = 30

def load_user_memory(path=MEMORY_PATH):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}

def save_user_memory(memory, path=MEMORY_PATH):
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def init_user_if_missing(memory, user):
    if user not in memory:
        memory[user] = {
            "flags": 0,
            "last_action": None,
            "ignore_until": None
        }

def increment_user_flags(memory, user):
    init_user_if_missing(memory, user)
    memory[user]["flags"] += 1
    memory[user]["last_action"] = "flagged"

def set_ignore_for_24h(memory, user):
    init_user_if_missing(memory, user)
    ignore_until = datetime.utcnow() + timedelta(hours=24)
    memory[user]["ignore_until"] = ignore_until.isoformat()

def is_user_ignored(memory, user):
    ignore_until = memory.get(user, {}).get("ignore_until")
    if ignore_until:
        return datetime.utcnow() < datetime.fromisoformat(ignore_until)
    return False

def get_user_flags(memory, user):
    return memory.get(user, {}).get("flags", 0)

