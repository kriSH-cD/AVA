"""Audio processing utilities using ffmpeg for conversion."""
import base64
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple
import numpy as np
import soundfile as sf
from app.config import settings


class AudioProcessor:
    """Handle audio file conversion and loading using ffmpeg."""
    
    def __init__(self):
        """Initialize audio processor."""
        self.temp_dir = Path(settings.TEMP_DIR)
        self.temp_dir.mkdir(exist_ok=True)
        self.sample_rate = settings.SAMPLE_RATE
    
    def base64_to_audio(self, base64_string: str) -> Tuple[np.ndarray, int]:
        """
        Convert base64 encoded audio to waveform using ffmpeg.
        
        Args:
            base64_string: Base64 encoded audio (MP3, WAV, etc.)
            
        Returns:
            Tuple of (waveform array, sample rate)
            
        Raises:
            ValueError: If audio format is invalid or conversion fails
        """
        try:
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(base64_string)
            
            # Create temporary input file
            with tempfile.NamedTemporaryFile(
                suffix='.mp3',
                dir=self.temp_dir,
                delete=False
            ) as temp_input:
                temp_input.write(audio_bytes)
                input_path = temp_input.name
            
            # Create temporary output WAV file
            with tempfile.NamedTemporaryFile(
                suffix='.wav',
                dir=self.temp_dir,
                delete=False
            ) as temp_output:
                output_path = temp_output.name
            
            try:
                # Use ffmpeg to convert to WAV
                subprocess.run([
                    'ffmpeg',
                    '-i', input_path,
                    '-ar', str(self.sample_rate),  # Set sample rate
                    '-ac', '1',  # Convert to mono
                    '-y',  # Overwrite output file
                    output_path
                ], check=True, capture_output=True, text=True)
                
                # Load the WAV file with soundfile
                waveform, sr = sf.read(output_path, dtype='float32')
                
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
                # Clean up temporary files
                for path in [input_path, output_path]:
                    if os.path.exists(path):
                        try:
                            os.unlink(path)
                        except:
                            pass
                    
        except base64.binascii.Error:
            raise ValueError("Invalid base64 encoding")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to convert audio: {e.stderr}")
        except Exception as e:
            raise ValueError(f"Failed to process audio: {str(e)}")
    
    def validate_audio_format(self, audio_bytes: bytes) -> bool:
        """
        Validate that the audio is in a supported format.
        
        Args:
            audio_bytes: Raw audio bytes
            
        Returns:
            True if valid format, False otherwise
        """
        # Check common audio file signatures
        signatures = [
            b'\\xff\\xfb',  # MP3
            b'\\xff\\xf3',  # MP3
            b'ID3',        # MP3 with ID3
            b'RIFF',       # WAV
            b'fLaC',       # FLAC
        ]
        
        return any(audio_bytes.startswith(sig) for sig in signatures)
    
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
