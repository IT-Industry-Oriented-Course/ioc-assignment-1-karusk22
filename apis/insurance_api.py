# apis/insurance_api.py

def check(patient_id: str, service_type: str):
    """
    Sandbox insurance eligibility API
    """
    return {
        "patient_id": patient_id,
        "service_type": service_type,
        "eligible": True,
        "provider": "ABC Health Insurance"
    }
