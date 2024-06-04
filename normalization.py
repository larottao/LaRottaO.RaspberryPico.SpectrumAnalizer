# Maximum expected intensity
MAXIMUM_EXPECTED_INTENSITY = 100

# Normalize samples for FFT
def normalize_samples(samples):
    min_sample = min(samples)
    max_sample = max(samples)
    normalized = [(sample - min_sample) / (max_sample - min_sample) * 2 - 1 for sample in samples]
    return normalized

# Normalize intensity to range 0-8 where 0 is 0 and max_intensity is 100
def normalize_intensity(intensity):
    return (intensity / MAXIMUM_EXPECTED_INTENSITY) * 8 if intensity < MAXIMUM_EXPECTED_INTENSITY else 8