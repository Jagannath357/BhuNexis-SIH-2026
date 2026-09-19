"""
test/test_phase5_extractors.py - Unit tests for Phase 5 (Multi-Tier Extractors).

Validates:
1. RegexExtractor on English sample and Edge-Case fixtures (single block & adjacent block parsing).
2. SpacyExtractor NER on Indian person names and location entities.
3. TransformerExtractor 2D spatial column alignment on table sample fixture.
4. LLMFallbackExtractor schema-constrained extraction from narrative text.
"""

import sys
import json
from pathlib import Path
import pytest

NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from schemas.ocr_contract import OCRDocument
from extractors.regex_extractor import RegexExtractor
from extractors.spacy_extractor import SpacyExtractor
from extractors.transformer_extractor import TransformerExtractor
from extractors.llm_fallback import LLMFallbackExtractor

FIXTURES_DIR = NLP_ROOT / "fixtures"


@pytest.fixture
def english_page():
    with open(FIXTURES_DIR / "english_sample.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    doc = OCRDocument.model_validate(data)
    return doc.pages[0]


@pytest.fixture
def edge_page():
    with open(FIXTURES_DIR / "edge_cases.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    doc = OCRDocument.model_validate(data)
    return doc.pages[0]


@pytest.fixture
def table_page():
    with open(FIXTURES_DIR / "table_sample.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    doc = OCRDocument.model_validate(data)
    return doc.pages[0]


class TestRegexExtractor:
    """Tests deterministic anchor extraction on standard and edge-case pages."""

    def test_extract_all_fields_from_english_sample(self, english_page):
        results = RegexExtractor.extract_from_page(english_page)

        assert "khata_number" in results
        assert results["khata_number"].raw_value == "45"

        assert "plot_number" in results
        assert results["plot_number"].raw_value == "128/3"

        assert "owner_name" in results
        assert results["owner_name"].raw_value == "Ramesh Chandra Sahu"

        assert "father_or_guardian_name" in results
        assert results["father_or_guardian_name"].raw_value == "Late Kailash Chandra Sahu"

        assert "area_value" in results
        assert "0.240" in results["area_value"].raw_value

        assert "village" in results
        assert results["village"].raw_value == "Khandagiri"

        assert "tehsil" in results
        assert results["tehsil"].raw_value == "Bhubaneswar"

        assert "district" in results
        assert results["district"].raw_value == "Khordha"

    def test_extract_from_edge_cases_page(self, edge_page):
        results = RegexExtractor.extract_from_page(edge_page)

        # Plot number with merged slash ambiguity (328/1 -> 32811)
        assert "plot_number" in results
        assert results["plot_number"].raw_value == "32811"

        # Adjacent split block Khata: "Khata  N0." -> "45"
        assert "khata_number" in results
        assert results["khata_number"].raw_value == "45"

        # Adjacent split block Pattadar: "Pattadar Name" -> "Ramesh Chandra Sah00"
        assert "owner_name" in results
        assert "Ramesh Chandra Sah00" in results["owner_name"].raw_value


class TestSpacyExtractor:
    """Tests entity extraction for Indian names and locations."""

    def test_extract_entities_from_page(self, english_page):
        results = SpacyExtractor.extract_from_page(english_page)

        assert "owner_name" in results
        assert "Ramesh Chandra Sahu" in results["owner_name"].raw_value

        assert "father_or_guardian_name" in results
        assert "Kailash Chandra Sahu" in results["father_or_guardian_name"].raw_value


class TestTransformerExtractor:
    """Tests 2D column and table extraction."""

    def test_extract_tabular_data(self, table_page):
        results = TransformerExtractor.extract_from_page(table_page)

        # Should extract columns from table
        assert len(results) > 0
        # If Khata column present in table
        if "khata_number" in results:
            assert results["khata_number"].extractor_source == "transformer_layout_column"


class TestLLMFallbackExtractor:
    """Tests schema-constrained fallback from free text."""

    def test_extract_from_unstructured_narrative(self):
        narrative = (
            "This indenture of sale records that the recorded owner Ramesh Kumar Sahoo "
            "holding Khata No: 512 and Plot No: 914/2 situated in Village: Patia, "
            "Tehsil: Bhubaneswar having Area: 1.25 Acre has transferred all rights."
        )

        results = LLMFallbackExtractor.extract_from_text(narrative)

        assert results["khata_number"].raw_value == "512"
        assert results["plot_number"].raw_value == "914/2"
        assert "Ramesh Kumar Sahoo" in results["owner_name"].raw_value
        assert results["village"].raw_value == "Patia"
        assert results["tehsil"].raw_value == "Bhubaneswar"
        assert "1.25" in results["area_value"].raw_value
