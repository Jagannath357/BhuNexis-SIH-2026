"""
schemas package - Data contracts for OCR, Canonical Records, and Field Results.
"""

from .ocr_contract import OCRDocument, OCRPage, OCRBlock
from .field_result import FieldResult, FieldStatus, FieldTier, EvidenceSnippet
from .canonical_record import CanonicalRecord, STATE_TERMINOLOGY_MAP

__all__ = [
    "OCRDocument",
    "OCRPage",
    "OCRBlock",
    "FieldResult",
    "FieldStatus",
    "FieldTier",
    "EvidenceSnippet",
    "CanonicalRecord",
    "STATE_TERMINOLOGY_MAP",
]
