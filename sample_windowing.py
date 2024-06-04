import math

# Hamming window function UNUSED
def hamming_window(samples):
    windowed_samples = []
    for n in range(len(samples)):
        window_value = 0.54 - 0.46 * math.cos(2 * math.pi * n / (len(samples) - 1))
        windowed_samples.append(samples[n] * window_value)
    return windowed_samples

# Kaiser window function
def kaiser_window(samples, beta=10):
    windowed_samples = []
    for n in range(len(samples)):
        arg = 1 - ((n - (len(samples) - 1) / 2) / ((len(samples) - 1) / 2)) ** 2
        bessel = math.sqrt(math.pi) * math.e ** (1 / beta) / (2 * beta)
        window_value = bessel * math.sqrt(arg)
        windowed_samples.append(samples[n] * window_value)
    return windowed_samples