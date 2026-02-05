#!/usr/bin/env python3
"""Quick test script for the trained model."""
import sys
import pickle
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.audio_processor import AudioProcessor
from utils.feature_extractor import FeatureExtractor
from utils.classifier import VoiceClassifier

def test_model(audio_file: str):
    """Test the trained model on an audio file."""
    print("=" * 60)
    print(f"🧪 Testing Model on: {Path(audio_file).name}")
    print("=" * 60)
    
    # Load audio
    with open(audio_file, 'rb') as f:
        audio_bytes = f.read()
    
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Process
    audio_processor = AudioProcessor()
    feature_extractor = FeatureExtractor()
    classifier = VoiceClassifier()
    
    print("\n📊 Processing audio...")
    waveform, sr = audio_processor.base64_to_audio(base64_audio)
    print(f"   ✅ Audio loaded: {len(waveform)/sr:.2f}s duration")
    
    print("\n🔍 Extracting features...")
    features = feature_extractor.extract_features(waveform, sr)
    feature_vector = feature_extractor.get_feature_vector(features)
    print(f"   ✅ Extracted {len(feature_vector)} features")
    
    print("\n🤖 Classifying...")
    classification, confidence, feature_importances = classifier.predict(feature_vector)
    
    # Detect language
    language = feature_extractor.detect_language(waveform, sr)
    
    print("\n" + "=" * 60)
    print("📋 RESULTS")
    print("=" * 60)
    print(f"Classification: {classification}")
    print(f"Confidence: {confidence*100:.2f}%")
    print(f"Language: {language}")
    
    explanation = classifier.generate_explanation(
        classification, confidence, features, feature_importances
    )
    print(f"\nExplanation:\n{explanation}")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_test.py <audio_file.mp3>")
        sys.exit(1)
    
    test_model(sys.argv[1])
