import librosa
import numpy as np
import aubio
import pitch
import soundfile as sf
from IPython.display import Audio
import aubio
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play
import pyaudio


def extract_vocals(filename):
    y, sr = librosa.load(filename)
    S_full, phase = librosa.magphase(librosa.stft(y))
    S_filter = librosa.decompose.nn_filter(S_full,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr)))

    S_filter = np.minimum(S_full, S_filter)
    margin_i, margin_v = 2, 10
    power = 2

    mask_i = librosa.util.softmask(S_filter,
                               margin_i * (S_full - S_filter),
                               power=power)

    mask_v = librosa.util.softmask(S_full - S_filter,
                               margin_v * S_filter,
                               power=power)

    S_foreground = mask_v * S_full
    S_background = mask_i * S_full
    new_y = librosa.istft(S_foreground*phase)
    sf.write("output.wav", new_y, samplerate=sr, subtype='PCM_24')
 

def get_freqs(filename):
    y, sr = librosa.load(filename)
    hop_length = 128
    pitch_o = aubio.pitch("mcomb", hop_length, hop_length, sr)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(0.2)

    pitches = []
    total_frames = len(y) // hop_length
    for i in range(total_frames):
        frame = y[i * hop_length: (i + 1) * hop_length]
        pitch = pitch_o(frame)[0]
        pitches.append(pitch)
    return pitches

def get_framerate(filename):
    y, sr = librosa.load(filename)
    return sr
