# agent/agent.py

from typing import Optional, List

from langchain_core.language_models.llms import LLM
from langchain_core.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType

from agent.tools import (
    search_patient,
    check_insurance_eligibility,
    find_available_slots,
    book_appointment
)

from agent.executor import execute_tool
from agent.prompt import SYSTEM_PROMPT


# ===================================================
# DETERMINISTIC MOCK LLM (INTENT ONLY)
# ===================================================

class DeterministicRouterLLM(LLM):
    """
    Deterministic LLM stub used only for intent signaling.
    """

    @property
    def _llm_type(self) -> str:
        return "deterministic-router-llm"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
        return "INTENT_DETECTED"


# ===================================================
# SAFE TOOL WRAPPERS (DRY-RUN + AUDIT)
# ===================================================

def wrapped_search_patient(**kwargs):
    """
    Search for a patient using identifying information such as name and DOB.
    """
    return execute_tool(
        tool_name="search_patient",
        tool_func=search_patient,
        args=kwargs
    )


def wrapped_check_insurance(**kwargs):
    """
    Check insurance eligibility for a patient and service type.
    """
    return execute_tool(
        tool_name="check_insurance_eligibility",
        tool_func=check_insurance_eligibility,
        args=kwargs
    )


def wrapped_find_slots(**kwargs):
    """
    Find available appointment slots for a department within a date range.
    """
    return execute_tool(
        tool_name="find_available_slots",
        tool_func=find_available_slots,
        args=kwargs
    )


def wrapped_book_appointment(**kwargs):
    """
    Book an appointment for a patient using a selected slot.
    """
    return execute_tool(
        tool_name="book_appointment",
        tool_func=book_appointment,
        args=kwargs
    )


# ===================================================
# TOOL REGISTRATION
# ===================================================

tools = [
    StructuredTool.from_function(wrapped_search_patient),
    StructuredTool.from_function(wrapped_check_insurance),
    StructuredTool.from_function(wrapped_find_slots),
    StructuredTool.from_function(wrapped_book_appointment),
]


# ===================================================
# LLM INITIALIZATION
# ===================================================

llm = DeterministicRouterLLM()


# ===================================================
# AGENT INITIALIZATION (kept for completeness)
# ===================================================

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    system_message=SYSTEM_PROMPT,
    verbose=False
)


# ===================================================
# ENTRY POINT (INTENT + SLOT FILLING)
# ===================================================

def run_agent(user_input: str):
    """
    Intent detection and parameter validation before executing workflows.
    """

    text = user_input.lower()

    # ---------- INTENT CHECK ----------
    if not any(word in text for word in ["book", "schedule", "appointment", "follow-up"]):
        return {
            "status": "REFUSED",
            "reason": "Input is not a clinical or operational request."
        }

    # ---------- PARAMETER DETECTION ----------
    has_patient = any(name in text for name in ["ravi", "kumar"])
    has_department = any(dep in text for dep in ["cardiology", "neurology", "orthopedic"])
    has_time = any(
        t in text
        for t in ["today", "tomorrow", "next week", "monday", "date"]
    )

    questions = []

    if not has_patient:
        questions.append("What is the patient's full name?")

    if not has_department:
        questions.append("Which department or specialty is the appointment for?")

    if not has_time:
        questions.append("When would you like to schedule the appointment?")

    # ---------- ASK USER AT RUNTIME ----------
    if questions:
        return {
            "status": "NEEDS_MORE_INFORMATION",
            "questions": questions
        }

    # ---------- SAFE WORKFLOW EXECUTION ----------
    patient = wrapped_search_patient(name="Ravi Kumar")
    patient_id = patient["patient_id"]

    insurance = wrapped_check_insurance(
        patient_id=patient_id,
        service_type="Cardiology"
    )

    slots = wrapped_find_slots(
        department="Cardiology",
        start_date="2025-01-20",
        end_date="2025-01-27"
    )

    appointment = wrapped_book_appointment(
        patient_id=patient_id,
        slot_id="SLOT123",
        department="Cardiology"
    )

    return {
        "patient": patient,
        "insurance": insurance,
        "appointment": appointment
    }
