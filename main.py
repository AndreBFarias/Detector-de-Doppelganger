#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import customtkinter

import config
from src.app.bootstrap import initialize_application
from src.ui.main_window import MainWindow
from src.ui.splash_screen import SplashScreen


def main() -> int:
    logger, error = initialize_application()

    if error:
        logger.error(f"Falha na inicializacao: {error}")
        return 1

    try:
        root = customtkinter.CTk()
        root.withdraw()

        def start_main_app() -> None:
            root.title("Detector de Doppelganger")
            root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
            root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)

            app = MainWindow(master=root)
            app.pack(expand=True, fill="both")

            root.update_idletasks()
            root.attributes("-zoomed", True)
            root.update_idletasks()

            def show_window():
                root.deiconify()
                root.lift()
                root.focus_force()
                root.update_idletasks()

            root.after(150, show_window)
            root.mainloop()

        splash = SplashScreen(root)
        splash.start_download(callback=start_main_app)
        splash.mainloop()

        return 0

    except KeyboardInterrupt:
        logger.info("Encerrado pelo usuario")
        return 0

    except Exception as e:
        logger.exception(f"Erro fatal: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

# "A tarefa nao e tanto ver aquilo que ninguem viu, mas pensar o que ninguem
#  ainda pensou sobre aquilo que todo mundo ve." - Arthur Schopenhauer
