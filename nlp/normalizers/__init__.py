"""
normalizers package - Ambiguity detection, safe normalization, and candidate generation.
"""

from .ambiguity_detector import AmbiguityDetector, AmbiguityReport, OCR_CONFUSION_MATRIX
from .safe_normalizer import SafeNormalizer, AREA_UNIT_TO_SQM, UNIT_ALIAS_MAP
from .candidate_generator import CandidateGenerator

__all__ = [
    "AmbiguityDetector",
    "AmbiguityReport",
    "OCR_CONFUSION_MATRIX",
    "SafeNormalizer",
    "AREA_UNIT_TO_SQM",
    "UNIT_ALIAS_MAP",
    "CandidateGenerator",
]
