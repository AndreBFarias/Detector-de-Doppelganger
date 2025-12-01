# 5
import customtkinter
from PIL import Image
import os
from src.utils.config import Config # Importando o caminho base correto

class Banner(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(height=140, fg_color="transparent", border_width=0, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        # 5
        # --- TÍTULO ---
        self.title_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="")
        
        # "Detector de " (Cinza)
        self.title_part1 = customtkinter.CTkLabel(self.title_frame, text="Detector de ", text_color=("gray80", "gray90"), font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_part1.pack(side="left")
        
        # "Mímico" (Verde)
        self.title_part2 = customtkinter.CTkLabel(self.title_frame, text="Mímico", text_color=Config.ACCENT_GREEN, font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_part2.pack(side="left")
        
        # " - Identificador e Humanizador de " (Cinza)
        self.title_part3 = customtkinter.CTkLabel(self.title_frame, text=" - Identificador e Humanizador de ", text_color=("gray60", "gray70"), font=customtkinter.CTkFont(size=22))
        self.title_part3.pack(side="left")

        # "IA" (Verde)
        self.title_part4 = customtkinter.CTkLabel(self.title_frame, text="IA", text_color=Config.ACCENT_GREEN, font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_part4.pack(side="left")
