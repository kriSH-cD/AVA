#!/usr/bin/env python3
"""Download and organize Kaggle dataset for human voice samples."""
import os
import shutil
from pathlib import Path
import kagglehub

def download_and_organize():
    """Download Kaggle dataset and organize human voices."""
    
    print("=" * 60)
    print("📥 Downloading Indian Languages Audio Dataset from Kaggle")
    print("=" * 60)
    
    # Download dataset
    try:
        path = kagglehub.dataset_download("hmsolanki/indian-languages-audio-dataset")
        print(f"\n✅ Dataset downloaded to: {path}")
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\nNote: You may need to authenticate with Kaggle first:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Create an API token")
        print("3. Save kaggle.json to ~/.kaggle/kaggle.json")
        return
    
    # Create training_data directory structure
    project_root = Path(__file__).parent.parent
    training_data_dir = project_root / "training_data"
    human_dir = training_data_dir / "human"
    ai_dir = training_data_dir / "ai_generated"
    
    # Create directories
    human_dir.mkdir(parents=True, exist_ok=True)
    ai_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Created training directories:")
    print(f"   - {human_dir}")
    print(f"   - {ai_dir}")
    
    # Copy audio files from downloaded dataset to human folder
    source_path = Path(path)
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}
    
    copied_count = 0
    print(f"\n📋 Scanning for audio files in: {source_path}")
    
    # Recursively find all audio files
    for audio_file in source_path.rglob('*'):
        if audio_file.is_file() and audio_file.suffix.lower() in audio_extensions:
            # Create unique filename to avoid conflicts
            dest_file = human_dir / f"{audio_file.parent.name}_{audio_file.name}"
            
            try:
                shutil.copy2(audio_file, dest_file)
                copied_count += 1
                if copied_count % 10 == 0:
                    print(f"   Copied {copied_count} files...", end='\r')
            except Exception as e:
                print(f"\n⚠️  Error copying {audio_file.name}: {e}")
    
    print(f"\n✅ Copied {copied_count} human voice samples to training_data/human/")
    
    # Create placeholder in ai_generated folder
    placeholder_file = ai_dir / "README.txt"
    with open(placeholder_file, 'w') as f:
        f.write("Place AI-generated voice samples here.\n\n")
        f.write("Supported formats: .mp3, .wav, .m4a, .flac, .ogg\n\n")
        f.write("Once you add AI samples, run:\n")
        f.write("  python scripts/train_model.py\n")
    
    print(f"\n📝 Created placeholder in training_data/ai_generated/")
    
    print("\n" + "=" * 60)
    print("✅ Dataset Setup Complete!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   Human samples: {copied_count} files")
    print(f"   AI samples: 0 files (waiting for user)")
    print(f"\n📍 Next Steps:")
    print(f"   1. Add AI-generated voice samples to: {ai_dir}")
    print(f"   2. Run training: python scripts/train_model.py")
    print("=" * 60)

if __name__ == "__main__":
    download_and_organize()
