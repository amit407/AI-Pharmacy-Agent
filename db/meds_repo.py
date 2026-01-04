import json
from pathlib import Path

BASE = Path(__file__).parent


def load_medications():
    with open(BASE / "medications.json", encoding="utf-8") as f:
        return json.load(f)


MEDICATIONS = load_medications()


def find_medication_by_name(name: str):
    return next((m for m in MEDICATIONS if m["name"].lower() == name.lower()), None)
