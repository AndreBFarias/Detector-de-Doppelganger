#!/bin/bash
set -e

APP_NAME="detector-doppelganger"
APP_DISPLAY_NAME="Detector de Doppelganger"

DESKTOP_ENTRY_DIR_USER="${HOME}/.local/share/applications"
ICON_DIR_USER="${HOME}/.local/share/icons/hicolor"
DESKTOP_ENTRY_DIR_SYSTEM="/usr/local/share/applications"
ICON_DIR_SYSTEM="/usr/local/share/icons/hicolor"

echo "=== Iniciando Desinstalação do ${APP_DISPLAY_NAME} ==="

remove_file() {
    local file="$1"
    local sudo_cmd="$2"
    if [ -f "$file" ]; then
        $sudo_cmd rm "$file"
        echo "Removido: $file"
    fi
}

remove_dir() {
    local dir="$1"
    local sudo_cmd="$2"
    if [ -d "$dir" ]; then
        $sudo_cmd rm -rf "$dir"
        echo "Removido: $dir"
    fi
}

echo "[1/3] Removendo atalho do usuário..."
remove_file "${DESKTOP_ENTRY_DIR_USER}/${APP_NAME}.desktop" ""

echo "[2/3] Removendo ícones do usuário..."
for size in 16 32 64 128 256; do
    remove_file "${ICON_DIR_USER}/${size}x${size}/apps/${APP_NAME}.png" ""
done

echo "[3/3] Removendo instalação do sistema (se existir)..."
if [ -f "${DESKTOP_ENTRY_DIR_SYSTEM}/${APP_NAME}.desktop" ]; then
    sudo rm "${DESKTOP_ENTRY_DIR_SYSTEM}/${APP_NAME}.desktop"
    echo "Removido: ${DESKTOP_ENTRY_DIR_SYSTEM}/${APP_NAME}.desktop"
fi

for size in 16 32 64 128 256; do
    if [ -f "${ICON_DIR_SYSTEM}/${size}x${size}/apps/${APP_NAME}.png" ]; then
        sudo rm "${ICON_DIR_SYSTEM}/${size}x${size}/apps/${APP_NAME}.png"
    fi
done

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "${DESKTOP_ENTRY_DIR_USER}" 2>/dev/null || true
fi

if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache "${ICON_DIR_USER}" -f -t 2>/dev/null || true
fi

echo "=== Desinstalação Concluída ==="
echo "O ${APP_DISPLAY_NAME} foi removido do sistema."
echo "Nota: O diretório do projeto e o venv não foram removidos."


# "Destruir e facil; construir e dificil." - Proverbio
