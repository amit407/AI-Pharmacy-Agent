from typing import Dict
from db.meds_repo import find_medication_by_name
from db.users_repo import find_user_by_name


def get_medication_field(med_name: str, field: str) -> Dict:
    med = find_medication_by_name(med_name)
    if not med:
        return {"error": f"Medication '{med_name}' not found. Please check the spelling or ask a pharmacist."}

    return {"name": med["name"], field: med.get(field, "N/A")}


def get_stock(med_name: str) -> Dict:
    return get_medication_field(med_name, "stock")


def get_dosage(med_name: str) -> Dict:
    return get_medication_field(med_name, "dosage")


def get_active_ingredient(med_name: str) -> Dict:
    return get_medication_field(med_name, "active_ingredient")


def get_user_prescription(user_name: str) -> Dict:
    user = find_user_by_name(user_name)
    if not user:
        return {"error": "User not found. Please check your name."}
    return {"name": user["name"], "prescription": user.get("prescription", [])}
