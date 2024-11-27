import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class Interface(ttk.Frame):
    def __init__(self, parent):
        super().__init__()  
        # open button
        self.open_button = ttk.Button(
            self,
            text='Open a File',
            command=self.select_file
        )
        self.open_button.grid(row=1, column=0, padx=10)
        #expand the button when the window expand
        self.open_button.pack(expand=True, fill='both')

        
    
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

            gfile = filename
            self.label = ttk.Label(self, text='File Name:')
            self.label.grid(row=2, column=0)

            self.gfile_label = ttk.Label(self, text=gfile)
            self.gfile_label.grid(row =2, column= 1)
