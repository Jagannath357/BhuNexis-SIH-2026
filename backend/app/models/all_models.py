from datetime import datetime
from typing import Optional, List, Any, Dict
from sqlalchemy import BigInteger, String, Text, Boolean, DateTime, Numeric, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    documents: Mapped[List["Document"]] = relationship("Document", back_populates="uploader")
    assigned_reviews: Mapped[List["ReviewCase"]] = relationship("ReviewCase", back_populates="assignee")
    audit_events: Mapped[List["AuditEvent"]] = relationship("AuditEvent", back_populates="user")


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    document_uid: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    document_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    source_system: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tehsil: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    village: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    document_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    upload_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    page_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    checksum: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    uploaded_by: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.users.id"), nullable=True)
    processing_status: Mapped[str] = mapped_column(String, nullable=False, default="UPLOADED")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @property
    def file_size(self) -> Optional[int]:
        return None

    @property
    def updated_at(self) -> Optional[datetime]:
        return self.created_at

    uploader: Mapped[Optional["User"]] = relationship("User", back_populates="documents")
    pages: Mapped[List["DocumentPage"]] = relationship("DocumentPage", back_populates="document", cascade="all, delete-orphan")
    extracted_fields: Mapped[List["ExtractedField"]] = relationship("ExtractedField", secondary="core.document_pages", primaryjoin="Document.id == DocumentPage.document_id", secondaryjoin="DocumentPage.id == ExtractedField.document_page_id", viewonly=True)
    validation_results: Mapped[List["ValidationResult"]] = relationship("ValidationResult", back_populates="document")



class DocumentPage(Base):
    __tablename__ = "document_pages"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core.documents.id"), nullable=False)
    page_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    image_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quality_score: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    ocr_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @property
    def ocr_text(self) -> Optional[str]:
        return None

    @property
    def confidence_score(self) -> Optional[float]:
        return float(self.quality_score) if self.quality_score is not None else None

    document: Mapped["Document"] = relationship("Document", back_populates="pages")
    extracted_fields: Mapped[List["ExtractedField"]] = relationship("ExtractedField", back_populates="page")


class Owner(Base):
    __tablename__ = "owners"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    owner_uid: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    local_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    father_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    village: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tehsil: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def father_or_husband_name(self) -> Optional[str]:
        return self.father_name

    land_rights: Mapped[List["LandRight"]] = relationship("LandRight", back_populates="owner")


class Parcel(Base):
    __tablename__ = "parcels"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    parcel_uid: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    survey_number: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    khasra_number: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    khata_number: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    plot_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    village: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    tehsil: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    district: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    area: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    area_unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    land_classification: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    land_use: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ulpin: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="DRAFT")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def recorded_area(self) -> Optional[float]:
        return self.area

    @property
    def recorded_area_unit(self) -> Optional[str]:
        return self.area_unit

    land_rights: Mapped[List["LandRight"]] = relationship("LandRight", back_populates="parcel")
    validation_results: Mapped[List["ValidationResult"]] = relationship("ValidationResult", back_populates="parcel")
    review_cases: Mapped[List["ReviewCase"]] = relationship("ReviewCase", back_populates="parcel")
    parcel_geometry: Mapped[Optional["ParcelGeometry"]] = relationship("ParcelGeometry", back_populates="parcel", uselist=False)


class LandRight(Base):
    __tablename__ = "land_rights"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core.owners.id"), nullable=False)
    parcel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core.parcels.id"), nullable=False)
    ownership_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    share_percentage: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    valid_from: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_to: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_current: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    source_document_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.documents.id"), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="land_rights")
    owner: Mapped["Owner"] = relationship("Owner", back_populates="land_rights")


class ExtractedField(Base):
    __tablename__ = "extracted_fields"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    document_page_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.document_pages.id"), nullable=True)
    parcel_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.parcels.id"), nullable=True)
    field_name: Mapped[str] = mapped_column(String, nullable=False)
    extracted_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    normalized_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    source_bbox: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    extractor: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    model_version: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    validation_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @property
    def document_id(self) -> Optional[int]:
        return self.page.document_id if self.page else None

    @property
    def status(self) -> Optional[str]:
        return self.validation_status

    @property
    def bounding_box(self) -> Optional[Dict[str, Any]]:
        return self.source_bbox

    document: Mapped[Optional["Document"]] = relationship("Document", secondary="core.document_pages", primaryjoin="ExtractedField.document_page_id == DocumentPage.id", secondaryjoin="DocumentPage.document_id == Document.id", viewonly=True)
    page: Mapped[Optional["DocumentPage"]] = relationship("DocumentPage", back_populates="extracted_fields")


class ValidationResult(Base):
    __tablename__ = "validation_results"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    parcel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core.parcels.id"), nullable=False)
    document_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.documents.id"), nullable=True)
    validation_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    field_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    expected_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actual_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="validation_results")
    document: Mapped[Optional["Document"]] = relationship("Document", back_populates="validation_results")
    review_cases: Mapped[List["ReviewCase"]] = relationship("ReviewCase", back_populates="validation_result")


class ReviewCase(Base):
    __tablename__ = "review_cases"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    parcel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core.parcels.id"), nullable=False)
    document_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.documents.id"), nullable=True)
    validation_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.validation_results.id"), nullable=True)
    assigned_to: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.users.id"), nullable=True)
    priority: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="PENDING")
    reviewer_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    corrected_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    @property
    def case_uid(self) -> str:
        return f"REV-{self.id:05d}"

    @property
    def reviewer_notes(self) -> Optional[str]:
        return self.reviewer_comment

    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="review_cases")
    assignee: Mapped[Optional["User"]] = relationship("User", back_populates="assigned_reviews")
    validation_result: Mapped[Optional["ValidationResult"]] = relationship("ValidationResult", back_populates="review_cases")


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("core.users.id"), nullable=True)
    entity_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    entity_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False, index=True)
    old_value: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    new_value: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @property
    def changes(self) -> Optional[Dict[str, Any]]:
        return {"old": self.old_value, "new": self.new_value} if (self.old_value or self.new_value) else None

    @property
    def ip_address(self) -> Optional[str]:
        return "127.0.0.1"

    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_events")


class ParcelGeometry(Base):
    __tablename__ = "parcel_geometry"
    __table_args__ = {"schema": "gis"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    parcel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("core.parcels.id"), unique=True, nullable=False)
    geometry: Mapped[Any] = mapped_column(Geometry("POLYGON", srid=4326), nullable=False)
    geometry_source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gis_area_sq_m: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    coordinate_system: Mapped[str] = mapped_column(String, nullable=False, default="EPSG:4326")
    gis_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="parcel_geometry")


