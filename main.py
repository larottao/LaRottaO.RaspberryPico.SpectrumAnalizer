import wave_simulation
import freq_analysis
import normalization
import sample_windowing
import helpers

# Constants
FREQUENCY =  250
SAMPLES = 256  # Increased number of samples
SAMPLING_RATE = 48000  # Total number of samples per second

# Frequencies to analyze
TARGET_FREQUENCIES = [125, 250, 375, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000, 20000]

# Main Loop

helpers.print_bins(SAMPLING_RATE, SAMPLES, TARGET_FREQUENCIES)
audio_samples = wave_simulation.generate_sine_wave(FREQUENCY, SAMPLES, SAMPLING_RATE)
windowed_samples = sample_windowing.kaiser_window(audio_samples)
normalized_samples = normalization.normalize_samples(windowed_samples)
intensities = freq_analysis.analyze_frequencies(normalized_samples, SAMPLING_RATE, TARGET_FREQUENCIES)
helpers.print_intensities(FREQUENCY, SAMPLES, SAMPLING_RATE, TARGET_FREQUENCIES, intensities)





    
    

