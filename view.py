import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm
import numpy as np

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  


        self.resolution = 150
        self.num_size = 6
        self.letter_size = 8

        #Variables that will communicate with controller
        self.filename = ''
        self.filepath = ''
        self.controller = None
        self.length = 0 
        self.rfrequency = 0
        self.time = None
        self.data = None
        self.sample_rate = None
        self.difference = None
        
        self.t = None
        self.current = 0 #For Low, Miu, High button
        
        self.data_in_db_low = None
        self.data_in_db_mid = None
        self.data_in_db_high = None
        
        self.points_low = None
        self.points_mid = None
        self.points_high = None

        self.rt60_low = None
        self.rt60_mid = None
        self.rt60_high = None

        
    # open button
        self.open_button = ttk.Button(
            self,
            text='Open a File',
            command=self.open_button_clicked
        )
        self.open_button.grid(row=1, column = 0, sticky= "w", padx = 20)

    # analyze button
        self.analyze_button = ttk.Button(
            self,
            text='Analyze File',
            command=self.analyze_file
        )
        self.analyze_button.grid(row=1, column = 2, padx = 20, sticky= "e")
        self.analyze_button.grid_remove() #hide the button when there is no file opened

        self.label_analyzing = ttk.Label(self, text= "")
        self.label_analyzing.grid(row=1, column = 2, padx = 10, sticky= "e")
        self.label_analyzing.grid_remove()

    #display the selected file
        self.label_fname = ttk.Label(self, text='File Name:')
        self.label_fname.grid(row=2, column=0, sticky = "e")
        self.label_gfile = ttk.Label(self, text= "")
        self.label_gfile.grid(row=2, column= 1, sticky = "w")

    # default graph
        # Create a frame for the plot
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=3, column=0, columnspan=3, sticky="nsew") #columnspan is the key to spacing of the buttons/labels
        #display the default plot
        self.default_plot()
        
    #Three graph buttons. Initially hidden
        #Intensity graph
        self.intensity_button = ttk.Button(
            self,
            text='Intensity Graph',
            command=self.intensity_button_clicked
        )
        self.intensity_button.grid(row = 4, column = 0,  pady = 10, sticky = "")

        #Waveform graph
        self.waveform_button = ttk.Button(
            self,
            text='Waveform Graph',
            command=self.waveform_button_clicked
        )
        self.waveform_button.grid(row = 4, column = 1,  pady = 10, sticky = "")

        #RT60 graphs
        self.cycle_RT60_button = ttk.Button(
            self,
            text='Cycle RT60 Graph',
            command=self.cycle_RT60_button_clicked
        )
        self.cycle_RT60_button.grid(row = 4, column = 2, pady = 10, sticky = "")

        #Combined RT60 graphs
        self.combine_cycle_RT60_button = ttk.Button(
            self,
            text='Combined RT60 Graphs',
            command=self.combine_cycle_RT60_button_clicked
        )
        self.combine_cycle_RT60_button.grid(row = 5, column = 2, pady = 10,  sticky = "")

        #Hide buttons
        self.intensity_button.grid_remove()
        self.waveform_button.grid_remove()
        self.cycle_RT60_button.grid_remove()
        self.combine_cycle_RT60_button.grid_remove()


    #Display information of the audio file
        #display the file length 
        self.label_length = ttk.Label(self, text='File Length: 0s')
        self.label_length.grid(row=5, column=1, sticky = "", pady = 5)

        #display the frequency 
        self.label_frequency = ttk.Label(self, text='Resonant Frequency: ___ Hz')
        self.label_frequency.grid(row=6,column=1, sticky = "",  pady = 5)

        #display the difference 
        self.label_difference = ttk.Label(self, text='Difference: _.__s ')
        self.label_difference.grid(row=7, column=1,sticky = "", pady = 5)
        

#Functions

    #Connect view with controller
    def set_controller(self, controller):
        self.controller = controller
    
    #Create a default plot when user have yet clicked the analyze button
    def default_plot(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        x = [0, .2, .4, .6, .8, 1]
        y = [0, .2, .4, .6, .8, 1]
        axes.set_title("Default Graph")
        axes.set_xlabel("X-axis", fontsize = self.letter_size )
        axes.set_ylabel("Y-axis", fontsize = self.letter_size)
        axes.tick_params(axis='x', labelsize=self.num_size)  
        axes.tick_params(axis='y', labelsize=self.num_size)  
    
        #Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        #Plot the graph    
        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew")

    #Reset to initial condition when open a new file    
    def reset_state(self):
        #Reset the infomation
        self.label_length.config(text='File Length: 0s')
        self.label_frequency.config(text='Resonant Frequency: ___ Hz')
        self.label_difference.config(text='Difference: _.__s')

        #Hide these buttons and labels
        self.intensity_button.grid_remove()
        self.waveform_button.grid_remove()
        self.cycle_RT60_button.grid_remove()
        self.combine_cycle_RT60_button.grid_remove()
        self.label_analyzing.grid_remove()

        #Reset these
        self.analyze_button.grid(row=1, column = 2, padx = 20, sticky= "e")
        self.current = 0
        self.cycle_RT60_button.config(text="Cycle RT60 Graph")
        self.default_plot()

    #Run when user clicked open file button
    def open_button_clicked(self):
            filetypes = (
                ('wav files', '*.wav'),
                ('mp3 files', '*.mp3')
            )

            self.filepath = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            #If the file was selected
            if self.filepath:

                # Extract the file name by splitting the path to use for display
                self.filename = self.filepath.split('/')[-1] if '/' in self.filepath else self.filepath.split('\\')[-1]
                           
                self.reset_state()

                #Show the analyze button
                self.analyze_button.grid() 

                
            #Display file name
            self.label_gfile.config(text = self.filename)
         
    #When clicked analyze button
    def analyze_file(self):
        # Hide the button after it's clicked
        self.analyze_button.grid_forget()
        
        # Label for the analyze button action
        self.label_analyzing.config(text= f"Analyzing file: {self.filename}")
        self.label_analyzing.grid()

        #Send the file path to controller
        if self.controller:
            self.controller.analyze_file(self.filepath)

        
        #Show waveform graph
        self.waveform_button_clicked()

        #Add buttons for different graphs
        self.add_buttons()
        self.display_info()
 
    #Show four buttons for different graphs
    def add_buttons(self):
        self.intensity_button.grid()
        self.waveform_button.grid()
        self.cycle_RT60_button.grid()
        self.combine_cycle_RT60_button.grid()

    #Display these information after user clicked analyze button
    def display_info(self):
        self.label_length.config(text = f'File Length: {self.length}s')
        self.label_frequency.config(text = f'Resonant Frequency: {self.rfrequency} Hz')
        self.label_difference.config(text = f'Difference: { self.difference:.2f}s') #might need to format later
    
    #Plot the intensity graph
    def intensity_button_clicked(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        spectrum, freqs, t, im = axes.specgram(
            self.data, 
            Fs=self.sample_rate, 
            NFFT=1024, 
            cmap=cm.get_cmap('autumn_r'))
        cbar = figure.colorbar(im, ax=axes)
        cbar.set_label("Intensity (dB)")

        axes.set_title("Frequency Graph")
        axes.set_xlabel("Time (s)", fontsize = self.letter_size)
        axes.set_ylabel("Frequency (Hz)", fontsize = self.letter_size)
        axes.tick_params(axis='x', labelsize=self.num_size) 
        axes.tick_params(axis='y', labelsize=self.num_size)  # Reduce label font size

        #Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew")
    
    #Plot the waveform graph
    def waveform_button_clicked(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        x = self.time
        y = self.data
        axes.plot(x, y)
        axes.set_title("Waveform Graph")
        axes.set_xlabel("Time (s)", fontsize = self.letter_size)
        axes.set_ylabel("Amplitude", fontsize = self.letter_size)
        axes.tick_params(axis='x', labelsize=self.num_size) 
        axes.tick_params(axis='y', labelsize=self.num_size)  # Reduce label font size

        #Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew")

    #Plot each RT60 graphs
    def cycle_RT60_button_clicked(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        axes.set_xlabel("Time (s)", fontsize = self.letter_size)
        axes.set_ylabel("Power (dB)", fontsize = self.letter_size)
        axes.tick_params(axis='x', labelsize=self.num_size) 
        axes.tick_params(axis='y', labelsize=self.num_size)  # Reduce label font size

        if self.current == 0:
            self.cycle_RT60_button.config(text = "Low")
            axes.set_title("Low RT60 Graph")

            axes.plot(self.t, self.data_in_db_low, linewidth=1, alpha=0.7, color='#ffd700')
            axes.plot(self.points_low[0][0], self.points_low[0][1], 'go')
            axes.plot(self.points_low[1][0], self.points_low[1][1], 'yo')
            axes.plot(self.points_low[2][0], self.points_low[2][1], 'ro')
            self.current = 1

        elif self.current == 1:
            self.cycle_RT60_button.config(text = "Mid")
            axes.set_title("Mid RT60 Graph")

            axes.plot(self.t, self.data_in_db_mid, linewidth=1, alpha=0.7, color='#ff4500')
            axes.plot(self.points_mid[0][0], self.points_mid[0][1], 'go')
            axes.plot(self.points_mid[1][0], self.points_mid[1][1], 'yo')
            axes.plot(self.points_mid[2][0], self.points_mid[2][1], 'ro')
            
            self.current = 2
        
        elif self.current == 2:
            self.cycle_RT60_button.config(text = "High")
            axes.set_title("High RT60 Graph")

            axes.plot(self.t, self.data_in_db_high, linewidth=1, alpha=0.7, color='#004bc6')
            axes.plot(self.points_high[0][0], self.points_high[0][1], 'go')
            axes.plot(self.points_high[1][0], self.points_high[1][1], 'yo')
            axes.plot(self.points_high[2][0], self.points_high[2][1], 'ro')
            self.current = 0


        #Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew")

    #Plot all the RT60 graphs
    def combine_cycle_RT60_button_clicked(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        axes.set_title("Combined RT60 Graphs")
        axes.set_xlabel("Time (s)", fontsize = self.letter_size)
        axes.set_ylabel("Power (dB)", fontsize = self.letter_size)
        axes.tick_params(axis='x', labelsize=self.num_size) 
        axes.tick_params(axis='y', labelsize=self.num_size)

        #Low graph
        axes.plot(self.t, self.data_in_db_low, linewidth=1, alpha=0.7, color='#ffd700')
        axes.plot(self.points_low[0][0], self.points_low[0][1], 'go')
        axes.plot(self.points_low[1][0], self.points_low[1][1], 'yo')
        axes.plot(self.points_low[2][0], self.points_low[2][1], 'ro')

        #Mid graph
        axes.plot(self.t, self.data_in_db_mid, linewidth=1, alpha=0.7, color='#ff4500')
        axes.plot(self.points_mid[0][0], self.points_mid[0][1], 'go')
        axes.plot(self.points_mid[1][0], self.points_mid[1][1], 'yo')
        axes.plot(self.points_mid[2][0], self.points_mid[2][1], 'ro')

        #High graph
        axes.plot(self.t, self.data_in_db_high, linewidth=1, alpha=0.7, color='#004bc6')
        axes.plot(self.points_high[0][0], self.points_high[0][1], 'go')
        axes.plot(self.points_high[1][0], self.points_high[1][1], 'yo')
        axes.plot(self.points_high[2][0], self.points_high[2][1], 'ro')

        
        #Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew")