import os
import json

CONFIG_PATH = "config.json"
ACCOUNTS_DIR = "accounts"
os.makedirs(ACCOUNTS_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "admins": [123456789],  # Replace with your Telegram ID
    "groups": [],
    "accounts": []
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)
