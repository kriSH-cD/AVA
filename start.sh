#!/bin/bash

# Voice Detection API - Start Script

echo "🎙️  Starting Voice Detection API..."
echo "=================================="

# Activate virtual environment
source venv/bin/activate

# Display API key
echo ""
echo "📋 Configuration:"
echo "   API Key: $(grep API_KEY .env | cut -d'=' -f2)"
echo "   Host: 0.0.0.0"
echo "   Port: 8000"
echo ""

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
