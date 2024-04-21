import aubio
import numpy as np
import pyaudio

import time
import argparse

import queue

import music21

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
parser.add_argument("-volume", required=False, type=float, help="Volume Threshold")
args = parser.parse_args()

if not args.input:
		print("No input device specified. Printing list of input devices now: ")
		p = pyaudio.PyAudio()
		for i in range(p.get_device_count()):
				print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))
		print("Run this program with -input 1, or the number of the input you'd like to use.")
		exit()

if not args.volume:
		print("No volume threshold specified. Select a float between 0-1 for specific device: ")
		print("Run this program with -volume 0.08, or the float of the threshold you'd like to use.")
		exit()

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream
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


def get_current_freq(volume_thresh=args.volume, printOut=False):

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
					q.put(current_pitch.frequency)



def get_mean_freq(volume_thresh=args.volume):

	current_pitch = music21.pitch.Pitch()

	# Start Timer
	start_time = time.time() 

	freqs = []
	while time.time() - start_time < 3:

			data = stream.read(1024, exception_on_overflow=False)
			samples = np.fromstring(data,
															dtype=aubio.float_type)
			pitch = pDetection(samples)[0]

			volume = np.sum(samples**2)/len(samples) * 100

			if pitch and volume > volume_thresh:  # adjust with your mic!
					current_pitch.frequency = pitch
					freqs.append(pitch)

			else:
					continue
	
	# return [np.min(freqs), np.max(freqs)]
	if freqs:
		return np.mean(freqs)
	else:
		return -1

		

if __name__ == '__main__':

	low_calced = True
	high_calced = True

	song_read = True

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

	print("Low: ", low_frequency)
	print("High: ", high_frequency)

"""
END
"""