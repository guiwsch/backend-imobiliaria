from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Imobiliária API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    USE_CLOUDINARY: bool = False  # Se True, usa Cloudinary; se False, usa armazenamento local

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://frontend-imobiliaria.vercel.app,https://*.vercel.app"
    FRONTEND_URL: Optional[str] = None
    ENVIRONMENT: str = "development"

    @field_validator('USE_CLOUDINARY', mode='before')
    @classmethod
    def parse_use_cloudinary(cls, v):
        """Aceita variações de true/false para USE_CLOUDINARY"""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 't', 'y')
        return bool(v)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
