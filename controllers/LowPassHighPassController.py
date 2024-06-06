from scipy.signal import butter, lfilter


class LowPassHighPassController:
    def __init__(self):
        pass
    # formula for lowpass filter

    def lowpass_filter(self, signal, sampling_rate, cutoff, order=5):
        nyquist = 0.5 * sampling_rate
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        filtered_signal = lfilter(b, a, signal)
        return filtered_signal
    # formula for highpass filter

    def highpass_filter(self, signal, sampling_rate, cutoff, order=5):
        nyquist = 0.5 * sampling_rate
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        filtered_signal = lfilter(b, a, signal)
        return filtered_signal
