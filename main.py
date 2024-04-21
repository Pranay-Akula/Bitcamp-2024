from audio_processing import *
from soundDetector import get_mean_freq
import numpy as np
filename = input("Enter the file path to a song of your choice (.wav): ")
extract_vocals(filename)
song_freqs = np.array(get_freqs("output.wav"))

# soundDetector
low_calced = True
high_calced = True

while low_calced:
    user_input = input("Are you ready to record your lowest pitch? (yes/no): ").strip().lower()
    # Check user's response
    if user_input == "yes":
        low_frequency = get_mean_freq()
        low_calced = False
        
    elif user_input == "no":
        continue
    else:
        print("Please respond with 'yes' or 'no'.")
        continue

while high_calced:
    user_input = input("Are you ready to record your highest pitch? (yes/no): ").strip().lower()

    # Check user's response
    if user_input == "yes":
        high_frequency = get_mean_freq()
        high_calced = False    
    elif user_input == "no":
        continue
    else:
        print("Please respond with 'yes' or 'no'.")
        continue
song_freqs[song_freqs > high_frequency or song_freqs < low_frequency] = 0






