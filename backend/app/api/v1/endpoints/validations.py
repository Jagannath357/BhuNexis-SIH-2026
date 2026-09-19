from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.all_models import ValidationResult, User

router = APIRouter()

@router.get("")
def list_validations(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    parcel_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ValidationResult)
    if status:
        query = query.filter(ValidationResult.status == status)
    if severity:
        query = query.filter(ValidationResult.severity == severity)
    if parcel_id:
        query = query.filter(ValidationResult.parcel_id == parcel_id)
        
    validations = query.offset(skip).limit(limit).all()
    return validations

@router.get("/{validation_id}")
def get_validation_by_id(
    validation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    val = db.query(ValidationResult).filter(ValidationResult.id == validation_id).first()
    if not val:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "VALIDATION_NOT_FOUND", "message": f"Validation ID {validation_id} not found."}
        )
    return val
