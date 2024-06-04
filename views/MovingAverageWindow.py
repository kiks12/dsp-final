
import customtkinter
import tkinter as tk

from controllers import MovingAverageController


class MovingAverageWindow(customtkinter.CTk):

    RANDOM_FORM_WIDTH = 250
    controller: MovingAverageController.MovingAverageController

    def __init__(self, controller):
        super().__init__()
        self.geometry("1000x700")
        self.title("Moving Average Filter")
        self.resizable(False, False)

        self.controller = controller
        self.time_vector_start = tk.IntVar(self, 0)
        self.time_vector_end = tk.IntVar(self, 100)
        self.time_vector_jump = tk.IntVar(self, 100)
        self.random_window = tk.IntVar(self, 2)
        self.import_window = tk.IntVar(self, 2)

        self.import_start = tk.IntVar(self, 0)
        self.import_end = tk.IntVar(self, 0)

        self.initialize_layout()

    def initialize_layout(self):
        self.initialize_header()
        self.initialize_tabview()

    def clear_plots(self):
        for widget in self.random_plot_frame.winfo_children():
            widget.destroy()
        customtkinter.CTkLabel(self.random_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")
        for widget in self.import_plot_frame.winfo_children():
            widget.destroy()
        customtkinter.CTkLabel(self.import_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")

    def initialize_header(self):
        self.header = customtkinter.CTkFrame(
            self, width=1000, height=100
        )
        self.clear_button = customtkinter.CTkButton(
            self.header, text="Clear", command=self.clear_plots, width=100, height=40)
        self.quit_button = customtkinter.CTkButton(
            self.header, text="Exit", command=lambda: self.close_window(), width=100, height=40
        )
        self.header_label = customtkinter.CTkLabel(
            self.header, text="Moving Average Filter", font=("Helvetica", 20), width=740, anchor="w")
        self.header_label.grid(
            column=0, row=0, columnspan=8, padx=10, pady=10, sticky="w")
        self.clear_button.grid(column=8, row=0, padx=5, pady=10, sticky="e")
        self.quit_button.grid(column=9, row=0, padx=5, pady=10, sticky="e")
        self.header.pack(padx=10, pady=10)

    def initialize_tabview(self):
        self.tab_view = customtkinter.CTkTabview(
            self,
            width=1000, height=680, anchor="nw"
        )
        self.random_tab = self.tab_view.add("Random")
        self.csv_tab = self.tab_view.add("Import CSV")

        self.initialize_random_form()
        self.initialize_import_form()

        self.tab_view.pack(pady=10, padx=10)

    def initialize_random_form(self):
        self.random_form_frame = customtkinter.CTkFrame(
            self.random_tab, width=self.RANDOM_FORM_WIDTH, height=600
        )
        self.create_time_vector_form()

        self.random_plot_frame = customtkinter.CTkFrame(
            self.random_tab, width=850, height=600
        )
        customtkinter.CTkLabel(self.random_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")

        self.random_form_frame.grid(column=0, row=0, padx=20)
        self.random_plot_frame.grid(column=1, row=0)

    def initialize_import_form(self):
        self.import_form_frame = customtkinter.CTkFrame(
            self.csv_tab, width=self.RANDOM_FORM_WIDTH, height=600
        )

        self.create_import_form()

        self.import_plot_frame = customtkinter.CTkFrame(
            self.csv_tab, width=850, height=600
        )
        customtkinter.CTkLabel(self.import_plot_frame, text="Please Generate Data first.").place(
            relx=0.5, rely=0.5, anchor="center")

        self.import_form_frame.grid(column=0, row=0, padx=20)
        self.import_plot_frame.grid(column=1, row=0)

    def create_import_form(self):
        self.x_combobox = customtkinter.CTkComboBox(
            self.import_form_frame, values=[], width=self.RANDOM_FORM_WIDTH, height=40, command=lambda x: self.controller.set_selected_x_column(x)
        )
        self.y_combobox = customtkinter.CTkComboBox(
            self.import_form_frame, values=[], width=self.RANDOM_FORM_WIDTH, height=40, command=lambda y: self.controller.set_selected_y_column(y)
        )
        self.x_combobox.set("Please select column for x: ")
        self.y_combobox.set("Please select column for y: ")
        self.import_button = customtkinter.CTkButton(
            self.import_form_frame, text="Import CSV", command=lambda: self.controller.import_csv(self.x_combobox, self.y_combobox, self.import_data_range_slider_start, self.import_data_range_slider_end, self.window_end_label), corner_radius=10, width=self.RANDOM_FORM_WIDTH, height=40
        ).pack(pady=10)
        customtkinter.CTkFrame(
            self.import_form_frame, width=self.RANDOM_FORM_WIDTH, height=10, fg_color="transparent"
        ).pack()
        customtkinter.CTkLabel(
            self.import_form_frame, text="Select Column (X Values): ", anchor="w", font=("Helvetica", 16), width=self.RANDOM_FORM_WIDTH
        ).pack()
        self.x_combobox.pack(pady=10)
        customtkinter.CTkLabel(
            self.import_form_frame, text="Select Column (Y Values): ", anchor="w", font=("Helvetica", 16), width=self.RANDOM_FORM_WIDTH
        ).pack()
        self.y_combobox.pack(pady=10)
        customtkinter.CTkFrame(
            self.import_form_frame, width=self.RANDOM_FORM_WIDTH, height=20, fg_color="transparent"
        ).pack()
        self.import_show_data_button = customtkinter.CTkButton(
            self.import_form_frame, text="Plot Data", width=self.RANDOM_FORM_WIDTH, height=40, command=lambda: self.controller.plot_import_values(self.import_plot_frame, self.import_start.get(), self.import_end.get())
        ).pack(pady=5)
        self.create_window_form_import()

    def create_time_vector_form(self):
        self.create_start_form()
        self.create_end_form()
        self.create_jump_form()
        self.generate_time_vector_button = customtkinter.CTkButton(
            self.random_form_frame, text="Generate Time Vector", command=lambda: self.controller.create_time_vector(self.time_vector_start.get(), self.time_vector_end.get(), self.time_vector_jump.get()), corner_radius=10, width=self.RANDOM_FORM_WIDTH, height=40
        ).pack(pady=10)
        self.create_random_signal_button = customtkinter.CTkButton(
            self.random_form_frame, text="Generate Random Values", command=lambda: self.controller.create_y_values(self.random_plot_frame), corner_radius=10, width=self.RANDOM_FORM_WIDTH, height=40
        ).pack(pady=10)
        customtkinter.CTkFrame(self.random_form_frame, width=self.RANDOM_FORM_WIDTH,
                               height=30, fg_color="transparent").pack()
        self.create_window_form_random()
        self.random_apply_filter_button = customtkinter.CTkButton(
            self.random_form_frame, text="Apply Filter", width=self.RANDOM_FORM_WIDTH, height=40, corner_radius=10, command=lambda: self.controller.apply_moving_average_filter_random(self.random_window.get(), self.random_plot_frame)
        ).pack(pady=10)

    def create_start_form(self):
        self.start_form = customtkinter.CTkFrame(
            self.random_form_frame, width=self.RANDOM_FORM_WIDTH, fg_color="transparent"
        )
        self.start_label = customtkinter.CTkLabel(
            self.start_form, text=f"Start: {self.time_vector_start.get()}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.start_slider = customtkinter.CTkSlider(
            self.start_form, from_=0, to=1000, state="disabled", variable=self.time_vector_start, width=self.RANDOM_FORM_WIDTH, command=lambda x: self.time_vector_start.set(x)
        )
        self.start_label.pack()
        self.start_slider.pack()
        self.start_form.pack(pady=15)

    def create_end_form(self):
        self.end_form = customtkinter.CTkFrame(
            self.random_form_frame, width=self.RANDOM_FORM_WIDTH, fg_color="transparent"
        )
        self.end_label = customtkinter.CTkLabel(
            self.end_form, text=f"End: {self.time_vector_end.get()}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.end_slider = customtkinter.CTkSlider(
            self.end_form, from_=0, to=1000, state="normal", variable=self.time_vector_end,
            width=self.RANDOM_FORM_WIDTH, command=lambda x: self.end_label.configure(
                text=f"End: {int(x)}")
        )
        self.end_label.pack()
        self.end_slider.pack()
        self.end_form.pack(pady=15)

    def create_jump_form(self):
        self.jump_form = customtkinter.CTkFrame(
            self.random_form_frame, width=self.RANDOM_FORM_WIDTH, fg_color="transparent"
        )
        self.jump_label = customtkinter.CTkLabel(
            self.jump_form, text=f"Lines: {self.time_vector_jump.get()}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.jump_slider = customtkinter.CTkSlider(
            self.jump_form, from_=0, to=1000, state="normal", variable=self.time_vector_jump, width=self.RANDOM_FORM_WIDTH, command=lambda x: self.jump_label.configure(text=f"Lines: {int(x)}")
        )
        self.jump_label.pack()
        self.jump_slider.pack()
        self.jump_form.pack(pady=15)

    def create_window_form_random(self):
        self.window_form = customtkinter.CTkFrame(
            self.random_form_frame, width=self.RANDOM_FORM_WIDTH, fg_color="transparent"
        )
        self.window_label = customtkinter.CTkLabel(
            self.window_form, text=f"Window: {self.random_window.get()}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.window_slider = customtkinter.CTkSlider(
            self.window_form, from_=0, to=100, state="normal", variable=self.random_window, width=self.RANDOM_FORM_WIDTH, command=lambda x: self.window_label.configure(text=f"Window: {int(x)}")
        )
        self.window_label.pack()
        self.window_slider.pack()
        self.window_form.pack(pady=15)

    def on_start_slider_change(self, new_value):
        self.window_start_label.configure(text=f"Start: {int(new_value)}")
        self.controller.set_new_start_value(new_value)

    def on_end_slider_change(self, new_value):
        self.window_end_label.configure(text=f"End: {int(new_value)}")
        self.controller.set_end_start_value(new_value)

    def create_window_form_import(self):
        self.window_form_import = customtkinter.CTkFrame(
            self.import_form_frame, width=self.RANDOM_FORM_WIDTH, fg_color="transparent"
        )
        self.window_label_import = customtkinter.CTkLabel(
            self.window_form_import, text=f"Window: {self.import_window.get()}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.window_slider_import = customtkinter.CTkSlider(
            self.window_form_import, from_=0, to=100, state="normal", variable=self.import_window, width=self.RANDOM_FORM_WIDTH, command=lambda x: self.window_label_import.configure(text=f"Window: {int(x)}")
        )
        self.window_start_label = customtkinter.CTkLabel(
            self.window_form_import, text=f"Start: {int(self.import_start.get())}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.import_data_range_slider_start = customtkinter.CTkSlider(
            self.window_form_import, from_=0, to=100, variable=self.import_start, width=self.RANDOM_FORM_WIDTH, command=lambda x: self.on_start_slider_change(x)
        )
        self.window_end_label = customtkinter.CTkLabel(
            self.window_form_import, text=f"End: {int(self.import_end.get())}", font=("Helvetica", 16), anchor="w", width=self.RANDOM_FORM_WIDTH)
        self.import_data_range_slider_end = customtkinter.CTkSlider(
            self.window_form_import, from_=0, to=100, variable=self.import_end, width=self.RANDOM_FORM_WIDTH, command=lambda x: self.on_end_slider_change(x)
        )
        self.apply_filter_import_button = customtkinter.CTkButton(
            self.window_form_import, text="Apply Filter", command=lambda: self.controller.apply_moving_average_filter_import(int(self.import_window.get()), self.import_plot_frame, self.import_start.get(), self.import_end.get()), width=self.RANDOM_FORM_WIDTH, height=40
        )
        self.window_label_import.pack()
        self.window_slider_import.pack()
        self.window_start_label.pack()
        self.import_data_range_slider_start.pack()
        self.window_end_label.pack()
        self.import_data_range_slider_end.pack()
        self.apply_filter_import_button.pack(pady=10)
        self.window_form_import.pack(pady=15)

    def close_window(self):
        self.destroy()
