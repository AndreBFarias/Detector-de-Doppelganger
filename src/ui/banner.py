from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import customtkinter

import config


class Banner(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(height=140, fg_color="transparent", border_width=0, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        self.title_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="")

        # "Detector de " (Cinza)
        self.title_part1 = customtkinter.CTkLabel(self.title_frame, text="Detector de ", text_color=("gray80", "gray90"), font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_part1.pack(side="left")

        self.title_part2 = customtkinter.CTkLabel(self.title_frame, text="Mimico", text_color=config.ACCENT_GREEN, font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_part2.pack(side="left")

        # " - Identificador e Humanizador de " (Cinza)
        self.title_part3 = customtkinter.CTkLabel(self.title_frame, text=" - Identificador e Humanizador de ", text_color=("gray60", "gray70"), font=customtkinter.CTkFont(size=22))
        self.title_part3.pack(side="left")

        self.title_part4 = customtkinter.CTkLabel(self.title_frame, text="IA", text_color=config.ACCENT_GREEN, font=customtkinter.CTkFont(size=22, weight="bold"))
        self.title_part4.pack(side="left")
