import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class Interface(ttk.Frame):
    def __init__(self, parent):
        super().__init__()  

    # Configure rows and columns to expand
        self.grid_rowconfigure(0, weight=1)  # Row 0 expands
        self.grid_columnconfigure(0, weight=1) # Column 0 expand
        self.grid_rowconfigure(1, weight=1)  # Row 0 expands
        self.grid_columnconfigure(1, weight=1) # Column 0 expand
    
    # open button
        self.open_button = ttk.Button(
            self,
            text='Open a File',
            command=self.select_file
        )
        self.open_button.grid(row=1, sticky= "nsew")
        
        

    #display the selected file

        self.label = ttk.Label(self, text='File Name:')
        self.label.grid(row=2, column=0)



        
    
    gfile = ''
    def select_file(self):
            filetypes = (
                ('wav files', '*.wav'),
                ('mp3 files', '*.mp3')
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            #self.gfile = filename
            if filename:  # Check if a file was selected
                # Extract the file name by splitting the path
                self.gfile = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]


            self.gfile_label = ttk.Label(self, text= self.gfile)
            self.gfile_label.grid(row =2, column= 1, sticky = "nsew")
            
