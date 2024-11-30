import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interface(ttk.Frame):
    def __init__(self, parent):
        super().__init__()  

    # # Configure rows and columns to expand
    #     self.grid_rowconfigure(0, weight=1)  # Row 0 expands
    #     self.grid_columnconfigure(0, weight=1) # Column 0 expand
    #     self.grid_rowconfigure(1, weight=1)  # Row 0 expands
    #     self.grid_columnconfigure(1, weight=1) # Column 0 expand
    
    # open button
        self.open_button = ttk.Button(
            self,
            text='Open a File',
            command=self.open_button_clicked
        )
        self.open_button.grid(row=1, column = 0, sticky= "w")

    # analyze button
        self.analyze_button = ttk.Button(
            self,
            text='Analyze File',
            command=self.analyze_file
        )
        self.analyze_button.grid(row=1, column = 1, sticky= "w")
        self.analyze_button.grid_forget() #hide the button when there is no file opened

    #display the selected file
        self.label_fname = ttk.Label(self, text='File Name:')
        self.label_fname.grid(row=2, column=0, sticky = "w")

    

    # default graph
        # Create a frame for the plot
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.default_plot()
        
    
    #display the file length 
        self.label_flength = ttk.Label(self, text='File Length: 0s')
        self.label_flength.grid(row=5, column=0, sticky = "ew")
        self.length = None #place holder

    #display the frequency 
        self.label_ffrequency = ttk.Label(self, text='File Resonant Frequency: ___ Hz')
        self.label_ffrequency.grid(row=6, column=0, sticky = "ew")
        self.frequency = None

    #display the difference 
        self.label_fdiff = ttk.Label(self, text='Difference: _.__ s ')
        self.label_fdiff.grid(row=7, column=0, sticky = "ew")
        self.difference = None

    def set_controller(self, controller):
        self.controller = controller

    gfile = ''
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
                self.analyze_button.grid(row=1, column = 1, sticky= "w")
            
            #Display file name
            self.gfile_label = ttk.Label(self, text= self.gfile)
            self.gfile_label.grid(row =2, column= 1, sticky = "w")

            #
            if self.controller:
                self.controller.information(self.gfile) # place holder

    #use in controller
    def diplay_data(self, length, frequency, time):
        self.length = length 
        self.frequency = frequency
        self.time = time  
            
        self.label_flength.config(text = f'File Length: {self.length}')
        self.label_ffrequency.config(text = f'File Resonant Frequency: {self.frequency} Hz')
        self.label_fdiff.config(text = f'Difference: {self.time} s') #might need to format later

    def analyze_file(self):
        # Hide the button after it's clicked
        self.analyze_button.grid_forget()

        # Placeholder for the analyze button action
        self.label_analyzing = ttk.Label(self, text= f"Analyzing file: {self.gfile}")
        self.label_analyzing.grid(row=1, column = 1, padx = 10, sticky= "e")

        #Add buttons for different graphs
        self.add_buttons()

    #Add four buttons for different graphs
    def add_buttons(self):
        #
        self.intensity_button = ttk.Button(
            self,
            text='Intensity Graph',
            #command=self.intensity_button_clicked
        )
        self.intensity_button.grid(row = 4, column = 0, padx = 10, pady = 10)
        
        #
        self.waveform_button = ttk.Button(
            self,
            text='Waveform Graph',
            #command=self.waveform_button_clicked
        )
        self.waveform_button.grid(row = 4, column = 1, padx = 20, pady = 10)
        
        #
        self.cycle_RT60_button = ttk.Button(
            self,
            text='Cycle RT60 Graph',
            #command=self.cycle_RT60_button_clicked
        )
        self.cycle_RT60_button.grid(row = 4, column = 2, padx = 20, pady = 10)
        
        self.combine_cycle_RT60_button = ttk.Button(
            self,
            text='Combine RT60 Graphs',
            #command=self.cycle_RT60_button_clicked
        )
        self.combine_cycle_RT60_button.grid(row = 5, column = 2, padx = 30, pady = 10)




    def default_plot(self):
        figure = Figure(figsize=(5, 4), dpi=120)
        axes = figure.add_subplot(1, 1, 1) #nrows, ncols, index

        x = [0, .2, .4, .6, .8, 1]
        y = [0, .2, .4, .6, .8, 1]
        axes.set_title("Default Graph")
        axes.set_xlabel("X-axis")
        axes.set_ylabel("Y-axis")
        

    
        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True) 
