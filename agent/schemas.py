from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientSearchRequest(BaseModel):
    name: str
    dob: Optional[date]

class InsuranceEligibilityRequest(BaseModel):
    patient_id: str
    service_type: str

class AppointmentSlotRequest(BaseModel):
    department: str
    start_date: date
    end_date: date

class AppointmentBookingRequest(BaseModel):
    patient_id: str
    slot_id: str
    department: str
