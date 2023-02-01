# 12
import customtkinter

from src.utils.config import Config
from src.ui.context_menu import ContextMenu

class TextInputFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", border_width=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Faz o textbox crescer

        # 13
        # --- CABEÇALHO ---
        self.header = customtkinter.CTkLabel(self, text="Matéria Prima", text_color="white", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, padx=10, pady=(10,5), sticky="w")

        # 13
        # --- CAIXA DE TEXTO ---
        self.textbox = customtkinter.CTkTextbox(self, wrap="word", corner_radius=8, border_width=2)
        self.textbox.grid(row=1, column=0, padx=5, pady=(5,0), sticky="nsew")
        
        # Configurar cor de seleção (acessando o widget tkinter interno)
        self.textbox._textbox.configure(selectbackground=Config.ACCENT_PURPLE, selectforeground=Config.BG_COLOR)
        
        # Adicionar Menu de Contexto e Atalhos (passando o widget interno tkinter)
        self.context_menu = ContextMenu(self.textbox._textbox)

        # 14
        # --- RODAPÉ COM LABELS DE STATUS ---
        self.footer = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.footer.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.footer.grid_columnconfigure((0, 1), weight=1)

        # Frame interno para alinhar os status
        self.stats_frame = customtkinter.CTkFrame(self.footer, fg_color="transparent", border_width=0)
        self.stats_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.stats_frame.grid_columnconfigure(2, weight=1) # Espaçador central

        # Semelhança IA
        self.ia_label_static = customtkinter.CTkLabel(self.stats_frame, text="% Semelhança IA: ", text_color="white", font=customtkinter.CTkFont(size=12))
        self.ia_label_static.grid(row=0, column=0, sticky="w")
        
        self.ia_label_value = customtkinter.CTkLabel(self.stats_frame, text="--", font=customtkinter.CTkFont(size=12))
        self.ia_label_value.grid(row=0, column=1, sticky="w")

        # Naturalidade
        self.nat_label_static = customtkinter.CTkLabel(self.stats_frame, text="% Naturalidade: ", text_color="white", font=customtkinter.CTkFont(size=12))
        self.nat_label_static.grid(row=0, column=3, sticky="e")
        
        self.nat_label_value = customtkinter.CTkLabel(self.stats_frame, text="--", font=customtkinter.CTkFont(size=12))
        self.nat_label_value.grid(row=0, column=4, sticky="e")
