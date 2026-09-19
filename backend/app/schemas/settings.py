from pydantic import BaseModel

class SystemSettingsUpdate(BaseModel):
    ocr_confidence_threshold: float = 0.85
    validation_confidence_threshold: float = 0.80
    auto_approve_high_confidence: bool = False
    max_batch_upload_size: int = 50
    default_district: str = "Khordha"
