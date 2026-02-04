#!/usr/bin/env python3
"""
Generate large-scale AI voice samples using Google TTS.
This creates enough samples to match the human dataset.
"""
from gtts import gTTS
from pathlib import Path
import time
import random

# Common phrases in different Indian languages
PHRASES = {
    'tamil': [
        "வணக்கம், இது செயற்கை நுண்ணறிவு குரல் சோதனை",
        "இன்று வானிலை மிகவும் நன்றாக உள்ளது",
        "தொழில்நுட்பம் நமது வாழ்க்கையை மாற்றியுள்ளது",
        "நான் இன்று சந்தைக்கு செல்கிறேன்",
        "புத்தகம் படிப்பது எனக்கு மிகவும் பிடிக்கும்",
        "காலை உணவு தயாராக உள்ளது",
        "இசை கேட்பது மிகவும் இனிமையானது",
        "கல்வி மிகவும் முக்கியமானது",
    ],
    'hindi': [
        "नमस्ते, यह कृत्रिम बुद्धिमत्ता आवाज़ परीक्षण है",
        "आज मौसम बहुत अच्छा है",
        "प्रौद्योगिकी ने हमारे जीवन को बदल दिया है",
        "मैं आज बाजार जा रहा हूं",
        "मुझे किताबें पढ़ना बहुत पसंद है",
        "नाश्ता तैयार है",
        "संगीत सुनना बहुत सुखद है",
        "शिक्षा बहुत महत्वपूर्ण है",
    ],
    'telugu': [
        "నమస్కారం, ఇది కృత్రిమ మేధస్సు వాయిస్ పరీక్ష",
        "ఈరోజు వాతావరణం చాలా బాగుంది",
        "సాంకేతికత మన జీవితాలను మార్చింది",
        "నేను ఈరోజు మార్కెట్‌కు వెళ్తున్నాను",
        "పుస్తకాలు చదవడం నాకు చాలా ఇష్టం",
        "అల్పాహారం సిద్ధంగా ఉంది",
        "సంగీతం వినడం చాలా ఆనందంగా ఉంటుంది",
        "విద్య చాలా ముఖ్యం",
    ],
    'malayalam': [
        "നമസ്കാരം, ഇത് കൃത്രിമ ബുദ്ധി ശബ്ദ പരീക്ഷണമാണ്",
        "ഇന്ന് കാലാവസ്ഥ വളരെ നല്ലതാണ്",
        "സാങ്കേതികവിദ്യ നമ്മുടെ ജീവിതം മാറ്റിമറിച്ചു",
        "ഞാൻ ഇന്ന് മാർക്കറ്റിലേക്ക് പോകുന്നു",
        "പുസ്തകങ്ങൾ വായിക്കുന്നത് എനിക്ക് വളരെ ഇഷ്ടമാണ്",
        "പ്രഭാതഭക്ഷണം തയ്യാറാണ്",
        "സംഗീതം കേൾക്കുന്നത് വളരെ സുഖകരമാണ്",
        "വിദ്യാഭ്യാസം വളരെ പ്രധാനമാണ്",
    ],
    'bengali': [
        "নমস্কার, এটি কৃত্রিম বুদ্ধিমত্তা ভয়েস পরীক্ষা",
        "আজ আবহাওয়া খুব ভালো",
        "প্রযুক্তি আমাদের জীবন বদলে দিয়েছে",
        "আমি আজ বাজারে যাচ্ছি",
        "আমি বই পড়তে খুব পছন্দ করি",
        "নাস্তা প্রস্তুত",
        "গান শোনা খুব আনন্দদায়ক",
        "শিক্ষা খুবই গুরুত্বপূর্ণ",
    ],
    'english': [
        "Hello, this is an artificial intelligence voice test",
        "The weather is very nice today",
        "Technology has transformed our lives",
        "I am going to the market today",
        "I love reading books",
        "Breakfast is ready",
        "Listening to music is very pleasant",
        "Education is very important",
    ]
}

def generate_ai_samples(target_count: int = 2000, output_dir: str = "training_data/ai_generated"):
    """
    Generate AI voice samples using Google TTS.
    
    Args:
        target_count: Number of samples to generate (default: 2000)
        output_dir: Output directory for generated samples
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🤖 Generating AI Voice Samples with Google TTS")
    print("=" * 60)
    print(f"Target: {target_count} samples")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    total = 0
    errors = 0
    
    # Calculate samples per language
    languages = list(PHRASES.keys())
    samples_per_lang = target_count // len(languages)
    
    for lang in languages:
        print(f"\n📝 Generating {lang.upper()} samples ({samples_per_lang} files)...")
        lang_phrases = PHRASES[lang]
        
        for i in range(samples_per_lang):
            try:
                # Randomly select a phrase
                text = random.choice(lang_phrases)
                
                # Add variation by repeating or combining phrases
                if i % 3 == 0:
                    text = f"{text}. {random.choice(lang_phrases)}"
                
                # Generate TTS (use 2-letter language code)
                lang_code = 'en' if lang == 'english' else lang[:2]
                tts = gTTS(text=text, lang=lang_code, slow=False)
                
                # Save file
                filename = output_path / f"{lang}_{i+1:05d}.mp3"
                tts.save(str(filename))
                
                total += 1
                
                # Progress indicator
                if total % 50 == 0:
                    print(f"   ✅ Generated {total}/{target_count} samples...", end='\r')
                
                # Small delay to avoid rate limiting
                time.sleep(0.3)
                
            except Exception as e:
                errors += 1
                if errors < 10:  # Only show first 10 errors
                    print(f"\n   ⚠️  Error on {lang}_{i+1}: {e}")
    
    print(f"\n\n{'=' * 60}")
    print(f"✅ Generation Complete!")
    print(f"{'=' * 60}")
    print(f"📊 Summary:")
    print(f"   Total generated: {total} files")
    print(f"   Errors: {errors}")
    print(f"   Success rate: {(total/(total+errors)*100):.1f}%")
    print(f"   Output directory: {output_path}")
    print(f"{'=' * 60}")
    print(f"\n💡 Next Steps:")
    print(f"   1. Verify samples: ls -lh {output_path}")
    print(f"   2. Train model: python scripts/train_model.py")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate AI voice samples using Google TTS')
    parser.add_argument('--count', type=int, default=2000, 
                        help='Number of samples to generate (default: 2000)')
    parser.add_argument('--output', type=str, default='training_data/ai_generated',
                        help='Output directory (default: training_data/ai_generated)')
    
    args = parser.parse_args()
    
    try:
        generate_ai_samples(target_count=args.count, output_dir=args.output)
    except ImportError:
        print("❌ Error: gtts not installed")
        print("\n📦 Install with:")
        print("   pip install gtts")
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
