# apis/slots_api.py

def find(department: str, start_date: str, end_date: str):
    """
    Sandbox appointment slot lookup API
    """
    return [
        {
            "slot_id": "SLOT123",
            "department": department,
            "date": "2025-01-22",
            "time": "10:00 AM"
        }
    ]
