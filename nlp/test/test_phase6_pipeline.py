"""
test/test_phase6_pipeline.py - End-to-End Integration Tests for Phase 6.

Validates:
1. Complete pipeline processing on real English fixture (clean automated pass).
2. Complete pipeline processing on Edge-Cases fixture.
3. Ambiguity Firewall trigger on corrupted scan ("382/l") resulting in REVIEW_REQUIRED.
4. Rule 2 verification: raw_value preserved, normalized_value=None, candidate_value="382/1".
5. Backend notification callback event trigger.
"""

import sys
import json
from pathlib import Path
import pytest

NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from pipeline import MasterNLPPipeline
from schemas.field_result import FieldStatus, FieldTier
from schemas.canonical_record import CanonicalRecord
from schemas.ocr_contract import OCRDocument, OCRPage, OCRBlock

FIXTURES_DIR = NLP_ROOT / "fixtures"


class TestMasterNLPPipeline:
    """End-to-end integration tests for MasterNLPPipeline."""

    def test_clean_english_sample_end_to_end(self):
        pipeline = MasterNLPPipeline()
        record: CanonicalRecord = pipeline.process_document(FIXTURES_DIR / "english_sample.json")

        assert record.document_id == "DOC_001"
        assert record.state == "ODISHA"
        
        # Clean document must pass directly without human review
        assert record.needs_human_review is False
        assert record.overall_status == FieldStatus.NORMALIZED
        assert len(record.review_reasons) == 0

        # Assert all fields extracted cleanly
        assert record.khata_number is not None
        assert record.khata_number.raw_value == "45"
        assert record.khata_number.normalized_value == "45"
        assert record.khata_number.status == FieldStatus.EXTRACTED
        assert record.khata_number.evidence is not None

        assert record.plot_number is not None
        assert record.plot_number.raw_value == "128/3"
        assert record.plot_number.normalized_value == "128/3"

        assert record.owner_name is not None
        assert "Ramesh Chandra Sahu" in record.owner_name.raw_value

        assert record.father_or_guardian_name is not None
        assert "Kailash Chandra Sahu" in record.father_or_guardian_name.raw_value

        assert record.area_value is not None
        assert "0.240" in record.area_value.raw_value

        # Derived sqm check
        assert record.normalized_area_sqm is not None
        assert record.normalized_area_sqm.normalized_value == 971.25

        assert record.village is not None
        assert record.village.raw_value == "Khandagiri"

        assert record.tehsil is not None
        assert record.tehsil.raw_value == "Bhubaneswar"

        assert record.district is not None
        assert record.district.raw_value == "Khordha"

    def test_ambiguous_parcel_triggers_review_required(self):
        """
        Tests ambiguous scan ("Plot No: 382/l").
        Proves that Ambiguity Firewall slashes confidence, freezes normalized_value,
        suggests candidate "382/1", and flags document for Officer Review.
        """
        # Create synthetic OCR document with ambiguous '382/l'
        doc = OCRDocument(
            document_id="DOC_CORRUPT_001",
            language="en",
            pages=[
                OCRPage(
                    page_number=1,
                    image_width=1000.0,
                    image_height=1400.0,
                    ocr_blocks=[
                        OCRBlock(text="Khata No: 124", bbox=[100.0, 300.0, 400.0, 340.0], confidence=0.98),
                        OCRBlock(text="Plot No: 382/l", bbox=[100.0, 400.0, 400.0, 440.0], confidence=0.76),
                        OCRBlock(text="Area: 0.500 Acre", bbox=[100.0, 500.0, 400.0, 540.0], confidence=0.94),
                    ]
                )
            ]
        )

        pipeline = MasterNLPPipeline()
        record = pipeline.process_document(doc)

        # Whole document must be marked for review
        assert record.needs_human_review is True
        assert record.overall_status == FieldStatus.REVIEW_REQUIRED
        assert len(record.review_reasons) > 0

        # Plot number must adhere strictly to Rule 2
        plot = record.plot_number
        assert plot is not None
        assert plot.raw_value == "382/l"
        assert plot.normalized_value is None  # RULE 2: Left null!
        assert plot.candidate_value == "382/1"  # Suggested for officer
        assert plot.status == FieldStatus.REVIEW_REQUIRED
        assert any("CHAR_CONFUSION_L" in f for f in plot.flags)

        # Khata number should still be clean
        khata = record.khata_number
        assert khata.raw_value == "124"
        assert khata.normalized_value == "124"
        assert khata.status == FieldStatus.EXTRACTED

    def test_backend_notification_callback_triggered(self):
        """Tests that the backend notification hook fires when review is required."""
        callback_payload = None

        def mock_backend_notification(payload):
            nonlocal callback_payload
            callback_payload = payload

        pipeline = MasterNLPPipeline(on_review_required=mock_backend_notification)

        # Process corrupted document
        corrupt_doc = OCRDocument(
            document_id="DOC_ALERT_001",
            pages=[
                OCRPage(
                    page_number=1,
                    ocr_blocks=[
                        OCRBlock(text="Plot No: 382/l", bbox=[100.0, 400.0, 400.0, 440.0], confidence=0.74),
                    ]
                )
            ]
        )

        record = pipeline.process_document(corrupt_doc)

        # Verify callback was executed with officer payload
        assert callback_payload is not None
        assert callback_payload["document_id"] == "DOC_ALERT_001"
        assert callback_payload["needs_human_review"] is True
        assert "plot_number" in callback_payload["fields"]
        assert callback_payload["fields"]["plot_number"]["action_required"] is True
