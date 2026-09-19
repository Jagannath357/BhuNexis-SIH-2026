"""
nlp package - BhuNexis Document Understanding & NLP Extraction Module.
"""

import sys
from pathlib import Path

# Ensure nlp root directory is in sys.path for clean submodule resolution
_NLP_ROOT = str(Path(__file__).resolve().parent)
if _NLP_ROOT not in sys.path:
    sys.path.insert(0, _NLP_ROOT)

from .pipeline import MasterNLPPipeline
from .schemas.ocr_contract import OCRDocument, OCRPage, OCRBlock
from .schemas.canonical_record import CanonicalRecord, STATE_TERMINOLOGY_MAP
from .schemas.field_result import FieldResult, FieldStatus, FieldTier, EvidenceSnippet

__all__ = [
    "MasterNLPPipeline",
    "OCRDocument",
    "OCRPage",
    "OCRBlock",
    "CanonicalRecord",
    "FieldResult",
    "FieldStatus",
    "FieldTier",
    "EvidenceSnippet",
    "STATE_TERMINOLOGY_MAP",
]
