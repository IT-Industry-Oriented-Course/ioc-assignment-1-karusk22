# apis/appointment_api.py

def book(patient_id: str, slot_id: str, department: str):
    """
    Sandbox appointment booking API
    """
    return {
        "appointment_id": "APT456",
        "patient_id": patient_id,
        "slot_id": slot_id,
        "department": department,
        "status": "CONFIRMED"
    }
