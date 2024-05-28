
import numpy as np
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox, filedialog


class MovingAverageController:

    random_time_vector: np.ndarray
    random_y_values: np.ndarray
    random_figure: Figure

    import_figure: Figure
    import_y_values: np.ndarray
    import_x_values: np.ndarray

    def __init__(self):
        print("Initialize MovingAverageController")
        self.random_figure = Figure(figsize=(7, 5))
        self.import_figure = Figure(figsize=(7, 5))
        np.random.seed(0)

    def create_time_vector(self, start, end, jump) -> np.array:
        self.random_time_vector = np.linspace(start, end, jump)
        messagebox.showinfo("Generate Time Vector",
                            "Time Vector generated successfully.")

    def show_random_plot_in_gui(self, master):
        for widget in master.winfo_children():
            widget.destroy()

        self.random_canvas = FigureCanvasTkAgg(self.random_figure, master)
        self.random_canvas.draw()
        self.random_canvas.get_tk_widget().pack()

    def show_import_plot_in_gui(self, master):
        for widget in master.winfo_children():
            widget.destroy()

        self.import_canvas = FigureCanvasTkAgg(self.import_figure, master)
        self.import_canvas.draw()
        self.import_canvas.get_tk_widget().pack()

    def create_y_values(self, master):
        self.random_y_values = np.random.randn(len(self.random_time_vector))
        self.random_figure.clear()
        self.random_original_plot = self.random_figure.add_subplot(111)
        self.random_original_plot.plot(
            self.random_time_vector, self.random_y_values, label="Original")
        self.random_original_plot.legend()

        self.show_random_plot_in_gui(master)

    def moving_average_filter(self, a, window):
        ret = np.cumsum(a, dtype=float)
        ret[window:] = ret[window:] - ret[:-window]
        ret = ret[window - 1:] / window
        return ret

    def apply_moving_average_filter_random(self, window, master):
        filtered_values = self.moving_average_filter(
            self.random_y_values, window)
        self.random_figure.clear()
        self.random_filtered_plot = self.random_figure.add_subplot(111)
        self.random_filtered_plot.plot(
            self.random_time_vector, self.random_y_values, label="Original")
        self.random_filtered_plot.plot(
            self.random_time_vector[window -
                                    1:], filtered_values, label="Filtered"
        )
        self.random_filtered_plot.legend()
        self.show_random_plot_in_gui(master)

    def apply_moving_average_filter_import(self, window, master):
        filtered_values = self.moving_average_filter(
            np.array(self.import_y_values), window)
        self.import_figure.clear()
        self.import_filtered_plot = self.import_figure.add_subplot(111)
        self.import_filtered_plot.plot(
            self.import_x_values, self.import_y_values, label="Original")
        self.import_filtered_plot.plot(
            self.import_x_values[window -
                                 1:], filtered_values, label="Filtered"
        )
        self.import_filtered_plot.legend()

        self.show_import_plot_in_gui(master)

    def import_csv(self, x, y):
        self.filename = filedialog.askopenfilename()
        self.csv_data = pd.read_csv(self.filename)
        x.configure(values=self.csv_data.columns.tolist())
        y.configure(values=self.csv_data.columns.tolist())
        messagebox.showinfo("Import CSV", "Successfully imported csv data")

    def set_selected_x_column(self, column):
        self.import_x_values = self.csv_data[column]

    def set_selected_y_column(self, column):
        self.import_y_values = self.csv_data[column]

    def plot_import_values(self, master):
        self.import_figure.clear()
        self.import_original_plot = self.import_figure.add_subplot(111)
        self.import_original_plot.plot(
            self.import_x_values, self.import_y_values, label="Original")
        self.import_original_plot.legend()

        self.show_import_plot_in_gui(master)
