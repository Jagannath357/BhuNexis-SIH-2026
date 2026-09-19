from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ReviewUpdateRequest(BaseModel):
    corrected_value: Optional[str] = None
    field_name: Optional[str] = None
    reviewer_comment: Optional[str] = None

class ReviewActionRequest(BaseModel):
    reviewer_comment: Optional[str] = None

class ReviewCaseResponse(BaseModel):
    id: int
    case_uid: str
    parcel_id: int
    document_id: Optional[int] = None
    validation_id: Optional[int] = None
    review_type: Optional[str] = None
    priority: Optional[str] = None
    status: str
    assigned_to: Optional[int] = None
    reviewer_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
