"""
test/test_phase1_schemas.py - Unit tests for Phase 1 (Schemas & Contracts).

Validates:
1. Ingestion of real OCR fixtures (English, Edge-Cases, Multilingual, Tables).
2. Field-level Two-Track schema behavior.
3. Rule 5 Programmatic Security Guardrail against auto-normalizing Tier 1 fields.
4. Human verification handshake.
5. Canonical record quality status gating and state terminology resolution.
"""

import json
import sys
from pathlib import Path
import pytest

# Ensure nlp module root is in sys.path
NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from schemas.ocr_contract import OCRDocument, OCRPage, OCRBlock
from schemas.field_result import FieldResult, FieldStatus, FieldTier, EvidenceSnippet
from schemas.canonical_record import CanonicalRecord, STATE_TERMINOLOGY_MAP

FIXTURES_DIR = NLP_ROOT / "fixtures"


class TestOCRContract:
    """Tests the OCR input contract schema against fixture payloads."""

    def test_load_english_sample_fixture(self):
        with open(FIXTURES_DIR / "english_sample.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        doc = OCRDocument.model_validate(data)
        assert doc.document_id == "DOC_001"
        assert len(doc.pages) == 1
        page = doc.pages[0]
        assert len(page.ocr_blocks) == 10
        assert doc.average_confidence > 0.90
        assert "Ramesh Chandra Sahu" in page.get_full_text()

    def test_load_all_multilingual_and_edge_fixtures(self):
        fixture_files = ["edge_cases.json", "hindi_sample.json", "odia_sample.json", "table_sample.json"]
        for fname in fixture_files:
            file_path = FIXTURES_DIR / fname
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                doc = OCRDocument.model_validate(data)
                assert doc.document_id.startswith("DOC_")
                assert len(doc.pages) >= 1
                assert doc.total_blocks > 0

    def test_ocr_block_bbox_validation(self):
        # Valid bbox [x1, y1, x2, y2]
        block = OCRBlock(text="Khata 45", bbox=[100.0, 200.0, 300.0, 250.0], confidence=0.95)
        assert block.width == 200.0
        assert block.height == 50.0

        # Invalid: len != 4
        with pytest.raises(ValueError, match="Bounding box must contain exactly 4 coordinates"):
            OCRBlock(text="Invalid", bbox=[100.0, 200.0, 300.0], confidence=0.95)

        # Invalid: x1 > x2
        with pytest.raises(ValueError, match="Invalid horizontal coordinates"):
            OCRBlock(text="Invalid", bbox=[400.0, 200.0, 300.0, 250.0], confidence=0.95)


class TestFieldResultAndRule5Guardrail:
    """Tests FieldResult two-track logic and Rule 5 security guardrails."""

    def test_clean_tier_1_field_accepted(self):
        """Clean Tier 1 identifier where raw_value equals normalized_value."""
        field = FieldResult(
            field_name="khata_number",
            tier=FieldTier.TIER_1_IMMUTABLE,
            raw_value="124",
            normalized_value="124",
            status=FieldStatus.EXTRACTED,
            confidence=0.98
        )
        assert field.raw_value == "124"
        assert field.normalized_value == "124"
        assert field.status == FieldStatus.EXTRACTED

    def test_rule_5_guardrail_prevents_auto_normalization_of_tier_1(self):
        """
        RULE 5 GUARDRAIL:
        Code is strictly forbidden from auto-normalizing a high-risk Tier 1 field (e.g. 382/l -> 382/1)
        unless status is VERIFIED_BY_HUMAN.
        """
        with pytest.raises(ValueError, match="SECURITY VIOLATION"):
            FieldResult(
                field_name="plot_number",
                tier=FieldTier.TIER_1_IMMUTABLE,
                raw_value="382/l",
                normalized_value="382/1",  # Attempted silent auto-correction!
                status=FieldStatus.EXTRACTED,
                confidence=0.90
            )

    def test_rule_2_proper_way_to_handle_ambiguous_tier_1(self):
        """
        RULE 2:
        Ambiguous Tier 1 field must keep normalized_value=None and suggest candidate_value instead.
        """
        field = FieldResult(
            field_name="plot_number",
            tier=FieldTier.TIER_1_IMMUTABLE,
            raw_value="382/l",
            normalized_value=None,  # Left NULL!
            candidate_value="382/1",  # Candidate for officer display
            status=FieldStatus.REVIEW_REQUIRED,
            flags=["CHAR_CONFUSION_1_L"],
            confidence=0.65,
            review_reason="Ambiguous character 'l' in plot number position."
        )
        assert field.raw_value == "382/l"
        assert field.normalized_value is None
        assert field.candidate_value == "382/1"
        assert field.status == FieldStatus.REVIEW_REQUIRED

    def test_tier_2_safe_normalization_allowed(self):
        """Tier 2 fields (e.g. unit/date) can be auto-normalized safely."""
        field = FieldResult(
            field_name="document_date",
            tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
            raw_value="15/06/1998",
            normalized_value="1998-06-15",
            status=FieldStatus.NORMALIZED,
            confidence=0.95
        )
        assert field.normalized_value == "1998-06-15"

    def test_rule_4_human_verification_handshake(self):
        """Officer sign-off allows updating normalized_value with audit trail."""
        field = FieldResult(
            field_name="plot_number",
            tier=FieldTier.TIER_1_IMMUTABLE,
            raw_value="382/l",
            normalized_value="382/1",  # Officer confirmed candidate
            candidate_value="382/1",
            status=FieldStatus.VERIFIED_BY_HUMAN,
            verified_by="OFFICER_PATNAIK_042",
            verified_at="2026-09-18T17:30:00Z",
            confidence=1.0
        )
        assert field.status == FieldStatus.VERIFIED_BY_HUMAN
        assert field.normalized_value == "382/1"
        assert field.verified_by == "OFFICER_PATNAIK_042"


class TestCanonicalRecord:
    """Tests CanonicalRecord consolidation, terminology mapping, and quality status."""

    def test_state_terminology_mapping(self):
        assert STATE_TERMINOLOGY_MAP["dag"] == "plot_number"
        assert STATE_TERMINOLOGY_MAP["khasra"] == "plot_number"
        assert STATE_TERMINOLOGY_MAP["khatian"] == "khata_number"
        assert STATE_TERMINOLOGY_MAP["pattadar"] == "owner_name"
        assert STATE_TERMINOLOGY_MAP["mouza"] == "village"
        assert STATE_TERMINOLOGY_MAP["tahasil"] == "tehsil"

    def test_canonical_record_quality_gating(self):
        record = CanonicalRecord(document_id="DOC_001", state="ODISHA")
        
        # Add clean Khata
        record.khata_number = FieldResult(
            field_name="khata_number",
            tier=FieldTier.TIER_1_IMMUTABLE,
            raw_value="45",
            normalized_value="45",
            status=FieldStatus.EXTRACTED,
            confidence=0.98
        )
        
        # Add ambiguous Plot number
        record.plot_number = FieldResult(
            field_name="plot_number",
            tier=FieldTier.TIER_1_IMMUTABLE,
            raw_value="128/l",
            normalized_value=None,
            candidate_value="128/1",
            status=FieldStatus.REVIEW_REQUIRED,
            confidence=0.60,
            review_reason="Ambiguous character 'l' in plot number."
        )

        record.update_quality_status(min_tier1_confidence=0.85)

        # Record MUST require human review because Plot is REVIEW_REQUIRED and confidence < 0.85
        assert record.needs_human_review is True
        assert record.overall_status == FieldStatus.REVIEW_REQUIRED
        assert len(record.review_reasons) > 0

        officer_view = record.to_officer_payload()
        assert officer_view["needs_human_review"] is True
        assert "plot_number" in officer_view["fields"]
        assert officer_view["fields"]["plot_number"]["action_required"] is True
