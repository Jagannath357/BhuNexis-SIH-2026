"""
confidence/quality_gate.py - Area 4, Area 6 & Rule 3 (The Quality Gatekeeper).

Evaluates field confidences, enforces the Ambiguity Firewall, generates candidates,
and routes records to either downstream validation or the Officer Review Queue.
"""

from typing import Optional, List, Any
from schemas.field_result import FieldResult, FieldStatus, FieldTier, EvidenceSnippet
from schemas.canonical_record import CanonicalRecord
from .field_weights import get_field_profile, FieldRiskProfile
from .confidence_engine import ConfidenceEngine, ConfidenceScore
from normalizers.candidate_generator import CandidateGenerator
from normalizers.safe_normalizer import SafeNormalizer


class QualityGate:
    """The Quality Gatekeeper enforcing Rule 1, Rule 2, and Rule 3."""

    @classmethod
    def evaluate_field(
        cls,
        field_name: str,
        raw_value: str,
        c_ocr: float,
        c_model: float,
        bbox_value: Optional[List[float]] = None,
        bbox_label: Optional[List[float]] = None,
        evidence: Optional[Any] = None
    ) -> FieldResult:
        """
        Runs the 4-pillar confidence engine, executes the Ambiguity Firewall,
        and produces a strictly validated FieldResult.
        """
        profile: FieldRiskProfile = get_field_profile(field_name)

        # 1. Compute multi-factor confidence score
        score: ConfidenceScore = ConfidenceEngine.calculate_confidence(
            field_name=field_name,
            raw_value=raw_value,
            c_ocr=c_ocr,
            c_model=c_model,
            bbox_value=bbox_value,
            bbox_label=bbox_label
        )

        # 2. Ambiguity & Threshold Gating Decision
        below_threshold = score.final_confidence < profile.min_confidence_threshold
        triggers_review = score.is_ambiguous or below_threshold

        if triggers_review:
            # RULE 2 & 3: Ambiguous fields generate suggested candidate for officer UI
            candidate_val: Optional[str] = None
            if profile.tier in (FieldTier.TIER_1_IMMUTABLE, FieldTier.TIER_3_ENTITY_LINGUISTIC):
                candidates = CandidateGenerator.generate_candidates(raw_value, field_type=field_name)
                candidate_val = candidates[0] if candidates else None

            reason = score.review_reason
            if not reason and below_threshold:
                reason = (
                    f"Confidence ({round(score.final_confidence*100, 1)}%) "
                    f"is below mandatory threshold ({round(profile.min_confidence_threshold*100, 1)}%)."
                )

            return FieldResult(
                field_name=field_name,
                tier=profile.tier,
                raw_value=raw_value.strip(),
                normalized_value=None,  # Frozen! Never auto-modified
                candidate_value=candidate_val,
                status=FieldStatus.REVIEW_REQUIRED,
                confidence=score.final_confidence,
                flags=score.flags,
                review_reason=reason,
                evidence=evidence
            )

        # 3. Clean Field Passed All Checks
        if profile.tier == FieldTier.TIER_1_IMMUTABLE:
            # Clean Tier 1 identifier: raw matches normalized
            return FieldResult(
                field_name=field_name,
                tier=profile.tier,
                raw_value=raw_value.strip(),
                normalized_value=raw_value.strip(),
                status=FieldStatus.EXTRACTED,
                confidence=score.final_confidence,
                flags=score.flags,
                evidence=evidence
            )
        elif profile.tier == FieldTier.TIER_2_SAFE_NORMALIZABLE:
            # Safe Tier 2 field: run SafeNormalizer
            norm_val = raw_value.strip()
            if field_name == "document_date":
                norm_val = SafeNormalizer.normalize_date(raw_value) or raw_value.strip()
            elif field_name in ("area_value", "area_unit"):
                area_dict = SafeNormalizer.normalize_area(raw_value)
                if area_dict:
                    norm_val = area_dict["value"] if field_name == "area_value" else area_dict["unit"]

            return FieldResult(
                field_name=field_name,
                tier=profile.tier,
                raw_value=raw_value.strip(),
                normalized_value=norm_val,
                status=FieldStatus.NORMALIZED,
                confidence=score.final_confidence,
                flags=score.flags,
                evidence=evidence
            )
        else:
            # Tier 3 Entity: clean name
            clean_name, _ = SafeNormalizer.normalize_person_name(raw_value)
            return FieldResult(
                field_name=field_name,
                tier=profile.tier,
                raw_value=raw_value.strip(),
                normalized_value=clean_name or raw_value.strip(),
                status=FieldStatus.EXTRACTED,
                confidence=score.final_confidence,
                flags=score.flags,
                evidence=evidence
            )

    @classmethod
    def evaluate_document(cls, record: CanonicalRecord) -> CanonicalRecord:
        """
        Evaluates document-level status across all extracted fields.
        Routes to RELIABLE downstream validation or REVIEW_REQUIRED officer queue.
        """
        record.update_quality_status(min_tier1_confidence=0.85)
        return record
