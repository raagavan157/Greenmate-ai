import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in root or backend
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    DB_NAME: str = os.getenv("DB_NAME", "greenmate_db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "greenmate_botanical_secret_key_2026_dev")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    UPLOAD_DIR: Path = Path(__file__).resolve().parent / "uploads"

    # Paytm Payment Gateway Settings
    PAYTM_MID: str = os.getenv("PAYTM_MID", "DIY123867073269")
    PAYTM_MERCHANT_KEY: str = os.getenv("PAYTM_MERCHANT_KEY", "bKMfNxPPCHdGyB4r")
    PAYTM_WEBSITE: str = os.getenv("PAYTM_WEBSITE", "WEBSTAGING")
    PAYTM_CHANNEL_ID: str = os.getenv("PAYTM_CHANNEL_ID", "WEB")
    PAYTM_INDUSTRY_TYPE_ID: str = os.getenv("PAYTM_INDUSTRY_TYPE_ID", "Retail")
    PAYTM_ENV: str = os.getenv("PAYTM_ENV", "staging")

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
