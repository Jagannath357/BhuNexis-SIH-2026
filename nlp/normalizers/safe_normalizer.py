"""
normalizers/safe_normalizer.py - Area 3 & Rule 1 (Tier 2: Safe Deterministic Normalization).

Performs safe mathematical and standardizing transformations on dates, areas,
units, and whitespace without altering high-risk legal identifiers.
"""

import re
from datetime import datetime
from typing import Optional, Dict, Any, Tuple


# Conversion factors to Square Meters (m²)
AREA_UNIT_TO_SQM: Dict[str, float] = {
    "acre": 4046.8564224,
    "hectare": 10000.0,
    "sq_meter": 1.0,
    "sq_ft": 0.092903,
    "decimal": 40.46856,     # 1 decimal = 0.01 acre
    "dismil": 40.46856,
    "guntha": 101.1714,      # 1 guntha = 1/40 acre
    "gunt": 101.1714,
    "bigha": 2529.285,       # Standard Bigha
    "katha": 126.464,        # 1/20 Bigha
    "biswa": 126.464,
}

# Unit alias mapping to canonical unit names
UNIT_ALIAS_MAP: Dict[str, str] = {
    "acre": "acre",
    "acres": "acre",
    "ac": "acre",
    "ac.": "acre",
    "ekad": "acre",
    "hectare": "hectare",
    "hectares": "hectare",
    "hec": "hectare",
    "hec.": "hectare",
    "ha": "hectare",
    "ha.": "hectare",
    "sq.m": "sq_meter",
    "sq.m.": "sq_meter",
    "sqm": "sq_meter",
    "sq meter": "sq_meter",
    "sq meters": "sq_meter",
    "square meter": "sq_meter",
    "square meters": "sq_meter",
    "sq.ft": "sq_ft",
    "sq.ft.": "sq_ft",
    "sqft": "sq_ft",
    "square feet": "sq_ft",
    "decimal": "decimal",
    "decimals": "decimal",
    "dec": "decimal",
    "dec.": "decimal",
    "dismil": "dismil",
    "guntha": "guntha",
    "gunthas": "guntha",
    "gunt": "guntha",
    "bigha": "bigha",
    "katha": "katha",
    "biswa": "biswa",
}

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}


class SafeNormalizer:
    """Deterministic normalizer for Tier 2 and Tier 3 safe operations."""

    @staticmethod
    def clean_whitespace(text: Optional[str]) -> Optional[str]:
        """Collapses multiple spaces, tabs, and trims string."""
        if text is None:
            return None
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def normalize_date(raw_date_str: str) -> Optional[str]:
        """
        Parses various legacy date formats and normalizes into ISO 'YYYY-MM-DD'.
        Returns None if date string is unparseable or outside realistic calendar bounds.
        """
        cleaned = SafeNormalizer.clean_whitespace(raw_date_str)
        if not cleaned:
            return None

        # Format 1: ISO YYYY-MM-DD
        m = re.fullmatch(r"(\d{4})[-/. ](\d{1,2})[-/. ](\d{1,2})", cleaned)
        if m:
            y, mth, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return SafeNormalizer._format_calendar_date(y, mth, d)

        # Format 2: DD/MM/YYYY or DD-MM-YYYY
        m = re.fullmatch(r"(\d{1,2})[-/. ](\d{1,2})[-/. ](\d{4})", cleaned)
        if m:
            d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return SafeNormalizer._format_calendar_date(y, mth, d)

        # Format 3: DD-Mon-YYYY (e.g. 15-Jun-1998 or 15th June 1998)
        m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?[-/.\s]+([A-Za-z]+)[-/.\s]+(\d{4})", cleaned)
        if m:
            d = int(m.group(1))
            mth_str = m.group(2).lower()
            y = int(m.group(3))
            mth = MONTH_MAP.get(mth_str)
            if mth:
                return SafeNormalizer._format_calendar_date(y, mth, d)

        return None

    @staticmethod
    def _format_calendar_date(year: int, month: int, day: int) -> Optional[str]:
        """Validates real calendar boundaries."""
        if not (1800 <= year <= 2035):
            return None
        if not (1 <= month <= 12):
            return None
        if not (1 <= day <= 31):
            return None
        try:
            dt = datetime(year, month, day)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None

    @staticmethod
    def normalize_area(raw_area_text: str) -> Optional[Dict[str, Any]]:
        """
        Parses an area string (e.g. '0.240 Acre', '2.5 Hectares', '1000 Sq.Mtr.')
        Returns normalized dictionary with:
        - raw_value: original string
        - value: float numeric value
        - unit: canonical unit name (e.g. 'acre')
        - sqm: converted area in square meters (m²)
        """
        cleaned = SafeNormalizer.clean_whitespace(raw_area_text)
        if not cleaned:
            return None

        # Regex captures: (number) (unit)
        match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([A-Za-z.]+)?", cleaned)
        if not match:
            return None

        val_str = match.group(1)
        raw_unit_str = (match.group(2) or "").lower().strip()

        try:
            num_val = float(val_str)
        except ValueError:
            return None

        # Canonicalize unit (defaults to 'acre' in Indian land records if unspecified)
        canonical_unit = UNIT_ALIAS_MAP.get(raw_unit_str, "acre")
        conversion_factor = AREA_UNIT_TO_SQM.get(canonical_unit, AREA_UNIT_TO_SQM["acre"])
        sqm_value = round(num_val * conversion_factor, 2)

        return {
            "value": num_val,
            "unit": canonical_unit,
            "sqm": sqm_value,
            "raw": cleaned
        }

    @staticmethod
    def normalize_person_name(raw_name: str) -> Tuple[str, Optional[str]]:
        """
        Normalizes a name string for Tier 3 entity fields.
        Returns:
            clean_name: Title-cased name without noisy honorifics (e.g. 'Ramesh Chandra Sahu')
            honorific: Detected prefix (e.g. 'Late', 'Sri', 'Smt') if present
        """
        cleaned = SafeNormalizer.clean_whitespace(raw_name)
        if not cleaned:
            return "", None

        honorific_pattern = r"^(late|shri|sri|smt|smti|mr|mrs|dr|kumari)[.\s]+"
        match = re.match(honorific_pattern, cleaned, re.IGNORECASE)
        honorific = None
        base_name = cleaned

        if match:
            honorific = match.group(1).capitalize()
            base_name = cleaned[match.end():].strip()

        return base_name.title(), honorific
