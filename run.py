# 1
import sys
import os
import customtkinter

# 1
# --- CORREÇÃO DO PATH ---
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
# 1
# -------------------------
from src.ui.main_window import MainWindow
from src.ui.splash_screen import SplashScreen
from src.utils.logger import setup_logger

def main():
    # Inicializa o logger antes de qualquer coisa
    setup_logger()
    
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.environ['HF_HOME'] = os.path.join(os.path.dirname(__file__), 'models', 'cache')
    
    # 2
    # Define o caminho para o arquivo de tema customizado
    theme_path = os.path.join(project_root, "src", "utils", "ctk_theme.json")

    # 3
    # Configurações da aparência - Apontando para o JSON customizado
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme(theme_path) 

    # 4
    # Cria a janela raiz mas a esconde
    root = customtkinter.CTk()
    root.withdraw()

    # 4
    # Função para iniciar a aplicação principal
    def start_main_app():
        root.deiconify() 
        root.title("Detector de Doppelgänger")
        root.geometry("1200x800")
        root.minsize(1100, 700)
        
        app = MainWindow(master=root)
        app.pack(expand=True, fill="both")
        
        root.attributes('-zoomed', True)
        root.mainloop()

    # 4
    # Inicia o Splash Screen
    splash = SplashScreen(root)
    splash.start_download(callback=start_main_app)
    splash.mainloop()

# 4
if __name__ == "__main__":
    main()
