import json
from pathlib import Path

BASE = Path(__file__).parent


def load_users():
    with open(BASE / "users.json", encoding="utf-8") as f:
        return json.load(f)


USERS = load_users()


def find_user_by_name(name: str):
    return next((u for u in USERS if u["name"].lower() == name.lower()), None)

