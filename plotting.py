from scipy.io import wavfile
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

wav_fname = 'Clap_AulaMagna_1.wav'
sample_rate, data = wavfile.read(wav_fname)
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

print(f"number of channels = {data.shape[len(data.shape) -1]}")
print(f"sample rate = {sample_rate}Hz")
length = data.shape[0] / sample_rate
print(f"length = {length}s")

time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label = "Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

cbar = plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cbar.set_label('Intensity (dB)')
plt.show()