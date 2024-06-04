# Perform FFT and get the intensity of target frequencies

import fft_imp

def analyze_frequencies(audio_samples, sampling_rate, target_frequencies):
    fft_result = fft_imp.fft(audio_samples)
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