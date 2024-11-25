# pip install scipy
from scipy.io import wavfile

def import_audio():
    # This variable will be used by the UI to display the name of the file.
    # The input function will be removed and replaced by however it can be
    # inputted through the UI.
    file_name = input("Enter the file name of an audio file: ")
    try:
        # Debugging statements
        sample_rate, audio_data = wavfile.read(file_name)
        print(f"File name: {file_name}")
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Audio Data Type: {audio_data.dtype}")
        print(f"Audio Data Shape: {audio_data.shape}")
    except ValueError as e:
        print(f"Error reading .wav file: {e}")

def main():
    import_audio()

main()