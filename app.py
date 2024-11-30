from model import Model
from controller import Controller
from view import View

import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #window size - adjustable. Set default size and position: 800x700, 300 pixels from the left and 100 pixels from the top
        self.geometry("800x700+300+100")

        self.title('Acoustic Modeling App')

        model = Model(self)
        #interface
        view = View(self)
        view.grid(row=0, column=0, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
