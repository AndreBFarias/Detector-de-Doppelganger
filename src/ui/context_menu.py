import tkinter
import customtkinter
from tkinter import filedialog
import logging

class ContextMenu:
    def __init__(self, textbox, save_callback=None):
        self.textbox = textbox
        self.save_callback = save_callback
        self.menu = tkinter.Menu(
            textbox, 
            tearoff=0, 
            bg="#181825", 
            fg="white", 
            activebackground="#50FA7B", 
            activeforeground="#181825",
            bd=0,
            relief="flat"
        )
        
        # Definir opções do menu
        self.menu.add_command(label="Selecionar Tudo", command=self.select_all)
        self.menu.add_separator()
        self.menu.add_command(label="Copiar", command=self.copy)
        self.menu.add_command(label="Colar", command=self.paste)
        self.menu.add_command(label="Recortar", command=self.cut)
        self.menu.add_command(label="Apagar", command=self.delete)
        
        if self.save_callback:
            self.menu.add_separator()
            self.menu.add_command(label="Salvar Como...", command=self.save_as)
        else:
             # Adiciona Salvar Como mesmo sem callback (usando implementação padrão)
            self.menu.add_separator()
            self.menu.add_command(label="Salvar Como...", command=self.save_as)

        # Bindings do Mouse (Botão Direito)
        self.textbox.bind("<Button-3>", self.show_menu)
        
        # Bindings de Teclado
        # Nota: CTkTextbox já lida com Ctrl+C, V, X, Del nativamente via tk.Text subjacente.
        # Precisamos adicionar Ctrl+A e Ctrl+S.
        # Adicionando múltiplas variantes para garantir compatibilidade
        for key in ["<Control-a>", "<Control-A>", "<Control-Key-a>", "<Control-Key-A>"]:
            self.textbox.bind(key, self.select_all)
            
        for key in ["<Control-s>", "<Control-S>", "<Control-Key-s>", "<Control-Key-S>"]:
            self.textbox.bind(key, self.save_as)
        
        # Removido binding de FocusOut que causava fechamento indesejado

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def copy(self):
        try:
            text = self.textbox.get("sel.first", "sel.last")
            self.textbox.clipboard_clear()
            self.textbox.clipboard_append(text)
        except tkinter.TclError:
            pass # Nada selecionado

    def paste(self):
        try:
            text = self.textbox.clipboard_get()
            self.textbox.insert("insert", text)
        except tkinter.TclError:
            pass

    def cut(self):
        try:
            self.copy()
            self.delete()
        except tkinter.TclError:
            pass

    def delete(self):
        try:
            self.textbox.delete("sel.first", "sel.last")
        except tkinter.TclError:
            pass

    def select_all(self, event=None):
        logging.info("Selecionar Tudo acionado.")
        self.textbox.tag_add("sel", "1.0", "end")
        self.textbox.mark_set("insert", "end")
        return "break" # Impede propagação se necessário

    def save_as(self, event=None):
        logging.info("Salvar Como acionado.")
        if self.save_callback:
            self.save_callback()
        else:
            # Implementação padrão se nenhum callback for fornecido
            text = self.textbox.get("1.0", "end-1c")
            if not text.strip():
                logging.warning("Texto vazio, não salvando.")
                return "break"
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text)
                except Exception as e:
                    print(f"Erro ao salvar: {e}")
        return "break"
