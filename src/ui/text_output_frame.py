from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import customtkinter

import config
from src.ui.context_menu import ContextMenu


class TextOutputFrame(customtkinter.CTkFrame):
    HEADER_COLOR = config.ACCENT_GREEN
    TEXTBOX_BG = config.OUTPUT_BG
    TEXTBOX_BORDER = config.OUTPUT_BORDER
    CORNER_RADIUS = 12

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", border_width=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.header_icon = customtkinter.CTkLabel(
            self.header_frame,
            text="~",
            text_color=self.HEADER_COLOR,
            font=customtkinter.CTkFont(size=22, weight="bold"),
        )
        self.header_icon.pack(side="left", padx=(0, 8))

        self.header = customtkinter.CTkLabel(
            self.header_frame,
            text="Essência Destilada",
            text_color=self.HEADER_COLOR,
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.header.pack(side="left")

        self.textbox_frame = customtkinter.CTkFrame(
            self,
            fg_color=self.TEXTBOX_BG,
            corner_radius=self.CORNER_RADIUS,
            border_width=2,
            border_color=self.TEXTBOX_BORDER,
        )
        self.textbox_frame.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="nsew")
        self.textbox_frame.grid_columnconfigure(0, weight=1)
        self.textbox_frame.grid_rowconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(
            self.textbox_frame,
            wrap="word",
            corner_radius=self.CORNER_RADIUS,
            border_width=0,
            fg_color=self.TEXTBOX_BG,
            text_color=config.TEXT_COLOR,
            font=customtkinter.CTkFont(size=14),
            state="disabled",
        )
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.textbox._textbox.configure(
            selectbackground=config.ACCENT_GREEN, selectforeground=config.BG_COLOR, insertbackground=config.ACCENT_GREEN
        )

        self.context_menu = ContextMenu(self.textbox._textbox)

        self.footer = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.footer.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.footer.grid_columnconfigure((0, 1), weight=1)

        self.stats_frame = customtkinter.CTkFrame(self.footer, fg_color="transparent", border_width=0)
        self.stats_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.stats_frame.grid_columnconfigure(2, weight=1)

        self.ia_label_static = customtkinter.CTkLabel(
            self.stats_frame,
            text="% Semelhança IA: ",
            text_color=config.ACCENT_GREEN,
            font=customtkinter.CTkFont(size=12),
        )
        self.ia_label_static.grid(row=0, column=0, sticky="w")

        self.ia_label_value = customtkinter.CTkLabel(
            self.stats_frame, text="--", font=customtkinter.CTkFont(size=12, weight="bold")
        )
        self.ia_label_value.grid(row=0, column=1, sticky="w")

        self.nat_label_static = customtkinter.CTkLabel(
            self.stats_frame,
            text="% Naturalidade: ",
            text_color=config.ACCENT_GREEN,
            font=customtkinter.CTkFont(size=12),
        )
        self.nat_label_static.grid(row=0, column=3, sticky="e")

        self.nat_label_value = customtkinter.CTkLabel(
            self.stats_frame, text="--", font=customtkinter.CTkFont(size=12, weight="bold")
        )
        self.nat_label_value.grid(row=0, column=4, sticky="e")
