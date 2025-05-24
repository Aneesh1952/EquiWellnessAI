from pydub.generators import Sine
import os

def generate_wav(filename, duration=2, freq=440, sample_rate=16000):
    # Generate a sine wave audio segment
    sine_wave = Sine(freq).to_audio_segment(duration=duration * 1000)  # duration in milliseconds
    sine_wave = sine_wave.set_frame_rate(sample_rate).set_sample_width(2).set_channels(1)
    sine_wave.export(filename, format="wav")

# Ensure the 'recordings' directory exists
os.makedirs("recordings", exist_ok=True)

# List of file paths for the WAV files
file_paths = [
    "recordings/voice_feedback_001.wav",
    "recordings/voice_feedback_002.wav",
    "recordings/voice_feedback_003.wav"
]

for file in file_paths:
    generate_wav(file)
    print(f"Generated {file}")

print("All sample WAV files have been generated in the 'recordings' directory.")
