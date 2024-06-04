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
    
    for freq, index in zip(target_frequencies, bin_indices):
        if(index == 0):
            print(f"Frequency {freq} Hz: Bin index {index}")   
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
        if(normalized_intensity > 1.0):
            print(f"Frequency {freq} Hz: Intensity {intensity}, Normalized Intensity {normalized_intensity}")