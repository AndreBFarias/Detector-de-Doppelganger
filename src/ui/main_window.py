# 4
import customtkinter
from tkinter import filedialog, messagebox
import tkinter
import queue
import logging
import os
from src.ui.left_menu import LeftMenu
from src.ui.banner import Banner
from src.ui.text_input_frame import TextInputFrame
from src.ui.text_output_frame import TextOutputFrame
from src.core.app_core import AppCore
from src.core.processing_thread import ProcessingThread
from src.output_formatter import save_output
from src.utils.colors import get_color_for_percentage

class MainWindow(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.core = AppCore()
        self.processing_thread = None
        self.ui_queue = queue.Queue()
        
        # Configurar ícone da janela
        try:
            # Caminho absoluto para o ícone
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icon.png"))
            if os.path.exists(icon_path):
                icon_image = tkinter.PhotoImage(file=icon_path)
                self.master.iconphoto(True, icon_image)
                self.master.title("Detector de Doppelgänger") # Força atualização do título/ícone
            else:
                logging.warning(f"Ícone não encontrado em: {icon_path}")
        except Exception as e:
            logging.warning(f"Erro ao definir ícone: {e}")

        # 4
        self.configure(fg_color="#181825", border_width=0, corner_radius=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 4
        self.left_menu = LeftMenu(self, width=280)
        self.left_menu.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        # 4
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        self.main_content.grid_columnconfigure((0, 1), weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # 4
        self.banner = Banner(self.main_content)
        self.banner.grid(row=0, column=0, columnspan=2, sticky="new", pady=(0, 10))

        # 4
        self.text_input = TextInputFrame(self.main_content)
        self.text_input.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

        # 4
        self.text_output = TextOutputFrame(self.main_content)
        self.text_output.grid(row=1, column=1, sticky="nsew", padx=(5, 0))

        # 4
        self.connect_widgets()
        self.after(100, self.process_ui_queue)
        
        # 4
        self.left_menu.humanize_button.configure(state="disabled", text="Carregando...")
        self.after(200, self.initial_load)

    # 4
    def initial_load(self):
        """Carrega os modelos e configurações essenciais ao iniciar a app."""
        style_keys = self.core.load_styles()
        logging.info(f"Chaves de estilo carregadas: {style_keys}")
        
        capitalized_keys = [k.title() for k in style_keys]
        logging.info(f"Chaves capitalizadas: {capitalized_keys}")
        
        # Capitaliza as chaves para exibição (ex: "default" -> "Default")
        self.left_menu.style_menu.configure(values=capitalized_keys)
        self.left_menu.style_menu.set("Default")
        
        if self.core.load_detector_models() and self.core.load_humanizer_model():
            self.left_menu.humanize_button.configure(state="normal", text="Humanizar")
            self.left_menu.time_label.configure(text="Pronto.")
        else:
            messagebox.showerror("Erro Crítico", "Não foi possível carregar os modelos de IA.")
            self.master.destroy()

    # 4
    def connect_widgets(self):
        """Conecta os comandos dos widgets às funções de controle."""
        self.left_menu.select_file_button.configure(command=self.select_file)
        self.left_menu.paste_button.configure(command=self.paste_text)
        self.left_menu.humanize_button.configure(command=self.start_processing)
        self.left_menu.copy_button.configure(command=self.copy_output)
        self.left_menu.model_menu.configure(command=self.on_model_select)
        self.left_menu.save_button.configure(command=self.save_output_as)

    # 4
    def on_model_select(self, model_key):
        """Chamado quando um novo modelo de humanização é selecionado."""
        self.left_menu.humanize_button.configure(state="disabled", text=f"Carregando...")
        self.update() # Força a atualização da UI
        if self.core.load_humanizer_model(model_key):
             self.left_menu.humanize_button.configure(state="normal", text="Humanizar")
        else:
            messagebox.showerror("Erro", f"Não foi possível carregar o modelo {model_key}")
            self.left_menu.humanize_button.configure(state="disabled", text="Erro no modelo")

    # 4
    def start_processing(self):
        """Inicia ou interrompe a thread de processamento de texto."""
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.stop()
            self.left_menu.humanize_button.configure(text="Humanizar")
            self.left_menu.time_label.configure(text="Interrompido.")
            return

        text = self.text_input.textbox.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para humanizar.")
            return

        # 4
        # Limpa a área de saída e os status antigos
        self.text_output.textbox.configure(state="normal")
        self.text_output.textbox.delete("1.0", "end")
        self.text_output.textbox.configure(state="disabled")
        
        # Resetar labels de valor
        self.text_input.ia_label_value.configure(text="--", text_color="white")
        self.text_input.nat_label_value.configure(text="--", text_color="white")
        self.text_output.ia_label_value.configure(text="--", text_color="white")
        self.text_output.nat_label_value.configure(text="--", text_color="white")
        
        self.left_menu.humanize_button.configure(text="Interromper")
        
        self.processing_thread = ProcessingThread(
            app_core=self.core,
            text=text,
            criatividade=self.left_menu.creativity_slider.get(),
            intensidade=self.left_menu.intensity_slider.get(),
            ui_queue=self.ui_queue,
            style_key=self.left_menu.style_menu.get().lower()
        )
        self.processing_thread.start()

    # 4
    def process_ui_queue(self):
        """Processa eventos da thread de processamento para atualizar a UI."""
        try:
            while not self.ui_queue.empty():
                message = self.ui_queue.get_nowait()
                msg_type = message.get("type")

                if msg_type == "status":
                    self.left_menu.time_label.configure(text=message["value"])
                elif msg_type == "initial_stats":
                    color_ia = get_color_for_percentage(message['prob_ia'], inverse=True)
                    color_nat = get_color_for_percentage(message['naturalidade'], inverse=False)
                    
                    self.text_input.ia_label_value.configure(
                        text=f"{message['prob_ia']*100:.2f}%",
                        text_color=color_ia,
                        font=customtkinter.CTkFont(size=16, weight="bold")
                    )
                    self.text_input.nat_label_value.configure(
                        text=f"{message['naturalidade']*100:.2f}%",
                        text_color=color_nat,
                        font=customtkinter.CTkFont(size=16, weight="bold")
                    )
                elif msg_type == "progress":
                    self.left_menu.progress_bar.set(message["progress"])
                    self.text_output.textbox.configure(state="normal")
                    self.text_output.textbox.insert("end", message["chunk"])
                    self.text_output.textbox.see("end")
                    self.text_output.textbox.configure(state="disabled")
                elif msg_type == "final_result":
                    color_ia = get_color_for_percentage(message['prob_ia'], inverse=True)
                    color_nat = get_color_for_percentage(message['naturalidade'], inverse=False)

                    self.text_output.ia_label_value.configure(
                        text=f"{message['prob_ia']*100:.2f}%",
                        text_color=color_ia,
                        font=customtkinter.CTkFont(size=16, weight="bold")
                    )
                    self.text_output.nat_label_value.configure(
                        text=f"{message['naturalidade']*100:.2f}%",
                        text_color=color_nat,
                        font=customtkinter.CTkFont(size=16, weight="bold")
                    )
                elif msg_type == "finished":
                    self.left_menu.humanize_button.configure(text="Humanizar")
                    self.left_menu.progress_bar.set(0)

        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_ui_queue)

    # 4
    def select_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text/Doc Files", "*.txt *.docx *.md"), ("All files", "*.*")])
        if not filepath: return
        
        try:
            if filepath.endswith('.docx'):
                import docx
                doc = docx.Document(filepath)
                full_text = "\n".join([para.text for para in doc.paragraphs])
                self.text_input.textbox.delete("1.0", "end")
                self.text_input.textbox.insert("1.0", full_text)
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.text_input.textbox.delete("1.0", "end")
                    self.text_input.textbox.insert("1.0", f.read())
        except Exception as e:
            messagebox.showerror("Erro ao Abrir", f"Não foi possível ler o arquivo:\n{e}")

    # 4
    def paste_text(self):
        try:
            text = self.clipboard_get()
            self.text_input.textbox.insert("insert", text)
        except Exception:
            logging.warning("Clipboard vazio ou com conteúdo inválido.")
            
    # 4
    def copy_output(self):
        text = self.text_output.textbox.get("1.0", "end-1c")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.left_menu.time_label.configure(text="Texto copiado!")
            self.after(2000, lambda: self.left_menu.time_label.configure(text="Pronto."))

    # 4
    def save_output_as(self):
        """Abre a caixa de diálogo para salvar o arquivo com o estilo selecionado."""
        text_to_save = self.text_output.textbox.get("1.0", "end-1c").strip()
        if not text_to_save:
            messagebox.showwarning("Nada para Salvar", "A caixa de texto de saída está vazia.")
            return

        selected_style = self.left_menu.style_menu.get()
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de Texto", "*.txt"),
                ("Documento Word", "*.docx"),
                ("Markdown", "*.md"),
                ("JSON", "*.json"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if not filepath:
            return

        try:
            # Converter estilo de volta para minúsculo para corresponder às chaves do prompts.json
            save_output(text_to_save, filepath, style=selected_style.lower())
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{filepath}")
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo: {e}", exc_info=True)
            messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro: {e}")
