"""
normalizers/candidate_generator.py - Area 3 & Rule 2 (Candidate Generation for Human Review).

Generates plausible alternative interpretations for ambiguous identifiers (e.g. '382/l' -> ['382/1', '382/I'])
for the Officer Verification UI without ever overwriting raw OCR text.
"""

from typing import List, Dict, Tuple
from itertools import product
from .ambiguity_detector import AmbiguityDetector, AmbiguityReport, OCR_CONFUSION_MATRIX


class CandidateGenerator:
    """Generates and ranks plausible interpretations for ambiguous land record tokens."""

    @classmethod
    def generate_candidates(
        cls, 
        raw_text: str, 
        field_type: str = "parcel_id",
        max_candidates: int = 4
    ) -> List[str]:
        """
        Takes an ambiguous raw string and generates plausible candidates.
        
        Example:
            raw_text = "382/l"
            output = ["382/1", "382/I"]
        """
        report: AmbiguityReport = AmbiguityDetector.analyze_identifier(raw_text, field_type=field_type)

        if not report.is_ambiguous or not report.confused_positions:
            # If no confused characters detected, return raw text as the only candidate
            return [raw_text.strip()]

        # Generate character option lists for each position
        chars = list(raw_text.strip())
        options_per_pos: List[List[str]] = []

        is_entity_field = field_type in (
            "owner_name", "father_or_guardian_name", "village", "tehsil", "district"
        )

        for idx, char in enumerate(chars):
            if idx in report.confused_positions:
                orig_char, alts = report.confused_positions[idx]
                if is_entity_field:
                    # For names and places, prioritize lowercase letters over uppercase and digits
                    sorted_alts = sorted(alts, key=lambda x: (x.isdigit(), x.isupper(), x))
                else:
                    # For parcel/khata identifiers, prioritize standard digits first
                    sorted_alts = sorted(alts, key=lambda x: (not x.isdigit(), x))
                options_per_pos.append(sorted_alts)
            else:
                options_per_pos.append([char])

        # Compute cartesian product of candidate permutations
        candidates = []
        for combo in product(*options_per_pos):
            cand_str = "".join(combo)
            if cand_str != raw_text and cand_str not in candidates:
                candidates.append(cand_str)
            if len(candidates) >= max_candidates:
                break

        # Fallback if no valid alternative generated
        if not candidates:
            return [raw_text]

        return candidates
