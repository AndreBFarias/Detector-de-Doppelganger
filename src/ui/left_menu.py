from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import customtkinter
from PIL import Image

import config


class LeftMenu(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#181825", corner_radius=0, border_width=0)

        # Configuração do Grid Principal (4 linhas com peso igual para distribuição vertical)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- BLOCO 1: LOGO ---
        self.logo_frame = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.logo_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_rowconfigure(0, weight=1)

        try:
            # CORREÇÃO DO ÍCONE: Usando o arquivo icon.png existente
            logo_path = os.path.join(config.ASSETS_DIR, "icon.png")

            if os.path.exists(logo_path):
                # Exibe o ícone em 180x180 no menu
                self.logo_image = customtkinter.CTkImage(light_image=Image.open(logo_path),
                                                         dark_image=Image.open(logo_path),
                                                         size=(180, 180))
                self.logo_label = customtkinter.CTkLabel(self.logo_frame, image=self.logo_image, text="")
                self.logo_label.grid(row=0, column=0)
            else:
                 self.logo_label = customtkinter.CTkLabel(self.logo_frame, text="🧠", font=("Inter", 60))
                 self.logo_label.grid(row=0, column=0)

        except Exception as e:
            print(f"Erro ao carregar a logo no menu: {e}")
            self.logo_label = customtkinter.CTkLabel(self.logo_frame, text="🧠", font=("Inter", 60))
            self.logo_label.grid(row=0, column=0)


        # --- BLOCO 2: MODELOS E CONTROLES ---
        self.models_frame = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.models_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.models_frame.grid_columnconfigure(0, weight=1)

        self.mode_label = customtkinter.CTkLabel(self.models_frame, text="Modo de Operacao", text_color=config.ACCENT_GREEN, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.mode_label.grid(row=0, column=0, padx=20, pady=(5, 2))

        self.mode_menu = customtkinter.CTkOptionMenu(self.models_frame, values=["Local (Offline)", "API (Groq/Gemini)"])
        self.mode_menu.set("Local (Offline)")
        self.mode_menu.grid(row=1, column=0, padx=20, pady=2, sticky="ew")

        self.model_label = customtkinter.CTkLabel(self.models_frame, text="Modelo de Humanizacao", text_color=config.ACCENT_GREEN, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.model_label.grid(row=2, column=0, padx=20, pady=(5, 2))

        self.model_menu = customtkinter.CTkOptionMenu(self.models_frame, values=["Leve (CPU)", "Equilibrado (CPU)", "Profundo (CPU)"])
        self.model_menu.grid(row=3, column=0, padx=20, pady=2, sticky="ew")

        self.creativity_label = customtkinter.CTkLabel(self.models_frame, text="Nivel de Criatividade")
        self.creativity_label.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="w")

        self.creativity_slider = customtkinter.CTkSlider(self.models_frame, from_=0.5, to=1.2, progress_color=config.ACCENT_GREEN, button_color=config.ACCENT_PURPLE, button_hover_color=config.ACCENT_PINK)
        self.creativity_slider.set(0.8)
        self.creativity_slider.grid(row=5, column=0, padx=20, pady=(0, 2), sticky="ew")

        self.intensity_label = customtkinter.CTkLabel(self.models_frame, text="Intensidade do Processamento")
        self.intensity_label.grid(row=6, column=0, padx=20, pady=(2, 0), sticky="w")

        self.intensity_slider = customtkinter.CTkSlider(self.models_frame, from_=1, to=5, progress_color=config.ACCENT_GREEN, button_color=config.ACCENT_PURPLE, button_hover_color=config.ACCENT_PINK)
        self.intensity_slider.set(3)
        self.intensity_slider.grid(row=7, column=0, padx=20, pady=(0, 5), sticky="ew")


        # --- BLOCO 3: AÇÕES DE ENTRADA E PROCESSAMENTO ---
        self.input_frame = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.input_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)
        # Distribuição vertical igualitária
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_rowconfigure(2, weight=1)
        self.input_frame.grid_rowconfigure(3, weight=1)
        self.input_frame.grid_rowconfigure(4, weight=1)
        self.input_frame.grid_rowconfigure(5, weight=1)

        self.input_actions_label = customtkinter.CTkLabel(self.input_frame, text="Ações de Entrada", text_color=config.ACCENT_GREEN, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.input_actions_label.grid(row=0, column=0, padx=20, pady=2)

        self.select_file_button = customtkinter.CTkButton(self.input_frame, text="Selecionar Arquivo", text_color="black", height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.select_file_button.grid(row=1, column=0, padx=20, pady=2, sticky="ew")

        self.paste_button = customtkinter.CTkButton(self.input_frame, text="Colar Texto", text_color="black", height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.paste_button.grid(row=2, column=0, padx=20, pady=2, sticky="ew")

        self.humanize_button = customtkinter.CTkButton(self.input_frame, text="Humanizar", height=40, fg_color=config.ACCENT_GREEN, text_color="black", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.humanize_button.grid(row=3, column=0, padx=20, pady=2, sticky="ew")

        self.progress_bar = customtkinter.CTkProgressBar(self.input_frame, height=8, progress_color=config.ACCENT_GREEN)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=2, sticky="ew")

        self.time_label = customtkinter.CTkLabel(self.input_frame, text="Tempo estimado: --")
        self.time_label.grid(row=5, column=0, padx=20, pady=2)


        # --- BLOCO 4: AÇÕES DE SAÍDA ---
        self.output_frame = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.output_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.output_frame.grid_columnconfigure(0, weight=1)
        # Distribuição vertical igualitária
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_rowconfigure(2, weight=1)
        self.output_frame.grid_rowconfigure(3, weight=1)
        self.output_frame.grid_rowconfigure(4, weight=1)

        self.output_actions_label = customtkinter.CTkLabel(self.output_frame, text="Ações de Saída", text_color=config.ACCENT_GREEN, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.output_actions_label.grid(row=0, column=0, padx=20, pady=2)

        self.style_label = customtkinter.CTkLabel(self.output_frame, text="Estilo de Saída")
        self.style_label.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        self.style_menu = customtkinter.CTkOptionMenu(self.output_frame, values=["default"])
        self.style_menu.grid(row=2, column=0, padx=20, pady=2, sticky="ew")

        self.copy_button = customtkinter.CTkButton(self.output_frame, text="Copiar Essência", height=40, fg_color=config.ACCENT_PURPLE, hover_color=config.ACCENT_PINK, text_color="black", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.copy_button.grid(row=3, column=0, padx=20, pady=2, sticky="ew")

        self.save_button = customtkinter.CTkButton(self.output_frame, text="Salvar Como...", height=40, fg_color=config.ACCENT_PURPLE, hover_color=config.ACCENT_PINK, text_color="black", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.save_button.grid(row=4, column=0, padx=20, pady=2, sticky="ew")
