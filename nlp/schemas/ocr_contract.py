"""
schemas/ocr_contract.py - Area 1 Contract with OCR Module.

Strict Pydantic models for consuming OCR engine outputs.
Treats OCR as structured spatial tokens/blocks with bounding boxes and confidences.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator, model_validator


class OCRBlock(BaseModel):
    """Represents a single text element (word or line block) from OCR."""
    text: str = Field(..., description="Recognized string from OCR")
    bbox: List[float] = Field(..., description="Bounding box [x1, y1, x2, y2]")
    confidence: float = Field(..., ge=0.0, le=1.0, description="OCR engine confidence score (0.0 to 1.0)")
    language: Optional[str] = Field(default="en", description="Detected language code (e.g. en, or, hi)")

    @field_validator("bbox")
    @classmethod
    def validate_bbox(cls, v: List[float]) -> List[float]:
        if len(v) != 4:
            raise ValueError(f"Bounding box must contain exactly 4 coordinates [x1, y1, x2, y2], got {len(v)}")
        x1, y1, x2, y2 = v
        if x1 > x2:
            raise ValueError(f"Invalid horizontal coordinates: x1 ({x1}) > x2 ({x2})")
        if y1 > y2:
            raise ValueError(f"Invalid vertical coordinates: y1 ({y1}) > y2 ({y2})")
        return [float(coord) for coord in v]

    @property
    def width(self) -> float:
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self) -> float:
        return self.bbox[3] - self.bbox[1]

    @property
    def area(self) -> float:
        return self.width * self.height


class OCRPage(BaseModel):
    """Represents a single scanned page containing OCR blocks."""
    page_number: int = Field(default=1, ge=1, description="1-indexed page number")
    image_width: float = Field(default=1000.0, gt=0, description="Page width in pixels")
    image_height: float = Field(default=1400.0, gt=0, description="Page height in pixels")
    ocr_blocks: List[OCRBlock] = Field(default_factory=list, description="Extracted OCR text blocks")

    @model_validator(mode="before")
    @classmethod
    def handle_tokens_alias(cls, data: Any) -> Any:
        """Allows either 'tokens' or 'ocr_blocks' as the input key for blocks."""
        if isinstance(data, dict):
            if "ocr_blocks" not in data and "tokens" in data:
                data = dict(data)
                data["ocr_blocks"] = data.pop("tokens")
            elif "image_width" not in data and "width" in data:
                data = dict(data)
                data["image_width"] = data.pop("width")
            if "image_height" not in data and "height" in data:
                data = dict(data)
                data["image_height"] = data.pop("height")
        return data

    def get_full_text(self) -> str:
        """Returns concatenated text of all blocks on this page."""
        return "\n".join(b.text for b in self.ocr_blocks)

    def filter_by_confidence(self, min_confidence: float) -> List[OCRBlock]:
        """Returns only blocks meeting the minimum confidence threshold."""
        return [b for b in self.ocr_blocks if b.confidence >= min_confidence]


class OCRDocument(BaseModel):
    """Root model for OCR payloads passed to the NLP understanding pipeline."""
    document_id: str = Field(..., description="Unique document reference ID")
    language: Optional[str] = Field(default="en", description="Primary document language")
    pages: List[OCRPage] = Field(default_factory=list, description="Pages in the document")

    @property
    def total_blocks(self) -> int:
        return sum(len(p.ocr_blocks) for p in self.pages)

    @property
    def average_confidence(self) -> float:
        total = self.total_blocks
        if total == 0:
            return 0.0
        return sum(b.confidence for p in self.pages for b in p.ocr_blocks) / total

    def get_page(self, page_number: int) -> Optional[OCRPage]:
        for p in self.pages:
            if p.page_number == page_number:
                return p
        return None

    def get_all_blocks(self) -> List[OCRBlock]:
        blocks = []
        for p in self.pages:
            blocks.extend(p.ocr_blocks)
        return blocks
