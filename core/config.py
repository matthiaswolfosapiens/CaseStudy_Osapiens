import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Holds all application settings, loaded from environment variables.
    """
    API_KEY_V1: str = os.getenv("API_KEY_V1") # We will make V1 mandatory
    API_KEY_V2: Optional[str] = os.getenv("API_KEY_V2") # V2 is now optional
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/casedb")

# Create a single settings instance to be used across the application
settings = Settings()

# Add a check to ensure the application doesn't start without the required V1 key
if not settings.API_KEY_V1:
    raise ValueError("FATAL: API_KEY_V1 is not set in the .env file. The application cannot start.")