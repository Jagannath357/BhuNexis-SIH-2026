from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse, SignupRequest
from app.models.all_models import User
from app.core.security import verify_password, hash_password, create_access_token
from app.core.rbac import normalize_role, AppRole
from app.core.audit import log_audit_event
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password."}
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "INACTIVE_ACCOUNT", "message": "User account is deactivated. Contact system admin."}
        )
        
    if not verify_password(request_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password."}
        )
        
    actual_role = normalize_role(user.role)
    requested_role = normalize_role(request_data.role)
    
    if actual_role != requested_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "ROLE_MISMATCH",
                "message": f"Account is registered as '{actual_role}', not '{requested_role}'."
            }
        )
        
    token = create_access_token(subject=user.id, role=actual_role, email=user.email)
    
    log_audit_event(
        db=db,
        action="LOGIN",
        user_id=user.id,
        entity_type="User",
        entity_id=user.id,
        ip_address=request.client.host if request.client else None
    )
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        expires_in=28800,
        user=UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            role=actual_role,
            phone=user.phone,
            is_active=user.is_active
        )
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=normalize_role(current_user.role),
        phone=current_user.phone,
        is_active=current_user.is_active
    )

@router.post("/signup", response_model=UserResponse)
def signup(data: SignupRequest, request: Request, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "EMAIL_EXISTS", "message": "An account with this email already exists."}
        )
        
    new_user = User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role="CITIZEN", # Force public self-registration to CITIZEN
        phone=data.phone,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_audit_event(
        db=db,
        action="CITIZEN_SIGNUP",
        user_id=new_user.id,
        entity_type="User",
        entity_id=new_user.id,
        ip_address=request.client.host if request.client else None
    )
    
    return UserResponse(
        id=new_user.id,
        full_name=new_user.full_name,
        email=new_user.email,
        role="CITIZEN",
        phone=new_user.phone,
        is_active=new_user.is_active
    )

@router.post("/logout")
def logout(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    log_audit_event(
        db=db,
        action="LOGOUT",
        user_id=current_user.id,
        entity_type="User",
        entity_id=current_user.id,
        ip_address=request.client.host if request.client else None
    )
    return {"success": True, "message": "Logged out successfully."}
