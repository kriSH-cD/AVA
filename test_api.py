#!/usr/bin/env python3
"""Test script for Voice Detection API."""
import base64
import json
import sys
from pathlib import Path

def test_api_with_file(mp3_file_path: str, api_key: str):
    """Test the API with a local MP3 file."""
    import requests
    
    # Read and encode MP3 file
    with open(mp3_file_path, 'rb') as f:
        mp3_bytes = f.read()
        base64_audio = base64.b64encode(mp3_bytes).decode('utf-8')
    
    # Prepare request
    url = "http://localhost:8000/api/voice-detection"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "audio_base64": base64_audio
    }
    
    print(f"🧪 Testing with file: {mp3_file_path}")
    print(f"📦 File size: {len(mp3_bytes)} bytes")
    print(f"📡 Sending request...")
    
    # Send request
    response = requests.post(url, headers=headers, json=payload)
    
    # Display results
    print(f"\n📊 Response Status: {response.status_code}")
    print(f"📄 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()


def test_health_check():
    """Test the health check endpoint."""
    import requests
    
    url = "http://localhost:8000/health"
    print("🏥 Testing health check endpoint...")
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()


if __name__ == "__main__":
    print("=" * 60)
    print("🎙️  Voice Detection API - Test Script")
    print("=" * 60)
    
    # First test health
    print("\n1️⃣  Health Check")
    print("-" * 60)
    try:
        health = test_health_check()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("\n⚠️  Make sure the API server is running!")
        print("   Run: ./start.sh")
        sys.exit(1)
    
    # Then test with file if provided
    if len(sys.argv) > 1:
        mp3_file = sys.argv[1]
        api_key = sys.argv[2] if len(sys.argv) > 2 else "AVA-2026-847392"
        
        print(f"\n2️⃣  Voice Detection Test")
        print("-" * 60)
        try:
            result = test_api_with_file(mp3_file, api_key)
            print("\n✅ Test completed successfully!")
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            sys.exit(1)
    else:
        print("\n💡 To test with an MP3 file:")
        print("   python test_api.py <path_to_mp3> [api_key]")
    
    print("\n" + "=" * 60)
