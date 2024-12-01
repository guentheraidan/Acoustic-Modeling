class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def analyze_file(self, file_name):
        # if the file is a .mp3 file, convert to .wav
        if file_name[-4::] == '.mp3':
            self.model.mp3_to_wav(file_name)
        # if the file is a .wav file, send as is
        elif file_name[-4::] == '.wav':
            self.model.set_file_name(file_name)

        self.model.channel_handler() # convert multiple channels to mono
        self.model.compute_frequency() # get spectrogram data

        # access values to display data and create waveform and frequency graphs
        self.view.time = self.model.time
        self.view.data = self.model.data
        self.view.length = self.model.length
        self.view.rfrequency = self.model.get_highest_resonance()
        self.view.sample_rate = self.model.sample_rate

        # access time array for RT60 graphs
        self.view.t = self.model.t

        # access values for low, mid, and high RT60 graphs
        #   points_[low/mid/high] will hold three points: [0] = max, [1] = max less 5, [2] = max less 25
        #     each point will have two values: [0] = time (s), [1] = value (dB)
        self.view.data_in_db_low, self.view.points_low, rt60_low = self.model.compute_rt60(250)
        self.view.data_in_db_mid, self.view.points_mid, rt60_mid = self.model.compute_rt60(1000)
        self.view.data_in_db_high, self.view.points_high, rt60_high = self.model.compute_rt60(5000)

        # average RT60 values and compute less 0.5
        self.view.difference = self.model.compute_difference(rt60_low, rt60_mid, rt60_high)