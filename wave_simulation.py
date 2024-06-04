# Function to generate simulated sine wave samples

import math
import time

def generate_sine_wave(frequency, samples, sampling_rate):
    audio_samples = []
    for n in range(samples):
        t = n / sampling_rate
        sine_value = 0.5 * math.sin(2 * math.pi * frequency * t)
        audio_samples.append(sine_value)
        time.sleep_us(int(1e6 / sampling_rate))  # Microsecond delay
    return audio_samples