
import sys

from views import MovingAverageWindow
from controllers import MovingAverageController


class MainController:

    def __init__(self):
        print("Initialize Main Controller")

    def open_moving_average_window(self):
        self.moving_average_controller = MovingAverageController.MovingAverageController()
        self.moving_average_window = MovingAverageWindow.MovingAverageWindow(
            self.moving_average_controller
        )
        self.moving_average_window.start_mainloop()

    def exit_app(self):
        sys.exit()
