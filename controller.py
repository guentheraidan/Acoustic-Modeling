class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def analyze_file(self, file_name):
        # this fills the data in the model object
        if file_name[-4::] == '.mp3':
            self.model.mp3_to_wav(file_name)
        elif file_name[-4::] == '.wav':
            self.model.set_file_name(file_name)

        self.model.channel_handler()
    
    def compute_waveform(self):
        # can send these variables to create graphs in View
        # and display info about the graph
        time = self.model.get_time()
        data = self.model.get_data()
        length = self.model.get_length()
        resonance_frequency = self.model.get_highest_resonance()

    def compute_frequency(self):
        data = self.model.get_data()
        sample_rate = self.model.get_sample_rate()
        # use this line in View (you wont need the first 3 variables):
        # spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))