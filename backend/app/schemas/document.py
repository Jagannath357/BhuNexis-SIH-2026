from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class DocumentUploadResponse(BaseModel):
    id: int
    document_uid: str
    file_name: str
    processing_status: str
    uploaded_by: Optional[int] = None

class DocumentStatusResponse(BaseModel):
    document_id: int
    processing_status: str
    pages_total: int
    pages_processed: int

class ExtractedFieldSchema(BaseModel):
    id: int
    field_name: str
    extracted_value: Optional[str] = None
    confidence_score: Optional[float] = None
    bounding_box: Optional[dict] = None
    status: Optional[str] = None

class DocumentPageSchema(BaseModel):
    id: int
    page_number: int
    ocr_text: Optional[str] = None
    confidence_score: Optional[float] = None
    processed_at: Optional[datetime] = None

class DocumentDetailResponse(BaseModel):
    id: int
    document_uid: str
    file_name: str
    file_size: Optional[int] = None
    document_type: Optional[str] = None
    language: Optional[str] = None
    district: Optional[str] = None
    tehsil: Optional[str] = None
    village: Optional[str] = None
    document_date: Optional[datetime] = None
    processing_status: str
    uploaded_by: Optional[int] = None
    created_at: datetime
    pages: List[DocumentPageSchema] = []
    extracted_fields: List[ExtractedFieldSchema] = []

    model_config = ConfigDict(from_attributes=True)
