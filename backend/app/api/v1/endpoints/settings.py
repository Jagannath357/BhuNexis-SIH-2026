from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import require_roles
from app.core.rbac import AppRole
from app.schemas.settings import SystemSettingsUpdate
from app.models.all_models import User
from app.core.audit import log_audit_event

router = APIRouter()

# In-memory settings state for runtime parameters
system_settings_state = {
    "ocr_confidence_threshold": 0.85,
    "validation_confidence_threshold": 0.80,
    "auto_approve_high_confidence": False,
    "max_batch_upload_size": 50,
    "default_district": "Khordha"
}

@router.get("")
def get_system_settings(
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
):
    return {"success": True, "settings": system_settings_state}

@router.patch("")
def update_system_settings(
    data: SystemSettingsUpdate,
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    system_settings_state["ocr_confidence_threshold"] = data.ocr_confidence_threshold
    system_settings_state["validation_confidence_threshold"] = data.validation_confidence_threshold
    system_settings_state["auto_approve_high_confidence"] = data.auto_approve_high_confidence
    system_settings_state["max_batch_upload_size"] = data.max_batch_upload_size
    system_settings_state["default_district"] = data.default_district
    
    log_audit_event(
        db=db,
        action="SETTINGS_UPDATED",
        user_id=current_user.id,
        entity_type="SystemSettings",
        changes=system_settings_state
    )
    return {"success": True, "settings": system_settings_state}
