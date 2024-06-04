import sys
from views import MovingAverageWindow, FIRFilterWindow, LowPassHighPassWindow
from controllers import MovingAverageController, FIRFilterController, LowPassHighPassController


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
        # kabit yung code for opening new window
        pass

    def open_fir_window(self):
        fir_filter_controller = FIRFilterController.FIRFilterController()
        self.fir_filter_window = FIRFilterWindow.FIRFilterWindow(fir_filter_controller)
        self.fir_filter_window.mainloop()

        
    def open_low_high_window(self):
        self.low_high_controller = LowPassHighPassController.LowPassHighPassController()
        self.low_high_window = LowPassHighPassWindow.lowPassHighPassWindow(
            self.low_high_controller
        )
        self.low_high_window.mainloop()

    def exit_app(self):
        sys.exit()
