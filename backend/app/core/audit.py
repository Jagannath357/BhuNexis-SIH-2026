from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def log_audit_event(
    db: Session,
    action: str,
    user_id: Optional[int] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    changes: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
) -> None:
    try:
        from app.models.all_models import AuditEvent
        audit = AuditEvent(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            new_value=changes,
            created_at=datetime.now(timezone.utc)
        )
        db.add(audit)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log audit event '{action}': {str(e)}")
        db.rollback()
