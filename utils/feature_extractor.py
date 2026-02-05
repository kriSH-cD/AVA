"""Feature extraction for voice analysis."""
import numpy as np
import librosa
from typing import Dict, List
from app.config import settings
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

try:
    import speech_recognition
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False


class FeatureExtractor:
    """Extract acoustic features from audio for AI detection."""
    
    def __init__(self):
        """Initialize feature extractor."""
        self.sample_rate = settings.SAMPLE_RATE
        self.n_fft = settings.N_FFT
        self.hop_length = settings.HOP_LENGTH
    
    def extract_features(self, waveform: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Extract all acoustic features from audio waveform.
        
        Args:
            waveform: Audio waveform array
            sr: Sample rate
            
        Returns:
            Dictionary of feature names and values
        """
        features = {}
        
        # 1. Pitch variance (F0 stability)
        features.update(self._extract_pitch_features(waveform, sr))
        
        # 2. Energy variance
        features.update(self._extract_energy_features(waveform))
        
        # 3. Spectral features
        features.update(self._extract_spectral_features(waveform, sr))
        
        # 4. Zero-crossing rate
        features.update(self._extract_zcr_features(waveform))
        
        # 5. Speaking rate and pause features
        features.update(self._extract_temporal_features(waveform, sr))
        
        return features
    
    def _extract_pitch_features(self, waveform: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract pitch-related features."""
        # Use librosa's pyin for pitch tracking
        f0, voiced_flag, voiced_probs = librosa.pyin(
            waveform,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr
        )
        
        # Remove NaN values
        f0_clean = f0[~np.isnan(f0)]
        
        if len(f0_clean) > 0:
            pitch_variance = np.var(f0_clean)
            pitch_std = np.std(f0_clean)
            pitch_range = np.ptp(f0_clean)
            pitch_mean = np.mean(f0_clean)
        else:
            pitch_variance = pitch_std = pitch_range = pitch_mean = 0.0
        
        return {
            'pitch_variance': float(pitch_variance),
            'pitch_std': float(pitch_std),
            'pitch_range': float(pitch_range),
            'pitch_mean': float(pitch_mean)
        }
    
    def _extract_energy_features(self, waveform: np.ndarray) -> Dict[str, float]:
        """Extract energy-related features."""
        # RMS energy
        rms = librosa.feature.rms(y=waveform, hop_length=self.hop_length)[0]
        
        energy_variance = np.var(rms)
        energy_std = np.std(rms)
        energy_range = np.ptp(rms)
        energy_mean = np.mean(rms)
        
        return {
            'energy_variance': float(energy_variance),
            'energy_std': float(energy_std),
            'energy_range': float(energy_range),
            'energy_mean': float(energy_mean)
        }
    
    def _extract_spectral_features(self, waveform: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract spectral features."""
        # Spectral flatness
        spectral_flatness = librosa.feature.spectral_flatness(
            y=waveform,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )[0]
        
        # Spectral centroid
        spectral_centroid = librosa.feature.spectral_centroid(
            y=waveform,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )[0]
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=waveform,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )[0]
        
        return {
            'spectral_flatness_mean': float(np.mean(spectral_flatness)),
            'spectral_flatness_std': float(np.std(spectral_flatness)),
            'spectral_centroid_mean': float(np.mean(spectral_centroid)),
            'spectral_centroid_std': float(np.std(spectral_centroid)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
            'spectral_rolloff_std': float(np.std(spectral_rolloff))
        }
    
    def _extract_zcr_features(self, waveform: np.ndarray) -> Dict[str, float]:
        """Extract zero-crossing rate features."""
        zcr = librosa.feature.zero_crossing_rate(
            waveform,
            hop_length=self.hop_length
        )[0]
        
        return {
            'zcr_mean': float(np.mean(zcr)),
            'zcr_std': float(np.std(zcr)),
            'zcr_variance': float(np.var(zcr))
        }
    
    def _extract_temporal_features(self, waveform: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract temporal features (speaking rate, pauses)."""
        # Detect non-silent intervals
        intervals = librosa.effects.split(
            waveform,
            top_db=30,
            hop_length=self.hop_length
        )
        
        if len(intervals) > 0:
            # Calculate pause durations
            pause_durations = []
            for i in range(len(intervals) - 1):
                pause_start = intervals[i][1]
                pause_end = intervals[i + 1][0]
                pause_duration = (pause_end - pause_start) / sr
                pause_durations.append(pause_duration)
            
            # Speaking segments
            speech_durations = [(end - start) / sr for start, end in intervals]
            
            pause_regularity = np.std(pause_durations) if pause_durations else 0.0
            avg_pause_duration = np.mean(pause_durations) if pause_durations else 0.0
            avg_speech_duration = np.mean(speech_durations) if speech_durations else 0.0
            speech_rate = len(intervals) / (len(waveform) / sr)  # segments per second
        else:
            pause_regularity = avg_pause_duration = avg_speech_duration = speech_rate = 0.0
        
        return {
            'pause_regularity': float(pause_regularity),
            'avg_pause_duration': float(avg_pause_duration),
            'avg_speech_duration': float(avg_speech_duration),
            'speech_rate': float(speech_rate)
        }
    
    def get_feature_vector(self, features: Dict[str, float]) -> np.ndarray:
        """
        Convert feature dictionary to ordered vector for model input.
        
        Args:
            features: Dictionary of features
            
        Returns:
            Feature vector as numpy array
        """
        # Define feature order (must match training)
        feature_order = [
            'pitch_variance', 'pitch_std', 'pitch_range', 'pitch_mean',
            'energy_variance', 'energy_std', 'energy_range', 'energy_mean',
            'spectral_flatness_mean', 'spectral_flatness_std',
            'spectral_centroid_mean', 'spectral_centroid_std',
            'spectral_rolloff_mean', 'spectral_rolloff_std',
            'zcr_mean', 'zcr_std', 'zcr_variance',
            'pause_regularity', 'avg_pause_duration', 'avg_speech_duration', 'speech_rate'
        ]
        
        return np.array([features.get(f, 0.0) for f in feature_order])
    
    def detect_language(self, waveform: np.ndarray, sr: int) -> str:
        """
        Detect language using speech recognition.
        
        This uses Google Speech Recognition API to attempt transcription
        in multiple languages and identifies which one succeeds.
        
        Args:
            waveform: Audio waveform
            sr: Sample rate
            
        Returns:
            Detected language (tamil, hindi, telugu, malayalam, bengali, english, etc.)
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            return "multilingual"
        
        try:
            import io
            import soundfile as sf
            
            # Convert to mono if stereo
            if len(waveform.shape) > 1:
                waveform = waveform.mean(axis=1)
            
            # Convert waveform to WAV format for speech recognition
            wav_buffer = io.BytesIO()
            sf.write(wav_buffer, waveform, sr, format='WAV', subtype='PCM_16')
            wav_buffer.seek(0)
            
            # Initialize recognizer
            recognizer = speech_recognition.Recognizer()
            
            # Load audio
            with speech_recognition.AudioFile(wav_buffer) as source:
                # Record only first 5 seconds for faster processing
                audio_data = recognizer.record(source, duration=5)
            
            # Language codes to try
            language_attempts = [
                ('en-US', 'english', 'en'),
                ('hi-IN', 'hindi', 'hi'),
                ('ta-IN', 'tamil', 'ta'),
                ('te-IN', 'telugu', 'te'),
                ('ml-IN', 'malayalam', 'ml'),
                ('kn-IN', 'kannada', 'kn'),
                ('bn-IN', 'bengali', 'bn'),
                ('gu-IN', 'gujarati', 'gu'),
                ('mr-IN', 'marathi', 'mr'),
                ('pa-IN', 'punjabi', 'pa'),
                ('ur-IN', 'urdu', 'ur'),
            ]
            
            # Try all languages and collect successful transcriptions
            transcriptions = {}
            for lang_code, lang_name, lang_detect_code in language_attempts:
                try:
                    text = recognizer.recognize_google(audio_data, language=lang_code)
                    if text and len(text.strip()) > 0:
                        transcriptions[lang_name] = (text, lang_detect_code)
                except speech_recognition.UnknownValueError:
                    continue
                except speech_recognition.RequestError:
                    break
            
            # If we got transcriptions, use langdetect to find the best match
            if transcriptions:
                try:
                    from langdetect import detect
                    
                    # Try to detect language from each transcription
                    best_match = None
                    best_confidence = 0
                    
                    for lang_name, (text, expected_code) in transcriptions.items():
                        try:
                            detected_lang = detect(text)
                            # If detected language matches expected, this is likely correct
                            if detected_lang == expected_code:
                                return lang_name
                            # For English, also check if it's romanized version
                            elif lang_name == 'english' and detected_lang == 'en':
                                best_match = lang_name
                                best_confidence = 1
                        except:
                            continue
                    
                    # If we found a confident match, return it
                    if best_match and best_confidence > 0:
                        return best_match
                    
                    # Otherwise, return the first successful transcription
                    # (prefer specific Indian languages over English for Indian audio)
                    for lang_name in ['tamil', 'hindi', 'telugu', 'malayalam', 'kannada', 'bengali', 'gujarati', 'marathi', 'punjabi', 'urdu', 'english']:
                        if lang_name in transcriptions:
                            return lang_name
                            
                except ImportError:
                    # langdetect not available, return first successful
                    return list(transcriptions.keys())[0]
            
            # If no language worked, return multilingual
            return "multilingual"
            
        except Exception as e:
            # If anything fails, return multilingual
            # The model still works regardless of language
            return "multilingual"


