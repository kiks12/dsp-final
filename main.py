
from views import MainWindow
from controllers import MainController

main_controller = MainController()
main_window = MainWindow.MainWindow(main_controller)
main_window.start_mainloop()
