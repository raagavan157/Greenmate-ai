import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in root or backend (defensive for local dev, no-op in serverless)
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

IS_VERCEL = bool(
    os.getenv("VERCEL") 
    or os.getenv("AWS_LAMBDA_FUNCTION_NAME") 
    or "/var/task" in str(Path(__file__).resolve())
)

class Settings:
    # MongoDB Atlas Connection
    MONGO_URI: str = (
        os.getenv("MONGODB_URI") 
        or os.getenv("MONGO_URI") 
        or ""
    )
    DB_NAME: str = (
        os.getenv("DATABASE_NAME") 
        or os.getenv("DB_NAME") 
        or "greenmate_db"
    )

    # Gemini Vision & AI API Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Security & JWT Authentication
    JWT_SECRET: str = (
        os.getenv("SECRET_KEY") 
        or os.getenv("JWT_SECRET") 
        or "greenmate_botanical_secret_key_2026_dev"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production" if IS_VERCEL else "development")

    # Cloudinary Cloud Storage
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")

    # File Upload Directory (Never use /var/task; use /tmp in serverless)
    if IS_VERCEL:
        UPLOAD_DIR: Path = Path(tempfile.gettempdir()) / "greenmate_uploads"
    else:
        UPLOAD_DIR: Path = Path(__file__).resolve().parent / "uploads"

    # Paytm Payment Gateway Settings
    PAYTM_MID: str = os.getenv("PAYTM_MID", "DIY123867073269")
    PAYTM_MERCHANT_KEY: str = os.getenv("PAYTM_MERCHANT_KEY", "bKMfNxPPCHdGyB4r")
    PAYTM_WEBSITE: str = os.getenv("PAYTM_WEBSITE", "WEBSTAGING")
    PAYTM_CHANNEL_ID: str = os.getenv("PAYTM_CHANNEL_ID", "WEB")
    PAYTM_INDUSTRY_TYPE_ID: str = os.getenv("PAYTM_INDUSTRY_TYPE_ID", "Retail")
    PAYTM_ENV: str = os.getenv("PAYTM_ENV", "staging")

    @property
    def has_cloudinary(self) -> bool:
        return bool(self.CLOUDINARY_CLOUD_NAME and self.CLOUDINARY_API_KEY and self.CLOUDINARY_API_SECRET)

    def ensure_upload_dir(self) -> Path:
        """Safely ensure the upload directory exists without crashing on read-only environments."""
        try:
            self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            # Fallback to temp directory if custom directory is not writable
            fallback = Path(tempfile.gettempdir()) / "greenmate_uploads"
            try:
                fallback.mkdir(parents=True, exist_ok=True)
                return fallback
            except Exception:
                pass
        return self.UPLOAD_DIR

settings = Settings()
# Create directory defensively without raising at module load
try:
    settings.ensure_upload_dir()
except Exception:
    pass
