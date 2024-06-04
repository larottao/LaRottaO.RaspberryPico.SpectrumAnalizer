import math
import time

# Constants
FREQUENCY = 250 
SAMPLES = 256  # Increased number of samples
SAMPLING_RATE = 48000  # Total number of samples per second

# Frequencies to analyze
TARGET_FREQUENCIES = [30, 60, 125, 250, 375, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000, 20000]

# Maximum expected intensity
MAXIMUM_EXPECTED_INTENSITY = 100

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
    return (intensity / MAXIMUM_EXPECTED_INTENSITY) * 8 if intensity < MAXIMUM_EXPECTED_INTENSITY else 8

# Hamming window function
def hamming_window(samples):
    windowed_samples = []
    for n in range(len(samples)):
        window_value = 0.54 - 0.46 * math.cos(2 * math.pi * n / (len(samples) - 1))
        windowed_samples.append(samples[n] * window_value)
    return windowed_samples

# Kaiser window function
def kaiser_window(samples, beta=5):
    windowed_samples = []
    for n in range(len(samples)):
        arg = 1 - ((n - (len(samples) - 1) / 2) / ((len(samples) - 1) / 2)) ** 2
        bessel = math.sqrt(math.pi) * math.e ** (1 / beta) / (2 * beta)
        window_value = bessel * math.sqrt(arg)
        windowed_samples.append(samples[n] * window_value)
    return windowed_samples

def print_bins():
    
    #Bin frequency= Sampling rate​/Number of samples
    #Each bin will correspond to a frequency range determined by this formula.
    #For example, if you have 256 samples and a sampling rate of 48000 Hz, each frequency bin will cover:
    #48000256≈187.5 Hz25648000​≈187.5 Hz

    # Calculate frequency range per bin
    bin_frequency = SAMPLING_RATE / SAMPLES

    # Calculate bin indices for target frequencies
    bin_indices = [round(freq / bin_frequency) for freq in TARGET_FREQUENCIES]

    print("Bin indices for target frequencies:")
    for freq, index in zip(TARGET_FREQUENCIES, bin_indices):
        print(f"Frequency {freq} Hz: Bin index {index}")
    print(f"\n")

# Main Loop

print_bins()

audio_samples = generate_sine_wave(FREQUENCY, SAMPLES, SAMPLING_RATE)
windowed_samples = kaiser_window(audio_samples)
normalized_samples = normalize_samples(windowed_samples)
intensities = analyze_frequencies(normalized_samples, SAMPLING_RATE, TARGET_FREQUENCIES)


print(f"INPUT FREQUENCY: {FREQUENCY}")
print(f"SAMPLES: {SAMPLES}")
print(f"SAMPLING_RATE: {SAMPLING_RATE}")
print(f"\n")

# Print the intensities for the target frequencies
for freq in TARGET_FREQUENCIES:
    intensity = intensities[freq]
    normalized_intensity = normalize_intensity(intensity)
    print(f"Frequency {freq} Hz: Intensity {intensity}, Normalized Intensity {normalized_intensity:.2f}")
    
    

