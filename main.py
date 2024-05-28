
from views import MainWindow
from controllers import MainController

main_controller = MainController.MainController()
main_window = MainWindow.MainWindow(main_controller)
main_window.mainloop()
