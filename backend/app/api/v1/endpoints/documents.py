from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import uuid
from app.db.session import get_db
from app.api.deps import require_roles, get_current_user
from app.core.rbac import AppRole
from app.core.storage import storage_service
from app.models.all_models import Document, DocumentPage, User
from app.schemas.document import DocumentUploadResponse, DocumentStatusResponse, DocumentDetailResponse
from app.core.audit import log_audit_event

router = APIRouter()

@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(None),
    language: Optional[str] = Form("odia"),
    district: Optional[str] = Form(None),
    tehsil: Optional[str] = Form(None),
    village: Optional[str] = Form(None),
    document_date: Optional[str] = Form(None),
    current_user: User = Depends(require_roles([AppRole.OFFICER, AppRole.ADMIN])),
    db: Session = Depends(get_db)
):
    try:
        saved_path, unique_name, file_size = await storage_service.save_file(file, prefix="DOC")
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_FILE", "message": str(ve)}
        )
        
    doc_uid = f"DOC-{uuid.uuid4().hex[:6].upper()}"
    parsed_date = None
    if document_date:
        try:
            parsed_date = datetime.fromisoformat(document_date)
        except Exception:
            pass
            
    doc = Document(
        document_uid=doc_uid,
        file_name=file.filename,
        file_path=saved_path,
        file_size=file_size,
        document_type=document_type or "Khatian / RoR",
        language=language or "odia",
        district=district or "Khordha",
        tehsil=tehsil or "Jatni",
        village=village or "Sample Village",
        document_date=parsed_date,
        processing_status="UPLOADED",
        uploaded_by=current_user.id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Create initial page entry
    page = DocumentPage(
        document_id=doc.id,
        page_number=1,
        image_path=saved_path,
        ocr_status="PENDING",
        language=language or "odia",
        ocr_text=""
    )
    db.add(page)
    db.commit()
    
    # Run end-to-end OCR -> NLP -> Persistence pipeline
    try:
        from app.services.pipeline_service import run_end_to_end_pipeline
        run_end_to_end_pipeline(db=db, document_id=doc.id)
        db.refresh(doc)
    except Exception as pe:
        pass

    log_audit_event(
        db=db,
        action="DOCUMENT_UPLOADED",
        user_id=current_user.id,
        entity_type="Document",
        entity_id=doc.id,
        changes={"document_uid": doc.document_uid, "file_name": doc.file_name}
    )
    
    return DocumentUploadResponse(
        id=doc.id,
        document_uid=doc.document_uid,
        file_name=doc.file_name,
        processing_status=doc.processing_status,
        uploaded_by=doc.uploaded_by
    )

@router.get("", response_model=List[DocumentDetailResponse])
def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    district: Optional[str] = None,
    village: Optional[str] = None,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Document)
    if status:
        query = query.filter(Document.processing_status == status)
    if district:
        query = query.filter(Document.district.ilike(f"%{district}%"))
    if village:
        query = query.filter(Document.village.ilike(f"%{village}%"))
    if document_type:
        query = query.filter(Document.document_type == document_type)
        
    documents = query.order_by(Document.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return documents

@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document_details(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": f"Document ID {document_id} not found."}
        )
    return doc

@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
def get_document_status(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": f"Document ID {document_id} not found."}
        )
        
    total_pages = db.query(DocumentPage).filter(DocumentPage.document_id == document_id).count()
    processed_pages = db.query(DocumentPage).filter(DocumentPage.document_id == document_id, DocumentPage.ocr_status.isnot(None)).count()
    
    return DocumentStatusResponse(
        document_id=doc.id,
        processing_status=doc.processing_status,
        pages_total=max(total_pages, 1),
        pages_processed=processed_pages
    )

