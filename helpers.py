import normalization

def print_bins(sampling_rate, samples, target_frequencies):
    
    #Bin frequency= Sampling rate​/Number of samples
    #Each bin will correspond to a frequency range determined by this formula.
    #For example, if you have 256 samples and a sampling rate of 48000 Hz, each frequency bin will cover:
    #48000256≈187.5 Hz25648000​≈187.5 Hz

    # Calculate frequency range per bin
    bin_frequency = sampling_rate / samples

    # Calculate bin indices for target frequencies
    bin_indices = [round(freq / bin_frequency) for freq in target_frequencies]

    print("Bin indices for target frequencies:")
    for freq, index in zip(target_frequencies, bin_indices):
        print(f"Frequency {freq} Hz: Bin index {index}")
    
    frequency_resolution = sampling_rate / samples

    # Original target frequencies below 500 Hz
    original_frequencies_below_500 = [30, 60, 125, 250, 375]

    # Adjust frequencies to align with frequency resolution
    adjusted_frequencies_below_500 = [
        int(frequency_resolution * round(freq / frequency_resolution)) 
        for freq in original_frequencies_below_500
        ]
    
    print(f"\n")
    print("Adjusted Frequencies Below 500 Hz:", adjusted_frequencies_below_500)
    print(f"\n")
    
def print_intensities(frequency, samples, sampling_rate, target_frequencies, intensities):
    
    print(f"INPUT FREQUENCY: {frequency}")
    print(f"SAMPLES: {samples}")
    print(f"SAMPLING_RATE: {sampling_rate}")
    print(f"\n")

    # Print the intensities for the target frequencies
    for freq in target_frequencies:
        intensity = intensities[freq]
        normalized_intensity = normalization.normalize_intensity(intensity)
        print(f"Frequency {freq} Hz: Intensity {intensity}, Normalized Intensity {normalized_intensity:.2f}")