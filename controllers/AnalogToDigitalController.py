import numpy as np
import matplotlib.pyplot as plt

class AnalogToDigitalController:
    def __init__(self, bit_depth=8):
        self.bit_depth = bit_depth

    def adc_process(self, analog_signal, sampling_interval):
        if sampling_interval <= 0:
            raise ValueError("Sampling interval must be a positive value greater than zero.")

        # Sampling
        sample_points = np.arange(0, len(analog_signal), int(sampling_interval))
        sampled_signal = analog_signal[sample_points]

        # Quantization
        min_amplitude = np.min(sampled_signal)
        max_amplitude = np.max(sampled_signal)
        quantization_levels = 2 ** self.bit_depth

        quantized_signal = np.round((sampled_signal - min_amplitude) / (max_amplitude - min_amplitude) * (quantization_levels - 1))
        quantized_signal = quantized_signal / (quantization_levels - 1) * (max_amplitude - min_amplitude) + min_amplitude

        return quantized_signal, sample_points

    def plot_signal(self, signal, sample_points=None, title='Signal'):
        plt.figure()
        plt.plot(signal, label='Analog Signal')
        if sample_points is not None:
            plt.plot(sample_points, signal[sample_points], 'ro', label='Sampled Points')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()
