'''
All of the data associated with the sound file will be held
as a member variable here. This means you should be able to access
most functions from the Controller class without passing parameters,
except for a few that require outside input.

This means that the Controller will need to:

- Create a model object with a file name (can be mp3 or wav)
- Check that the file is an mp3
    if model.file_name[-4::] == '.mp3':
        file_name = model.mp3_to_wav(file_name)
- Call compute_frequency()
- Call frequency_check()
'''

from scipy.io import wavfile
from scipy.signal import welch
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from os import path

class Model:
    def __init__(self):
        self.wav_file_name = None # .wav file name
        self.sample_rate = None
        self.data = None
        self.time = None
        self.length = None
        self.spectrum = None
        self.freqs = None
        self.t = None # time array
        self.im = None

        self.data_in_db = [None, None, None]
        self.index_of_frequency = [None, None, None]
        self.low_points = [[None, None], [None, None], [None, None]]
        self.mid_points = [[None, None], [None, None], [None, None]]
        self.high_points = [[None, None], [None, None], [None, None]]
        self.rt60 = [None, None, None]
        self.difference = None

    def set_file_name(self, file_name):
        self.wav_file_name = file_name

# FROM TEMP-PLOTTING.PY
    def mp3_to_wav(self, mp3_file_name):
        self.wav_file_name = path.splitext(mp3_file_name)[0] + ".wav" # create .wav destination name
        print(f"DEBUG: Converting {mp3_file_name} to {self.wav_file_name}")

        sound = AudioSegment.from_mp3(mp3_file_name)
        sound.export(self.wav_file_name, format="wav")

    def channel_handler(self):
        self.sample_rate, self.data = wavfile.read(self.wav_file_name) # analyze .wav file

        if len(self.data.shape) > 1: # if multiple channels
            print(f"DEBUG: Converted {self.data.shape[1]} channels to mono")
            self.data = np.mean(self.data, axis=1) # average channels to convert to mono

        self.length = round(self.data.shape[0] / self.sample_rate, 2)
        self.time = np.linspace(0., self.length, self.data.shape[0]) # create time array

        print(f"DEBUG: number of channels = {self.data.shape[len(self.data.shape) -1]}")
        print(f"DEBUG: sample rate = {self.sample_rate}Hz")
        print(f"DEBUG: length = {self.length}s")
    
    def compute_frequency(self):
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

    def get_highest_resonance(self):
        frequencies, power = welch(self.data, self.sample_rate, nperseg=4096)
        __highest_resonance = frequencies[np.argmax(power)]
        highest_resonance = round(__highest_resonance, 2)
        return highest_resonance

    def get_length(self):
        return self.length
    
    def get_time(self):
        return self.time
    
    def get_data(self):
        return self.data
    
    def get_sample_rate(self):
        return self.sample_rate
    
# FROM TEMP-REVERB.PY
    def find_target_frequency(self, target):
        for x in self.freqs:
            if x > target:
                break
        return x # return target frequency

    def frequency_check(self):
        # identify a frequency to check
        #print(freqs)
        target_frequency = [None, None, None]
        target_frequency[0] = self.find_target_frequency(250)
        target_frequency[1] = self.find_target_frequency(1000)
        target_frequency[2] = self.find_target_frequency(5000)

        data_for_frequency = [None, None, None]
        for i in range(0, len(target_frequency)):
            self.index_of_frequency[i] = np.where(self.freqs == target_frequency[i])[0][0]
            data_for_frequency[i] = self.spectrum[self.index_of_frequency[i]]
            self.data_in_db[i] = 10 * np.log10(data_for_frequency[i])

        #index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
        # find sound data for a particular frequency
        #data_for_frequency = self.spectrum[index_of_frequency]
        # change a digital signal for a values in decibels
        #data_in_db = 10 * np.log10(data_for_frequency)

    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def compute_rt60(self):
        index_of_max = [None, None, None]
        value_of_max = [None, None, None]
        for i in range(0, len(self.data_in_db)):
            index_of_max[i] = np.argmax(self.data_in_db[i])
            value_of_max[i] = self.data_in_db[i][index_of_max[i]]
            #plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        print(f"SELF.DATA: {self.data_in_db}")
        print(f"\n\nINDEX: {index_of_max}")
        self.low_points[0] = [self.t[index_of_max[0]], self.data_in_db[index_of_max[0]]]
        self.mid_points[0] = [self.t[index_of_max[1]], self.data_in_db[index_of_max[1]]]
        self.high_points[0] = [self.t[index_of_max[2]], self.data_in_db[index_of_max[2]]]

        sliced_array = [None, None, None]
        value_of_max_less_5 = [None, None, None]
        index_of_max_less_5 = [None, None, None]
        value_of_max_less_25 = [None, None, None]
        index_of_max_less_25 = [None, None, None]
        for i in range(0, len(self.data_in_db)):
            sliced_array[i] = self.data_in_db[i][index_of_max[i]:]

            value_of_max_less_5[i] = value_of_max[i] - 5
            value_of_max_less_5[i] = self.find_nearest_value(sliced_array[i], value_of_max_less_5[i])
            index_of_max_less_5[i] = np.where(self.data_in_db[i] == value_of_max_less_5[i])
            value_of_max_less_25[i] = value_of_max[i] = 25

            value_of_max_less_25[i] = self.find_nearest_value(sliced_array[i], value_of_max_less_25)
            index_of_max_less_25[i] = np.where(self.data_in_db[i] == value_of_max_less_25[i])

        self.low_points[1] = [self.t[index_of_max_less_5[0]], self.data_in_db[index_of_max_less_5[0]]]
        self.mid_points[1] = [self.t[index_of_max_less_5[1]], self.data_in_db[index_of_max_less_5[1]]]
        self.high_points[1] = [self.t[index_of_max_less_5[2]], self.data_in_db[index_of_max_less_5[2]]]

        self.low_points[2] = [self.t[index_of_max_less_25[0]], self.data_in_db[index_of_max_less_25[0]]]
        self.mid_points[2] = [self.t[index_of_max_less_25[1]], self.data_in_db[index_of_max_less_25[1]]]
        self.high_points[2] = [self.t[index_of_max_less_25[2]], self.data_in_db[index_of_max_less_25[2]]]

        rt20 = [None, None, None]
        for i in range(len(rt20)):
            rt20[i] = (self.t[index_of_max_less_5[i]] - self.t[index_of_max_less_25[i]])
            self.rt60[i] = 3 * rt20[i]
            print(f"{i} RT60 = {self.rt60[i]}")

        for value in self.rt60:
            self.difference += value
        self.difference /= len(self.rt60)
        print(f"difference: {self.difference}")