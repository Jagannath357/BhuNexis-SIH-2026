from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "BhuNexis API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/bhunexis"
    
    JWT_SECRET_KEY: str = "bhunexis-secure-jwt-secret-key-2026-production-grade"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    OCR_SERVICE_URL: str = "http://localhost:8001"
    NLP_SERVICE_URL: str = "http://localhost:8002"
    VALIDATION_SERVICE_URL: str = "http://localhost:8003"
    
    STORAGE_TYPE: str = "local"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 25
    
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "bhunexisadmin"
    MINIO_SECRET_KEY: str = "bhunexispassword123"
    MINIO_BUCKET: str = "bhunexis-documents"
    MINIO_SECURE: bool = False

    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

