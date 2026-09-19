from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class AuditEventResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    changes: Optional[Any] = None
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AuditAnalyticsResponse(BaseModel):
    total_events: int
    events_by_action: dict
    events_by_user: dict
    error_rate: float
    throughput_per_day: dict
