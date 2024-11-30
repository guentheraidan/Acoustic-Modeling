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
        self.model.compute_frequency()

        # can send these variables to create graphs in View
        # and display info about the graph
        self.view.time = self.model.get_time()
        self.view.data = self.model.get_data()
        self.view.length = self.model.get_length()
        self.view.rfrequency = self.model.get_highest_resonance()

        self.view.sample_rate = self.model.get_sample_rate()
        # use this line in View (you wont need the first 3 variables):
        # spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

        # Below is for RT60 graphs. These are displayed with:
        #plt.figure(2)
        #plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        #plt.xlabel('Time (s)')
        #plt.ylabel('Power (dB)')
        #plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        #plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
        #plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
        #plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
        #plt.grid()
        #plt.show()

        self.view.t = self.model.t

        self.model.frequency_check()
        self.model.compute_rt60()

        # these are arrays ([0] = low, [1] = mid, [2] = high)
        self.view.data_in_db = self.model.data_in_db
        # these are arrays of arrays corresponding with the line: plt.plot(...)
        # [0] = t[index_of_max], [1] = data_in_db[index_of_max]
        # [0] = max, [1] = -5, [2] = -25
        # so, the line plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        # will look like: plt.plot(low_points[0][0], lowpoints[1][0])
        self.view.low_points = self.model.low_points
        self.view.mid_points = self.model.mid_points
        self.view.high_points = self.model.high_points
        # this is another array ([0] = low, [1] = mid, [2] = high)
        self.view.rt60 = self.model.rt60
        self.view.difference = self.model.difference