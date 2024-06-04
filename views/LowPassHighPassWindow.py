import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import scipy.io.wavfile as wav
from controllers import LowPassHighPassController
import numpy as np
import sys

class lowPassHighPassWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.geometry("1000x700")
        self.title("Low Pass and High Pass Filter")
        self.resizable(False, False)

        self.controller = controller
        self.cut_off = tk.IntVar(value=10000)
        self.file_path = None
        self.audio_signal = None
        self.filtered_signal = None
        self.sampling_rate = None
        self.current_filter = None

        self.initialize_layout()

    def initialize_layout(self):
        self.initialize_header()
        self.initialize_tabview()

    def clear_plots(self):
        for widget in self.filter_plot_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.filter_plot_frame, text="Please Load Audio first.").place(
            relx=0.5, rely=0.5, anchor="center")

    def initialize_header(self):
        self.header = ctk.CTkFrame(self, width=1000, height=100)
        self.clear_button = ctk.CTkButton(
            self.header, text="Clear", command=self.clear_plots, width=100, height=40)
        self.quit_button = ctk.CTkButton(
            self.header, text="Exit", command=self.close_window, width=100, height=40
        )
        self.header_label = ctk.CTkLabel(
            self.header, text="Low Pass and High Pass Filter", font=("Helvetica", 20), width=740, anchor="w")
        self.header_label.grid(
            column=0, row=0, columnspan=8, padx=10, pady=10, sticky="w")
        self.clear_button.grid(column=8, row=0, padx=5, pady=10, sticky="e")
        self.quit_button.grid(column=9, row=0, padx=5, pady=10, sticky="e")
        self.header.pack(padx=10, pady=10)

    def initialize_tabview(self):
        self.tab_view = ctk.CTkTabview(
            self, width=1000, height=680, anchor="nw"
        )
        self.filter_tab = self.tab_view.add("Filter")

        self.initialize_filter_form()

        self.tab_view.pack(pady=10, padx=10)

    def initialize_filter_form(self):
        self.filter_form_frame = ctk.CTkFrame(self.filter_tab, width=250, height=600)
        self.create_filter_form()

        self.filter_plot_frame = ctk.CTkFrame(self.filter_tab, width=750, height=600)
        ctk.CTkLabel(self.filter_plot_frame, text="Please Load Audio first.").place(
            relx=0.5, rely=0.5, anchor="center")

        self.filter_form_frame.grid(column=0, row=0, padx=20)
        self.filter_plot_frame.grid(column=1, row=0)

    def create_filter_form(self):
        ctk.CTkLabel(self.filter_form_frame, text="Cut Off Frequency (Hz)", font=("Helvetica", 16)).pack(pady=10)
        self.cut_off_slider = ctk.CTkSlider(self.filter_form_frame, from_=1, to=22000, variable=self.cut_off, command=self.update_cut_off_slider)
        self.cut_off_slider.pack(pady=10)
        self.cut_off_val_label = ctk.CTkLabel(self.filter_form_frame, text="10000")
        self.cut_off_val_label.pack(pady=5)

        ctk.CTkButton(self.filter_form_frame, text="Load Audio File", command=self.load_audio_file).pack(pady=10)
        ctk.CTkButton(self.filter_form_frame, text="Low Pass Filter", command=lambda: self.apply_filter('lowpass')).pack(pady=10)
        ctk.CTkButton(self.filter_form_frame, text="High Pass Filter", command=lambda: self.apply_filter('highpass')).pack(pady=10)
        ctk.CTkButton(self.filter_form_frame, text="Save Filtered Audio", command=self.save_filtered_audio).pack(pady=10)

    def update_cut_off_slider(self, value):
        self.cut_off_val_label.configure(text=f"{int(value)}")

    def load_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.file_path = file_path
            self.sampling_rate, self.audio_signal = wav.read(file_path)
            self.filtered_signal = None
            self.plot_audio_signal(self.audio_signal, None, self.filter_plot_frame)

    def plot_audio_signal(self, original_signal, filtered_signal, plot_frame):
        for widget in plot_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots()
        ax.plot(original_signal, label='Original Signal', color="green")
        if filtered_signal is not None:
            filter_label = f'{self.current_filter.capitalize()} Filtered Signal'
            ax.plot(filtered_signal, label=filter_label, linestyle='--', color="blue")
        else:
            filter_label = None
        legend_elements = [
            plt.Line2D([0], [0], color='green', linestyle='-', label='Original Signal'),
            plt.Line2D([0], [0], color='blue', linestyle='--', label=filter_label)
        ]
        ax.legend(handles=legend_elements)
        ax.set_xlabel('Sample Number')
        ax.set_ylabel('Amplitude')
        ax.set_title('Audio Signal')
        ax.grid(True)
        
        ax.set_xlim(-0.02 * len(original_signal), len(original_signal) + 0.02 * len(original_signal))
        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


    def apply_filter(self, filter_type):
        if self.audio_signal is None:
            return

        cutoff_frequency = self.cut_off.get()

        if filter_type == 'lowpass':
            self.filtered_signal = self.controller.lowpass_filter(self.audio_signal, self.sampling_rate, cutoff=cutoff_frequency)
            self.current_filter = 'lowpass'
        elif filter_type == 'highpass':
            self.filtered_signal = self.controller.highpass_filter(self.audio_signal, self.sampling_rate, cutoff=cutoff_frequency)
            self.current_filter = 'highpass'

        self.plot_audio_signal(self.audio_signal, self.filtered_signal, self.filter_plot_frame)

    def save_filtered_audio(self):
        if self.filtered_signal is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if save_path:
                wav.write(save_path, self.sampling_rate, self.filtered_signal.astype(np.int16))

    def close_window(self):
        sys.exit()

if __name__ == "__main__":
    controller = LowPassHighPassController()
    app = lowPassHighPassWindow(controller)
    app.mainloop()
