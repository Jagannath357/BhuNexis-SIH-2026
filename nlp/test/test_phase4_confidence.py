"""
test/test_phase4_confidence.py - Unit tests for Phase 4 (Confidence Engine & Quality Gate).

Validates:
1. Field risk profiles and weight constraints (sum to 1.0).
2. 4-Pillar composite scoring and ambiguity penalty multiplier.
3. Syntax evaluation across field types (Khata, Plot, Date, Area, Names).
4. Quality Gate routing (ACCEPTED vs REVIEW_REQUIRED).
5. Document-level gating decisions.
"""

import sys
from pathlib import Path
import pytest

NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from schemas.field_result import FieldResult, FieldStatus, FieldTier
from schemas.canonical_record import CanonicalRecord
from confidence.field_weights import get_field_profile, FIELD_RISK_PROFILES
from confidence.confidence_engine import ConfidenceEngine, ConfidenceScore
from confidence.quality_gate import QualityGate


class TestFieldRiskProfiles:
    """Tests risk profile configurations and weight constraints."""

    def test_all_profiles_sum_to_one(self):
        for name, profile in FIELD_RISK_PROFILES.items():
            total = profile.w_ocr + profile.w_model + profile.w_syntax + profile.w_spatial
            assert abs(total - 1.0) < 0.001, f"Profile {name} weights do not sum to 1.0"

    def test_tier_1_fields_have_strict_threshold(self):
        for name in ["plot_number", "khata_number", "mutation_number"]:
            profile = get_field_profile(name)
            assert profile.tier == FieldTier.TIER_1_IMMUTABLE
            assert profile.min_confidence_threshold >= 0.85


class TestConfidenceEngine:
    """Tests composite 4-pillar confidence calculation and ambiguity penalty."""

    def test_clean_plot_number_receives_high_confidence(self):
        label_box = [100.0, 500.0, 220.0, 530.0]
        val_box = [230.0, 500.0, 330.0, 530.0]

        score: ConfidenceScore = ConfidenceEngine.calculate_confidence(
            field_name="plot_number",
            raw_value="128/3",
            c_ocr=0.96,
            c_model=0.95,
            bbox_value=val_box,
            bbox_label=label_box
        )
        assert score.final_confidence >= 0.95
        assert score.ambiguity_penalty == 1.0
        assert score.is_ambiguous is False
        assert len(score.flags) == 0

    def test_ambiguous_plot_number_drops_confidence_sharply(self):
        label_box = [100.0, 500.0, 220.0, 530.0]
        val_box = [230.0, 500.0, 330.0, 530.0]

        # 382/l has 'l' instead of '1'
        score: ConfidenceScore = ConfidenceEngine.calculate_confidence(
            field_name="plot_number",
            raw_value="382/l",
            c_ocr=0.76,
            c_model=0.88,
            bbox_value=val_box,
            bbox_label=label_box
        )
        # Score must drop significantly below 0.85 threshold
        assert score.final_confidence <= 0.60
        assert score.ambiguity_penalty == 0.65
        assert score.is_ambiguous is True
        assert any("CHAR_CONFUSION_L" in f for f in score.flags)

    def test_syntax_evaluation(self):
        # Khata numbers
        assert ConfidenceEngine.evaluate_syntax("khata_number", "124") == 1.0
        assert ConfidenceEngine.evaluate_syntax("khata_number", "12@4") == 0.10

        # Plot numbers
        assert ConfidenceEngine.evaluate_syntax("plot_number", "128/3") == 1.0
        assert ConfidenceEngine.evaluate_syntax("plot_number", "128/3-A") == 0.85
        assert ConfidenceEngine.evaluate_syntax("plot_number", "invalid") == 0.10

        # Dates
        assert ConfidenceEngine.evaluate_syntax("document_date", "15/06/1998") == 1.0
        assert ConfidenceEngine.evaluate_syntax("document_date", "32/13/1998") == 0.0


class TestQualityGate:
    """Tests gatekeeper routing, candidate generation, and document status."""

    def test_clean_field_passes_gate(self):
        res: FieldResult = QualityGate.evaluate_field(
            field_name="khata_number",
            raw_value="45",
            c_ocr=0.98,
            c_model=0.96
        )
        assert res.status == FieldStatus.EXTRACTED
        assert res.raw_value == "45"
        assert res.normalized_value == "45"
        assert res.confidence >= 0.85

    def test_ambiguous_field_routes_to_review_required(self):
        res: FieldResult = QualityGate.evaluate_field(
            field_name="plot_number",
            raw_value="382/l",
            c_ocr=0.76,
            c_model=0.85
        )
        # RULE 2: normalized_value MUST be None
        assert res.status == FieldStatus.REVIEW_REQUIRED
        assert res.raw_value == "382/l"
        assert res.normalized_value is None
        # Must suggest candidate "382/1"
        assert res.candidate_value == "382/1"
        assert res.review_reason is not None

    def test_safe_date_normalized_by_gate(self):
        res: FieldResult = QualityGate.evaluate_field(
            field_name="document_date",
            raw_value="15/06/1998",
            c_ocr=0.95,
            c_model=0.90
        )
        assert res.status == FieldStatus.NORMALIZED
        assert res.raw_value == "15/06/1998"
        assert res.normalized_value == "1998-06-15"

    def test_document_quality_routing(self):
        record = CanonicalRecord(document_id="DOC_001", state="ODISHA")
        
        # Clean Khata
        record.khata_number = QualityGate.evaluate_field("khata_number", "45", 0.98, 0.96)
        # Ambiguous Plot
        record.plot_number = QualityGate.evaluate_field("plot_number", "382/l", 0.76, 0.85)

        evaluated_record = QualityGate.evaluate_document(record)

        # Whole document must be blocked for human review
        assert evaluated_record.needs_human_review is True
        assert evaluated_record.overall_status == FieldStatus.REVIEW_REQUIRED
        assert len(evaluated_record.review_reasons) >= 1
