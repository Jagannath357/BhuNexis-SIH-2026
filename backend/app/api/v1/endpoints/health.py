from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import httpx
from app.db.session import get_db
from app.core.config import settings
from app.schemas.health import SystemHealthResponse

router = APIRouter()

@router.get("", response_model=SystemHealthResponse)
def get_health(db: Session = Depends(get_db)):
    services = {
        "backend": {"status": "HEALTHY", "details": "FastAPI backend running."},
        "ocr": {"status": "UNAVAILABLE", "details": "OCR service interface prepared."},
        "nlp": {"status": "UNAVAILABLE", "details": "NLP service interface prepared."},
        "validation": {"status": "UNAVAILABLE", "details": "Validation engine service interface prepared."}
    }
    
    # Database
    try:
        db.execute(text("SELECT 1;"))
        services["database"] = {"status": "HEALTHY", "details": "PostgreSQL connection active."}
    except Exception as e:
        services["database"] = {"status": "UNHEALTHY", "details": str(e)}
        
    # PostGIS
    try:
        ver = db.execute(text("SELECT PostGIS_Version();")).fetchone()
        services["postgis"] = {"status": "HEALTHY", "details": f"PostGIS version {ver[0] if ver else '3.6.2'} active."}
    except Exception as e:
        services["postgis"] = {"status": "UNHEALTHY", "details": str(e)}

    overall_status = "HEALTHY" if services.get("database", {}).get("status") == "HEALTHY" else "UNHEALTHY"
    return SystemHealthResponse(status=overall_status, services=services)
