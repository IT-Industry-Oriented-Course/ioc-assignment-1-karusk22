# agent/executor.py

from agent.config import DRY_RUN
from agent.validator import audit_log


def execute_tool(tool_name: str, tool_func, args: dict):
    audit_log({
        "event": "TOOL_SELECTED",
        "tool": tool_name,
        "arguments": args
    })

    if DRY_RUN:
        result = {
            "mode": "DRY_RUN",
            "tool": tool_name,
            "arguments": args
        }

        audit_log({
            "event": "DRY_RUN_EXECUTED",
            "result": result
        })

        return result

    output = tool_func(**args)

    audit_log({
        "event": "TOOL_EXECUTED",
        "tool": tool_name,
        "result": output
    })

    return output
