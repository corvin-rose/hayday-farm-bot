import customtkinter
import mss
import cv2

from PIL import Image
from bot import Bot
from threading import Thread

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

screen_dim = {
    'left': 0,
    'top': 0,
    'width': 1920,
    'height': 1080
}


class Logger(customtkinter.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")

    def log(self, *message):
        self.configure(state="normal")
        self.insert("0.0", " ".join(map(lambda m: str(m), message)) + "\n")
        self.configure(state="disabled")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.sct = mss.mss()

        # configure window
        self.title("Hay Day Farm Bot")
        self.geometry(f"{800}x{710}")

        # configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_columnconfigure(0, weight=1)

        # create toolbar
        self.console_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0)
        self.console_frame.grid(row=0, column=0, sticky="nsew")
        self.console_frame.grid_columnconfigure(0, weight=1)
        self.start_button = customtkinter.CTkButton(self.console_frame, command=self.start_button_click, text="Start")
        self.start_button.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.stop_button = customtkinter.CTkButton(self.console_frame, command=self.stop_button_click, text="Stop")
        self.stop_button.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        self.stop_button.configure(state="disabled")

        # create tracking frame
        self.tracking_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.tracking_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.tracking_image_label = customtkinter.CTkLabel(self.tracking_frame, text="")
        self.tracking_image_label.grid(row=0, column=0, sticky="nsew")
        self.update_screen()

        # create console frame
        self.console_frame = customtkinter.CTkFrame(self, height=100, corner_radius=0)
        self.console_frame.grid(row=2, column=0, sticky="nsew")
        self.console_frame.grid_columnconfigure(0, weight=1)

        self.logger = Logger(master=self.console_frame)
        self.logger.grid(row=0, column=0, sticky="nsew")
        self.logger.log("Initialized Bot UI")

        # bot
        self.bot = Bot(self.logger, self.set_tracking_img)
        self.bot_thread = None

    def update_screen(self):
        data = self.sct.grab(screen_dim)
        tracking_image = customtkinter.CTkImage(Image.frombytes('RGB', data.size, data.bgra, 'raw', 'BGRX'), size=(790, 450))
        self.tracking_image_label.configure(image=tracking_image)
        self.tracking_image_label.image = tracking_image

    def set_tracking_img(self, cv2_data):
        data = cv2.cvtColor(cv2_data, cv2.COLOR_RGB2BGR)
        tracking_image = customtkinter.CTkImage(Image.fromarray(data), size=(790, 450))
        self.tracking_image_label.configure(image=tracking_image)
        self.tracking_image_label.image = tracking_image

    def start_button_click(self):
        self.logger.log("Start")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.start_bot()

    def stop_button_click(self):
        self.logger.log("Stop")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.stop_bot()

    def start_bot(self):
        self.bot_thread = Thread(target=self.bot.bot_loop)
        self.bot_thread.start()

    def stop_bot(self):
        self.bot_thread = None
