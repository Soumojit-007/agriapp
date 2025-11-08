import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # Gemini
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not self.GEMINI_API_KEY:
            raise ValueError("❌ Missing required environment variable: GEMINI_API_KEY")

        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        self.GEMINI_URL = os.getenv(
            "GEMINI_URL",
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.GEMINI_MODEL}:generateContent"
        )

        # Allowed Origins
        allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501")
        self.ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

        # AgmarkNet API
        self.AGMARKET_API_KEY = os.getenv("AGMARKET_API_KEY")
        if not self.AGMARKET_API_KEY:
            raise ValueError("❌ Missing required environment variable: AGMARKET_API_KEY")

        self.AGMARKNET_RESOURCE = os.getenv("AGMARKNET_RESOURCE")
        if not self.AGMARKNET_RESOURCE:
            raise ValueError("❌ Missing required environment variable: AGMARKNET_RESOURCE")

settings = Settings()
