# apis/patient_api.py

def search(name: str, dob: str = None):
    """
    Sandbox patient search API
    """
    return {
        "patient_id": "PAT123",
        "name": name,
        "dob": dob,
        "status": "FOUND"
    }
