
import sys

from views import MovingAverageWindow
from views import AnalogToDigitalWindow
from controllers import MovingAverageController
from controllers import AnalogToDigitalController


class MainController:

    def __init__(self):
        print("Initialize Main Controller")

    def open_moving_average_window(self):
        self.moving_average_controller = MovingAverageController.MovingAverageController()
        self.moving_average_window = MovingAverageWindow.MovingAverageWindow(
            self.moving_average_controller
        )
        self.moving_average_window.mainloop()

    def open_analog_digital_window(self):
        self.analog_to_digital_controller = AnalogToDigitalController.AnalogToDigitalController()
        self.analog_to_digital_window = AnalogToDigitalWindow.AnalogToDigitalWindow(
            self.analog_to_digital_controller
        )
        self.analog_to_digital_window.mainloop()

    def open_fir_window(self):
        # kabit yung code for opening new window
        pass

    def open_low_high_window(self):
        # kabit yung code for opening new window
        pass

    def exit_app(self):
        sys.exit()
