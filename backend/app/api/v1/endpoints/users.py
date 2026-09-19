from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.api.deps import require_roles
from app.core.rbac import AppRole, normalize_role
from app.schemas.user import UserCreate, UserUpdate, UserStatusUpdate, UserDetailResponse
from app.models.all_models import User
from app.core.security import hash_password
from app.core.audit import log_audit_event

router = APIRouter()

@router.get("", response_model=List[UserDetailResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserDetailResponse)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": f"User ID {user_id} not found."}
        )
    return user

@router.post("", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
def create_internal_user(
    data: UserCreate,
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "EMAIL_EXISTS", "message": f"User with email '{data.email}' already exists."}
        )
        
    user = User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role.upper(),
        phone=data.phone,
        is_active=data.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    log_audit_event(
        db=db,
        action="USER_CREATED",
        user_id=current_user.id,
        entity_type="User",
        entity_id=user.id,
        changes={"role": user.role, "email": user.email}
    )
    return user

@router.patch("/{user_id}", response_model=UserDetailResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": f"User ID {user_id} not found."}
        )
        
    changes = {}
    if data.full_name is not None:
        user.full_name = data.full_name
        changes["full_name"] = data.full_name
    if data.email is not None:
        user.email = data.email
        changes["email"] = data.email
    if data.role is not None:
        user.role = data.role.upper()
        changes["role"] = data.role
    if data.phone is not None:
        user.phone = data.phone
        changes["phone"] = data.phone
    if data.is_active is not None:
        user.is_active = data.is_active
        changes["is_active"] = data.is_active
        
    db.commit()
    db.refresh(user)
    
    log_audit_event(
        db=db,
        action="USER_UPDATED",
        user_id=current_user.id,
        entity_type="User",
        entity_id=user.id,
        changes=changes
    )
    return user

@router.patch("/{user_id}/status", response_model=UserDetailResponse)
def update_user_status(
    user_id: int,
    data: UserStatusUpdate,
    current_user: User = Depends(require_roles([AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": f"User ID {user_id} not found."}
        )
        
    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    
    action = "USER_ACTIVATED" if data.is_active else "USER_DEACTIVATED"
    log_audit_event(
        db=db,
        action=action,
        user_id=current_user.id,
        entity_type="User",
        entity_id=user.id,
        changes={"is_active": data.is_active}
    )
    return user
