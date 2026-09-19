from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.db.session import get_db
from app.schemas.integration import OCRResultPayload, NLPResultPayload, ValidationResultPayload
from app.models.all_models import Document, DocumentPage, ExtractedField, ValidationResult, ReviewCase, Parcel
from app.core.audit import log_audit_event

router = APIRouter()

@router.post("/ocr/results", status_code=status.HTTP_200_OK)
def receive_ocr_results(
    payload: OCRResultPayload,
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.document_uid == payload.document_uid).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": f"Document UID {payload.document_uid} not found."}
        )
        
    doc.processing_status = "OCR_PROCESSED"
    
    for page_data in payload.pages:
        page = db.query(DocumentPage).filter(
            DocumentPage.document_id == doc.id,
            DocumentPage.page_number == page_data.page_number
        ).first()
        
        if not page:
            page = DocumentPage(
                document_id=doc.id,
                page_number=page_data.page_number,
                ocr_text=page_data.text,
                language=page_data.language,
                confidence_score=page_data.confidence
            )
            db.add(page)
            db.flush()
        else:
            page.ocr_text = page_data.text
            page.confidence_score = page_data.confidence
            
        for field in page_data.fields:
            extracted = ExtractedField(
                document_id=doc.id,
                page_id=page.id,
                field_name=field.field_name,
                extracted_value=field.value,
                confidence_score=field.confidence,
                bounding_box={"bbox": field.bbox} if field.bbox else None,
                status="EXTRACTED"
            )
            db.add(extracted)

    db.commit()
    
    log_audit_event(
        db=db,
        action="OCR_PROCESSED",
        entity_type="Document",
        entity_id=doc.id,
        changes={"document_uid": doc.document_uid, "pages_count": len(payload.pages)}
    )
    
    return {"success": True, "message": f"OCR results processed for {doc.document_uid}"}

@router.post("/nlp/results", status_code=status.HTTP_200_OK)
def receive_nlp_results(
    payload: NLPResultPayload,
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.document_uid == payload.document_uid).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": f"Document UID {payload.document_uid} not found."}
        )
        
    doc.processing_status = "EXTRACTED"
    
    for record in payload.records:
        # Create extracted field representations
        field_mappings = [
            ("owner_name", record.owner_name, record.confidence),
            ("survey_number", record.survey_number, record.confidence),
            ("khata_number", record.khata_number, record.confidence),
            ("area", str(record.area), record.confidence),
            ("village", record.village, record.confidence),
            ("district", record.district or "Khordha", record.confidence)
        ]
        for fname, val, conf in field_mappings:
            ef = ExtractedField(
                document_id=doc.id,
                field_name=fname,
                extracted_value=val,
                confidence_score=conf,
                status="EXTRACTED"
            )
            db.add(ef)
            
    db.commit()
    
    log_audit_event(
        db=db,
        action="NLP_PROCESSED",
        entity_type="Document",
        entity_id=doc.id,
        changes={"document_uid": doc.document_uid, "records_count": len(payload.records)}
    )
    
    return {"success": True, "message": f"NLP structured records processed for {doc.document_uid}"}

@router.post("/validation/results", status_code=status.HTTP_200_OK)
def receive_validation_results(
    payload: ValidationResultPayload,
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.document_uid == payload.document_uid).first()
    parcel = db.query(Parcel).filter(Parcel.parcel_uid == payload.parcel_uid).first() if payload.parcel_uid else None
    
    doc_id = doc.id if doc else None
    parcel_id = parcel.id if parcel else (db.query(Parcel.id).first()[0] if db.query(Parcel).first() else 1)
    
    has_conflicts = False
    for res in payload.results:
        val_entry = ValidationResult(
            parcel_id=parcel_id,
            document_id=doc_id,
            validation_type=res.validation_type,
            field_name=res.field_name,
            expected_value=res.expected_value,
            actual_value=res.actual_value,
            severity=res.severity,
            status=res.status,
            message=res.message
        )
        db.add(val_entry)
        db.flush()
        
        if res.status in ["CONFLICT", "WARNING", "REVIEW_REQUIRED"]:
            has_conflicts = True
            review_case = ReviewCase(
                case_uid=f"REV-{uuid.uuid4().hex[:6].upper()}",
                parcel_id=parcel_id,
                document_id=doc_id,
                validation_id=val_entry.id,
                review_type=res.validation_type,
                priority="HIGH" if res.severity in ["HIGH", "CRITICAL"] else "MEDIUM",
                status="PENDING",
                reviewer_notes=f"Auto-generated review case: {res.message}"
            )
            db.add(review_case)

    if doc:
        doc.processing_status = "REVIEW_REQUIRED" if has_conflicts else "VALIDATED"
        
    db.commit()
    
    log_audit_event(
        db=db,
        action="VALIDATION_COMPLETED",
        entity_type="Document",
        entity_id=doc_id,
        changes={"document_uid": payload.document_uid, "has_conflicts": has_conflicts}
    )
    
    return {"success": True, "message": f"Validation results processed for {payload.document_uid}", "has_conflicts": has_conflicts}
