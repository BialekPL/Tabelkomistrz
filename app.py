import tkinter as tk
from model import Table
from view import View
from controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        view = View(self)
        model = Table(30, 15)
        #export = Export()
        controller = Controller(model, view)
        view.setController(controller)

if __name__ == '__main__':
    app = App()
    app.mainloop()
    