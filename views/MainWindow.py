
import customtkinter

from PIL import Image
from controllers.MainController import MainController


class MainWindow(customtkinter.CTk):

    controller: MainController

    def __init__(self, controller):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        self.geometry("800x500")
        self.title("Digital Signal Processing")
        self.controller = controller

        self.initialize_layout()

    def initialize_layout(self):
        side_image = Image.open("./images/side-img.png")
        self.design_frame = customtkinter.CTkFrame(
            self, width=450, height=500
        )
        self.image = customtkinter.CTkImage(
            dark_image=side_image, light_image=side_image, size=(450, 500)
        )
        self.image_label = customtkinter.CTkLabel(
            self.design_frame, text="", image=self.image
        )
        self.image_label.pack()
        self.design_frame.grid(column=0, row=0)
        self.initialize_buttons()

    def initialize_buttons(self):
        self.buttons_frame = customtkinter.CTkFrame(
            self, width=350, height=500, fg_color="transparent"
        )
        self.header_label = customtkinter.CTkLabel(
            self.buttons_frame, text="Digital Signal Processing", font=("Helvetica", 24)
        )
        self.adc_button = customtkinter.CTkButton(
            self.buttons_frame, text="Analog to Digital Conversion", width=300, height=40, corner_radius=10, command=lambda: self.controller.open_analog_digital_window()
        )
        self.fir_button = customtkinter.CTkButton(
            self.buttons_frame, text="Finite Impulse Response Filter", width=300, height=40, corner_radius=10
        )
        self.moving_average_button = customtkinter.CTkButton(
            self.buttons_frame, text="Moving Average Filter", width=300, height=40, corner_radius=10, command=lambda: self.controller.open_moving_average_window()
        )
        self.low_high_button = customtkinter.CTkButton(
            self.buttons_frame, text="Low/High Pass Filter Conversion", width=300, height=40, corner_radius=10
        )
        self.exit_button = customtkinter.CTkButton(
            self.buttons_frame, text="Exit", width=300, height=40, corner_radius=10, command=lambda: self.controller.exit_app()
        )

        self.header_label.pack(pady=35, padx=25, anchor="center")
        self.adc_button.pack(pady=10, padx=25)
        self.fir_button.pack(pady=10, padx=25)
        self.moving_average_button.pack(pady=10, padx=25)
        self.low_high_button.pack(pady=10, padx=25)
        self.exit_button.pack(pady=35, padx=25)

        self.buttons_frame.grid(column=1, row=0)
