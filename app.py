#import model here
#import model here
from view import Interface

import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #window size - adjustable. Set default size and position: 800x600, 300 pixels from the left and 150 pixels from the top
        self.geometry("800x600+300+150")

        self.title('Acoustic Modeling App')

        #interface
        interface = Interface(self)
        interface.grid(row=0, column=0, pady=10)


if __name__ == '__main__':
    app = App()
    app.mainloop()
