from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from os import path

def mp3_to_wav(mp3_file_name):
    wav_file_name = path.splitext(mp3_file_name)[0] + ".wav"
    print(f"DEBUG: Converting {mp3_file_name} to {wav_file_name}")

    # Source: https://www.geeksforgeeks.org/convert-mp3-to-wav-using-python/
    sound = AudioSegment.from_mp3(mp3_file_name)
    sound.export(wav_file_name, format="wav")

    return wav_file_name

def file_handler(wav_file_name):
    sample_rate, data = wavfile.read(wav_file_name) # analyze wav file

    if len(data.shape) > 1: # if multiple channels
        print(f"DEBUG: Converted {data.shape[1]} channels to mono")
        data = np.mean(data, axis=1) # average channels

    length = data.shape[0] / sample_rate
    time = np.linspace(0., length, data.shape[0])

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

if __name__ == '__main__':
    file_name = 'test.mp3' # placeholder file

    if file_name[-4::] == '.mp3':
        print(f"DEBUG: {file_name[-4::]}")
        file_name = mp3_to_wav(file_name)

    
    sample_rate, data, time = file_handler(file_name)
    plot_waveform(data, time)
    plot_frequency(sample_rate, data)