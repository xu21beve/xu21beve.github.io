import wave
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample

# Sample Koala object
class Koala:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

# Input path (existing WAV file)
input_path = 'input.wav'

# Output path (new WAV file)
output_path = 'output.wav'

# Create a Koala object with a specific sample rate
koala = Koala(16000)  # New sample rate

# Read the existing WAV file
rate, audio_data = wavfile.read(input_path)

# Resample the audio data to match the new frame rate
resampled_audio = resample(audio_data, int(len(audio_data) * (koala.sample_rate / rate)))

# Ensure the resampled audio is in 16-bit PCM format
resampled_audio = resampled_audio.astype(np.int16)

# Write the resampled audio data to the new WAV file
with wave.open(output_path, 'wb') as output_file:
    output_file.setnchannels(1)
    output_file.setsampwidth(2)
    output_file.setframerate(koala.sample_rate)
    output_file.writeframes(resampled_audio.tobytes())

print(f"New WAV file '{output_path}' created with frame rate {koala.sample_rate}.")
