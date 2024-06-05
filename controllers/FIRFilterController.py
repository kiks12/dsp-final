import numpy as np
import cv2
import pygame
import soundfile as sf
from scipy import signal
from matplotlib.figure import Figure
from PIL import Image, ImageFilter

EDGE_DETECTION_FILTER = "edge_detection"
BLUR_DETECTION_FILTER = "blur"

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
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        sobel = np.hypot(sobelx, sobely)
        sobel = sobel / sobel.max() * 255
        sobel = np.uint8(sobel)
        kernel = np.ones((1,5), np.uint8)
        dilated_sobel = cv2.dilate(sobel, kernel, iterations=1)
        return dilated_sobel
        
    def apply_blur_filter(self, image, blur_kernel_size=5, pixelation_factor=10):
        blurred_image = cv2.GaussianBlur(image, (blur_kernel_size, blur_kernel_size), 0)
        height, width = blurred_image.shape[:2]
        small = cv2.resize(blurred_image, (width//pixelation_factor, height//pixelation_factor), interpolation=cv2.INTER_LINEAR)
        pixelated_image = cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)

        return pixelated_image

    def process_image(self, filename, selected_filter):
        if filename:
            original_image = cv2.imread(filename)
            if original_image is None:
                print("Error: Unable to load the original image.")
                return

            if selected_filter == EDGE_DETECTION_FILTER:
                filtered_image = self.apply_edge_detection_to_image(original_image)
            elif selected_filter == BLUR_DETECTION_FILTER:
                filtered_image = self.apply_blur_filter(original_image)

            if filtered_image is None:
                print("Error: Unable to process the filtered image.")
                return

            common_height = min(original_image.shape[0], filtered_image.shape[0])
            common_width = min(original_image.shape[1], filtered_image.shape[1])

            original_image_resized = cv2.resize(original_image, (common_width, common_height))
            filtered_image_resized = cv2.resize(filtered_image, (common_width, common_height))

            if len(filtered_image_resized.shape) == 2: 
                filtered_image_colored = cv2.cvtColor(filtered_image_resized, cv2.COLOR_GRAY2BGR)
            else: 
                filtered_image_colored = filtered_image_resized

            combined_image = np.hstack((original_image_resized, filtered_image_colored))
            max_width = 800 
            if combined_image.shape[1] > max_width:
                scale_factor = max_width / combined_image.shape[1]
                combined_image_resized = cv2.resize(combined_image, (0, 0), fx=scale_factor, fy=scale_factor)
            else:
                combined_image_resized = combined_image

            cv2.imshow('Original and Filtered Image', combined_image_resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def process_audio(self, filename, cutoff):
        if filename:
            try:
                original_audio, samplerate = sf.read(filename)
                
                if cutoff <= 0 or cutoff >= samplerate / 2:
                    print("Invalid cutoff frequency. Using default value.")
                    cutoff = 1000 
                
                filtered_audio = self.apply_fir_to_audio(original_audio, cutoff, samplerate)
                adjusted_filtered_audio = self.adjust_amplitude(filtered_audio, cutoff)
                
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()

                self.plot_audio(original_audio, adjusted_filtered_audio, samplerate)
            except Exception as e:
                print("Error playing audio:", e)

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
