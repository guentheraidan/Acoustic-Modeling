# pip install scipy
from scipy.io import wavfile

def import_audio():
    file_path = input("Enter the file name of an audio file: ")
    try:
        # Debugging statements
        sample_rate, audio_data = wavfile.read(file_path)
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Audio Data Type: {audio_data.dtype}")
        print(f"Audio Data Shape: {audio_data.shape}")
    except ValueError as e:
        print(f"Error reading .wav file: {e}")

def main():
    import_audio()

main()