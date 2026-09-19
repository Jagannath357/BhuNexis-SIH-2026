"""
schemas/field_result.py - Area 2, 3 & 4 Two-Track Data Contract.

Enforces Rule 1 (Tier Classification), Rule 2 (Two-Track Raw vs Candidate),
and Rule 5 (Code-Level Programmatic Guardrail against auto-normalizing high-risk fields).
"""

from enum import Enum
from typing import Optional, List, Any
from pydantic import BaseModel, Field, model_validator


class FieldStatus(str, Enum):
    """Lifecycle status of an extracted field."""
    EXTRACTED = "EXTRACTED"
    NORMALIZED = "NORMALIZED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    VERIFIED_BY_HUMAN = "VERIFIED_BY_HUMAN"
    NOT_FOUND = "NOT_FOUND"


class FieldTier(str, Enum):
    """
    Rule 1 Policy Tiers:
    - TIER_1_IMMUTABLE: Zero tolerance. Identifiers that must never be auto-modified (Plot, Khata, Mutation).
    - TIER_2_SAFE_NORMALIZABLE: Units, dates, whitespaces that can be mathematically/synthetically standardized.
    - TIER_3_ENTITY_LINGUISTIC: Owner names, locations where raw string is preserved alongside aliases.
    """
    TIER_1_IMMUTABLE = "TIER_1_IMMUTABLE"
    TIER_2_SAFE_NORMALIZABLE = "TIER_2_SAFE_NORMALIZABLE"
    TIER_3_ENTITY_LINGUISTIC = "TIER_3_ENTITY_LINGUISTIC"


class EvidenceSnippet(BaseModel):
    """Grounding provenance linking extracted value back to document coordinates."""
    page_number: int = Field(default=1, ge=1)
    bbox: List[float] = Field(..., description="Bounding box [x1, y1, x2, y2] enclosing the evidence")
    source_text: str = Field(..., description="Exact OCR text string from which this was extracted")
    ocr_confidence: float = Field(..., ge=0.0, le=1.0, description="OCR confidence of the source token(s)")


class FieldResult(BaseModel):
    """
    Rule 2: Two-Track representation of an extracted field.
    Preserves raw OCR evidence permanently while tracking candidates and normalization safely.
    """
    field_name: str = Field(..., description="Canonical field identifier (e.g. plot_number, khata_number)")
    tier: FieldTier = Field(..., description="Risk tier governing modification rules")
    
    # Track 1: Permanent, frozen raw OCR text
    raw_value: Optional[str] = Field(default=None, description="Exact, unaltered characters from OCR")
    
    # Track 2: Normalized representation (ONLY allowed for Tier 2 or Human-Verified Tier 1)
    normalized_value: Optional[Any] = Field(
        default=None, 
        description="Standardized value (e.g. ISO date, standard sq. meters). None if Tier 1 is ambiguous."
    )
    
    # Officer Suggestion (For display and 1-click confirmation ONLY)
    candidate_value: Optional[str] = Field(
        default=None, 
        description="Suggested correction (e.g. '382/1' for '382/l') to aid the officer"
    )
    
    status: FieldStatus = Field(default=FieldStatus.EXTRACTED, description="Current field lifecycle status")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Composite confidence score (0.0 to 1.0)")
    
    # Audit & Diagnostics
    flags: List[str] = Field(default_factory=list, description="Diagnostic flags (e.g. CHAR_CONFUSION_1_L, LOW_OCR_CONF)")
    review_reason: Optional[str] = Field(default=None, description="Human-readable reason if review is required")
    evidence: Optional[EvidenceSnippet] = Field(default=None, description="Spatial evidence grounding snippet")
    
    # Human-in-the-Loop Audit Trail
    verified_by: Optional[str] = Field(default=None, description="Officer ID who verified or edited this field")
    verified_at: Optional[str] = Field(default=None, description="ISO timestamp of human verification")

    @model_validator(mode="after")
    def enforce_rule_5_guardrail(self) -> "FieldResult":
        """
        Rule 5 Programmatic Guardrail:
        Strictly forbids code from altering characters in Tier 1 fields without Human Sign-off.
        """
        if self.tier == FieldTier.TIER_1_IMMUTABLE:
            # If normalized_value is provided and differs from raw_value:
            if self.normalized_value is not None and str(self.normalized_value).strip() != str(self.raw_value).strip():
                if self.status != FieldStatus.VERIFIED_BY_HUMAN:
                    raise ValueError(
                        f"SECURITY VIOLATION: Attempted to auto-normalize high-risk Tier 1 field '{self.field_name}' "
                        f"from raw '{self.raw_value}' to '{self.normalized_value}' without human verification! "
                        f"Status must be VERIFIED_BY_HUMAN, or use candidate_value instead."
                    )
        return self

    def to_officer_view(self) -> dict:
        """Returns a serialized view formatted for the Officer Verification UI."""
        return {
            "field_name": self.field_name,
            "tier": self.tier.value,
            "raw_value": self.raw_value,
            "normalized_value": self.normalized_value,
            "candidate_value": self.candidate_value,
            "status": self.status.value,
            "confidence_percentage": round(self.confidence * 100, 1),
            "flags": self.flags,
            "review_reason": self.review_reason,
            "evidence": self.evidence.model_dump() if self.evidence else None,
            "action_required": self.status == FieldStatus.REVIEW_REQUIRED
        }
