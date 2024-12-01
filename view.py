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

    # # Configure rows and columns to expand

        self.grid_columnconfigure(0, weight=1) # Column 0 expand
        self.grid_columnconfigure(1, weight=1) # Column 0 expand
        self.grid_columnconfigure(2, weight=0) # Column 0 expand



        self.resolution = 150
        self.num_size = 6
        self.letter_size = 8
        self.gfile = ''
        self.controller = None
        self.length = 0 
        self.rfrequency = 0
        self.time = []
        self.data = []
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

        self.default_plot()
        
    #Three graphs button. Initially hidden
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

        #Combine RT60 graphs
        self.combine_cycle_RT60_button = ttk.Button(
            self,
            text='Combine RT60 Graphs',
            command=self.combine_cycle_RT60_button_clicked
        )
        self.combine_cycle_RT60_button.grid(row = 5, column = 2, pady = 10,  sticky = "")

        #Hide buttons
        self.intensity_button.grid_remove()
        self.waveform_button.grid_remove()
        self.cycle_RT60_button.grid_remove()
        self.combine_cycle_RT60_button.grid_remove()

    #display the file length 
        self.label_flength = ttk.Label(self, text='File Length: 0 s')
        self.label_flength.grid(row=5, column=1, sticky = "", pady = 5)


    #display the frequency 
        self.label_ffrequency = ttk.Label(self, text='Resonant Frequency: ___ Hz')
        self.label_ffrequency.grid(row=6,column=1, sticky = "",  pady = 5)
        

    #display the difference 
        self.label_fdiff = ttk.Label(self, text='Difference: _.__ s ')
        self.label_fdiff.grid(row=7, column=1,sticky = "", pady = 5)
        

    def set_controller(self, controller):
        self.controller = controller

    
    def open_button_clicked(self):
            filetypes = (
                ('wav files', '*.wav'),
                ('mp3 files', '*.mp3')
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            
            if filename:  # Check if a file was selected
                # Extract the file name by splitting the path
                self.gfile = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]
                self.reset_state()
                self.analyze_button.grid() 

                
            #Display file name
            self.label_gfile.config(text = self.gfile)
    
    def reset_state(self):
        #Hide these 
        self.intensity_button.grid_remove()
        self.waveform_button.grid_remove()
        self.cycle_RT60_button.grid_remove()
        self.combine_cycle_RT60_button.grid_remove()
        self.label_analyzing.grid_remove()

        #Reset these
        self.analyze_button.grid(row=1, column = 2, padx = 20, sticky= "e")
        self.current = 0
        self.cycle_RT60_button.config(text="Cycle RT60 Graph")

    def default_plot(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        x = [0, .2, .4, .6, .8, 1]
        y = [0, .2, .4, .6, .8, 1]
        axes.set_title("Default Graph")
        axes.set_xlabel("X-axis", fontsize = self.letter_size )
        axes.set_ylabel("Y-axis", fontsize = self.letter_size)
        axes.tick_params(axis='x', labelsize=self.num_size)  # Reduce label font size
        axes.tick_params(axis='y', labelsize=self.num_size)  # Reduce label font size
    
        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew")
           

    def analyze_file(self):
        # Hide the button after it's clicked
        self.analyze_button.grid_forget()
        
        # Placeholder for the analyze button action
        self.label_analyzing.config(text= f"Analyzing file: {self.gfile}")
        self.label_analyzing.grid()

        #Send the file name to controller
        if self.controller:
            self.controller.analyze_file(self.gfile)

        
        #Show waveform graph
        self.waveform_button_clicked()

        #Add buttons for different graphs
        self.add_buttons()

        self.display_info()
 
    #use in controller
    def display_info(self):
        self.label_flength.config(text = f'File Length: {self.length} s')
        self.label_ffrequency.config(text = f'Resonant Frequency: {self.rfrequency} Hz')
        self.label_fdiff.config(text = f'Difference: { self.difference:.2f} s') #might need to format later
    
    #Show four buttons for different graphs
    def add_buttons(self):
        self.intensity_button.grid()
        self.waveform_button.grid()
        self.cycle_RT60_button.grid()
        self.combine_cycle_RT60_button.grid()

    #plotting intensity graph
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
    
    #plotting waveform graph
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


    def combine_cycle_RT60_button_clicked(self):
        figure = Figure(figsize=(5, 4), dpi=self.resolution)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        axes.set_title("Combine RT60 Graphs")
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