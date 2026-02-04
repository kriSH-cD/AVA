#!/usr/bin/env python3
"""
Quick script to generate AI voice samples using Google TTS.
Requires: pip install gtts
"""
from gtts import gTTS
from pathlib import Path
import time

# Sample texts in different languages
SAMPLES = {
    'tamil': [
        "வணக்கம், இது செயற்கை நுண்ணறிவு குரல் சோதனை",
        "இன்று வானிலை மிகவும் நன்றாக உள்ளது",
        "தொழில்நுட்பம் நமது வாழ்க்கையை மாற்றியுள்ளது",
    ],
    'hindi': [
        "नमस्ते, यह कृत्रिम बुद्धिमत्ता आवाज़ परीक्षण है",
        "आज मौसम बहुत अच्छा है",
        "प्रौद्योगिकी ने हमारे जीवन को बदल दिया है",
    ],
    'telugu': [
        "నమస్కారం, ఇది కృత్రిమ మేధస్సు వాయిస్ పరీక్ష",
        "ఈరోజు వాతావరణం చాలా బాగుంది",
        "సాంకేతికత మన జీవితాలను మార్చింది",
    ],
    'malayalam': [
        "നമസ്കാരം, ഇത് കൃത്രിമ ബുദ്ധി ശബ്ദ പരീക്ഷണമാണ്",
        "ഇന്ന് കാലാവസ്ഥ വളരെ നല്ലതാണ്",
        "സാങ്കേതികവിദ്യ നമ്മുടെ ജീവിതം മാറ്റിമറിച്ചു",
    ],
    'english': [
        "Hello, this is an artificial intelligence voice test",
        "The weather is very nice today",
        "Technology has transformed our lives",
    ]
}

def generate_samples(output_dir: str = "training_data/ai_generated/google_tts"):
    """Generate AI voice samples using Google TTS."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🤖 Generating AI Voice Samples with Google TTS")
    print("=" * 60)
    
    total = 0
    
    for lang, texts in SAMPLES.items():
        print(f"\n📝 Generating {lang} samples...")
        
        for i, text in enumerate(texts, 1):
            try:
                # Generate TTS
                tts = gTTS(text=text, lang=lang[:2])  # Use 2-letter code
                
                # Save file
                filename = output_path / f"{lang}_{i:02d}.mp3"
                tts.save(str(filename))
                
                print(f"   ✅ Generated: {filename.name}")
                total += 1
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Generated {total} AI voice samples!")
    print(f"📁 Saved to: {output_path}")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("   1. Add human voice samples to training_data/human/")
    print("   2. Run: python scripts/train_model.py")

if __name__ == "__main__":
    try:
        generate_samples()
    except ImportError:
        print("❌ Error: gtts not installed")
        print("\n📦 Install with:")
        print("   pip install gtts")
