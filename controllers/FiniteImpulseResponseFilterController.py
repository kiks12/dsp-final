import numpy as np
import scipy.signal as signal
import soundfile as sf
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
from PIL import Image
import pandas as pd

class FIRFilterController:
    def __init__(self):
        print("Initialize FIRFilterController")
        self.audio_data = None
        self.image_data = None
        self.sample_rate = None
        self.filter_taps = None

    def load_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac")])
        if file_path:
            self.audio_data, self.sample_rate = sf.read(file_path)
            messagebox.showinfo("Load Audio", "Audio file loaded successfully.")
            return self.audio_data, self.sample_rate
        return None, None

    def load_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_data = Image.open(file_path)
            messagebox.showinfo("Load Image", "Image file loaded successfully.")
            return self.image_data
        return None

    def design_fir_filter(self, numtaps, cutoff, filter_type='low'):
        self.filter_taps = signal.firwin(numtaps, cutoff, pass_zero=filter_type, fs=self.sample_rate)
        messagebox.showinfo("Design Filter", "FIR Filter designed successfully.")
        return self.filter_taps

    def apply_fir_filter_audio(self):
        if self.audio_data is not None and self.filter_taps is not None:
            filtered_audio = signal.lfilter(self.filter_taps, 1.0, self.audio_data)
            return filtered_audio
        messagebox.showerror("Error", "Audio data or filter not loaded.")
        return None

    def apply_fir_filter_image(self):
        if self.image_data is not None and self.filter_taps is not None:
            image_array = np.asarray(self.image_data)
            if image_array.ndim == 3:  # Color image
                for i in range(3):  # Apply the filter on each channel
                    image_array[:, :, i] = signal.convolve2d(image_array[:, :, i], self.filter_taps[:, None], mode='same')
            else:  # Grayscale image
                image_array = signal.convolve2d(image_array, self.filter_taps[:, None], mode='same')
            filtered_image = Image.fromarray(np.uint8(image_array))
            return filtered_image
        messagebox.showerror("Error", "Image data or filter not loaded.")
        return None

    def save_audio_file(self, filtered_audio):
        if filtered_audio is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if file_path:
                sf.write(file_path, filtered_audio, self.sample_rate)
                messagebox.showinfo("Save Audio", "Filtered audio saved successfully.")
        else:
            messagebox.showerror("Error", "No filtered audio to save.")

    def save_image_file(self, filtered_image):
        if filtered_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                filtered_image.save(file_path)
                messagebox.showinfo("Save Image", "Filtered image saved successfully.")
        else:
            messagebox.showerror("Error", "No filtered image to save.")
