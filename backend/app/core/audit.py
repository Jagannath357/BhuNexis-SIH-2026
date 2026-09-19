from sqlalchemy.orm import Session
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def log_audit_event(
    db: Session,
    action: str,
    user_id: int = None,
    entity_type: str = None,
    entity_id: int = None,
    changes: dict = None,
    ip_address: str = None
):
    try:
        from app.models import AuditEvent
        audit = AuditEvent(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            changes=changes,
            ip_address=ip_address,
            created_at=datetime.now(timezone.utc)
        )
        db.add(audit)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log audit event '{action}': {str(e)}")
        db.rollback()
