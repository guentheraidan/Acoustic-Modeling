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

        # data_in_db_### is used to create the initial plot
        # points_### hold three arrays, each with two coordinates
        #    the first array is max, second is max_less_5, and third is max_less_25
        #       the first coordinate in first array replaces t[index_of_max]
        #       the second coordinate in first array replaces data_in_db[index_of_max]

        #       the first coordinate in second array replaces t[index_of_max_less_5]
        #       the second coordinate in second array replaces data_in_db[index_of_max_less_5]

        #       the first coordinate in third array replaces t[index_of_max_less_25]
        #       the second coordinate in third array replaces data_in_db[index_of_max_less_25]

        self.view.data_in_db_low, self.view.points_low, rt60_low = self.model.compute_rt60(250)
        self.view.data_in_db_mid, self.view.points_mid, rt60_mid = self.model.compute_rt60(500)
        self.view.data_in_db_high, self.view.points_high, rt60_high = self.model.compute_rt60(1000)
        
        self.view.rt60_low = rt60_low
        self.view.rt60_mid = rt60_mid
        self.view.rt60_high = rt60_high

        self.view.difference = self.model.compute_difference(rt60_low, rt60_mid, rt60_high)