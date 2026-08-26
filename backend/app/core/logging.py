import logging
from datetime import datetime
import json

# Setup standard logger
logger = logging.getLogger("nexus")
logger.setLevel(logging.INFO)

# File handler for audit logs
audit_handler = logging.FileHandler("nexus_audit.log")
audit_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
audit_handler.setFormatter(formatter)
logger.addHandler(audit_handler)

class AuditLogger:
    @staticmethod
    def log_event(event_type: str, details: dict, user_id: str = "system"):
        """
        Logs a security-sensitive event without exposing secrets.
        """
        # Ensure no sensitive keys are passed in details
        safe_details = {k: v for k, v in details.items() if not any(sensitive in k.lower() for sensitive in ['password', 'secret', 'key', 'token'])}
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": safe_details
        }
        
        logger.info(f"AUDIT EVENT: {json.dumps(log_entry)}")
