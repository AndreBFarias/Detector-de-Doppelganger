import os
import threading
import time

import customtkinter
from PIL import Image, ImageDraw, ImageFilter

from src.core.models import ModelLoader


def create_logo_with_shadow(image: Image.Image, size: tuple[int, int], shadow_radius: int = 8) -> Image.Image:
    padding = shadow_radius * 2
    canvas_size = (size[0] + padding, size[1] + padding)

    img = image.copy()
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    img = img.resize(size, Image.Resampling.LANCZOS)

    shadow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", size, (0, 0, 0, 0))

    r, g, b, a = img.split()
    shadow_layer.putalpha(a)

    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.bitmap((0, 0), a, fill=(0, 0, 0, 180))

    offset = padding // 2
    shadow.paste(shadow_layer, (offset, offset))

    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_radius))

    result = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    result = Image.alpha_composite(result, shadow)
    result.paste(img, (offset, offset), img)

    return result


class SplashScreen(customtkinter.CTkToplevel):
    BG_COLOR = "#1a1a2e"
    CORNER_RADIUS = 20

    def __init__(self, master):
        super().__init__(master)

        self.width = 580
        self.height = 380

        self.title("Carregando Modelos...")
        self.overrideredirect(True)
        self.configure(fg_color=self.BG_COLOR)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (self.width / 2))
        y_cordinate = int((screen_height / 2) - (self.height / 2))
        self.geometry(f"{self.width}x{self.height}+{x_cordinate}+{y_cordinate}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(
            self, corner_radius=self.CORNER_RADIUS, fg_color=self.BG_COLOR, border_width=0
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.content_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        self.logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icon.png")

        try:
            self.logo_image = Image.open(self.logo_path)
            logo_with_shadow = create_logo_with_shadow(self.logo_image, (120, 120), shadow_radius=10)
            self.logo_ctk = customtkinter.CTkImage(
                light_image=logo_with_shadow, dark_image=logo_with_shadow, size=(150, 150)
            )
            self.logo_label = customtkinter.CTkLabel(
                self.content_frame, image=self.logo_ctk, text="", fg_color="transparent"
            )
            self.logo_label.pack(pady=(5, 15))
        except FileNotFoundError:
            print(f"Erro: icon.png nao encontrado em {self.logo_path}")
            self.logo_label = customtkinter.CTkLabel(self.content_frame, text="[Logo]", width=128, height=128)
            self.logo_label.pack(pady=(5, 15))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            self.logo_label = customtkinter.CTkLabel(self.content_frame, text="[!]", width=128, height=128)
            self.logo_label.pack(pady=(5, 15))

        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Detector de Doppelgänger",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            fg_color="transparent",
        )
        self.title_label.pack(pady=(0, 10))

        self.status_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Iniciando... Carregando modelos de IA.",
            font=customtkinter.CTkFont(size=14),
            fg_color="transparent",
        )
        self.status_label.pack(pady=5)

        self.progress_bar = customtkinter.CTkProgressBar(self.content_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(15, 10))

        self.callback = None

    def update_status(self, text, value):
        self.status_label.configure(text=text)
        self.progress_bar.set(value)

    def finish(self):
        self.destroy()
        if self.callback:
            self.callback()

    def load_models_thread(self):
        try:
            loader = ModelLoader(status_callback=self.update_status)
            loader.load_models()

            self.update_status("Modelos carregados. Iniciando aplicação...", 1.0)
            time.sleep(1.5)

            self.after(0, self.finish)
        except Exception as e:
            print(f"Erro critico: {e}")
            self.update_status(f"Erro ao carregar: {e}", 0.9)
            time.sleep(2)
            self.after(0, self.finish)

    def start_download(self, callback):
        self.callback = callback
        self.lift()
        self.focus_force()
        self.grab_set()

        threading.Thread(target=self.load_models_thread, daemon=True).start()
