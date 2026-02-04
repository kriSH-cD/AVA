"""Request/response models for API validation."""
import base64
from dataclasses import dataclass
from typing import Literal


@dataclass
class VoiceDetectionRequest:
    """Request model for voice detection."""
    audio_base64: str
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary with validation."""
        audio_base64 = data.get('audio_base64', '')
        
        if not audio_base64:
            raise ValueError("audio_base64 is required")
        
        # Validate base64
        try:
            base64.b64decode(audio_base64, validate=True)
        except Exception:
            raise ValueError("Invalid base64 encoding")
        
        return cls(audio_base64=audio_base64)


@dataclass
class VoiceDetectionResponse:
    """Response model for voice detection."""
    classification: str  # "AI_GENERATED" or "HUMAN"
    confidence: float
    explanation: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "classification": self.classification,
            "confidence": round(self.confidence, 2),
            "explanation": self.explanation
        }


@dataclass
class ErrorResponse:
    """Error response model."""
    detail: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {"detail": self.detail}

