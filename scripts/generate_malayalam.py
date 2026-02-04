#!/usr/bin/env python3
"""Generate Malayalam AI voice samples with correct language code."""
from gtts import gTTS
from pathlib import Path
import time
import random

MALAYALAM_PHRASES = [
    "നമസ്കാരം, ഇത് കൃത്രിമ ബുദ്ധി ശബ്ദ പരീക്ഷണമാണ്",
    "ഇന്ന് കാലാവസ്ഥ വളരെ നല്ലതാണ്",
    "സാങ്കേതികവിദ്യ നമ്മുടെ ജീവിതം മാറ്റിമറിച്ചു",
    "ഞാൻ ഇന്ന് മാർക്കറ്റിലേക്ക് പോകുന്നു",
    "പുസ്തകങ്ങൾ വായിക്കുന്നത് എനിക്ക് വളരെ ഇഷ്ടമാണ്",
    "പ്രഭാതഭക്ഷണം തയ്യാറാണ്",
    "സംഗീതം കേൾക്കുന്നത് വളരെ സുഖകരമാണ്",
    "വിദ്യാഭ്യാസം വളരെ പ്രധാനമാണ്",
]

def generate_malayalam_samples(count=333, output_dir="training_data/ai_generated"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🔧 Generating Malayalam AI Voice Samples")
    print("=" * 60)
    print(f"Target: {count} samples")
    print(f"Language code: ml (corrected)")
    print("=" * 60)
    
    total = 0
    errors = 0
    
    for i in range(count):
        try:
            # Randomly select and combine phrases
            text = random.choice(MALAYALAM_PHRASES)
            if i % 3 == 0:
                text = f"{text}. {random.choice(MALAYALAM_PHRASES)}"
            
            # Generate TTS with correct language code
            tts = gTTS(text=text, lang='ml', slow=False)
            
            # Save file
            filename = output_path / f"malayalam_{i+1:05d}.mp3"
            tts.save(str(filename))
            
            total += 1
            
            if total % 50 == 0:
                print(f"   ✅ Generated {total}/{count} samples...", end='\r')
            
            time.sleep(0.3)
            
        except Exception as e:
            errors += 1
            if errors < 10:
                print(f"\n   ⚠️  Error on malayalam_{i+1}: {e}")
    
    print(f"\n\n{'=' * 60}")
    print(f"✅ Malayalam Generation Complete!")
    print(f"{'=' * 60}")
    print(f"   Generated: {total} files")
    print(f"   Errors: {errors}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    generate_malayalam_samples()
