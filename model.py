from scipy.io import wavfile
from scipy.signal import welch
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from os import path

class Model:
    def __init__(self):
        self.wav_file_name = None # audio file name (if .mp3, converted to .wav)
        self.sample_rate = None # sample rate (Hz)
        self.data = None # raw audio data
        self.time = None # time (s)
        self.length = None # audio duration (s)
        self.spectrum = None # 2D NumPy array of spectrogram PSD
        self.freqs = None # 1D NumPy array of spectrogram frequency bins (Hz)
        self.t = None # 1D NumPy array of time bins (s)
        self.im = None # spectrogram image

    def set_file_name(self, file_name):
        self.wav_file_name = file_name

    def mp3_to_wav(self, mp3_file_name):
        self.wav_file_name = path.splitext(mp3_file_name)[0] + ".wav" # create .wav destination name
        #print(f"Converting {mp3_file_name} to {self.wav_file_name}")
        sound = AudioSegment.from_mp3(mp3_file_name) # load .mp3 file into AudioSegment
        sound.export(self.wav_file_name, format="wav") # convert and save as .wav file

    def channel_handler(self):
        self.sample_rate, self.data = wavfile.read(self.wav_file_name) # analyze .wav file

        if len(self.data.shape) > 1:
            #print(f"Converted {self.data.shape[1]} channels to mono")
            self.data = np.mean(self.data, axis=1) # if multiple channels, average channels to convert to mono

        self.length = round(self.data.shape[0] / self.sample_rate, 2)
        self.time = np.linspace(0., self.length, self.data.shape[0])
    
    def compute_frequency(self):
        # computes spectrogum spectrum, frequencies, times, and image
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

    def get_highest_resonance(self):
        frequencies, power = welch(self.data, self.sample_rate, nperseg=4096) # compute PSD using Welch's method
        highest_resonance = frequencies[np.argmax(power)] # find highest frequency based on index of highest power
        highest_resonance = round(highest_resonance, 2)
        return highest_resonance

    def find_target_frequency(self, target_freq):
        for freq in self.freqs:
            if freq > target_freq:
                break
        return freq # return target frequency

    def frequency_check(self, freq):
        target_frequency = self.find_target_frequency(freq) # find closest target frequency
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0] # get index of target frequency
        data_for_frequency = self.spectrum[index_of_frequency] # extract spectrum data for target frequency
        data_in_db = 10 * np.log10(data_for_frequency) # convert spectrum data to dB
        return data_in_db
    
    def find_nearest_value(self, array, value):
        array = np.asarray(array) # convert to NumPy array
        idx = (np.abs(array - value)).argmin() # find index of smallest absolute difference
        return array[idx]

    def compute_rt60(self, freq=1000):
        # stores time and dB for max, max less 5, and max less 25 points
        points = [None, None, None]

        data_in_db = self.frequency_check(freq)

        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        #print(f"\nIndex: {index_of_max}")
        #print(f"Time at index: {self.t[index_of_max]}")
        #print(f"Data at index: {data_in_db[index_of_max]}")
        points[0] = [self.t[index_of_max], data_in_db[index_of_max]] # store time and dB for max point

        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5) # get index where value is 5 dB below max
        points[1] = [self.t[index_of_max_less_5], data_in_db[index_of_max_less_5]] # store time and dB for max less 5 point

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25) # get index where value is 25 dB below max
        points[2] = [self.t[index_of_max_less_25], data_in_db[index_of_max_less_25]] # store time and dB for max less 25 point

        # calculate RT20 value and convert to RT60
        rt20 = (self.t[index_of_max_less_25] - self.t[index_of_max_less_5])[0]
        rt60 = 3 * rt20

        return data_in_db, points, rt60
    
    def compute_difference(self, rt60_low, rt60_mid, rt60_high):
        difference = (rt60_low + rt60_mid + rt60_high) / 3.0 # average RT60 values
        difference -= 0.5 # subtract optimum reverb time for voice intelligibility
        #print(f"\nDifference: {difference}")
        return difference