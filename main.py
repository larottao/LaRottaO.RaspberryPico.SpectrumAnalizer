import math
import time
from machine import Pin, ADC

# Constants
ADC_RESOLUTION = 65535
VOLTAGE_REF = 3.3
PEAK_VOLTAGE = 2.5
FREQUENCY = 30
SAMPLES = 256
SAMPLING_RATE = 48000  # Total number of samples per second
MAXIMUM_EXPECTED_INTENSITY = 128

# Frequencies to analyze
TARGET_FREQUENCIES = [30, 60, 125, 250, 375, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000, 20000]


# Function to generate simulated sine wave samples
def generate_sine_wave(frequency, samples, sampling_rate):
    audio_samples = []
    for n in range(samples):
        t = n / sampling_rate
        sine_value = 0.5 * math.sin(2 * math.pi * frequency * t)
        audio_samples.append(sine_value)
        time.sleep_us(int(1e6 / sampling_rate))  # Microsecond delay
    return audio_samples

# Custom FFT implementation
def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [complex(math.cos(-2 * math.pi * k / N), math.sin(-2 * math.pi * k / N)) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

# Perform FFT and get the intensity of target frequencies
def analyze_frequencies(audio_samples, sampling_rate, target_frequencies):
    fft_result = fft(audio_samples)
    magnitudes = [abs(x) for x in fft_result]
    freq_resolution = sampling_rate / len(audio_samples)

    intensities = {}
    for freq in target_frequencies:
        index = int(freq / freq_resolution)
        if index < len(magnitudes):
            intensities[freq] = magnitudes[index]
        else:
            intensities[freq] = 0  # If the frequency is out of the range
    
    return intensities

# Normalize samples for FFT
def normalize_samples(samples):
    min_sample = min(samples)
    max_sample = max(samples)
    normalized = [(sample - min_sample) / (max_sample - min_sample) * 2 - 1 for sample in samples]
    return normalized

# Normalize intensity to range 0-8 where 0 is 0 and max_intensity is 100
def normalize_intensity(intensity):
    return (intensity / MAXIMUM_EXPECTED_INTENSITY) * 8

# Example usage
audio_samples = generate_sine_wave(FREQUENCY, SAMPLES, SAMPLING_RATE)
normalized_samples = normalize_samples(audio_samples)

print(f"INPUT FREQUENCY: {FREQUENCY}")
print(f"SAMPLES: {SAMPLES}")
print(f"SAMPLING_RATE: {SAMPLING_RATE}")
print(f"\n")

intensities = analyze_frequencies(normalized_samples, SAMPLING_RATE, TARGET_FREQUENCIES)

# Print the intensities for the target frequencies
for freq in TARGET_FREQUENCIES:
    intensity = intensities[freq]
    normalized_intensity = normalize_intensity(intensity)
    print(f"Frequency {freq} Hz: Intensity {intensity}, Normalized Intensity {normalized_intensity:.2f}")
