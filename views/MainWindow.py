
import tkinter as tk

from controllers.MainController import MainController
from views import Window


class MainWindow(Window.Window):

    window: tk.Tk
    frame: tk.ttk.Frame
    adc_button: tk.ttk.Button
    fir_button: tk.ttk.Button
    moving_average_button: tk.ttk.Button
    pass_filter_button: tk.ttk.Button
    exit_button: tk.ttk.Button

    controller: MainController

    def __init__(self, controller):
        print("Initialize Main Window")
        self.controller = controller
        self.initialize_window()

    def initialize_window(self):
        self.window = tk.Tk()
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.title("Digital Signal Processing")

        self.initialize_buttons()

    def initialize_buttons(self):
        self.frame = tk.ttk.Frame(self.window)
        self.adc_button = tk.ttk.Button(
            self.frame,
            text="Analog to Digital Conversion",
            width=20,
        )
        self.fir_button = tk.ttk.Button(
            self.frame,
            text="Finite Impulse Response Filter",
            width=20
        )
        self.moving_average_button = tk.ttk.Button(
            self.frame,
            text="Moving Average Filter",
            width=20
        )
        self.pass_filter_button = tk.ttk.Button(
            self.frame,
            text="Low-Pass/High-Pass",
            width=20
        )
        self.exit_button = tk.ttk.Button(
            self.frame,
            text="Exit",
            width=20,
            command=lambda: self.controller.exit_app()
        )

        self.adc_button.grid(row=1, column=1, ipady=20, ipadx=10)
        self.fir_button.grid(row=2, column=1, ipady=20, ipadx=10)
        self.moving_average_button.grid(row=3, column=1, ipady=20, ipadx=10)
        self.pass_filter_button.grid(row=4, column=1, ipady=20, ipadx=10)
        self.exit_button.grid(row=5, column=1, ipady=20, ipadx=10)

        self.frame.pack()

    def start_mainloop(self):
        self.window.mainloop()
