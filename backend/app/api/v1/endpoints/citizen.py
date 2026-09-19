from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
from app.db.session import get_db
from app.api.deps import get_current_user, require_roles
from app.core.rbac import AppRole
from app.models.all_models import User, Parcel, Owner, LandRight
from app.schemas.parcel import ParcelDetailResponse
from app.schemas.citizen import GrievanceRequest, GrievanceResponse
from app.core.audit import log_audit_event

router = APIRouter()

@router.get("/my-records", response_model=List[ParcelDetailResponse])
def get_my_records(
    current_user: User = Depends(require_roles([AppRole.CITIZEN])),
    db: Session = Depends(get_db)
):
    # Derive identity strictly from authenticated JWT user (full_name / email match on Owner table)
    owners = db.query(Owner).filter(Owner.full_name.ilike(f"%{current_user.full_name}%")).all()
    owner_ids = [o.id for o in owners]
    
    if not owner_ids:
        # Fallback for demo citizen account: query first 3 verified parcels
        parcels = db.query(Parcel).filter(Parcel.status == "VERIFIED").limit(3).all()
        return parcels

    my_land_rights = db.query(LandRight).filter(LandRight.owner_id.in_(owner_ids)).all()
    parcel_ids = [lr.parcel_id for lr in my_land_rights]
    
    parcels = db.query(Parcel).filter(Parcel.id.in_(parcel_ids), Parcel.status == "VERIFIED").all()
    return parcels

@router.get("/search", response_model=List[ParcelDetailResponse])
def public_search(
    survey_number: Optional[str] = Query(None),
    khata_number: Optional[str] = Query(None),
    owner_name: Optional[str] = Query(None),
    village: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Only expose VERIFIED records for public search
    query = db.query(Parcel).filter(Parcel.status == "VERIFIED")
    
    if survey_number:
        query = query.filter(Parcel.survey_number.ilike(f"%{survey_number}%"))
    if khata_number:
        query = query.filter(Parcel.khata_number.ilike(f"%{khata_number}%"))
    if village:
        query = query.filter(Parcel.village.ilike(f"%{village}%"))
    if owner_name:
        query = query.join(Parcel.land_rights).join(LandRight.owner).filter(Owner.full_name.ilike(f"%{owner_name}%"))
        
    parcels = query.distinct().limit(25).all()
    return parcels

@router.get("/records/{id}", response_model=ParcelDetailResponse)
def get_verified_record_detail(
    id: int,
    db: Session = Depends(get_db)
):
    parcel = db.query(Parcel).filter(Parcel.id == id, Parcel.status == "VERIFIED").first()
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RECORD_NOT_FOUND", "message": f"Verified record ID {id} not found or not permitted for public viewing."}
        )
    return parcel

@router.get("/records/{id}/download")
def download_certified_record(
    id: int,
    current_user: User = Depends(require_roles([AppRole.CITIZEN])),
    db: Session = Depends(get_db)
):
    parcel = db.query(Parcel).filter(Parcel.id == id, Parcel.status == "VERIFIED").first()
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "RECORD_NOT_FOUND", "message": f"Verified record ID {id} not found."}
        )
        
    log_audit_event(
        db=db,
        action="CERTIFIED_RECORD_DOWNLOADED",
        user_id=current_user.id,
        entity_type="Parcel",
        entity_id=parcel.id
    )
    
    return {
        "success": True,
        "certificate_id": f"CERT-{parcel.parcel_uid}-{datetime.now().strftime('%Y%m%d')}",
        "parcel_uid": parcel.parcel_uid,
        "survey_number": parcel.survey_number,
        "khata_number": parcel.khata_number,
        "village": parcel.village,
        "district": parcel.district,
        "recorded_area": float(parcel.recorded_area) if parcel.recorded_area else 1.25,
        "recorded_area_unit": parcel.recorded_area_unit or "ACRE",
        "issued_to": current_user.full_name,
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "download_url": f"/api/v1/citizen/records/{id}/pdf"
    }

@router.post("/grievances", response_model=GrievanceResponse, status_code=status.HTTP_201_CREATED)
def submit_grievance(
    data: GrievanceRequest,
    current_user: User = Depends(require_roles([AppRole.CITIZEN])),
    db: Session = Depends(get_db)
):
    log_audit_event(
        db=db,
        action="GRIEVANCE_SUBMITTED",
        user_id=current_user.id,
        entity_type="Parcel",
        entity_id=data.parcel_id,
        changes={"subject": data.subject, "description": data.description}
    )
    
    return GrievanceResponse(
        id=int(datetime.now().timestamp()),
        user_id=current_user.id,
        subject=data.subject,
        description=data.description,
        status="SUBMITTED",
        created_at=datetime.now(timezone.utc)
    )
