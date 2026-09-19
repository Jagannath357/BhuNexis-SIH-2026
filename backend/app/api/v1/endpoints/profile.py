from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.auth import UserResponse
from app.schemas.user import PasswordChangeRequest, UserUpdate
from app.models.all_models import User
from app.core.security import verify_password, hash_password
from app.core.audit import log_audit_event

router = APIRouter()

@router.get("", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role,
        phone=current_user.phone,
        is_active=current_user.is_active
    )

@router.patch("", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.phone is not None:
        current_user.phone = data.phone
    db.commit()
    db.refresh(current_user)
    
    log_audit_event(
        db=db,
        action="PROFILE_UPDATED",
        user_id=current_user.id,
        entity_type="User",
        entity_id=current_user.id
    )
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role,
        phone=current_user.phone,
        is_active=current_user.is_active
    )

@router.patch("/password")
def update_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_PASSWORD", "message": "Incorrect current password."}
        )
        
    current_user.password_hash = hash_password(data.new_password)
    db.commit()
    
    log_audit_event(
        db=db,
        action="PASSWORD_CHANGED",
        user_id=current_user.id,
        entity_type="User",
        entity_id=current_user.id
    )
    return {"success": True, "message": "Password updated successfully."}
