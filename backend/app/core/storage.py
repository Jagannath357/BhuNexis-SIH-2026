import os
import io
import uuid
from typing import Tuple, Optional
from datetime import timedelta
from fastapi import UploadFile
from minio import Minio
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.upload_dir = os.path.abspath(settings.UPLOAD_DIR)
        os.makedirs(self.upload_dir, exist_ok=True)
        self.minio_client: Optional[Minio] = None
        
        try:
            if settings.MINIO_ENDPOINT:
                self.minio_client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=settings.MINIO_SECURE
                )
        except Exception:
            self.minio_client = None

    def _ensure_bucket(self, bucket_name: str):
        if self.minio_client:
            try:
                if not self.minio_client.bucket_exists(bucket_name):
                    self.minio_client.make_bucket(bucket_name)
            except Exception:
                pass

    async def save_file(self, file: UploadFile, prefix: str = "DOC") -> Tuple[str, str, int]:
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in [".pdf", ".jpg", ".jpeg", ".png", ".tiff"]:
            raise ValueError(f"Unsupported file format: {ext}. Only PDF and images are allowed.")
            
        unique_name = f"{prefix}_{uuid.uuid4().hex[:8]}{ext}"
        target_path = os.path.join(self.upload_dir, unique_name)
        
        content = await file.read()
        file_size = len(content)
        
        if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB.")
            
        with open(target_path, "wb") as f:
            f.write(content)

        if self.minio_client:
            try:
                bucket = settings.MINIO_BUCKET
                self._ensure_bucket(bucket)
                self.minio_client.put_object(
                    bucket_name=bucket,
                    object_name=unique_name,
                    data=io.BytesIO(content),
                    length=file_size,
                    content_type=file.content_type or "application/octet-stream"
                )
            except Exception:
                pass
            
        return target_path, unique_name, file_size

    def get_presigned_url(self, object_name: str, expires_hours: int = 1) -> Optional[str]:
        if not self.minio_client:
            return None
        try:
            return self.minio_client.presigned_get_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=object_name,
                expires=timedelta(hours=expires_hours)
            )
        except Exception:
            return None

storage_service = StorageService()

