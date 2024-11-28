from scipy.io import wavfile
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

wav_fname = 'Clap_AulaMagna_1.wav'
sample_rate, data = wavfile.read(wav_fname)

if len(data.shape) > 1: # if multi-channel
    print(f"Converted {data.shape[1]} channels to mono")
    data = np.mean(data, axis=1) # average channels

print(f"number of channels = {data.shape[len(data.shape) -1]}")
print(f"sample rate = {sample_rate}Hz")
length = data.shape[0] / sample_rate
print(f"length = {length}s")

time = np.linspace(0., length, data.shape[0])

plt.figure()
plt.plot(time, data)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Waveform Graph")
plt.show()

plt.figure()
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
cbar = plt.colorbar(im)
cbar.set_label('Intensity (dB)')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title("Frequency Graph")
plt.show()