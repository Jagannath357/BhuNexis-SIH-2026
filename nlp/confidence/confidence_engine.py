"""
confidence/confidence_engine.py - Area 4 & Rule 3 (Multi-Pillar Confidence Scoring Engine).

Computes deterministic field-level confidence using the 4 objective pillars:
1. Base OCR quality (C_ocr)
2. Semantic / LayoutLM model assignment (C_model)
3. Syntactic & Legal Pattern conformance (S_syntax)
4. Spatial proximity to label/column header (S_spatial)
And applies the Ambiguity Penalty Multiplier (mu_ambiguity).
"""

import re
from typing import List, Optional
from dataclasses import dataclass, field

from .field_weights import get_field_profile, FieldRiskProfile
from normalizers.ambiguity_detector import AmbiguityDetector, AmbiguityReport
from normalizers.safe_normalizer import SafeNormalizer
from evidence.bbox_utils import calculate_spatial_proximity_score


@dataclass
class ConfidenceScore:
    """Detailed mathematical breakdown of an extraction confidence score."""
    field_name: str
    final_confidence: float     # (Raw Score * Ambiguity Penalty)
    raw_weighted_score: float   # Before ambiguity penalty
    c_ocr: float                # Pillar 1
    c_model: float              # Pillar 2
    s_syntax: float             # Pillar 3
    s_spatial: float            # Pillar 4
    ambiguity_penalty: float    # Multiplier (1.0 = none, 0.65 = severe)
    is_ambiguous: bool
    flags: List[str] = field(default_factory=list)
    review_reason: Optional[str] = None


class ConfidenceEngine:
    """Computes explainable, multi-factor confidence scores for extracted land records."""

    @classmethod
    def evaluate_syntax(cls, field_name: str, raw_value: str) -> float:
        """
        Pillar 3: Evaluates legal and syntactic conformance (0.0 to 1.0).
        """
        val = raw_value.strip()
        if not val:
            return 0.0

        if field_name == "khata_number":
            # Khata must be a positive integer
            if re.fullmatch(r"^\d+$", val):
                return 1.0
            elif re.search(r"[^0-9a-zA-Z\s]", val):  # contains special symbols like @, #, $
                return 0.10
            elif re.search(r"\d+", val):
                return 0.40
            return 0.10

        elif field_name in ("plot_number", "dag_number", "khasra_number", "survey_number"):
            # Plot numbers can be "382", "382/1", "128/3-A"
            if len(val) >= 5 and "/" not in val and val.isdigit():
                return 0.50  # Unusually large plot number, likely merged slash like 32811
            elif re.fullmatch(r"^\d+(?:/\d+)?$", val):
                return 1.0
            elif re.fullmatch(r"^\d+(?:/[0-9A-Za-z\-]+)?$", val):
                return 0.85
            elif re.search(r"\d+", val):
                return 0.40
            return 0.10

        elif field_name == "document_date":
            # Must parse as a valid calendar date
            parsed = SafeNormalizer.normalize_date(val)
            return 1.0 if parsed is not None else 0.0

        elif field_name in ("area_value", "area_unit"):
            parsed_area = SafeNormalizer.normalize_area(val)
            return 1.0 if parsed_area is not None else 0.20

        elif field_name in ("owner_name", "father_or_guardian_name", "village", "tehsil", "district"):
            # Entity names: should contain alphabets, no digits/special characters
            if re.search(r"\d", val):
                return 0.40  # Digits inside a person/village name is suspicious
            if len(val) >= 3:
                return 1.0
            return 0.60

        return 0.80

    @classmethod
    def calculate_confidence(
        cls,
        field_name: str,
        raw_value: str,
        c_ocr: float,
        c_model: float,
        bbox_value: Optional[List[float]] = None,
        bbox_label: Optional[List[float]] = None
    ) -> ConfidenceScore:
        """
        Calculates the complete composite confidence score for a field.
        
        Formula:
            Raw_Score = (w1 * C_ocr) + (w2 * C_model) + (w3 * S_syntax) + (w4 * S_spatial)
            Final_Confidence = Raw_Score * Ambiguity_Penalty
        """
        profile: FieldRiskProfile = get_field_profile(field_name)

        # 1. Pillar 1: OCR Base Signal
        c_ocr_clamped = max(0.0, min(1.0, float(c_ocr)))

        # 2. Pillar 2: Model Semantic Probability
        c_model_clamped = max(0.0, min(1.0, float(c_model)))

        # 3. Pillar 3: Syntax Conformance
        s_syntax = cls.evaluate_syntax(field_name, raw_value)

        # 4. Pillar 4: Spatial Proximity
        if bbox_value is not None:
            s_spatial = calculate_spatial_proximity_score(bbox_label, bbox_value)
        else:
            s_spatial = 0.70  # Neutral baseline if bbox unavailable

        # Raw Weighted Score (0.0 to 1.0)
        raw_score = (
            (profile.w_ocr * c_ocr_clamped) +
            (profile.w_model * c_model_clamped) +
            (profile.w_syntax * s_syntax) +
            (profile.w_spatial * s_spatial)
        )

        # 5. Ambiguity Firewall Analysis (Checks for '1 ↔ l', '0 ↔ O', etc.)
        ambiguity_rep: AmbiguityReport = AmbiguityDetector.analyze_identifier(
            raw_value, 
            field_type=field_name, 
            ocr_confidence=c_ocr_clamped
        )

        # Apply Ambiguity Penalty Multiplier
        final_conf = raw_score * ambiguity_rep.ambiguity_penalty
        final_conf = round(max(0.0, min(1.0, final_conf)), 3)

        return ConfidenceScore(
            field_name=field_name,
            final_confidence=final_conf,
            raw_weighted_score=round(raw_score, 3),
            c_ocr=round(c_ocr_clamped, 3),
            c_model=round(c_model_clamped, 3),
            s_syntax=round(s_syntax, 3),
            s_spatial=round(s_spatial, 3),
            ambiguity_penalty=ambiguity_rep.ambiguity_penalty,
            is_ambiguous=ambiguity_rep.is_ambiguous,
            flags=ambiguity_rep.flags,
            review_reason=ambiguity_rep.review_reason
        )
