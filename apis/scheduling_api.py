def find_slots(department, start_date, end_date):
    return [
        {"slot_id": "SLOT123", "date": "2025-01-20", "time": "10:00"}
    ]

def book(patient_id, slot_id, department):
    return {
        "appointment_id": "APT999",
        "patient_id": patient_id,
        "department": department,
        "slot_id": slot_id,
        "status": "CONFIRMED"
    }
