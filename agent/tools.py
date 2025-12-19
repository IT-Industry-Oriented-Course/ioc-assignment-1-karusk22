# agent/tools.py

from agent.schemas import *
from apis import patient_api, insurance_api, slots_api, appointment_api


def search_patient(name: str, dob: str = None):
    """
    Search for a patient using name and optional DOB.
    """
    return patient_api.search(name, dob)


def check_insurance_eligibility(patient_id: str, service_type: str):
    """
    Check insurance eligibility for a given patient and service.
    """
    return insurance_api.check(patient_id, service_type)


def find_available_slots(department: str, start_date: str, end_date: str):
    """
    Find available appointment slots for a department.
    """
    return slots_api.find(department, start_date, end_date)


def book_appointment(patient_id: str, slot_id: str, department: str):
    """
    Book an appointment for a patient.
    """
    return appointment_api.book(patient_id, slot_id, department)
