"""
schemas/canonical_record.py - Canonical Land Record Schema & Terminology Normalization.

Consolidates heterogeneous state land-record labels (Dag, Khasra, Khatian, Plot, Survey)
into a unified schema with field-level Two-Track results.
"""

from typing import Optional, Dict, List, Any, Union
from pathlib import Path
from pydantic import BaseModel, Field
from .field_result import FieldResult, FieldStatus, FieldTier


# State-specific terminology mappings to canonical field names
STATE_TERMINOLOGY_MAP: Dict[str, str] = {
    # Parcel / Plot Identifiers
    "plot": "plot_number",
    "plot no": "plot_number",
    "plot number": "plot_number",
    "p1ot": "plot_number",
    "p1ot number": "plot_number",
    "dag": "plot_number",
    "dag no": "plot_number",
    "khasra": "plot_number",
    "khasra no": "plot_number",
    "survey": "plot_number",
    "survey no": "plot_number",
    "survey number": "plot_number",
    "chaka": "plot_number",

    # Khata / Khatian Identifiers
    "khata": "khata_number",
    "khata no": "khata_number",
    "khata number": "khata_number",
    "khata  n0": "khata_number",
    "khatian": "khata_number",
    "khatian no": "khata_number",
    "khatauni": "khata_number",
    "jamabandi": "khata_number",

    # Ownership / Pattadar
    "name": "owner_name",
    "pattadar": "owner_name",
    "pattadar name": "owner_name",
    "name of pattadar": "owner_name",
    "tenant": "owner_name",
    "raiyat": "owner_name",
    "recorded tenant": "owner_name",
    "father": "father_or_guardian_name",
    "father's name": "father_or_guardian_name",
    "guardian": "father_or_guardian_name",

    # Administrative Location
    "village": "village",
    "vil1age": "village",
    "mouza": "village",
    "mauza": "village",
    "gram": "village",
    "tehsil": "tehsil",
    "tehsi1": "tehsil",
    "tahasil": "tehsil",
    "taluk": "tehsil",
    "mandal": "tehsil",
    "block": "tehsil",
    "district": "district",
    "dist": "district",
    "distt": "district",
    "jilla": "district",
    "zilla": "district",

    # Area & Land
    "area": "area_value",
    "land area": "area_value",
    "rakba": "area_value",
    "total area": "area_value",
    "kisam": "land_classification",
    "land type": "land_classification",

    # Transactions & Legal
    "mutation": "mutation_number",
    "mutation no": "mutation_number",
    "case no": "mutation_number",
    "date": "document_date",
    "order date": "document_date",
    "registration date": "document_date",
}


class CanonicalRecord(BaseModel):
    """
    Standardized, canonical representation of a digitized land record.
    Every field is stored as a FieldResult supporting the Two-Track model and audit trails.
    """
    document_id: str = Field(..., description="Unique source document ID")
    state: Optional[str] = Field(default="ODISHA", description="State context (e.g. ODISHA, BENGAL, UP)")
    language: Optional[str] = Field(default="en", description="Primary document language code")
    
    # Overall Document Health & Gating
    overall_status: FieldStatus = Field(default=FieldStatus.EXTRACTED)
    overall_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    needs_human_review: bool = Field(default=False)
    review_reasons: List[str] = Field(default_factory=list)

    # Tier 1: High-Risk Identifiers (Zero-Tolerance Immutability)
    khata_number: Optional[FieldResult] = None
    plot_number: Optional[FieldResult] = None
    mutation_number: Optional[FieldResult] = None
    area_value: Optional[FieldResult] = None

    # Tier 2: Safe Standardizable Fields
    area_unit: Optional[FieldResult] = None
    normalized_area_sqm: Optional[FieldResult] = None
    document_date: Optional[FieldResult] = None

    # Tier 3: Entity & Linguistic Fields
    owner_name: Optional[FieldResult] = None
    father_or_guardian_name: Optional[FieldResult] = None
    village: Optional[FieldResult] = None
    tehsil: Optional[FieldResult] = None
    district: Optional[FieldResult] = None
    land_classification: Optional[FieldResult] = None

    def get_field(self, field_name: str) -> Optional[FieldResult]:
        """Retrieves a field result by canonical name."""
        return getattr(self, field_name, None)

    def set_field(self, field_name: str, result: FieldResult) -> None:
        """Sets a field result by canonical name."""
        if hasattr(self, field_name):
            setattr(self, field_name, result)

    def update_quality_status(self, min_tier1_confidence: float = 0.85) -> None:
        """
        Scans all fields to compute overall confidence and determine routing to 
        RELIABLE downstream validation vs REVIEW_REQUIRED officer queue.
        """
        fields = [
            self.khata_number, self.plot_number, self.mutation_number, self.area_value,
            self.area_unit, self.document_date, self.owner_name, self.father_or_guardian_name,
            self.village, self.tehsil, self.district
        ]
        active_fields = [f for f in fields if f is not None]

        if not active_fields:
            self.overall_status = FieldStatus.NOT_FOUND
            self.overall_confidence = 0.0
            self.needs_human_review = True
            self.review_reasons = ["No land-record fields were extracted."]
            return

        # Calculate average confidence
        self.overall_confidence = sum(f.confidence for f in active_fields) / len(active_fields)

        reasons = []
        needs_review = False

        for f in active_fields:
            # Check if any field is already flagged for review
            if f.status == FieldStatus.REVIEW_REQUIRED:
                needs_review = True
                msg = f.review_reason or f"Field '{f.field_name}' flagged as REVIEW_REQUIRED (flags: {f.flags})."
                reasons.append(msg)
            
            # Check if a Tier 1 field falls below strict threshold
            elif f.tier == FieldTier.TIER_1_IMMUTABLE and f.confidence < min_tier1_confidence:
                needs_review = True
                reasons.append(
                    f"Tier 1 field '{f.field_name}' confidence ({round(f.confidence*100, 1)}%) "
                    f"is below mandatory threshold ({round(min_tier1_confidence*100, 1)}%)."
                )

        self.needs_human_review = needs_review
        self.review_reasons = reasons

        if needs_review:
            self.overall_status = FieldStatus.REVIEW_REQUIRED
        else:
            self.overall_status = FieldStatus.NORMALIZED

    def to_officer_payload(self) -> Dict[str, Any]:
        """Formats the entire record for the Human-in-the-Loop review dashboard."""
        fields_data = {}
        for attr in [
            "khata_number", "plot_number", "mutation_number", "area_value",
            "area_unit", "normalized_area_sqm", "document_date", "owner_name",
            "father_or_guardian_name", "village", "tehsil", "district", "land_classification"
        ]:
            val = getattr(self, attr, None)
            if val is not None:
                fields_data[attr] = val.to_officer_view()

        return {
            "document_id": self.document_id,
            "state": self.state,
            "language": self.language,
            "overall_status": self.overall_status.value,
            "overall_confidence": round(self.overall_confidence * 100, 1),
            "needs_human_review": self.needs_human_review,
            "review_reasons": self.review_reasons,
            "fields": fields_data
        }

    def to_normalized_json(self, indent: int = 2) -> str:
        """Serializes the record including normalized data, ambiguity flags, and review messages."""
        import json
        return json.dumps(self.to_officer_payload(), indent=indent, ensure_ascii=False)

    def save_to_file(self, filepath: Union[str, Path], indent: int = 2) -> Path:
        """Saves the normalized record with audit details to a target JSON file."""
        from pathlib import Path
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(self.to_normalized_json(indent=indent))
        return p
