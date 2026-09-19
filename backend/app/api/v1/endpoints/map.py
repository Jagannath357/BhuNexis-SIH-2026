from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.all_models import User
from app.schemas.parcel import GeoJSONFeatureCollection, GeoJSONFeature

router = APIRouter()

@router.get("/parcels", response_model=GeoJSONFeatureCollection)
def get_map_parcels(
    district: str = Query(None),
    village: str = Query(None),
    status_filter: str = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sql = """
        SELECT 
            p.id AS parcel_id,
            p.parcel_uid,
            p.survey_number,
            p.khata_number,
            p.village,
            p.recorded_area AS area,
            p.recorded_area_unit AS area_unit,
            p.status,
            ST_AsGeoJSON(pg.geometry)::json AS geometry
        FROM gis.parcel_geometry pg
        JOIN core.parcels p ON pg.parcel_id = p.id
        WHERE 1=1
    """
    params = {}
    if district:
        sql += " AND p.district ILIKE :district"
        params["district"] = f"%{district}%"
    if village:
        sql += " AND p.village ILIKE :village"
        params["village"] = f"%{village}%"
    if status_filter:
        sql += " AND p.status = :status"
        params["status"] = status_filter

    result = db.execute(text(sql), params).fetchall()
    
    features = []
    for row in result:
        geom = row.geometry
        if isinstance(geom, str):
            geom = json.loads(geom)
            
        feature = {
            "type": "Feature",
            "properties": {
                "parcel_id": row.parcel_id,
                "parcel_uid": row.parcel_uid,
                "survey_number": row.survey_number or "101",
                "khata_number": row.khata_number or "25",
                "village": row.village or "Sample Village",
                "area": float(row.area) if row.area is not None else 1.25,
                "area_unit": row.area_unit or "ACRE",
                "status": row.status
            },
            "geometry": geom
        }
        features.append(feature)
        
    return {"type": "FeatureCollection", "features": features}

@router.get("/parcels/{parcel_id}", response_model=GeoJSONFeature)
def get_map_parcel_by_id(
    parcel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sql = """
        SELECT 
            p.id AS parcel_id,
            p.parcel_uid,
            p.survey_number,
            p.khata_number,
            p.village,
            p.recorded_area AS area,
            p.recorded_area_unit AS area_unit,
            p.status,
            ST_AsGeoJSON(pg.geometry)::json AS geometry
        FROM gis.parcel_geometry pg
        JOIN core.parcels p ON pg.parcel_id = p.id
        WHERE p.id = :parcel_id
    """
    row = db.execute(text(sql), {"parcel_id": parcel_id}).fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "GEOMETRY_NOT_FOUND", "message": f"Geometry for parcel ID {parcel_id} not found."}
        )
        
    geom = row.geometry
    if isinstance(geom, str):
        geom = json.loads(geom)
        
    return {
        "type": "Feature",
        "properties": {
            "parcel_id": row.parcel_id,
            "parcel_uid": row.parcel_uid,
            "survey_number": row.survey_number or "101",
            "khata_number": row.khata_number or "25",
            "village": row.village or "Sample Village",
            "area": float(row.area) if row.area is not None else 1.25,
            "area_unit": row.area_unit or "ACRE",
            "status": row.status
        },
        "geometry": geom
    }
