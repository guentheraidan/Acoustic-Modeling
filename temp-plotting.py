from scipy.io import wavfile
from scipy.signal import welch
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from os import path

def mp3_to_wav(mp3_file_name):
    wav_file_name = path.splitext(mp3_file_name)[0] + ".wav" # create .wav destination name
    print(f"DEBUG: Converting {mp3_file_name} to {wav_file_name}")

    sound = AudioSegment.from_mp3(mp3_file_name)
    sound.export(wav_file_name, format="wav")

    return wav_file_name

def channel_handler(wav_file_name):
    sample_rate, data = wavfile.read(wav_file_name) # analyze .wav file

    if len(data.shape) > 1: # if multiple channels
        print(f"DEBUG: Converted {data.shape[1]} channels to mono")
        data = np.mean(data, axis=1) # average channels to convert to mono

    length = data.shape[0] / sample_rate
    time = np.linspace(0., length, data.shape[0]) # create time array

    print(f"DEBUG: number of channels = {data.shape[len(data.shape) -1]}")
    print(f"DEBUG: sample rate = {sample_rate}Hz")
    print(f"DEBUG: length = {length}s")

    return sample_rate, data, time

def plot_waveform(data, time):
    plt.figure()
    plt.plot(time, data)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Waveform Graph")
    plt.show()

def plot_frequency(sample_rate, data):
    plt.figure()
    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    cbar = plt.colorbar(im)
    cbar.set_label('Intensity (dB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title("Frequency Graph")
    plt.show()

    return spectrum, freqs, t

def get_highest_resonance(sample_rate, data):
    frequencies, power = welch(data, sample_rate, nperseg=4096)
    highest_resonance = frequencies[np.argmax(power)]
    return round(highest_resonance, 2)

def get_length(time):
    return time[-1].round(2) # length of file (seconds)

if __name__ == '__main__':
    file_name = 'Clap_AulaMagna_1.wav' # placeholder file
    
    if file_name[-4::] == '.mp3':
        print(f"DEBUG: {file_name[-4::]}")
        file_name = mp3_to_wav(file_name)
    
    sample_rate, data, time = channel_handler(file_name)
    
    plot_waveform(data, time)
    spectrum, freqs, t = plot_frequency(sample_rate, data)

    print(f"DEBUG: length is {get_length(time)} seconds")
    print(f"DEBUG: dominant_frequency is {get_highest_resonance(sample_rate, data)} Hz")