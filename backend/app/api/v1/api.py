from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, profile, dashboard, documents, parcels, map,
    reviews, validations, citizen, audit, settings, integrations, health
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(parcels.router, prefix="/parcels", tags=["Parcels"])
api_router.include_router(map.router, prefix="/map", tags=["Map"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(validations.router, prefix="/validations", tags=["Validation"])
api_router.include_router(citizen.router, prefix="/citizen", tags=["Citizen"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
