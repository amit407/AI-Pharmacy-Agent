from db.meds_repo import MEDICATIONS
from db.users_repo import USERS


def extract_med_name(text: str):
    text_lower = text.lower()
    for med in MEDICATIONS:
        if med["name"].lower() in text_lower or med.get("hebrew_name", "").lower() in text_lower:
            return med["name"]   # always return English name
    return None


def detect_intent(text: str):
    t = text.lower()
    if any(k in t for k in ["stock", "available", "in stock", "מלאי", "זמין"]):
        return "stock"
    if any(k in t for k in ["dosage", "dose", "usage", "how to take", "מינון", "איך לקחת", "שימוש"]):
        return "dosage"
    if any(k in t for k in ["active ingredient", "ingredient", "חומר פעיל", "מרכיב"]):
        return "active_ingredient"
    if any(k in t for k in ["my prescription", "my meds", "my medication", "המרשם שלי", "התרופות שלי"]):
        return "prescription"
    return None


def extract_user_name(text: str):
    text_lower = text.lower()
    for user in USERS:
        if user["name"].lower() in text_lower:
            return user["name"]
    return None



