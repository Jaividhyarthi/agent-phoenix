import json
import os

MEMORY_FILE = "agent_phoenix_memory.json"

def load_memory():
    """Load memory from JSON file. Returns {} if no file exists."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory: dict):
    """Save memory safely."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
