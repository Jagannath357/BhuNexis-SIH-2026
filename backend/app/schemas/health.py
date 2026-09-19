from pydantic import BaseModel
from typing import Dict, Any

class SystemHealthResponse(BaseModel):
    status: str
    services: Dict[str, Dict[str, Any]]
