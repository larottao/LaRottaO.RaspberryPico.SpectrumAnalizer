import wave_simulation
import freq_analysis
import normalization
import sample_windowing
import helpers

from machine import ADC, Pin, SPI
import array
import time
import max7219


# Constants
FREQUENCY =  20
SAMPLES = 256  # Increased number of samples
SAMPLING_RATE = 96000  # Total number of samples per second

# Frequencies to analyze
#TARGET_FREQUENCIES = [125, 250, 375, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000, 20000]
TARGET_FREQUENCIES = [20,25,32,40,50,63,80,100,125,160, 200,250,315,400,500,635,800,1000,1200,1600, 2000, 2500, 3100, 4000,5000,6300,8000,10000,12000,16000,20000]

#Data input and led matrix

# SPI setup for the LED matrix display
spi = SPI(0, baudrate=115200, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
cs = Pin(15, Pin.OUT)  # Chip Select for SPI

sample_interval_us = int(1e6 / SAMPLING_RATE)

# Initialize the display
num_matrices = 4
matrix = max7219.Matrix8x8(spi, cs, num_matrices)

# Clear the display
matrix.fill(0)
matrix.show()

# Configure the analog pin (let's use ADC0 which is GP26 on the Pico)
# Input audio signal from 20 to 20.000 hz, 2.50v
# Coupled with a 10uF capacitor
adc = ADC(Pin(26))


# Function to sample the audio signal
def sample_audio(samples=SAMPLES):
    audio_samples = array.array('H')  # Use array for memory efficiency
    for _ in range(samples):
        audio_samples.append(adc.read_u16())  # Read the analog value (0-65535)
        time.sleep_us(sample_interval_us)  # Delay between samples
    return audio_samples

# Function to display intensities on the LED matrices
def display_intensities(target_frequencies, intensity_list):
    matrix.fill(0)  # Clear the display
    col = 1
    
    for freq in target_frequencies:
        intensity = intensities[freq]
        normalized_intensity = normalization.normalize_intensity(intensity)       
        for row in range(normalized_intensity):
                matrix.pixel(col, 7 - row, 1)  # Turn on the LED        
        col+=1
    
    matrix.show()
   


# Main Loop

while True:
    
    helpers.print_bins(SAMPLING_RATE, SAMPLES, TARGET_FREQUENCIES)

    #Use simulated wave
    audio_samples = wave_simulation.generate_sine_wave(FREQUENCY, SAMPLES, SAMPLING_RATE)

    #Use real wave from ADC input
    #audio_samples = sample_audio()   
    
    windowed_samples = sample_windowing.kaiser_window(audio_samples)
    normalized_samples = normalization.normalize_samples(windowed_samples)
    intensities = freq_analysis.analyze_frequencies(normalized_samples, SAMPLING_RATE, TARGET_FREQUENCIES)
    helpers.print_intensities(FREQUENCY, SAMPLES, SAMPLING_RATE, TARGET_FREQUENCIES, intensities)
    display_intensities(TARGET_FREQUENCIES, intensities)    
 
    FREQUENCY = FREQUENCY*1.25 

    if FREQUENCY >= 20000:
        FREQUENCY = 60