from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.all_models import Parcel, LandRight, Owner, ReviewCase, ValidationResult, User
from app.schemas.parcel import ParcelDetailResponse, OwnerSchema, LandRightSchema

router = APIRouter()

@router.get("", response_model=List[ParcelDetailResponse])
def list_parcels(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    village: Optional[str] = None,
    district: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Parcel)
    if status:
        query = query.filter(Parcel.status == status)
    if village:
        query = query.filter(Parcel.village.ilike(f"%{village}%"))
    if district:
        query = query.filter(Parcel.district.ilike(f"%{district}%"))
        
    parcels = query.offset(skip).limit(limit).all()
    return parcels

@router.get("/search", response_model=List[ParcelDetailResponse])
def search_parcels(
    survey_number: Optional[str] = Query(None),
    khasra_number: Optional[str] = Query(None),
    khata_number: Optional[str] = Query(None),
    owner_name: Optional[str] = Query(None),
    village: Optional[str] = Query(None),
    tehsil: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Parcel)
    
    if survey_number:
        query = query.filter(Parcel.survey_number.ilike(f"%{survey_number}%"))
    if khasra_number:
        query = query.filter(Parcel.khasra_number.ilike(f"%{khasra_number}%"))
    if khata_number:
        query = query.filter(Parcel.khata_number.ilike(f"%{khata_number}%"))
    if village:
        query = query.filter(Parcel.village.ilike(f"%{village}%"))
    if tehsil:
        query = query.filter(Parcel.tehsil.ilike(f"%{tehsil}%"))
    if district:
        query = query.filter(Parcel.district.ilike(f"%{district}%"))
        
    if owner_name:
        query = query.join(Parcel.land_rights).join(LandRight.owner).filter(Owner.full_name.ilike(f"%{owner_name}%"))
        
    parcels = query.distinct().limit(50).all()
    return parcels

@router.get("/{parcel_id}", response_model=ParcelDetailResponse)
def get_parcel_details(
    parcel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "PARCEL_NOT_FOUND", "message": f"Parcel ID {parcel_id} not found."}
        )
    return parcel

@router.get("/{parcel_id}/owners", response_model=List[LandRightSchema])
def get_parcel_owners(
    parcel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    land_rights = db.query(LandRight).filter(LandRight.parcel_id == parcel_id).all()
    return land_rights

@router.get("/{parcel_id}/history")
def get_parcel_history(
    parcel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reviews = db.query(ReviewCase).filter(ReviewCase.parcel_id == parcel_id).all()
    validations = db.query(ValidationResult).filter(ValidationResult.parcel_id == parcel_id).all()
    
    return {
        "parcel_id": parcel_id,
        "reviews": [
            {
                "case_uid": r.case_uid,
                "review_type": r.review_type,
                "status": r.status,
                "resolved_at": r.resolved_at,
                "notes": r.reviewer_notes
            } for r in reviews
        ],
        "validations": [
            {
                "validation_type": v.validation_type,
                "field_name": v.field_name,
                "expected": v.expected_value,
                "actual": v.actual_value,
                "status": v.status,
                "message": v.message
            } for v in validations
        ]
    }
