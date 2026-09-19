"""
normalizers/ambiguity_detector.py - Area 3 & Rule 3 (Ambiguity Firewall: Check 1 & Check 2).

Detects character confusions ('0 ↔ O', '1 ↔ I ↔ l', '2 ↔ Z', '5 ↔ S', '8 ↔ B')
in high-risk identifiers without performing silent auto-corrections.
"""

import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field


# Known OCR confusion mappings (character -> plausible alternatives)
OCR_CONFUSION_MATRIX: Dict[str, List[str]] = {
    "l": ["1", "I", "|"],
    "I": ["1", "l", "|"],
    "1": ["l", "I", "|"],
    "O": ["0", "Q", "D"],
    "o": ["0"],
    "0": ["O", "o", "D"],
    "S": ["5"],
    "s": ["5"],
    "5": ["S", "s"],
    "Z": ["2"],
    "z": ["2"],
    "2": ["Z", "z"],
    "B": ["8"],
    "8": ["B"],
    "G": ["6"],
    "6": ["G"],
}

# Letters frequently mistaken for numbers when appearing in numeric parcel positions
NUMERIC_MISTAKEN_LETTERS: Set[str] = {"l", "I", "O", "o", "S", "s", "Z", "z", "B", "G"}

# Digits frequently mistaken for letters when appearing in linguistic entity positions (e.g. Sah00)
ENTITY_MISTAKEN_DIGITS: Dict[str, List[str]] = {
    "0": ["o", "O"],
    "1": ["l", "I"],
    "2": ["z", "Z"],
    "5": ["s", "S"],
    "8": ["B"],
}


@dataclass
class AmbiguityReport:
    """Diagnostic report output by AmbiguityDetector."""
    raw_text: str
    is_ambiguous: bool
    has_syntax_violation: bool
    confused_positions: Dict[int, Tuple[str, List[str]]] = field(default_factory=dict)
    flags: List[str] = field(default_factory=list)
    ambiguity_penalty: float = 1.0  # 1.0 = no penalty, <1.0 = penalty multiplier
    review_reason: Optional[str] = None


class AmbiguityDetector:
    """
    Deterministic Ambiguity Firewall:
    Scans extracted tokens for OCR optical confusions and syntax deviations.
    """

    @classmethod
    def analyze_identifier(
        cls, 
        text: str, 
        field_type: str = "parcel_id",
        ocr_confidence: float = 1.0
    ) -> AmbiguityReport:
        """
        Analyzes an identifier or entity field for OCR confusion.
        
        Args:
            text: Raw string extracted by OCR (e.g. "328/l" or "Sah00")
            field_type: Field name or type
            ocr_confidence: Underlying OCR token confidence
        """
        cleaned = text.strip()
        flags = []
        confused_positions: Dict[int, Tuple[str, List[str]]] = {}
        
        # 1. Check for known character confusions
        is_numeric_field = field_type in (
            "parcel_id", "plot_number", "dag_number", "khasra_number", "survey_number",
            "khata_id", "khata_number", "khatian_number", "mutation_number", "general_numeric"
        )
        is_entity_field = field_type in (
            "owner_name", "father_or_guardian_name", "village", "tehsil", "district"
        )
        
        if is_numeric_field:
            for idx, char in enumerate(cleaned):
                if char in NUMERIC_MISTAKEN_LETTERS:
                    # E.g. in "328/l", char 'l' at index 4 is an alphabetic confusion
                    alternatives = OCR_CONFUSION_MATRIX.get(char, [])
                    confused_positions[idx] = (char, alternatives)
                    flag_name = f"CHAR_CONFUSION_{char.upper()}_TO_{alternatives[0]}"
                    if flag_name not in flags:
                        flags.append(flag_name)

            # Check for merged slash misrecognized as '1' (e.g. 328/1 -> 32811 or 328/2 -> 32812)
            if field_type in ("parcel_id", "plot_number", "dag_number", "khasra_number", "survey_number"):
                if "/" not in cleaned and len(cleaned) >= 4 and cleaned.isdigit():
                    # 5+ digits or 4 digits ending with 11 (e.g. 4511)
                    if len(cleaned) >= 5 or (len(cleaned) == 4 and cleaned.endswith("11")):
                        slash_match = re.search(r"^(\d{2,4})(1)(\d{1,2})$", cleaned)
                        if slash_match:
                            pos = len(slash_match.group(1))
                            confused_positions[pos] = ("1", ["/"])
                            if "SLASH_CONFUSION_1_FOR_SLASH" not in flags:
                                flags.append("SLASH_CONFUSION_1_FOR_SLASH")
        elif is_entity_field:
            for idx, char in enumerate(cleaned):
                if char in ENTITY_MISTAKEN_DIGITS:
                    alternatives = ENTITY_MISTAKEN_DIGITS[char]
                    confused_positions[idx] = (char, alternatives)
                    flag_name = f"CHAR_CONFUSION_DIGIT_IN_NAME_{char}"
                    if flag_name not in flags:
                        flags.append(flag_name)
            if any(c.isdigit() for c in cleaned):
                flags.append("ENTITY_CONTAINS_DIGITS")

        # 2. Syntax Check according to field type
        has_syntax_violation = False
        if field_type in ("khata_id", "khata_number"):
            # Khata should strictly be an integer: e.g. "124", "45"
            if not re.fullmatch(r"^\d+$", cleaned):
                has_syntax_violation = True
                flags.append("KHATA_NON_NUMERIC_SYNTAX")

        elif field_type in ("parcel_id", "plot_number", "dag_number", "khasra_number"):
            # Plot numbers can have subdivision slashes/hyphens: e.g. "128/3", "382", "382/1-A"
            # Pure standard format is: 1-4 digits optionally followed by /digits
            # A 5+ digit plot number without slash is unusually large and suspicious
            if len(cleaned) >= 5 and "/" not in cleaned:
                has_syntax_violation = True
                flags.append("UNUSUALLY_LARGE_PLOT_NUMBER")
            elif not re.fullmatch(r"^\d+(?:/\d+)?$", cleaned):
                has_syntax_violation = True
                flags.append("PARCEL_NON_STANDARD_SYNTAX")

        # 3. Low OCR Confidence Check (Check 3 of Ambiguity Firewall)
        if ocr_confidence < 0.85:
            flags.append("LOW_OCR_CONFIDENCE")

        # 4. Determine overall ambiguity and penalty multiplier
        is_ambiguous = len(confused_positions) > 0 or has_syntax_violation or (ocr_confidence < 0.85)

        penalty = 1.0
        review_reason = None

        if is_ambiguous:
            # Slashes score by 30% if character confusion present, 15% if only syntax or OCR confidence
            if confused_positions:
                penalty = 0.65
                reasons = [f"Character '{char}' at pos {idx} (possible {alts})" for idx, (char, alts) in confused_positions.items()]
                review_reason = f"OCR ambiguity detected: {'; '.join(reasons)}."
            elif has_syntax_violation:
                penalty = 0.80
                review_reason = f"Syntax violation: '{cleaned}' does not match expected legal format for {field_type}."
            else:
                penalty = 0.85
                review_reason = f"Low OCR token confidence ({round(ocr_confidence * 100, 1)}%)."

        return AmbiguityReport(
            raw_text=cleaned,
            is_ambiguous=is_ambiguous,
            has_syntax_violation=has_syntax_violation,
            confused_positions=confused_positions,
            flags=flags,
            ambiguity_penalty=penalty,
            review_reason=review_reason
        )
