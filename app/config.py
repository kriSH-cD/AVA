"""Configuration management for the Voice Detection API."""
import os
import secrets
from typing import Optional

class Settings:
    """Application settings."""
    
    # API Configuration
    API_KEY: str = os.getenv("API_KEY", f"AVA-2026-{secrets.randbelow(999999):06d}")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Audio Processing
    SAMPLE_RATE: int = 16000
    MAX_AUDIO_LENGTH: int = 300  # seconds
    TEMP_DIR: str = "temp"
    
    # Model Configuration
    MODEL_PATH: str = "models/voice_classifier.pkl"
    CONFIDENCE_THRESHOLD: float = 0.5
    
    # Feature extraction parameters
    N_MFCC: int = 13
    N_FFT: int = 2048
    HOP_LENGTH: int = 512
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the API key."""
        return cls.API_KEY
    
    @classmethod
    def validate_api_key(cls, key: str) -> bool:
        """Validate the provided API key."""
        return key == cls.API_KEY


settings = Settings()
