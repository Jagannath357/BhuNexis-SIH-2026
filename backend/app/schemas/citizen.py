from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class GrievanceRequest(BaseModel):
    parcel_id: Optional[int] = None
    survey_number: Optional[str] = None
    subject: str
    description: str

class GrievanceResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    description: str
    status: str = "SUBMITTED"
    created_at: datetime
