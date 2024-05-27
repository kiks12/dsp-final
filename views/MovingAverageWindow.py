
import tkinter as tk

from views import Window
from controllers import MovingAverageController


class MovingAverageWindow(Window.Window):

    window: tk.Tk
    frame: tk.Frame
    toolbar_frame: tk.Frame
    quit_button: tk.Button
    controller: MovingAverageController.MovingAverageController

    def __init__(self, controller):
        self.initialize_window()
        self.controller = controller

    def initialize_window(self):
        self.window = tk.Tk()
        self.window.geometry("600x300")
        self.window.resizable(False, False)

    def initialize_toolbar(self):
        self.toolbar_frame = tk.Frame(
            self.window,
            width=self.window.winfo_width,
            height=self.window.winfo_height * 0.1
        )
        self.quit_button = tk.Button(
            self.toolbar_frame,
            text="Quit",
            command=lambda: print("Quit Button Command"),
            width=10,
        )
        self.quit_button.grid(column=0, row=0, ipadx=10, ipady=10)
        self.toolbar_frame.pack()
