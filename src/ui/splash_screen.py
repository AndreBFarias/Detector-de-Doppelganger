import customtkinter
import os
from PIL import Image
import threading
import time

from src.models import ModelLoader

class SplashScreen(customtkinter.CTkToplevel):
    """
    Janela de splash screen que carrega os modelos em segundo plano.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.geometry("600x400")
        self.title("Carregando Modelos...")
        self.overrideredirect(True) 
        
        # Centraliza a janela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (600/2))
        y_cordinate = int((screen_height/2) - (400/2))
        self.geometry(f"600x400+{x_cordinate}+{y_cordinate}")

        # Configura o layout da grade
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame principal
        self.frame = customtkinter.CTkFrame(self, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # 1
        # --- CORREÇÃO DO CAMINHO DO ÍCONE ---
        # 1
        self.logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "assets", 
            "icon.png"
        )
        
        try:
            self.logo_image = Image.open(self.logo_path)
            self.logo_ctk = customtkinter.CTkImage(self.logo_image, size=(128, 128))
            self.logo_label = customtkinter.CTkLabel(self.frame, image=self.logo_ctk, text="")
            self.logo_label.pack(pady=40)
        except FileNotFoundError:
            print(f"Erro ao carregar a logo: Arquivo de ícone necessário não encontrado: {self.logo_path}")
            # Cria um label de fallback se a imagem não for encontrada
            self.logo_label = customtkinter.CTkLabel(self.frame, text="[Logo]", width=128, height=128)
            self.logo_label.pack(pady=40)
        except Exception as e:
            print(f"Erro inesperado ao carregar a logo: {e}")
            self.logo_label = customtkinter.CTkLabel(self.frame, text="[Logo Error]", width=128, height=128)
            self.logo_label.pack(pady=40)

        # Título
        self.title_label = customtkinter.CTkLabel(
            self.frame, 
            text="Detector de Doppelgänger", 
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 10))

        # Status
        self.status_label = customtkinter.CTkLabel(
            self.frame, 
            text="Iniciando... Carregando modelos de IA.", 
            font=customtkinter.CTkFont(size=14)
        )
        self.status_label.pack(pady=5)

        # Barra de Progresso
        self.progress_bar = customtkinter.CTkProgressBar(self.frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20, padx=20)
        
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
            
            # Simula um tempo extra para o usuário ler a mensagem final
            self.update_status("Modelos carregados. Iniciando aplicação...", 1.0)
            time.sleep(1.5) 

            self.after(0, self.finish)
        except Exception as e:
            # Em caso de erro, ainda tenta fechar o splash e abrir a main window
            # A main window (ou o AppCore) terá que lidar com o modelo não carregado
            print(f"Erro crítico ao carregar modelos: {e}")
            self.update_status(f"Erro ao carregar: {e}", 0.9)
            time.sleep(2) # Dá tempo para ler o erro
            self.after(0, self.finish)

    def start_download(self, callback):
        self.callback = callback
        self.lift()
        self.focus_force()
        self.grab_set()
        
        # Inicia o carregamento em uma thread separada
        threading.Thread(target=self.load_models_thread, daemon=True).start()
