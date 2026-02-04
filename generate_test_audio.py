#!/usr/bin/env python3
"""
Generate a simple test audio file for API testing.
This creates a short sine wave audio file.
"""
import numpy as np
import soundfile as sf

# Generate a 3-second sine wave at 440 Hz (A4 note)
duration = 3  # seconds
sample_rate = 16000
frequency = 440  # Hz

# Create time array
t = np.linspace(0, duration, int(sample_rate * duration))

# Generate sine wave
audio = 0.5 * np.sin(2 * np.pi * frequency * t)

# Save as WAV
output_file = "test_sample.wav"
sf.write(output_file, audio, sample_rate)

print(f"✅ Generated test audio: {output_file}")
print(f"   Duration: {duration}s")
print(f"   Sample rate: {sample_rate} Hz")
print(f"   Frequency: {frequency} Hz")
print("\n💡 Convert to MP3 with:")
print(f"   ffmpeg -i {output_file} test_sample.mp3")
