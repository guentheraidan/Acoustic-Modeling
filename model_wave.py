# pip install scipy
from scipy.io import wavfile

def import_audio():
    file_path = input("Enter the file name of an audio file: ")
    sample_rate, audio_data = wavfile.read(file_path)

    # Debugging statements
    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Audio Data Type: {audio_data.dtype}")
    print(f"Audio Data Shape: {audio_data.shape}")

def main():
    import_audio()

main()