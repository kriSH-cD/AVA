# 🎙️ AVA Voice Detection API

**Language-Agnostic AI Voice Detection** using acoustic features. Works across Tamil, Hindi, Telugu, Malayalam, Bengali, English, and all other languages.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🏆 Model Performance

- **Training Accuracy**: 99.97%
- **Testing Accuracy**: 100%
- **Dataset**: 11,663 samples (1,665 AI + 9,998 Human)
- **Languages Tested**: Tamil, Hindi, Telugu, Malayalam, Bengali, English
- **Inference Time**: ~1-2 seconds per audio

---

## 🧠 Core Strategy

This API detects AI-generated voices using **acoustic artifacts**, not speech content. This approach:
- ✅ Works across all languages automatically
- ✅ Detects AI patterns in pitch, energy, spectral characteristics
- ✅ No speech-to-text or language models needed
- ✅ Fast and explainable
- ✅ Language-agnostic by design

### How It Works

The model analyzes these acoustic features:
1. **Pitch variance** - AI voices have unnaturally stable pitch
2. **Energy patterns** - Humans have natural volume fluctuations
3. **Spectral features** - AI has smoother frequency distribution
4. **Pause patterns** - AI pauses are too regular
5. **Zero-crossing rate** - Different voice texture patterns

These features work identically across all languages!

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, FastAPI, Uvicorn
- **Audio Processing**: ffmpeg, soundfile, librosa
- **ML**: scikit-learn (RandomForestClassifier)
- **Security**: API key authentication
- **Deployment**: Railway-ready

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- ffmpeg (installed automatically on macOS via brew)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/zaheer-zee/AVA.git
cd AVA/voice-detection-api
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment**:
```bash
# The API will auto-generate an API key on first run
# Or create .env file with custom key:
echo "API_KEY=AVA-2026-YOUR-KEY" > .env
```

5. **Run the server**:
```bash
python -m app.main
```

The API will start at `http://localhost:8000`

### Web Interface

Open your browser and go to:
```
http://localhost:8000/static/index.html
```

Features:
- 📁 Drag & drop audio files
- 🎯 Real-time AI detection
- 📊 Confidence visualization
- 🌍 Multilingual support indicator

---

## 📡 API Usage

### Endpoint

```
POST /api/voice-detection
```

### Headers

```
x-api-key: AVA-2026-XXXXXX
Content-Type: application/json
```

### Request Body

```json
{
  "audio_base64": "BASE64_ENCODED_AUDIO_STRING"
}
```

### Response

```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "language": "multilingual",
  "explanation": "Analysis indicates synthetic speech patterns: unnaturally stable pitch, consistent energy levels."
}
```

### Example with cURL

```bash
# Convert MP3 to base64
BASE64_AUDIO=$(base64 -i sample.mp3)

# Make request
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: AVA-2026-910728" \
  -H "Content-Type: application/json" \
  -d "{\"audio_base64\": \"$BASE64_AUDIO\"}"
```

### Example with Python

```python
import base64
import requests

# Read and encode audio
with open('sample.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    'http://localhost:8000/api/voice-detection',
    headers={
        'x-api-key': 'AVA-2026-910728',
        'Content-Type': 'application/json'
    },
    json={'audio_base64': audio_base64}
)

result = response.json()
print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']*100:.1f}%")
```

---

## 📊 Understanding Results

### Confidence Score

The **confidence score** is a probability (0-100%) representing how certain the model is that the audio is **AI-generated**.

| Confidence | Meaning | Classification |
|------------|---------|----------------|
| 0-50% | Low AI probability | **HUMAN** |
| 50-100% | High AI probability | **AI_GENERATED** |

**Examples:**
- **4% confidence** = 96% sure it's HUMAN → Classification: HUMAN ✅
- **87% confidence** = 87% sure it's AI → Classification: AI_GENERATED ✅

### Language Support

The model shows **"multilingual"** because it's language-agnostic:
- Works across ALL languages (Hindi, Urdu, Tamil, English, etc.)
- Analyzes acoustic features, not words
- No language-specific training needed

---

## 🎯 Model Training

The API comes with a pre-trained model achieving 100% test accuracy. To retrain:

### Quick Training (Using Kaggle Dataset)

```bash
# Activate environment
source venv/bin/activate

# Download dataset and train (automated)
python scripts/download_dataset.py
python scripts/generate_ai_samples.py
python scripts/train_model.py
```

This will:
1. Download 10,000 human voice samples from Kaggle
2. Generate 2,000 AI voice samples using Google TTS
3. Train a RandomForestClassifier
4. Save model to `models/voice_classifier.pkl`

### Training Output

```
🎙️  Voice Detection Model Training
============================================================
📊 Collecting Training Samples...
   AI samples: 1665
   Human samples: 9998
   Total samples: 11663

🤖 Training Model...
   Training Accuracy: 99.97%
   Testing Accuracy: 100.00%

🏆 Excellent accuracy! You're ready to win!
```

### Custom Training Data

Place your audio files in:
```
training_data/
├── ai_generated/     # AI-generated voice samples
│   ├── sample1.mp3
│   └── sample2.mp3
└── human/            # Human voice samples
    ├── speaker1.mp3
    └── speaker2.mp3
```

Then run:
```bash
python scripts/train_model.py
```

---

## 🚢 Deployment

### Railway Deployment

1. **Push to GitHub**:
```bash
git add .
git commit -m "Deploy AVA Voice Detection API"
git push origin main
```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Add environment variable: `API_KEY=AVA-2026-YOUR-KEY`
   - Railway will auto-detect Python and deploy

3. **Configure**:
   - Railway will provide a URL like `https://your-app.railway.app`
   - Update your frontend to use this URL
   - Test with: `curl https://your-app.railway.app/health`

### Environment Variables

```bash
API_KEY=AVA-2026-910728    # Your API key
HOST=0.0.0.0               # Server host
PORT=8000                  # Server port
```

---

## 🧱 Features Extracted

| Feature | Description | Why It Helps |
|---------|-------------|--------------|
| **Pitch Variance** | Variation in voice pitch | AI voices are too stable |
| **Pitch Mean/Std** | Average pitch and deviation | AI has consistent pitch |
| **Energy Variance** | Volume fluctuation | Humans fluctuate naturally |
| **Energy Mean/Std** | Average energy levels | AI has uniform energy |
| **Spectral Flatness** | Frequency distribution smoothness | AI has smoother spectrum |
| **Spectral Centroid** | Brightness of sound | AI differs in timbre |
| **Spectral Rolloff** | High-frequency content | AI has different rolloff |
| **Zero-Crossing Rate** | Sign changes in waveform | AI patterns differ |
| **Pause Regularity** | Consistency of pauses | AI pauses unnaturally |
| **Speech Rate** | Speaking speed | AI is more consistent |

**Total: 21 features** analyzed per audio sample.

---

## 📊 Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | Success | Audio analyzed successfully |
| `400` | Bad Request | Invalid base64, corrupt audio, or unsupported format |
| `401` | Unauthorized | Missing API key |
| `403` | Forbidden | Invalid API key |
| `500` | Server Error | Internal processing error |

---

## 🔒 Security

- ✅ API key required for all requests
- ✅ Keys validated via `x-api-key` header
- ✅ No API key stored in code (environment variables)
- ✅ CORS enabled for web interface
- ✅ Input validation on all endpoints

---

## 🧪 Testing

### Test with Sample Audio

```bash
# Using the quick test script
python quick_test.py training_data/ai_generated/english_00001.mp3
```

### Test API Endpoint

```bash
# Health check
curl http://localhost:8000/health

# Voice detection
python test_api.py sample.mp3 AVA-2026-910728
```

---

## 📁 Project Structure

```
voice-detection-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   └── models.py            # Request/response models
├── utils/
│   ├── audio_processor.py   # Audio conversion (ffmpeg)
│   ├── feature_extractor.py # Feature extraction (librosa)
│   └── classifier.py        # ML classification
├── scripts/
│   ├── download_dataset.py  # Download Kaggle dataset
│   ├── generate_ai_samples.py # Generate AI voices
│   └── train_model.py       # Train the model
├── models/
│   └── voice_classifier.pkl # Trained model (712 KB)
├── static/
│   └── index.html           # Web interface
├── training_data/
│   ├── ai_generated/        # AI voice samples
│   └── human/               # Human voice samples
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

---

## 🐛 Troubleshooting

### "No module named 'aifc'"
Fixed! We use ffmpeg for audio conversion instead of librosa's built-in loader.

### "Invalid API key"
Check that:
1. Server is running and shows the API key in console
2. You're using the correct key in `x-api-key` header
3. `.env` file has the correct `API_KEY` value

### "Failed to process audio"
Ensure:
1. ffmpeg is installed: `brew install ffmpeg` (macOS)
2. Audio file is valid MP3/WAV/M4A
3. Audio is between 0.5s and 300s duration

### Low accuracy after training
- Add more diverse samples
- Balance AI/Human samples (equal counts)
- Use multiple AI voice generators
- Include samples from all target languages

---

## 💡 Pro Tips

### For Best Accuracy:
✅ **Balance is key**: Equal AI and Human samples  
✅ **Diversity wins**: Mix languages, voices, styles  
✅ **Quality matters**: Clear audio, 3-10 seconds  
✅ **Test often**: Validate accuracy after training  

### For Hackathon Success:
🏆 Use the pre-trained model (100% test accuracy)  
🏆 Demonstrate multilingual support  
🏆 Show the web interface for live demos  
🏆 Explain the language-agnostic approach  

---

## 📝 API Key

On startup, check the console for your API key:
```
============================================================
🎙️  Voice Detection API Starting...
============================================================
API Key: AVA-2026-910728
Model Path: models/voice_classifier.pkl
Sample Rate: 16000 Hz
============================================================
```

Use this key in all API requests!

---

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Report issues
- Suggest improvements
- Add new features
- Improve documentation

---

## 📄 License

MIT License - Built for Hackathon 2026

---

## 🎉 Acknowledgments

- **Kaggle** - Indian Languages Audio Dataset
- **Google TTS** - AI voice generation
- **scikit-learn** - Machine learning framework
- **FastAPI** - Modern web framework
- **librosa** - Audio analysis library

---

## 📞 Support

For questions or issues:
1. Check this README
2. Review the code comments
3. Test with provided samples
4. Check server logs for errors

---

**Built with ❤️ for AVA Hackathon 2026**

**Ready to detect AI voices across all languages! 🚀**
