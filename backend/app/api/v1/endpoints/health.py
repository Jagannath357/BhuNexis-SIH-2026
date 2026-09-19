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
    services = {}
    
    # 1. Backend API
    services["backend"] = {"status": "HEALTHY", "details": "FastAPI backend running."}
    
    # 2. Database
    try:
        db.execute(text("SELECT 1;"))
        services["database"] = {"status": "HEALTHY", "details": "PostgreSQL connection active."}
    except Exception as e:
        services["database"] = {"status": "UNHEALTHY", "details": str(e)}
        
    # 3. PostGIS
    try:
        ver = db.execute(text("SELECT PostGIS_Version();")).fetchone()
        services["postgis"] = {"status": "HEALTHY", "details": f"PostGIS version {ver[0] if ver else '3.6.2'} active."}
    except Exception as e:
        services["postgis"] = {"status": "UNHEALTHY", "details": str(e)}
        
    # 4. OCR Service
    try:
        r = httpx.get(f"{settings.OCR_SERVICE_URL}/health", timeout=1.0)
        if r.status_code == 200:
            services["ocr"] = {"status": "HEALTHY", "details": "OCR service responsive."}
        else:
            services["ocr"] = {"status": "UNAVAILABLE", "details": f"HTTP {r.status_code}"}
    except Exception:
        services["ocr"] = {"status": "UNAVAILABLE", "details": "OCR service not configured or offline."}
        
    # 5. NLP Service
    try:
        r = httpx.get(f"{settings.NLP_SERVICE_URL}/health", timeout=1.0)
        if r.status_code == 200:
            services["nlp"] = {"status": "HEALTHY", "details": "NLP service responsive."}
        else:
            services["nlp"] = {"status": "UNAVAILABLE", "details": f"HTTP {r.status_code}"}
    except Exception:
        services["nlp"] = {"status": "UNAVAILABLE", "details": "NLP service not configured or offline."}
        
    # 6. Validation Service
    try:
        r = httpx.get(f"{settings.VALIDATION_SERVICE_URL}/health", timeout=1.0)
        if r.status_code == 200:
            services["validation"] = {"status": "HEALTHY", "details": "Validation service responsive."}
        else:
            services["validation"] = {"status": "UNAVAILABLE", "details": f"HTTP {r.status_code}"}
    except Exception:
        services["validation"] = {"status": "UNAVAILABLE", "details": "Validation engine service not configured or offline."}

    overall_status = "HEALTHY" if services["database"]["status"] == "HEALTHY" else "UNHEALTHY"

    return SystemHealthResponse(status=overall_status, services=services)
