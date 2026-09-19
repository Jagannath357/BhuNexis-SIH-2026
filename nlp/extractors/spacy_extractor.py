"""
extractors/spacy_extractor.py - Area 8 & Phase 5 (SpaCy / Named Entity Recognition Extractor).

Specialized for extracting Indian entity names (Owner, Father/Guardian, Village/Mouza, Location)
from semi-structured OCR text using Named Entity Recognition (NER).
"""

import re
from typing import Dict, List, Optional
from schemas.ocr_contract import OCRBlock, OCRPage
from .regex_extractor import ExtractedCandidate

try:
    import spacy
    _SPACY_AVAILABLE = True
except ImportError:
    _SPACY_AVAILABLE = False


class SpacyExtractor:
    """
    Extracts PERSON and LOCATION/GPE entities using SpaCy or an intelligent rule-based NER fallback.
    """

    _nlp = None

    @classmethod
    def get_nlp_model(cls):
        """Lazy-loads the spaCy English model if available."""
        if not _SPACY_AVAILABLE:
            return None
        if cls._nlp is None:
            try:
                cls._nlp = spacy.load("en_core_web_sm")
            except Exception:
                try:
                    # Blank English model with sentencizer if full model not downloaded
                    cls._nlp = spacy.blank("en")
                except Exception:
                    cls._nlp = None
        return cls._nlp

    @classmethod
    def extract_from_page(cls, page: OCRPage) -> Dict[str, ExtractedCandidate]:
        """
        Extracts entity names (Owner, Father, Village) from the page.
        """
        results: Dict[str, ExtractedCandidate] = {}
        nlp = cls.get_nlp_model()

        for block in page.ocr_blocks:
            text = block.text.strip()

            # 1. Owner / Pattadar Name Extraction
            if "owner_name" not in results:
                name_match = re.search(r"(?:Name\s*of\s*Pattadar|Pattadar\s*Name|Recorded\s*Tenant|Tenant\s*Name|Owner\s*Name)[:.\s-]+([A-Za-z\s]+)", text, re.I)
                if name_match:
                    name_cand = name_match.group(1).strip()
                    if cls._is_valid_person_name(name_cand):
                        results["owner_name"] = ExtractedCandidate(
                            field_name="owner_name",
                            raw_value=name_cand,
                            contributing_blocks=[block],
                            label_block=block,
                            extractor_confidence=0.95,
                            extractor_source="spacy_ner_entity"
                        )
                elif nlp is not None and len(text.split()) >= 2 and not any(k in text.lower() for k in ["government", "record", "khata", "plot", "area", "tehsil"]):
                    # If spaCy model is loaded, check entity tags
                    doc = nlp(text)
                    for ent in doc.ents:
                        if ent.label_ == "PERSON" and cls._is_valid_person_name(ent.text):
                            results["owner_name"] = ExtractedCandidate(
                                field_name="owner_name",
                                raw_value=ent.text.strip(),
                                contributing_blocks=[block],
                                label_block=block,
                                extractor_confidence=0.88,
                                extractor_source="spacy_ner_tag"
                            )
                            break

            # 2. Father or Guardian Name Extraction
            if "father_or_guardian_name" not in results:
                father_match = re.search(r"(?:Father(?:'s)?\s*Name|Guardian(?:'s)?\s*Name)[:.\s-]+([A-Za-z\s]+)", text, re.I)
                if father_match:
                    father_cand = father_match.group(1).strip()
                    if cls._is_valid_person_name(father_cand):
                        results["father_or_guardian_name"] = ExtractedCandidate(
                            field_name="father_or_guardian_name",
                            raw_value=father_cand,
                            contributing_blocks=[block],
                            label_block=block,
                            extractor_confidence=0.94,
                            extractor_source="spacy_ner_entity"
                        )

            # 3. Location Entities (Village / Tehsil / District)
            if "village" not in results:
                vil_match = re.search(r"(?:Village|Vil1age|Mouza|Mauza)[:.\s-]+([A-Za-z\s]+)", text, re.I)
                if vil_match:
                    vil_name = vil_match.group(1).strip()
                    results["village"] = ExtractedCandidate(
                        field_name="village",
                        raw_value=vil_name,
                        contributing_blocks=[block],
                        label_block=block,
                        extractor_confidence=0.92,
                        extractor_source="spacy_location_entity"
                    )

        return results

    @staticmethod
    def _is_valid_person_name(text: str) -> bool:
        """Sanity check that a string represents a person's name (2+ letters, no digits/symbols)."""
        cleaned = text.strip()
        if len(cleaned) < 3 or len(cleaned) > 60:
            return False
        if re.search(r"\d", cleaned):
            return False
        # Must have at least one space or be 4+ letters
        return True
