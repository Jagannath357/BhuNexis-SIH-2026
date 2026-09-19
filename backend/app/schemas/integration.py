from pydantic import BaseModel, Field
from typing import List, Optional

# OCR Models
class OCRFieldResult(BaseModel):
    field_name: str
    value: str
    confidence: float
    bbox: Optional[List[int]] = None

class OCRPageResult(BaseModel):
    page_number: int
    text: str
    language: Optional[str] = "odia"
    confidence: float
    fields: List[OCRFieldResult] = []

class OCRResultPayload(BaseModel):
    document_uid: str
    pages: List[OCRPageResult]


# NLP Models
class NLPRecordResult(BaseModel):
    owner_name: str
    survey_number: str
    khata_number: str
    plot_number: Optional[str] = None
    area: float
    area_unit: str = "ACRE"
    village: str
    tehsil: Optional[str] = None
    district: Optional[str] = None
    classification: Optional[str] = "AGRICULTURAL"
    confidence: float

class NLPResultPayload(BaseModel):
    document_uid: str
    records: List[NLPRecordResult]


# Validation Engine Models
class ValidationItemResult(BaseModel):
    validation_type: str
    field_name: str
    expected_value: str
    actual_value: str
    severity: str = "LOW" # LOW, MEDIUM, HIGH, CRITICAL
    status: str = "PASSED" # PASSED, WARNING, CONFLICT, RESOLVED
    message: str

class ValidationResultPayload(BaseModel):
    document_uid: str
    parcel_uid: Optional[str] = None
    results: List[ValidationItemResult]
