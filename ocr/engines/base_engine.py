from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import numpy as np


@dataclass
class OCRBox:
    """Represents a single detected text region/line with its coordinates and confidence."""
    text: str
    confidence: float
    box: List[List[int]]  # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    language: str = "en"

    def get_bbox(self) -> List[float]:
        """Calculates flat [x_min, y_min, x_max, y_max] from polygon points as floats."""
        if not self.box:
            return [0.0, 0.0, 0.0, 0.0]
        xs = [float(p[0]) for p in self.box]
        ys = [float(p[1]) for p in self.box]
        return [
            round(min(xs), 1),
            round(min(ys), 1),
            round(max(xs), 1),
            round(max(ys), 1)
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "bbox": self.get_bbox(),
            "confidence": round(float(self.confidence), 2),
            "language": self.language
        }


@dataclass
class OCRResult:
    """Standardized OCR output format specified by Prototype Decision Plan."""
    document_id: str
    language: str
    ocr_engine: str
    text: str
    confidence: float
    boxes: List[OCRBox]
    status: str = "Ready for Human Verification"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "language": self.language,
            "ocr_engine": self.ocr_engine,
            "text": self.text,
            "confidence": round(self.confidence, 4),
            "status": self.status,
            "boxes_count": len(self.boxes),
            "boxes": [box.to_dict() for box in self.boxes]
        }

    def to_standard_format(self, image_width: int = 0, image_height: int = 0, page_number: int = 1) -> Dict[str, Any]:
        """Returns standardized SIH schema with pages and ocr_blocks."""
        return {
            "document_id": self.document_id,
            "language": "en",
            "pages": [
                {
                    "page_number": page_number,
                    "image_width": int(image_width),
                    "image_height": int(image_height),
                    "ocr_blocks": [box.to_dict() for box in self.boxes]
                }
            ]
        }



class BaseOCREngine(ABC):
    """Abstract base class for all land-record OCR engines."""

    @abstractmethod
    def initialize(self) -> None:
        """Loads and initializes model weights."""
        pass

    @abstractmethod
    def recognize(self, image: np.ndarray, document_id: str = "DOC_001") -> OCRResult:
        """
        Runs OCR recognition on an input image array.
        Returns a standardized OCRResult.
        """
        pass
