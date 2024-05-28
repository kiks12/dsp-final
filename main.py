
from views import MainWindow
from controllers import MainController
import customtkinter

customtkinter.set_default_color_theme("green")

main_controller = MainController.MainController()
main_window = MainWindow.MainWindow(main_controller)

main_window.mainloop()
