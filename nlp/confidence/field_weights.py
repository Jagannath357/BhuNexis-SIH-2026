"""
confidence/field_weights.py - Area 4 & Rule 1 (Field-Specific Risk Profiles & Weights).

Configures risk thresholds and mathematical pillar weights for every land-record field.
Tier 1 High-Risk fields have strict thresholds and heavy penalties.
"""

from dataclasses import dataclass
from typing import Dict
from schemas.field_result import FieldTier


@dataclass(frozen=True)
class FieldRiskProfile:
    """Configures weights and pass/review threshold for a specific land-record field."""
    field_name: str
    tier: FieldTier
    min_confidence_threshold: float  # Score below this triggers REVIEW_REQUIRED
    w_ocr: float                     # Pillar 1: OCR token quality weight
    w_model: float                   # Pillar 2: LayoutLM / Extractor probability weight
    w_syntax: float                  # Pillar 3: Format & legal pattern validity weight
    w_spatial: float                 # Pillar 4: Spatial proximity to label/column header weight

    def __post_init__(self):
        # Weights must sum to 1.0
        total_w = self.w_ocr + self.w_model + self.w_syntax + self.w_spatial
        if abs(total_w - 1.0) > 0.001:
            raise ValueError(f"Weights for field '{self.field_name}' must sum to 1.0, got {total_w}")


# Default Profiles per Field
FIELD_RISK_PROFILES: Dict[str, FieldRiskProfile] = {
    # -------------------------------------------------------------
    # TIER 1: HIGH-RISK IDENTIFIERS (Zero-Tolerance: Threshold 0.85)
    # -------------------------------------------------------------
    "plot_number": FieldRiskProfile(
        field_name="plot_number",
        tier=FieldTier.TIER_1_IMMUTABLE,
        min_confidence_threshold=0.85,
        w_ocr=0.25,
        w_model=0.35,
        w_syntax=0.25,
        w_spatial=0.15,
    ),
    "khata_number": FieldRiskProfile(
        field_name="khata_number",
        tier=FieldTier.TIER_1_IMMUTABLE,
        min_confidence_threshold=0.85,
        w_ocr=0.25,
        w_model=0.35,
        w_syntax=0.25,
        w_spatial=0.15,
    ),
    "mutation_number": FieldRiskProfile(
        field_name="mutation_number",
        tier=FieldTier.TIER_1_IMMUTABLE,
        min_confidence_threshold=0.85,
        w_ocr=0.25,
        w_model=0.35,
        w_syntax=0.25,
        w_spatial=0.15,
    ),
    "area_value": FieldRiskProfile(
        field_name="area_value",
        tier=FieldTier.TIER_1_IMMUTABLE,
        min_confidence_threshold=0.82,
        w_ocr=0.25,
        w_model=0.35,
        w_syntax=0.25,
        w_spatial=0.15,
    ),

    # -------------------------------------------------------------
    # TIER 2: SAFE STANDARDISABLE FIELDS (Threshold 0.75)
    # -------------------------------------------------------------
    "document_date": FieldRiskProfile(
        field_name="document_date",
        tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
        min_confidence_threshold=0.75,
        w_ocr=0.20,
        w_model=0.30,
        w_syntax=0.35,  # High weight on calendar validation
        w_spatial=0.15,
    ),
    "area_unit": FieldRiskProfile(
        field_name="area_unit",
        tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
        min_confidence_threshold=0.75,
        w_ocr=0.20,
        w_model=0.30,
        w_syntax=0.35,  # High weight on unit recognition
        w_spatial=0.15,
    ),
    "normalized_area_sqm": FieldRiskProfile(
        field_name="normalized_area_sqm",
        tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
        min_confidence_threshold=0.80,
        w_ocr=0.25,
        w_model=0.35,
        w_syntax=0.25,
        w_spatial=0.15,
    ),

    # -------------------------------------------------------------
    # TIER 3: ENTITY & LINGUISTIC FIELDS (Threshold 0.70)
    # -------------------------------------------------------------
    "owner_name": FieldRiskProfile(
        field_name="owner_name",
        tier=FieldTier.TIER_3_ENTITY_LINGUISTIC,
        min_confidence_threshold=0.70,
        w_ocr=0.25,
        w_model=0.45,  # High weight on SpaCy / NER probability
        w_syntax=0.15,
        w_spatial=0.15,
    ),
    "father_or_guardian_name": FieldRiskProfile(
        field_name="father_or_guardian_name",
        tier=FieldTier.TIER_3_ENTITY_LINGUISTIC,
        min_confidence_threshold=0.70,
        w_ocr=0.25,
        w_model=0.45,
        w_syntax=0.15,
        w_spatial=0.15,
    ),
    "village": FieldRiskProfile(
        field_name="village",
        tier=FieldTier.TIER_3_ENTITY_LINGUISTIC,
        min_confidence_threshold=0.70,
        w_ocr=0.25,
        w_model=0.45,
        w_syntax=0.15,
        w_spatial=0.15,
    ),
    "tehsil": FieldRiskProfile(
        field_name="tehsil",
        tier=FieldTier.TIER_3_ENTITY_LINGUISTIC,
        min_confidence_threshold=0.70,
        w_ocr=0.25,
        w_model=0.45,
        w_syntax=0.15,
        w_spatial=0.15,
    ),
    "district": FieldRiskProfile(
        field_name="district",
        tier=FieldTier.TIER_3_ENTITY_LINGUISTIC,
        min_confidence_threshold=0.70,
        w_ocr=0.25,
        w_model=0.45,
        w_syntax=0.15,
        w_spatial=0.15,
    ),
}


def get_field_profile(field_name: str) -> FieldRiskProfile:
    """Returns the risk profile for a canonical field, or a sensible Tier 2 default."""
    if field_name in FIELD_RISK_PROFILES:
        return FIELD_RISK_PROFILES[field_name]

    # Default fallback profile
    return FieldRiskProfile(
        field_name=field_name,
        tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
        min_confidence_threshold=0.75,
        w_ocr=0.25,
        w_model=0.35,
        w_syntax=0.25,
        w_spatial=0.15,
    )
