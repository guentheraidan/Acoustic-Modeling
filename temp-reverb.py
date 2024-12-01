import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def channel_handler(wav_file_name):
    sample_rate, data = wavfile.read(wav_file_name) # analyze .wav file

    if len(data.shape) > 1: # if multiple channels
        #print(f"DEBUG: Converted {data.shape[1]} channels to mono")
        data = np.mean(data, axis=1) # average channels to convert to mono

    length = data.shape[0] / sample_rate
    #print("LENGTH  " + str(length))
    time = np.linspace(0., length, data.shape[0]) # create time array

    #print(f"DEBUG: number of channels = {data.shape[len(data.shape) -1]}")
    #print(f"DEBUG: sample rate = {sample_rate}Hz")
    #print(f"DEBUG: length = {length}s")

    return sample_rate, data, time

def compute_frequency(data, sample_rate):
    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    return spectrum, freqs, t, im

def find_target_frequency(freqs):
    for x in freqs:
        if x > 5000:
            break
    return x

def frequency_check(freqs, spectrum):
    # identify a frequency to check
    #print(freqs)
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    # find sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    # change a digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun

sample_rate, data, time = channel_handler('Clap_AulaMagna_1.wav')

spectrum, freqs, t, im = compute_frequency(data, sample_rate)
data_in_db = frequency_check(freqs, spectrum)

plt.figure(2)

plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')

# find a index of a max value
index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
print(f"data: {data_in_db}")
print(f"\nindex: {index_of_max}")
print(f"t index: {t[index_of_max]}")
print(f"data index: {data_in_db[index_of_max]}")
plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

# slice our array from a max value
sliced_array = data_in_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5

# find a nearest value of less 5 dB
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

# slide array from a max-5dB
value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
#print(f'rt20= {rt20}')
rt60 = 3 * rt20
#print(f'rt60= {rt60}')
plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
plt.grid()
plt.show()

#print(f'The RT60 reverb time at freq {int(target_frequency)} Hz is {round(abs(rt60), 2)} seconds')