# uninstall.py - Ritual de Magia Negra Digital: "Expurgo do Símbolo Eterno"
# Remove o programa do sistema, apagando traços.

import os
import shutil
import logging

def uninstall():
    """
    Desinstala o programa do Pop!_OS/Linux.
    """
    app_name = "DetectorDeDoppelganger"
    install_dir = "/usr/local/bin"
    desktop_dir = os.path.join(os.path.expanduser("~"), ".local/share/applications")
    icon_dir = os.path.join(os.path.expanduser("~"), ".local/share/icons")

    # Remove .desktop
    desktop_path = os.path.join(desktop_dir, f"{app_name.lower()}.desktop")
    if os.path.exists(desktop_path):
        os.remove(desktop_path)
        logging.info(f"Removido {desktop_path}.")

    # Remove ícones
    icon_sizes = ["16x16", "32x32", "64x64", "128x128"]
    for size in icon_sizes:
        icon_path = os.path.join(icon_dir, f"icon_{size}.png")
        if os.path.exists(icon_path):
            os.remove(icon_path)
            logging.info(f"Removido {icon_path}.")

    # Remove script
    script_path = os.path.join(install_dir, f"{app_name.lower()}")
    if os.path.exists(script_path):
        os.remove(script_path)
        logging.info(f"Removido {script_path}.")

    logging.info("Desinstalação concluída.")
    print("Desinstalado com sucesso.")

if __name__ == "__main__":
    uninstall()

# "A ordem nasce do caos." – Nietzsche, o libertário que organiza nosso código.
