
import tkinter as tk

from views import Window


class MovingAverageWindow(Window.Window):

    window: tk.Tk
    frame: tk.ttk.Frame
    toolbar_frame: tk.ttk.Frame
    quit_button: tk.ttk.Button

    def __init__(self):
        self.initialize_window()

    def initialize_window(self):
        self.window = tk.Tk()
        self.window.geometry("600x300")
        self.window.resizable(False, False)

    def initialize_toolbar(self):
        self.toolbar_frame = tk.ttk.Frame(
            self.window, width=self.window.winfo_width
        )
        self.quit_button = tk.ttk.Button(
            self.toolbar_frame,
            text="Quit",
            command=lambda: print("Quit Button Command"),
            width=10,
        )
        self.quit_button.grid(column=0, row=0, ipadx=10, ipady=10)
