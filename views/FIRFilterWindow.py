import tkinter as tk
from tkinter import filedialog
from controllers import FIRFilterController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from PIL import Image, ImageFilter

EDGE_DETECTION_FILTER = "edge_detection"
BLUR_DETECTION_FILTER = "blur"


class FIRFilterWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.geometry("1000x700")
        self.title("FIR Filter Window")
        self.resizable(False, False)

        self.controller = controller

        self.initialize_layout()

    def initialize_layout(self):
        self.header = ctk.CTkFrame(self, width=1000, height=100)
        self.header_label = ctk.CTkLabel(self.header, text="FIR Filter", font=(
            "Helvetica", 20), width=740, anchor="w")
        self.header_label.grid(
            column=0, row=0, columnspan=8, padx=10, pady=10, sticky="w")
        self.header.pack(padx=10, pady=10)

        self.load_audio_button = ctk.CTkButton(
            self, text="Load Audio", command=self.open_file_dialog, width=100, height=40)
        self.load_audio_button.pack(pady=10)

        self.load_image_button = ctk.CTkButton(
            self, text="Load Image", command=self.open_image_dialog, width=100, height=40)
        self.load_image_button.pack(pady=10)

        self.figure_frame = ctk.CTkFrame(self, width=960, height=480)
        self.figure_frame.pack(pady=20)

    def open_file_dialog(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.show_cutoff_selection_dialog(filename)

    def open_image_dialog(self):
        self.image_filename = filedialog.askopenfilename()
        if self.image_filename:
            self.show_filter_selection_dialog()

    def show_filter_selection_dialog(self):
        filter_window = ctk.CTkToplevel(self)
        filter_window.geometry("200x100")
        filter_window.title("Confirm Filter")

        def confirm_filter():
            selected_filter = self.filter_var.get()
            self.controller.process_image(self.image_filename, selected_filter)
            filter_window.destroy()

        self.filter_var = tk.StringVar()
        ctk.CTkLabel(filter_window, text="Choose Filter: ",
                     font=("Helvica", 14)).pack(pady=20)

        blur_button = ctk.CTkButton(filter_window, text="Blur")
        blur_button.pack(pady=10)

        def on_blur_button_click():
            self.filter_var.set(BLUR_DETECTION_FILTER)
            blur_button.configure(text="Blur (selected)")

        blur_button.configure(command=on_blur_button_click)

        edge_button = ctk.CTkButton(filter_window, text="Edge Detection")
        edge_button.pack(pady=10)

        def on_edge_button_click():
            self.filter_var.set(EDGE_DETECTION_FILTER)
            edge_button.configure(text="Edge Detection (selected)")

        edge_button.configure(command=on_edge_button_click)

        ctk.CTkButton(filter_window, text="Confirm",
                      command=confirm_filter).pack(pady=10)

    def show_cutoff_selection_dialog(self, filename):
        cutoff_window = ctk.CTkToplevel(self)
        cutoff_window.geometry("300x200")
        cutoff_window.title("Select Cutoff Frequency")

        ctk.CTkLabel(cutoff_window, text="Select Cutoff Frequency:",
                     font=("Helvetica", 14)).pack(pady=20)

        ctk.CTkButton(cutoff_window, text="8 kHz", command=lambda: self.process_audio(
            filename, 8000)).pack(pady=5)
        ctk.CTkButton(cutoff_window, text="16 kHz", command=lambda: self.process_audio(
            filename, 16000)).pack(pady=5)
        ctk.CTkButton(cutoff_window, text="32 kHz", command=lambda: self.process_audio(
            filename, 32000)).pack(pady=5)

    def process_audio(self, filename, cutoff):
        self.controller.process_audio(filename, cutoff)
        self.plot_audio()

    def plot_audio(self):
        figure = self.controller.get_figure()
        canvas = FigureCanvasTkAgg(figure, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    controller = FIRFilterController.FIRFilterController()
    app = FIRFilterWindow(controller)
    app.mainloop()
