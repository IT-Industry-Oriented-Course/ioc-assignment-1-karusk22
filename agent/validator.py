import json
from datetime import datetime

def audit_log(event):
    with open("logs/audit.log", "a") as f:
        f.write(json.dumps({
            "timestamp": str(datetime.utcnow()),
            **event
        }) + "\n")
