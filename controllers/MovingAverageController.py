import numpy as np
import pandas as pd
import threading

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

    def create_y_values(self, master):
        self.random_y_values = np.random.randn(len(self.random_time_vector))
        self.random_figure.clear()
        self.random_original_plot = self.random_figure.add_subplot(111)
        self.random_original_plot.set_title("Random Generated Data")
        self.random_original_plot.plot(
            self.random_time_vector, self.random_y_values, label="Original")
        self.random_original_plot.legend()

        self.show_random_plot_in_gui(master)

    def show_random_plot_in_gui(self, master):
        if not hasattr(self, "random_canvas"):
            self.random_canvas = FigureCanvasTkAgg(self.random_figure, master)
            self.random_canvas.draw_idle()
            self.random_canvas.get_tk_widget().pack()
        else:
            self.random_canvas.draw_idle()

    def show_import_plot_in_gui(self, master):
        if not hasattr(self, "import_canvas"):
            self.import_canvas = FigureCanvasTkAgg(self.import_figure, master)
            self.import_canvas.draw_idle()
            self.import_canvas.get_tk_widget().pack()
        else:
            self.import_canvas.draw_idle()

    def moving_average_filter(self, a, window):
        ret = np.cumsum(a, dtype=float)
        ret[window:] = ret[window:] - ret[:-window]
        ret = ret[window - 1:] / window
        return ret

    def apply_moving_average_filter_random(self, window, master):
        self.window = window
        filtered_values = self.moving_average_filter(
            self.random_y_values, window)
        self.random_figure.clear()
        self.random_filtered_plot = self.random_figure.add_subplot(111)
        self.random_filtered_plot.set_title(
            f"Random Genereted Data -- Window: {self.window}")
        self.random_filtered_plot.plot(
            self.random_time_vector, self.random_y_values, label="Original")
        self.random_filtered_plot.plot(
            self.random_time_vector[window -
                                    1:], filtered_values, label="Filtered"
        )
        self.random_filtered_plot.legend()
        self.show_random_plot_in_gui(master)

    def apply_moving_average_filter_import(self, window, master, start, end):
        self.start = start
        self.end = end
        self.window = window
        filtered_values = self.moving_average_filter(
            np.array(self.import_y_values[self.start:self.end]), window)
        self.import_figure.clear()
        self.import_filtered_plot = self.import_figure.add_subplot(111)
        self.import_filtered_plot.set_title(
            f"Imported Data [{start}:{end}]-- Window: {self.window}")
        self.import_filtered_plot.plot(
            self.import_x_values[self.start:self.end], self.import_y_values[self.start:self.end], label="Original")
        self.import_filtered_plot.plot(
            self.import_x_values[self.start +
                                 window - 1:self.end], filtered_values, label="Filtered"
        )
        self.import_filtered_plot.legend()

        self.show_import_plot_in_gui(master)

    def import_csv(self, x, y, start, end, end_label):
        self.filename = filedialog.askopenfilename()
        self.csv_data = pd.read_csv(self.filename)
        x.configure(values=self.csv_data.columns.tolist())
        y.configure(values=self.csv_data.columns.tolist())
        start.configure(to=len(self.csv_data))
        end.configure(to=len(self.csv_data))
        end.set(len(self.csv_data))
        end_label.configure(text=f"End: {len(self.csv_data)}")
        messagebox.showinfo("Import CSV", "Successfully imported csv data")

    def set_selected_x_column(self, column):
        self.import_x_values = self.csv_data[column]

    def set_selected_y_column(self, column):
        self.import_y_values = self.csv_data[column]

    def set_new_start_value(self, start):
        self.start_thread = threading.Thread(
            target=self.plot_new_start_value, args=(start, ))
        self.start_thread.start()

    def plot_new_start_value(self, start):
        self.start_line.remove()
        self.start_line = self.import_original_plot.axvline(
            x=start, color="black", label="Start")
        self.import_canvas.draw_idle()

    def set_end_start_value(self, end):
        self.end_thread = threading.Thread(
            target=self.plot_new_end_value, args=(end, ))
        self.end_thread.start()

    def plot_new_end_value(self, end):
        self.end_line.remove()
        self.end_line = self.import_original_plot.axvline(
            x=end, color="red", label="End")
        self.import_canvas.draw_idle()

    def plot_import_values(self, master, start, end):
        self.import_figure.clear()
        self.start = start
        self.end = end
        self.import_original_plot = self.import_figure.add_subplot(111)
        self.import_original_plot.set_title("Imported Data")
        self.import_original_plot.plot(
            self.import_x_values, self.import_y_values, label="Original")
        self.start_line = self.import_original_plot.axvline(
            x=start, color="black", label="Start")
        self.end_line = self.import_original_plot.axvline(
            x=end, color="red", label="end")
        self.import_original_plot.legend()

        self.show_import_plot_in_gui(master)
