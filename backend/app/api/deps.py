from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Callable
from app.db.session import get_db
from app.core.security import decode_access_token
from app.core.rbac import AppRole, check_role_permission, normalize_role
from app.models.all_models import User

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Invalid or expired authentication token."}
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Malformed token payload."}
        )
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "USER_NOT_FOUND", "message": "User account no longer exists."}
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "INACTIVE_USER", "message": "User account is deactivated."}
        )
        
    return user

def require_roles(allowed_roles: List[AppRole]) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        check_role_permission(current_user.role, allowed_roles)
        return current_user
    return role_checker
