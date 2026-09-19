from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str
    phone: Optional[str] = None
    is_active: bool = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class UserStatusUpdate(BaseModel):
    is_active: bool

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class UserDetailResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
