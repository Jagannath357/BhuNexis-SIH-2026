from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
from app.db.session import get_db
from app.api.deps import require_roles
from app.core.rbac import AppRole
from app.models.all_models import ReviewCase, Parcel, ExtractedField, User, DocumentPage
from app.schemas.review import ReviewCaseResponse, ReviewUpdateRequest, ReviewActionRequest
from app.core.audit import log_audit_event

router = APIRouter()

@router.get("", response_model=List[ReviewCaseResponse])
def get_review_queue(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    current_user: User = Depends(require_roles([AppRole.REVIEWER, AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    query = db.query(ReviewCase)
    if status:
        query = query.filter(ReviewCase.status == status)
    if priority:
        query = query.filter(ReviewCase.priority == priority)
    if assigned_to:
        query = query.filter(ReviewCase.assigned_to == assigned_to)
        
    reviews = query.order_by(ReviewCase.created_at.desc()).limit(100).all()
    return reviews

@router.get("/{review_id}", response_model=ReviewCaseResponse)
def get_review_detail(
    review_id: int,
    current_user: User = Depends(require_roles([AppRole.REVIEWER, AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    review = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REVIEW_NOT_FOUND", "message": f"Review case ID {review_id} not found."}
        )
    return review

@router.patch("/{review_id}", response_model=ReviewCaseResponse)
def update_review_correction(
    review_id: int,
    data: ReviewUpdateRequest,
    current_user: User = Depends(require_roles([AppRole.REVIEWER])),
    db: Session = Depends(get_db)
):
    review = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REVIEW_NOT_FOUND", "message": f"Review case ID {review_id} not found."}
        )
        
    if data.reviewer_comment:
        review.reviewer_notes = data.reviewer_comment
    review.assigned_to = current_user.id
    
    if data.field_name and data.corrected_value and review.document_id:
        extracted = db.query(ExtractedField).join(
            DocumentPage, ExtractedField.document_page_id == DocumentPage.id
        ).filter(
            DocumentPage.document_id == review.document_id,
            ExtractedField.field_name == data.field_name
        ).first()
        if extracted:
            extracted.extracted_value = data.corrected_value
            extracted.status = "CORRECTED"
            
    db.commit()
    db.refresh(review)
    
    log_audit_event(
        db=db,
        action="FIELD_CORRECTED",
        user_id=current_user.id,
        entity_type="ReviewCase",
        entity_id=review.id,
        changes={"field_name": data.field_name, "corrected_value": data.corrected_value}
    )
    return review

@router.post("/{review_id}/approve", response_model=ReviewCaseResponse)
def approve_review(
    review_id: int,
    data: Optional[ReviewActionRequest] = None,
    current_user: User = Depends(require_roles([AppRole.REVIEWER])),
    db: Session = Depends(get_db)
):
    review = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REVIEW_NOT_FOUND", "message": f"Review case ID {review_id} not found."}
        )
        
    review.status = "APPROVED"
    review.assigned_to = current_user.id
    review.resolved_at = datetime.now(timezone.utc)
    if data and data.reviewer_comment:
        review.reviewer_notes = data.reviewer_comment
        
    db.commit()
    db.refresh(review)
    
    log_audit_event(
        db=db,
        action="REVIEW_APPROVED",
        user_id=current_user.id,
        entity_type="ReviewCase",
        entity_id=review.id
    )
    return review

@router.post("/{review_id}/reject", response_model=ReviewCaseResponse)
def reject_review(
    review_id: int,
    data: Optional[ReviewActionRequest] = None,
    current_user: User = Depends(require_roles([AppRole.REVIEWER])),
    db: Session = Depends(get_db)
):
    review = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REVIEW_NOT_FOUND", "message": f"Review case ID {review_id} not found."}
        )
        
    review.status = "REJECTED"
    review.assigned_to = current_user.id
    review.resolved_at = datetime.now(timezone.utc)
    if data and data.reviewer_comment:
        review.reviewer_notes = data.reviewer_comment
        
    db.commit()
    db.refresh(review)
    
    log_audit_event(
        db=db,
        action="REVIEW_REJECTED",
        user_id=current_user.id,
        entity_type="ReviewCase",
        entity_id=review.id
    )
    return review

@router.post("/{review_id}/verify", response_model=ReviewCaseResponse)
def verify_review(
    review_id: int,
    data: Optional[ReviewActionRequest] = None,
    current_user: User = Depends(require_roles([AppRole.REVIEWER])),
    db: Session = Depends(get_db)
):
    review = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REVIEW_NOT_FOUND", "message": f"Review case ID {review_id} not found."}
        )
        
    review.status = "RESOLVED"
    review.assigned_to = current_user.id
    review.resolved_at = datetime.now(timezone.utc)
    if data and data.reviewer_comment:
        review.reviewer_notes = data.reviewer_comment
        
    parcel = db.query(Parcel).filter(Parcel.id == review.parcel_id).first()
    if parcel:
        parcel.status = "VERIFIED"
        
    db.commit()
    db.refresh(review)
    
    log_audit_event(
        db=db,
        action="PARCEL_VERIFIED",
        user_id=current_user.id,
        entity_type="Parcel",
        entity_id=review.parcel_id,
        changes={"review_id": review.id, "status": "VERIFIED"}
    )
    return review
