#!/bin/bash
# Ritual de Magia Negra Digital: "Exorcismo do Portal"
# Remove o Detector de Doppelgänger, apagando seus rastros do sistema.

set -e

# 76
# --- Variáveis de Configuração ---
APP_NAME="DetectorDeDoppelganger"
APP_NAME_LOWER="detectordedoppelganger"
INSTALL_DIR="/opt/$APP_NAME"
EXECUTABLE="/usr/local/bin/$APP_NAME_LOWER"
DESKTOP_FILE="/usr/share/applications/$APP_NAME_LOWER.desktop"

# 77
echo "--- Iniciando Desinstalação do $APP_NAME ---"

# 78
# --- Remoção de Arquivos (com sudo) ---
echo "[1/4] Removendo diretório de instalação $INSTALL_DIR..."
if [ -d "$INSTALL_DIR" ]; then
    sudo rm -rf "$INSTALL_DIR"
else
    echo "Diretório $INSTALL_DIR não encontrado. Pulando."
fi

# 79
echo "[2/4] Removendo executável $EXECUTABLE..."
if [ -f "$EXECUTABLE" ]; then
    sudo rm "$EXECUTABLE"
else
    echo "Executável $EXECUTABLE não encontrado. Pulando."
fi

# 79
echo "[3/4] Removendo entrada .desktop $DESKTOP_FILE..."
if [ -f "$DESKTOP_FILE" ]; then
    sudo rm "$DESKTOP_FILE"
else
    echo "Entrada .desktop $DESKTOP_FILE não encontrada. Pulando."
fi

# 79
echo "[4/4] Removendo ícones do sistema..."
for size in 16 32 64 128; do
    ICON_PATH="/usr/share/icons/hicolor/${size}x${size}/apps/$APP_NAME_LOWER.png"
    if [ -f "$ICON_PATH" ]; then
        sudo rm "$ICON_PATH"
    fi
done

# 79
# --- Pós-Remoção ---
echo "Atualizando caches de ícones e aplicações do sistema..."
sudo gtk-update-icon-cache /usr/share/icons/hicolor -f || echo "Aviso: gtk-update-icon-cache falhou, mas a desinstalação principal foi concluída."
sudo update-desktop-database || echo "Aviso: update-desktop-database falhou, mas a desinstalação principal foi concluída."


# 80
echo "--- Desinstalação Concluída ---"
echo "O $APP_NAME foi exorcizado do seu sistema."
