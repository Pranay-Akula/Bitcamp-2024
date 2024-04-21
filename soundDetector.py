import aubio
import numpy as np
import pyaudio

import time
import argparse

import queue

import music21  # yes! new favorite library

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
args = parser.parse_args()

if not args.input:
		print("No input device specified. Printing list of input devices now: ")
		p = pyaudio.PyAudio()
		for i in range(p.get_device_count()):
				print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))
		print("Run this program with -input 1, or the number of the input you'd like to use.")
		exit()

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream.
stream = p.open(format=pyaudio.paFloat32,
								channels=1, rate=44100, input=True,
								input_device_index=args.input, frames_per_buffer=4096)
time.sleep(1)

# Aubio's pitch detection.
pDetection = aubio.pitch("default", 2048, 2048//2, 44100)
# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-40)

q = queue.Queue()


def get_current_freq(volume_thresh=0.7, printOut=False):

	current_pitch = music21.pitch.Pitch()

	while True:

			data = stream.read(1024, exception_on_overflow=False)
			samples = np.fromstring(data,
															dtype=aubio.float_type)
			pitch = pDetection(samples)[0]

			# Compute the energy (volume) of the
			# current frame.
			volume = np.sum(samples**2)/len(samples) * 100

			if pitch and volume > volume_thresh:  # adjust with your mic!
					current_pitch.frequency = pitch
			else:
					continue

			if printOut:
					print(current_pitch.frequency)

			else:
					# Puts Notes and Cents in Queue -- WILL CHANGE
					current = current_pitch.nameWithOctave
					q.put({'Note': current, 'Cents': current_pitch.microtone.cents})

def get_low_freq(volume_thresh=0.7):

	current_pitch = music21.pitch.Pitch()

	# Start Timer
	start_time = time.time() 

	while time.time() - start_time < 3:

			low_freqs = []

			data = stream.read(1024, exception_on_overflow=False)
			samples = np.fromstring(data,
															dtype=aubio.float_type)
			pitch = pDetection(samples)[0]

			volume = np.sum(samples**2)/len(samples) * 100

			if pitch and volume > volume_thresh:  # adjust with your mic!
					current_pitch.frequency = pitch
					low_freqs.append(pitch)
			else:
					continue
	
	return np.mean(low_freqs)

def get_high_freq(volume_thresh=0.7):

	current_pitch = music21.pitch.Pitch()

	# Start Timer
	start_time = time.time() 

	while time.time() - start_time < 3:

			high_freqs = []

			data = stream.read(1024, exception_on_overflow=False)
			samples = np.fromstring(data,
															dtype=aubio.float_type)
			pitch = pDetection(samples)[0]

			volume = np.sum(samples**2)/len(samples) * 100

			if pitch and volume > volume_thresh:  # adjust with your mic!
					current_pitch.frequency = pitch
					high_freqs.append(pitch)
			else:
					continue

	return np.mean(high_freqs)
		

if __name__ == '__main__':

	low_calced = True
	high_calced = True
 
	while low_calced:
		
		user_input = input("Are you ready to record your lowest pitch? (yes/no): ").strip().lower()

        # Check user's response
		if user_input == "yes":
			low_frequency = get_low_freq()
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
			high_frequency = get_high_freq()
			high_calced = False
			
		elif user_input == "no":
			continue
		else:
			print("Please respond with 'yes' or 'no'.")
			continue


	print("Vocal Range Calculated")
	print("Low: ", low_frequency)
	print("High: ", high_frequency)