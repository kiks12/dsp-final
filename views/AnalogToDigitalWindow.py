import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import csv

from controllers import AnalogToDigitalController

class AnalogToDigitalWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.geometry("1000x700")
        self.title("Analog to Digital Converter")
        self.resizable(False, False)

        self.controller = controller
        self.time_vector = tk.IntVar(value=50)
        self.sampling_interval = tk.IntVar(value=1)
        self.bit_depth = tk.IntVar(value=8)
        self.file_path = None

        self.initialize_layout()

    def initialize_layout(self):
        self.initialize_header()
        self.initialize_tabview()

    def clear_plots(self):
        for widget in self.random_plot_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.random_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")

    def initialize_header(self):
        self.header = ctk.CTkFrame(self, width=1000, height=100)
        self.clear_button = ctk.CTkButton(
            self.header, text="Clear", command=self.clear_plots, width=100, height=40)
        self.quit_button = ctk.CTkButton(
            self.header, text="Exit", command=self.close_window, width=100, height=40
        )
        self.header_label = ctk.CTkLabel(
            self.header, text="Analog to Digital Converter", font=("Helvetica", 20), width=740, anchor="w")
        self.header_label.grid(
            column=0, row=0, columnspan=8, padx=10, pady=10, sticky="w")
        self.clear_button.grid(column=8, row=0, padx=5, pady=10, sticky="e")
        self.quit_button.grid(column=9, row=0, padx=5, pady=10, sticky="e")
        self.header.pack(padx=10, pady=10)

    def initialize_tabview(self):
        self.tab_view = ctk.CTkTabview(
            self, width=1000, height=680, anchor="nw"
        )
        self.random_tab = self.tab_view.add("Random")
        self.csv_tab = self.tab_view.add("Import CSV")

        self.initialize_random_form()
        self.initialize_import_form()

        self.tab_view.pack(pady=10, padx=10)

    def initialize_random_form(self):
        self.random_form_frame = ctk.CTkFrame(self.random_tab, width=250, height=600)
        self.create_random_form()

        self.random_plot_frame = ctk.CTkFrame(self.random_tab, width=750, height=600)
        ctk.CTkLabel(self.random_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")

        self.random_form_frame.grid(column=0, row=0, padx=20)
        self.random_plot_frame.grid(column=1, row=0)

    def initialize_import_form(self):
        self.import_form_frame = ctk.CTkFrame(self.csv_tab, width=250, height=600)
        self.create_import_form()

        self.import_plot_frame = ctk.CTkFrame(self.csv_tab, width=750, height=600)
        ctk.CTkLabel(self.import_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")

        self.import_form_frame.grid(column=0, row=0, padx=20)
        self.import_plot_frame.grid(column=1, row=0)

    def create_random_form(self):
        ctk.CTkLabel(self.random_form_frame, text="Time Vector", font=("Helvetica", 16)).pack(pady=10)
        self.time_vector_slider = ctk.CTkSlider(self.random_form_frame, from_=1, to=100, variable=self.time_vector, number_of_steps=100)
        self.time_vector_slider.pack(pady=10)
        self.time_vector_label = ctk.CTkLabel(self.random_form_frame, textvariable=self.time_vector)
        self.time_vector_label.pack(pady=5)

        ctk.CTkLabel(self.random_form_frame, text="Sampling Interval", font=("Helvetica", 16)).pack(pady=10)
        self.sampling_slider = ctk.CTkSlider(self.random_form_frame, from_=1, to=10, variable=self.sampling_interval)
        self.sampling_slider.pack(pady=10)
        self.sampling_val_label = ctk.CTkLabel(self.random_form_frame, textvariable=self.sampling_interval)
        self.sampling_val_label.pack(pady=5)

        ctk.CTkLabel(self.random_form_frame, text="Bit Depth", font=("Helvetica", 16)).pack(pady=10)
        self.bit_depth_slider = ctk.CTkSlider(self.random_form_frame, from_=1, to=16, variable=self.bit_depth, number_of_steps=16)
        self.bit_depth_slider.pack(pady=10)
        self.bit_depth_label = ctk.CTkLabel(self.random_form_frame, textvariable=self.bit_depth)
        self.bit_depth_label.pack(pady=5)

        ctk.CTkButton(self.random_form_frame, text="Generate Random Signal", command=self.generate_random_signal).pack(pady=10)
        ctk.CTkButton(self.random_form_frame, text="Analog to Digital Conversion", command=lambda: self.analog_to_digital_conversion(self.analog_signal, self.random_plot_frame)).pack(pady=10)

    def create_import_form(self):
        ctk.CTkLabel(self.import_form_frame, text="Sampling Interval", font=("Helvetica", 16)).pack(pady=10)
        self.sampling_slider = ctk.CTkSlider(self.import_form_frame, from_=1, to=10, variable=self.sampling_interval)
        self.sampling_slider.pack(pady=10)
        self.sampling_val_label = ctk.CTkLabel(self.import_form_frame, textvariable=self.sampling_interval)
        self.sampling_val_label.pack(pady=5)

        ctk.CTkLabel(self.import_form_frame, text="Bit Depth", font=("Helvetica", 16)).pack(pady=10)
        self.bit_depth_slider = ctk.CTkSlider(self.import_form_frame, from_=1, to=16, variable=self.bit_depth, number_of_steps=16)
        self.bit_depth_slider.pack(pady=10)
        self.bit_depth_label = ctk.CTkLabel(self.import_form_frame, textvariable=self.bit_depth)
        self.bit_depth_label.pack(pady=5)

        ctk.CTkButton(self.import_form_frame, text="Load CSV File", command=self.load_csv_file).pack(pady=10)
        ctk.CTkButton(self.import_form_frame, text="Analog to Digital Conversion", command=lambda: self.analog_to_digital_conversion(self.analog_signal, self.import_plot_frame)).pack(pady=10)

    def generate_random_signal(self):
        time_vector = int(self.time_vector.get())
        time = np.linspace(0, 1, time_vector)
        self.analog_signal = np.sin(2 * np.pi * np.random.rand(time_vector) * time)
        self.plot_random_signal(self.analog_signal, self.random_plot_frame)

    def load_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            analog_signal = self.read_csv_file(file_path)
            self.analog_signal = analog_signal
            self.plot_random_signal(analog_signal, self.import_plot_frame)

    def read_csv_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            analog_signal = np.array([float(row[0]) for row in reader])
        return analog_signal
    
    def plot_random_signal(self, signal, plot_frame):
        for widget in plot_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots()
        ax.plot(signal, label='Analog Signal')
        ax.set_xlabel('Sample Number')
        ax.set_ylabel('Amplitude')
        ax.set_title('Signal')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def analog_to_digital_conversion(self, analog_signal, plot_frame):
        sampling_interval = self.sampling_interval.get()
        bit_depth = self.bit_depth.get()
        self.controller.bit_depth = bit_depth

        digital_signal, sample_points = self.controller.adc_process(analog_signal, sampling_interval)
        
        for widget in plot_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots()
        ax.plot(analog_signal, label='Original Signal')
        ax.plot(sample_points, digital_signal, label='Encoded Signal', linestyle='--')
        ax.legend()
        ax.set_xlabel('Sample Number')
        ax.set_ylabel('Amplitude')
        ax.set_title('Analog to Digital Conversion')
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def close_window(self):
        self.destroy()

if __name__ == "__main__":
    controller = AnalogToDigitalController()
    app = AnalogToDigitalWindow(controller)
    app.mainloop()
