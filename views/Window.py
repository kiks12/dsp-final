
import tkinter as tk


class Window:

    window: tk.Tk

    def __init__(self):
        print("Initialize Class")
        self.initialize_window()

    def initialize_window(self):
        print("Initialize Window")
        self.window = tk.Tk()

    def start_mainloop(self):
        print("Start Window Mainloop")
        self.window.mainloop()
