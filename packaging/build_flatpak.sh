#!/bin/bash

set -e

APP_ID="com.github.andrebfarias.DetectorDoppelganger"
APP_VERSION="${VERSION:-1.0.0}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="${PROJECT_ROOT}/build/flatpak"
DIST_DIR="${PROJECT_ROOT}/dist"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
mkdir -p "${DIST_DIR}"

cat > "${BUILD_DIR}/${APP_ID}.yml" << EOF
app-id: ${APP_ID}
runtime: org.freedesktop.Platform
runtime-version: '23.08'
sdk: org.freedesktop.Sdk
command: detector-doppelganger

finish-args:
  - --share=ipc
  - --socket=x11
  - --socket=wayland
  - --filesystem=home
  - --share=network
  - --device=dri

modules:
  - name: python-deps
    buildsystem: simple
    build-commands:
      - pip3 install --prefix=/app --no-deps -r requirements.txt
    sources:
      - type: file
        path: requirements.txt

  - name: detector-doppelganger
    buildsystem: simple
    build-commands:
      - install -Dm755 main.py /app/bin/detector-doppelganger
      - mkdir -p /app/lib/detector-doppelganger
      - cp -r src /app/lib/detector-doppelganger/
      - cp -r assets /app/lib/detector-doppelganger/
      - cp config.py /app/lib/detector-doppelganger/
      - cp prompts.json /app/lib/detector-doppelganger/ || true
      - install -Dm644 assets/icon.png /app/share/icons/hicolor/256x256/apps/${APP_ID}.png
      - install -Dm644 packaging/${APP_ID}.desktop /app/share/applications/${APP_ID}.desktop
    sources:
      - type: dir
        path: ..
EOF

cat > "${BUILD_DIR}/${APP_ID}.desktop" << EOF
[Desktop Entry]
Name=Detector de Doppelganger
Comment=Detector e Humanizador de Texto IA
Exec=detector-doppelganger
Icon=${APP_ID}
Type=Application
Categories=Utility;TextTools;
Terminal=false
EOF

cp "${BUILD_DIR}/${APP_ID}.desktop" "${PROJECT_ROOT}/packaging/"

echo "Manifesto Flatpak criado em: ${BUILD_DIR}/${APP_ID}.yml"
echo ""
echo "Para construir o Flatpak localmente, execute:"
echo "  cd ${BUILD_DIR}"
echo "  flatpak-builder --force-clean build-dir ${APP_ID}.yml"
echo ""
echo "Para criar o pacote .flatpak:"
echo "  flatpak build-export repo build-dir"
echo "  flatpak build-bundle repo ${DIST_DIR}/${APP_ID}.flatpak ${APP_ID}"
