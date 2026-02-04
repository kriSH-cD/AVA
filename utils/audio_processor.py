"""Audio processing utilities for converting and loading audio files."""
import base64
import os
import tempfile
from pathlib import Path
from typing import Tuple
import numpy as np
import librosa
import soundfile as sf
from app.config import settings


class AudioProcessor:
    """Handle audio file conversion and loading."""
    
    def __init__(self):
        """Initialize audio processor."""
        self.temp_dir = Path(settings.TEMP_DIR)
        self.temp_dir.mkdir(exist_ok=True)
        self.sample_rate = settings.SAMPLE_RATE
    
    def base64_to_audio(self, base64_string: str) -> Tuple[np.ndarray, int]:
        """
        Convert base64 encoded MP3 to audio waveform.
        
        Args:
            base64_string: Base64 encoded MP3 audio
            
        Returns:
            Tuple of (waveform array, sample rate)
            
        Raises:
            ValueError: If audio format is invalid or conversion fails
        """
        try:
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(base64_string)
            
            # Create temporary MP3 file
            with tempfile.NamedTemporaryFile(
                suffix='.mp3',
                dir=self.temp_dir,
                delete=False
            ) as temp_mp3:
                temp_mp3.write(audio_bytes)
                temp_mp3_path = temp_mp3.name
            
            try:
                # Load audio with librosa
                waveform, sr = librosa.load(
                    temp_mp3_path,
                    sr=self.sample_rate,
                    mono=True
                )
                
                # Validate audio length
                duration = len(waveform) / sr
                if duration > settings.MAX_AUDIO_LENGTH:
                    raise ValueError(
                        f"Audio too long: {duration:.1f}s (max: {settings.MAX_AUDIO_LENGTH}s)"
                    )
                
                if duration < 0.5:
                    raise ValueError(
                        f"Audio too short: {duration:.1f}s (min: 0.5s)"
                    )
                
                return waveform, sr
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_mp3_path):
                    os.unlink(temp_mp3_path)
                    
        except base64.binascii.Error:
            raise ValueError("Invalid base64 encoding")
        except Exception as e:
            raise ValueError(f"Failed to process audio: {str(e)}")
    
    def validate_audio_format(self, audio_bytes: bytes) -> bool:
        """
        Validate that the audio is in MP3 format.
        
        Args:
            audio_bytes: Raw audio bytes
            
        Returns:
            True if valid MP3, False otherwise
        """
        # Check MP3 magic numbers
        mp3_signatures = [
            b'\xff\xfb',  # MPEG-1 Layer 3
            b'\xff\xf3',  # MPEG-2 Layer 3
            b'\xff\xf2',  # MPEG-2.5 Layer 3
            b'ID3'        # ID3 tag
        ]
        
        return any(audio_bytes.startswith(sig) for sig in mp3_signatures)
    
    def cleanup_temp_files(self, max_age_hours: int = 1):
        """
        Clean up old temporary files.
        
        Args:
            max_age_hours: Maximum age of files to keep in hours
        """
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in self.temp_dir.glob('*'):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                    except Exception:
                        pass
