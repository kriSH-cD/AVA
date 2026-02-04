#!/usr/bin/env python3
"""
Automated training script for Voice Detection Model.
Trains RandomForest classifier on collected audio samples.
"""
import os
import sys
import pickle
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.audio_processor import AudioProcessor
from utils.feature_extractor import FeatureExtractor


class ModelTrainer:
    """Train voice detection model on collected data."""
    
    def __init__(self, data_dir: str = "training_data"):
        """Initialize trainer."""
        self.data_dir = Path(data_dir)
        self.audio_processor = AudioProcessor()
        self.feature_extractor = FeatureExtractor()
        
        self.ai_dir = self.data_dir / "ai_generated"
        self.human_dir = self.data_dir / "human"
        
        self.X = []  # Features
        self.y = []  # Labels (0=HUMAN, 1=AI)
        
    def collect_samples(self):
        """Collect and process all audio samples."""
        print("=" * 60)
        print("📊 Collecting Training Samples...")
        print("=" * 60)
        
        # Process AI samples
        ai_count = self._process_directory(self.ai_dir, label=1, label_name="AI")
        
        # Process Human samples
        human_count = self._process_directory(self.human_dir, label=0, label_name="HUMAN")
        
        print("\n" + "=" * 60)
        print(f"✅ Collection Complete!")
        print(f"   AI samples: {ai_count}")
        print(f"   Human samples: {human_count}")
        print(f"   Total samples: {ai_count + human_count}")
        print("=" * 60)
        
        return ai_count, human_count
    
    def _process_directory(self, directory: Path, label: int, label_name: str) -> int:
        """Process all audio files in a directory."""
        if not directory.exists():
            print(f"\n⚠️  Directory not found: {directory}")
            print(f"   Creating directory...")
            directory.mkdir(parents=True, exist_ok=True)
            return 0
        
        print(f"\n📁 Processing {label_name} samples from: {directory}")
        
        # Find all audio files
        audio_files = []
        for ext in ['*.mp3', '*.wav', '*.m4a', '*.flac']:
            audio_files.extend(directory.rglob(ext))
        
        if not audio_files:
            print(f"   ⚠️  No audio files found!")
            return 0
        
        count = 0
        errors = 0
        
        for audio_file in audio_files:
            try:
                # Read audio file
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                
                # Convert to base64 and process
                import base64
                base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
                
                # Extract features
                waveform, sr = self.audio_processor.base64_to_audio(base64_audio)
                features = self.feature_extractor.extract_features(waveform, sr)
                feature_vector = self.feature_extractor.get_feature_vector(features)
                
                # Add to dataset
                self.X.append(feature_vector)
                self.y.append(label)
                count += 1
                
                if count % 10 == 0:
                    print(f"   Processed: {count} samples...")
                
            except Exception as e:
                errors += 1
                print(f"   ❌ Error processing {audio_file.name}: {str(e)[:50]}")
                continue
        
        print(f"   ✅ Successfully processed: {count} samples")
        if errors > 0:
            print(f"   ⚠️  Errors: {errors} samples")
        
        return count
    
    def train_model(self, test_size: float = 0.2):
        """Train RandomForest classifier."""
        print("\n" + "=" * 60)
        print("🤖 Training Model...")
        print("=" * 60)
        
        if len(self.X) < 10:
            print("❌ Not enough samples to train!")
            print(f"   Found: {len(self.X)} samples")
            print(f"   Need: At least 10 samples")
            return None
        
        # Convert to numpy arrays
        X = np.array(self.X)
        y = np.array(self.y)
        
        print(f"\n📊 Dataset Info:")
        print(f"   Total samples: {len(X)}")
        print(f"   Features per sample: {X.shape[1]}")
        print(f"   AI samples: {np.sum(y == 1)}")
        print(f"   Human samples: {np.sum(y == 0)}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\n📈 Train/Test Split:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Testing samples: {len(X_test)}")
        
        # Train model
        print(f"\n🔧 Training RandomForest...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        print(f"   ✅ Training complete!")
        
        # Evaluate
        print(f"\n📊 Model Evaluation:")
        
        # Training accuracy
        train_pred = model.predict(X_train)
        train_acc = accuracy_score(y_train, train_pred)
        print(f"   Training Accuracy: {train_acc*100:.2f}%")
        
        # Testing accuracy
        test_pred = model.predict(X_test)
        test_acc = accuracy_score(y_test, test_pred)
        print(f"   Testing Accuracy: {test_acc*100:.2f}%")
        
        # Classification report
        print(f"\n📋 Detailed Report:")
        print(classification_report(
            y_test, test_pred,
            target_names=['HUMAN', 'AI_GENERATED']
        ))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, test_pred)
        print(f"📊 Confusion Matrix:")
        print(f"                Predicted")
        print(f"              HUMAN  AI")
        print(f"   Actual HUMAN  {cm[0][0]:3d}   {cm[0][1]:3d}")
        print(f"          AI     {cm[1][0]:3d}   {cm[1][1]:3d}")
        
        # Feature importance
        print(f"\n🔍 Top 5 Most Important Features:")
        feature_names = self.feature_extractor.feature_names if hasattr(self.feature_extractor, 'feature_names') else [
            'pitch_variance', 'pitch_std', 'pitch_range', 'pitch_mean',
            'energy_variance', 'energy_std', 'energy_range', 'energy_mean',
            'spectral_flatness_mean', 'spectral_flatness_std',
            'spectral_centroid_mean', 'spectral_centroid_std',
            'spectral_rolloff_mean', 'spectral_rolloff_std',
            'zcr_mean', 'zcr_std', 'zcr_variance',
            'pause_regularity', 'avg_pause_duration', 'avg_speech_duration', 'speech_rate'
        ]
        
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:5]
        
        for i, idx in enumerate(indices, 1):
            print(f"   {i}. {feature_names[idx]}: {importances[idx]:.4f}")
        
        return model, test_acc
    
    def save_model(self, model, output_path: str = "models/voice_classifier.pkl"):
        """Save trained model."""
        print(f"\n💾 Saving Model...")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"   ✅ Model saved to: {output_path}")
        print(f"   File size: {output_path.stat().st_size / 1024:.2f} KB")


def main():
    """Main training pipeline."""
    print("\n" + "=" * 60)
    print("🎙️  Voice Detection Model Training")
    print("=" * 60)
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Collect samples
    ai_count, human_count = trainer.collect_samples()
    
    if ai_count == 0 or human_count == 0:
        print("\n❌ Training Failed!")
        print("\n📝 Next Steps:")
        print("   1. Add AI-generated audio files to: training_data/ai_generated/")
        print("   2. Add human audio files to: training_data/human/")
        print("   3. See DATA_COLLECTION_GUIDE.md for sources")
        print("   4. Run this script again")
        return
    
    # Train model
    model, accuracy = trainer.train_model()
    
    if model is None:
        print("\n❌ Training failed!")
        return
    
    # Save model
    trainer.save_model(model)
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 Training Complete!")
    print("=" * 60)
    print(f"✅ Model Accuracy: {accuracy*100:.2f}%")
    print(f"✅ Model saved to: models/voice_classifier.pkl")
    print(f"\n💡 Next Steps:")
    print(f"   1. Restart your API server")
    print(f"   2. Test with: python test_api.py sample.mp3 AVA-2026-XXXXXX")
    print(f"   3. Deploy to Railway")
    
    if accuracy < 0.80:
        print(f"\n⚠️  Accuracy is below 80%!")
        print(f"   Consider adding more training samples")
        print(f"   See DATA_COLLECTION_GUIDE.md for tips")
    elif accuracy >= 0.90:
        print(f"\n🏆 Excellent accuracy! You're ready to win!")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
