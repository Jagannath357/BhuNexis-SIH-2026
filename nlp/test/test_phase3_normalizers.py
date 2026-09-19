"""
test/test_phase3_normalizers.py - Unit tests for Phase 3 (Normalization & Ambiguity Firewall).

Validates:
1. AmbiguityDetector character confusion matrix (0/O, 1/l, 2/Z, 5/S) and syntax firewall.
2. SafeNormalizer date standardizer (ISO 8601) and boundary checks.
3. SafeNormalizer area unit canonicalization and square meter conversions.
4. CandidateGenerator suggestions for human review.
"""

import sys
from pathlib import Path
import pytest

NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from normalizers.ambiguity_detector import AmbiguityDetector
from normalizers.safe_normalizer import SafeNormalizer
from normalizers.candidate_generator import CandidateGenerator


class TestAmbiguityDetector:
    """Tests Check 1 and Check 2 of the Ambiguity Firewall."""

    def test_detects_1_vs_l_confusion_in_parcel_id(self):
        report = AmbiguityDetector.analyze_identifier("382/l", field_type="parcel_id", ocr_confidence=0.92)
        assert report.is_ambiguous is True
        assert report.ambiguity_penalty == 0.65
        assert any("CHAR_CONFUSION_L" in flag for flag in report.flags)
        assert report.review_reason is not None
        assert "382/l" == report.raw_text

    def test_detects_0_vs_O_confusion_in_khata(self):
        report = AmbiguityDetector.analyze_identifier("4O5", field_type="khata_id", ocr_confidence=0.90)
        assert report.is_ambiguous is True
        assert any("CHAR_CONFUSION_O" in flag for flag in report.flags)
        assert report.ambiguity_penalty <= 0.80

    def test_clean_identifier_passes_without_penalty(self):
        report = AmbiguityDetector.analyze_identifier("128/3", field_type="parcel_id", ocr_confidence=0.98)
        assert report.is_ambiguous is False
        assert report.ambiguity_penalty == 1.0
        assert len(report.flags) == 0

    def test_low_ocr_confidence_triggers_flag(self):
        report = AmbiguityDetector.analyze_identifier("45", field_type="khata_id", ocr_confidence=0.74)
        assert report.is_ambiguous is True
        assert "LOW_OCR_CONFIDENCE" in report.flags
        assert report.ambiguity_penalty <= 0.85

    def test_khata_syntax_violation(self):
        report = AmbiguityDetector.analyze_identifier("12@4#", field_type="khata_id", ocr_confidence=0.95)
        assert report.has_syntax_violation is True
        assert "KHATA_NON_NUMERIC_SYNTAX" in report.flags


class TestSafeNormalizer:
    """Tests safe deterministic operations (Tier 2 and Tier 3)."""

    def test_normalize_valid_dates_to_iso(self):
        # DD/MM/YYYY
        assert SafeNormalizer.normalize_date("15/06/1998") == "1998-06-15"
        assert SafeNormalizer.normalize_date("15-06-1998") == "1998-06-15"
        # YYYY-MM-DD
        assert SafeNormalizer.normalize_date("1998-06-15") == "1998-06-15"
        # Textual month
        assert SafeNormalizer.normalize_date("15-Jun-1998") == "1998-06-15"
        assert SafeNormalizer.normalize_date("15th June 1998") == "1998-06-15"

    def test_rejects_invalid_or_impossible_dates(self):
        assert SafeNormalizer.normalize_date("32/13/1998") is None  # Day 32, Month 13
        assert SafeNormalizer.normalize_date("29/02/1999") is None  # Non-leap year Feb 29
        assert SafeNormalizer.normalize_date("15/06/2500") is None  # Far future

    def test_normalize_area_and_unit_conversion(self):
        # Acre conversion
        res_acre = SafeNormalizer.normalize_area("0.240 Acre")
        assert res_acre is not None
        assert res_acre["value"] == 0.24
        assert res_acre["unit"] == "acre"
        assert res_acre["sqm"] == 971.25

        # Hectare conversion
        res_hec = SafeNormalizer.normalize_area("2.5 Hectares")
        assert res_hec is not None
        assert res_hec["value"] == 2.5
        assert res_hec["unit"] == "hectare"
        assert res_hec["sqm"] == 25000.0

        # Decimal / Dismil conversion
        res_dec = SafeNormalizer.normalize_area("10 Decimals")
        assert res_dec is not None
        assert res_dec["value"] == 10.0
        assert res_dec["unit"] == "decimal"
        assert res_dec["sqm"] == 404.69

        # Guntha conversion
        res_guntha = SafeNormalizer.normalize_area("5 Guntha")
        assert res_guntha is not None
        assert res_guntha["value"] == 5.0
        assert res_guntha["unit"] == "guntha"
        assert res_guntha["sqm"] == 505.86

    def test_clean_person_name_with_honorific(self):
        name, honorific = SafeNormalizer.normalize_person_name("Late Kailash Chandra Sahu")
        assert name == "Kailash Chandra Sahu"
        assert honorific == "Late"

        name2, honorific2 = SafeNormalizer.normalize_person_name("Shri Ramesh  Sahu")
        assert name2 == "Ramesh Sahu"
        assert honorific2 == "Shri"


class TestCandidateGenerator:
    """Tests candidate suggestions for human review without silent overwriting."""

    def test_generates_plausible_candidates_for_ambiguous_plot(self):
        candidates = CandidateGenerator.generate_candidates("382/l", field_type="parcel_id")
        assert "382/1" in candidates
        assert len(candidates) >= 1
        # Raw value should not be in the alternatives list
        assert "382/l" not in candidates

    def test_generates_plausible_candidates_for_khata_o(self):
        candidates = CandidateGenerator.generate_candidates("4O5", field_type="khata_id")
        assert "405" in candidates

    def test_clean_value_returns_single_raw_candidate(self):
        candidates = CandidateGenerator.generate_candidates("128/3", field_type="parcel_id")
        assert candidates == ["128/3"]

    def test_generates_plausible_candidate_for_merged_slash_parcel(self):
        """Tests OCR error where slash was misread as 1 (e.g. 328/1 -> 32811)."""
        candidates = CandidateGenerator.generate_candidates("32811", field_type="plot_number")
        assert "328/1" in candidates

    def test_generates_plausible_candidate_for_digit_in_name(self):
        """Tests OCR error where letters 'oo' were misread as '00' (e.g. Sah00 -> Sahoo)."""
        candidates = CandidateGenerator.generate_candidates("Ramesh Chandra Sah00", field_type="owner_name")
        assert "Ramesh Chandra Sahoo" in candidates
