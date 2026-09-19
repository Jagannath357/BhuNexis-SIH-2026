from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class OwnerSchema(BaseModel):
    id: int
    owner_uid: str
    full_name: str
    father_or_husband_name: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LandRightSchema(BaseModel):
    id: int
    ownership_type: Optional[str] = None
    share_percentage: Optional[float] = None
    share_fraction: Optional[str] = None
    possession_status: Optional[str] = None
    encumbrances: Optional[str] = None
    owner: OwnerSchema

    model_config = ConfigDict(from_attributes=True)

class ParcelDetailResponse(BaseModel):
    id: int
    parcel_uid: str
    survey_number: Optional[str] = None
    khasra_number: Optional[str] = None
    khata_number: Optional[str] = None
    plot_number: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    tehsil: Optional[str] = None
    village: Optional[str] = None
    land_classification: Optional[str] = None
    land_use: Optional[str] = None
    recorded_area: Optional[float] = None
    recorded_area_unit: Optional[str] = None
    gis_area_sq_m: Optional[float] = None
    status: str
    created_at: datetime
    owners: List[LandRightSchema] = []

    model_config = ConfigDict(from_attributes=True)

class GeoJSONFeatureProperties(BaseModel):
    parcel_id: int
    parcel_uid: str
    survey_number: Optional[str] = None
    khata_number: Optional[str] = None
    village: Optional[str] = None
    area: Optional[float] = None
    area_unit: Optional[str] = None
    status: str

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    properties: GeoJSONFeatureProperties
    geometry: dict

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]
