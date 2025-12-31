from __future__ import annotations

import logging
import queue
import sys
import tkinter
from pathlib import Path
from tkinter import filedialog, messagebox

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import customtkinter

import config
from src.core.app_core import AppCore
from src.core.output_formatter import save_output
from src.core.processing_thread_v2 import ProcessingThreadV2
from src.ui.banner import Banner
from src.ui.left_menu import LeftMenu
from src.ui.text_input_frame import TextInputFrame
from src.ui.text_output_frame import TextOutputFrame
from src.utils.colors import get_color_for_percentage


class MainWindow(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.core = AppCore()
        self.processing_thread = None
        self.ui_queue = queue.Queue()

        self._setup_window_icon()
        self._setup_layout()
        self._setup_widgets()

        self.connect_widgets()
        self.after(100, self.process_ui_queue)

        self.left_menu.humanize_button.configure(state="disabled", text="Carregando...")
        self.after(200, self.initial_load)

    def _setup_window_icon(self) -> None:
        try:
            icon_path = config.ASSETS_DIR / "icon.png"
            if icon_path.exists():
                icon_image = tkinter.PhotoImage(file=str(icon_path))
                self.master.iconphoto(True, icon_image)
                self.master.title("Detector de Doppelganger")
            else:
                logging.warning(f"Icone nao encontrado em: {icon_path}")
        except Exception as e:
            logging.warning(f"Erro ao definir icone: {e}")

    def _setup_layout(self) -> None:
        self.configure(fg_color="#181825", border_width=0, corner_radius=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _setup_widgets(self) -> None:
        self.left_menu = LeftMenu(self, width=280)
        self.left_menu.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent", border_width=0)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        self.main_content.grid_columnconfigure((0, 1), weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.banner = Banner(self.main_content)
        self.banner.grid(row=0, column=0, columnspan=2, sticky="new", pady=(0, 10))

        self.text_input = TextInputFrame(self.main_content)
        self.text_input.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

        self.text_output = TextOutputFrame(self.main_content)
        self.text_output.grid(row=1, column=1, sticky="nsew", padx=(5, 0))

    def initial_load(self) -> None:
        style_keys = self.core.load_styles()
        logging.info(f"Chaves de estilo carregadas: {style_keys}")

        capitalized_keys = [k.title() for k in style_keys]
        logging.info(f"Chaves capitalizadas: {capitalized_keys}")

        self.left_menu.style_menu.configure(values=capitalized_keys)
        self.left_menu.style_menu.set("Default")

        if self.core.load_detector_models() and self.core.load_humanizer_model():
            self.left_menu.humanize_button.configure(state="normal", text="Humanizar")
            self.left_menu.time_label.configure(text="Pronto.")
        else:
            messagebox.showerror("Erro Critico", "Nao foi possivel carregar os modelos de IA.")
            self.master.destroy()

    def connect_widgets(self) -> None:
        self.left_menu.select_file_button.configure(command=self.select_file)
        self.left_menu.paste_button.configure(command=self.paste_text)
        self.left_menu.humanize_button.configure(command=self.start_processing)
        self.left_menu.copy_button.configure(command=self.copy_output)
        self.left_menu.model_menu.configure(command=self.on_model_select)
        self.left_menu.save_button.configure(command=self.save_output_as)

    def on_model_select(self, model_key: str) -> None:
        self.left_menu.humanize_button.configure(state="disabled", text="Carregando...")
        self.update()
        if self.core.load_humanizer_model(model_key):
            self.left_menu.humanize_button.configure(state="normal", text="Humanizar")
        else:
            messagebox.showerror("Erro", f"Nao foi possivel carregar o modelo {model_key}")
            self.left_menu.humanize_button.configure(state="disabled", text="Erro no modelo")

    def start_processing(self) -> None:
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.stop()
            self.left_menu.humanize_button.configure(text="Humanizar")
            self.left_menu.time_label.configure(text="Interrompido.")
            return

        text = self.text_input.textbox.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para humanizar.")
            return

        self._clear_output_area()

        self.left_menu.humanize_button.configure(text="Interromper")

        mode = self.left_menu.mode_menu.get()
        priority_map = {
            "Balanceado": "balanced",
            "Reducao Maxima": "max_reduction",
            "Preservar Conteudo": "preserve_content",
        }
        priority = priority_map.get(self.left_menu.priority_menu.get(), "balanced")

        if "API" in mode:
            humanizer_mode = "api"
        elif "Ollama" in mode:
            humanizer_mode = "ollama"
        else:
            humanizer_mode = "local"

        self.processing_thread = ProcessingThreadV2(
            text=text,
            criatividade=self.left_menu.creativity_slider.get(),
            intensidade=self.left_menu.intensity_slider.get(),
            ui_queue=self.ui_queue,
            style_key=self.left_menu.style_menu.get().lower(),
            detector_mode="local",
            humanizer_mode=humanizer_mode,
            priority=priority,
        )
        self.processing_thread.start()

    def _clear_output_area(self) -> None:
        self.text_output.textbox.configure(state="normal")
        self.text_output.textbox.delete("1.0", "end")
        self.text_output.textbox.configure(state="disabled")

        self.text_input.ia_label_value.configure(text="--", text_color="white")
        self.text_input.nat_label_value.configure(text="--", text_color="white")
        self.text_output.ia_label_value.configure(text="--", text_color="white")
        self.text_output.nat_label_value.configure(text="--", text_color="white")

    def process_ui_queue(self) -> None:
        try:
            while not self.ui_queue.empty():
                message = self.ui_queue.get_nowait()
                self._handle_ui_message(message)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_ui_queue)

    def _handle_ui_message(self, message: dict) -> None:
        msg_type = message.get("type")

        if msg_type == "status":
            self.left_menu.time_label.configure(text=message["value"])

        elif msg_type == "initial_stats":
            color_ia = get_color_for_percentage(message["prob_ia"], inverse=True)
            color_nat = get_color_for_percentage(message["naturalidade"], inverse=False)

            self.text_input.ia_label_value.configure(
                text=f"{message['prob_ia']*100:.2f}%",
                text_color=color_ia,
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.text_input.nat_label_value.configure(
                text=f"{message['naturalidade']*100:.2f}%",
                text_color=color_nat,
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )

        elif msg_type == "progress":
            self.left_menu.progress_bar.set(message["progress"])
            self.text_output.textbox.configure(state="normal")
            self.text_output.textbox.insert("end", message["chunk"])
            self.text_output.textbox.see("end")
            self.text_output.textbox.configure(state="disabled")

        elif msg_type == "final_result":
            color_ia = get_color_for_percentage(message["prob_ia"], inverse=True)
            color_nat = get_color_for_percentage(message["naturalidade"], inverse=False)

            self.text_output.ia_label_value.configure(
                text=f"{message['prob_ia']*100:.2f}%",
                text_color=color_ia,
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.text_output.nat_label_value.configure(
                text=f"{message['naturalidade']*100:.2f}%",
                text_color=color_nat,
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )

        elif msg_type == "finished":
            self.left_menu.humanize_button.configure(text="Humanizar")
            self.left_menu.progress_bar.set(0)

    def select_file(self) -> None:
        filepath = filedialog.askopenfilename(filetypes=[("Text/Doc Files", "*.txt *.docx *.md"), ("All files", "*.*")])
        if not filepath:
            return

        try:
            if filepath.endswith(".docx"):
                import docx

                doc = docx.Document(filepath)
                full_text = "\n".join([para.text for para in doc.paragraphs])
                self.text_input.textbox.delete("1.0", "end")
                self.text_input.textbox.insert("1.0", full_text)
            else:
                with open(filepath, encoding="utf-8") as f:
                    self.text_input.textbox.delete("1.0", "end")
                    self.text_input.textbox.insert("1.0", f.read())
        except Exception as e:
            messagebox.showerror("Erro ao Abrir", f"Nao foi possivel ler o arquivo:\n{e}")

    def paste_text(self) -> None:
        try:
            text = self.clipboard_get()
            self.text_input.textbox.insert("insert", text)
        except Exception:
            logging.warning("Clipboard vazio ou com conteudo invalido.")

    def copy_output(self) -> None:
        text = self.text_output.textbox.get("1.0", "end-1c")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.left_menu.time_label.configure(text="Texto copiado!")
            self.after(2000, lambda: self.left_menu.time_label.configure(text="Pronto."))

    def save_output_as(self) -> None:
        text_to_save = self.text_output.textbox.get("1.0", "end-1c").strip()
        if not text_to_save:
            messagebox.showwarning("Nada para Salvar", "A caixa de texto de saida esta vazia.")
            return

        selected_style = self.left_menu.style_menu.get()

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de Texto", "*.txt"),
                ("Documento Word", "*.docx"),
                ("Markdown", "*.md"),
                ("JSON", "*.json"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if not filepath:
            return

        try:
            save_output(text_to_save, filepath, style=selected_style.lower())
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{filepath}")
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo: {e}", exc_info=True)
            messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro: {e}")


# "A interface do usuario e como uma piada. Se voce precisa explicar, nao e boa." - Martin LeBlanc
