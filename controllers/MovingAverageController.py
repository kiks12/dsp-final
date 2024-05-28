
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox


class MovingAverageController:

    random_time_vector: np.ndarray
    random_y_values: np.ndarray
    random_figure: Figure

    def __init__(self):
        print("Initialize MovingAverageController")
        self.random_figure = Figure(figsize=(7, 5))
        np.random.seed(0)

    def create_time_vector(self, start, end, jump) -> np.array:
        self.random_time_vector = np.linspace(start, end, jump)
        messagebox.showinfo("Generate Time Vector",
                            "Time Vector generated successfully.")

    def plot_values(self, x, y, title, number):
        self.random_original_plot = self.random_figure.add_subplot(number)
        self.random_original_plot.plot(
            x, y, label=title)
        self.random_original_plot.legend()

    def show_plot_in_gui(self, master):
        for widget in master.winfo_children():
            widget.destroy()

        self.random_canvas = FigureCanvasTkAgg(self.random_figure, master)
        self.random_canvas.draw()
        self.random_canvas.get_tk_widget().pack()

    def create_y_values(self, master):
        self.random_y_values = np.random.randn(len(self.random_time_vector))
        self.random_figure.clear()
        self.random_original_plot = self.random_figure.add_subplot(111)
        self.random_original_plot.plot(
            self.random_time_vector, self.random_y_values, label="Original")
        self.random_original_plot.legend()

        self.show_plot_in_gui(master)

    def apply_moving_average_filter(self, window, master):
        ret = np.cumsum(self.random_y_values, dtype=float)
        ret[window:] = ret[window:] - ret[:-window]
        ret = ret[window - 1:] / window

        self.random_figure.clear()
        self.random_filtered_plot = self.random_figure.add_subplot(111)
        self.random_filtered_plot.plot(
            self.random_time_vector, self.random_y_values, label="Original")
        self.random_filtered_plot.plot(
            self.random_time_vector[window-1:], ret, label="Filtered"
        )
        self.random_filtered_plot.legend()

        self.random_filtered_plot.legend()
        self.show_plot_in_gui(master)
