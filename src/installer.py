# installer.py - Ritual de Magia Negra Digital: "Invocação do Ícone Eterno"
# Instala o programa no sistema, selando sua presença com .desktop e ícones.

import os
import shutil
import stat
import logging

def install():
    """
    Instala o programa no Pop!_OS/Linux.
    """
    app_name = "DetectorDeDoppelganger"
    install_dir = "/usr/local/bin"
    desktop_dir = os.path.join(os.path.expanduser("~"), ".local/share/applications")
    icon_dir = os.path.join(os.path.expanduser("~"), ".local/share/icons")
    src_dir = os.path.dirname(os.path.abspath(__file__))

    # Cria .desktop
    desktop_content = f"""[Desktop Entry]
Name={app_name}
Exec={install_dir}/{app_name.lower()}
Type=Application
Icon={icon_dir}/icon_64x64.png
Categories=Utility;
Terminal=false
"""
    desktop_path = os.path.join(desktop_dir, f"{app_name.lower()}.desktop")
    os.makedirs(desktop_dir, exist_ok=True)
    with open(desktop_path, "w") as f:
        f.write(desktop_content)
    os.chmod(desktop_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    # Copia ícones e script
    icon_sizes = ["16x16", "32x32", "64x64", "128x128"]
    for size in icon_sizes:
        src_icon = os.path.join(src_dir, "..", "assets", f"icon_{size}.png")
        dst_icon = os.path.join(icon_dir, f"icon_{size}.png")
        os.makedirs(icon_dir, exist_ok=True)
        if os.path.exists(src_icon):
            shutil.copy2(src_icon, dst_icon)
    script_path = os.path.join(src_dir, "main.py")
    dst_script = os.path.join(install_dir, f"{app_name.lower()}")
    shutil.copy2(script_path, dst_script)
    os.chmod(dst_script, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    logging.info(f"Instalação concluída em {install_dir}, {desktop_dir}, {icon_dir}.")
    print(f"Instalado. Execute com '{app_name.lower()}'.")

if __name__ == "__main__":
    install()

# "A ordem nasce do caos." – Nietzsche, o libertário que organiza nosso código.
