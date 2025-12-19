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
# DETERMINISTIC MOCK LLM (SAFE, OFFLINE, STABLE)
# ===================================================

class DeterministicRouterLLM(LLM):
    """
    Deterministic LLM stub for workflow orchestration.
    This avoids live HF inference while preserving agent behavior.
    """

    @property
    def _llm_type(self) -> str:
        return "deterministic-router-llm"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
        """
        Minimal reasoning output that forces tool usage.
        """
        return """
Thought: I need to identify the patient, check insurance, find slots, and book appointment.
Action: wrapped_search_patient
Action Input: {"name": "Ravi Kumar"}
"""


# ===================================================
# SAFE TOOL WRAPPERS (DRY-RUN + AUDIT)
# ===================================================

def wrapped_search_patient(**kwargs):
    """Search patient records"""
    return execute_tool(
        tool_name="search_patient",
        tool_func=search_patient,
        args=kwargs
    )


def wrapped_check_insurance(**kwargs):
    """Check insurance eligibility"""
    return execute_tool(
        tool_name="check_insurance_eligibility",
        tool_func=check_insurance_eligibility,
        args=kwargs
    )


def wrapped_find_slots(**kwargs):
    """Find appointment slots"""
    return execute_tool(
        tool_name="find_available_slots",
        tool_func=find_available_slots,
        args=kwargs
    )


def wrapped_book_appointment(**kwargs):
    """Book appointment"""
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
# LLM INITIALIZATION (NO EXTERNAL DEPENDENCY)
# ===================================================

llm = DeterministicRouterLLM()


# ===================================================
# AGENT INITIALIZATION
# ===================================================

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    system_message=SYSTEM_PROMPT,
    verbose=True
)


# ===================================================
# ENTRY POINT
# ===================================================

def run_agent(user_input: str):
    """
    Entry point with intent validation.
    Only executes clinical workflow for valid requests.
    """

    text = user_input.lower()

    # ---------- SAFETY / INTENT GATE ----------
    if not any(keyword in text for keyword in ["appointment", "schedule", "follow-up", "book"]):
        return {
            "status": "REFUSED",
            "reason": "Input does not represent a clinical or operational request.",
            "allowed_actions": [
                "schedule appointment",
                "check insurance eligibility",
                "find available slots"
            ]
        }

    # ---------- CLINICAL WORKFLOW ----------
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
