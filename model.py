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

    def set_file_name(self, file_name):
        self.wav_file_name = file_name

# FROM TEMP-PLOTTING.PY
    def mp3_to_wav(self, mp3_file_name):
        self.wav_file_name = path.splitext(mp3_file_name)[0] + ".wav" # create .wav destination name
        #print(f"DEBUG: Converting {mp3_file_name} to {self.wav_file_name}")

        sound = AudioSegment.from_mp3(mp3_file_name)
        sound.export(self.wav_file_name, format="wav")

    def channel_handler(self):
        self.sample_rate, self.data = wavfile.read(self.wav_file_name) # analyze .wav file

        if len(self.data.shape) > 1: # if multiple channels
            #print(f"DEBUG: Converted {self.data.shape[1]} channels to mono")
            self.data = np.mean(self.data, axis=1) # average channels to convert to mono

        self.length = round(self.data.shape[0] / self.sample_rate, 2)
        self.time = np.linspace(0., self.length, self.data.shape[0]) # create time array

        #print(f"DEBUG: number of channels = {self.data.shape[len(self.data.shape) -1]}")
        #print(f"DEBUG: sample rate = {self.sample_rate}Hz")
        #print(f"DEBUG: length = {self.length}s")
    
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

    def frequency_check(self, freq):
        target_frequency = self.find_target_frequency(freq)
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0] 
        data_for_frequency = self.spectrum[index_of_frequency]
        data_in_db = 10 * np.log10(data_for_frequency)
        return data_in_db
    
    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def compute_rt60(self, freq=1000):
        points = [None, None, None]
        data_in_db = self.frequency_check(freq)

        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        print(f"\nindex: {index_of_max}")
        print(f"t index: {self.t[index_of_max]}")
        print(f"data index: {data_in_db[index_of_max]}")
        points[0] = [self.t[index_of_max], data_in_db[index_of_max]]

        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        points[1] = [self.t[index_of_max_less_5], data_in_db[index_of_max_less_5]]

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        points[2] = [self.t[index_of_max_less_25], data_in_db[index_of_max_less_25]]

        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]
        rt60 = 3 * rt20

        return data_in_db, points, rt60
    
    def compute_difference(self, rt60_low, rt60_mid, rt60_high):
        difference = (rt60_low + rt60_mid + rt60_high) / 3.0
        difference -= 0.5
        print(f"\ndifference: {difference}")
        return difference