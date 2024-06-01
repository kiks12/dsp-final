import numpy as np
import cv2
import pygame
import soundfile as sf
from scipy import signal
from matplotlib.figure import Figure

class FIRFilterController:
    def __init__(self):
        print("Initialize FIRFilterController")
        pygame.mixer.init()
        self.figure = Figure(figsize=(7, 5))

    def apply_fir_to_audio(self, audio_data, cutoff, samplerate):
        taps = 30
        b = signal.firwin(taps, cutoff, fs=samplerate)
        filtered_audio = signal.lfilter(b, 1, audio_data)
        return filtered_audio

    def adjust_amplitude(self, filtered_audio, cutoff):
        if cutoff == 8000:
            return filtered_audio * 1.5
        elif cutoff == 16000:
            return filtered_audio * 1.2
        else:
            return filtered_audio

    def apply_edge_detection_to_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges

    def process_image(self, filename):
        if filename:
            original_image = cv2.imread(filename)
            filtered_image = self.apply_edge_detection_to_image(original_image)

            cv2.imshow('Original Image', original_image)
            cv2.imshow('Filtered Image', filtered_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def process_audio(self, filename, cutoff):
        if filename:
            original_audio, samplerate = sf.read(filename)
            
            if cutoff <= 0 or cutoff >= samplerate / 2:
                print("Invalid cutoff frequency. Using default value.")
                cutoff = 1000 
            
            filtered_audio = self.apply_fir_to_audio(original_audio, cutoff, samplerate)
            adjusted_filtered_audio = self.adjust_amplitude(filtered_audio, cutoff)
            
            self.plot_audio(original_audio, adjusted_filtered_audio, samplerate)

    def plot_audio(self, original_audio, filtered_audio, samplerate):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        time = np.arange(0, len(original_audio)) / samplerate
        ax.plot(time, original_audio, label="Original")
        ax.plot(time, filtered_audio, label="Filtered", alpha=0.7)
        ax.legend()

    def get_figure(self):
        return self.figure

    def close_window(self):
        pygame.mixer.quit()
