#!/bin/bash

set -e

APP_NAME="detector-doppelganger"
APP_VERSION="${VERSION:-1.0.0}"
MAINTAINER="Andre Farias <andre@example.com>"
DESCRIPTION="Detector e Humanizador de Texto IA"
ARCH="amd64"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="${PROJECT_ROOT}/build/deb"
DIST_DIR="${PROJECT_ROOT}/dist"
PACKAGE_DIR="${BUILD_DIR}/${APP_NAME}_${APP_VERSION}_${ARCH}"

rm -rf "${BUILD_DIR}"
mkdir -p "${PACKAGE_DIR}/DEBIAN"
mkdir -p "${PACKAGE_DIR}/opt/${APP_NAME}"
mkdir -p "${PACKAGE_DIR}/usr/share/applications"
mkdir -p "${PACKAGE_DIR}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${DIST_DIR}"

cp -r "${PROJECT_ROOT}/src" "${PACKAGE_DIR}/opt/${APP_NAME}/"
cp -r "${PROJECT_ROOT}/assets" "${PACKAGE_DIR}/opt/${APP_NAME}/"
cp "${PROJECT_ROOT}/main.py" "${PACKAGE_DIR}/opt/${APP_NAME}/"
cp "${PROJECT_ROOT}/config.py" "${PACKAGE_DIR}/opt/${APP_NAME}/"
cp "${PROJECT_ROOT}/requirements.txt" "${PACKAGE_DIR}/opt/${APP_NAME}/"
cp "${PROJECT_ROOT}/prompts.json" "${PACKAGE_DIR}/opt/${APP_NAME}/" 2>/dev/null || true

if [ -f "${PROJECT_ROOT}/assets/icon_256x256.png" ]; then
    cp "${PROJECT_ROOT}/assets/icon_256x256.png" "${PACKAGE_DIR}/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"
elif [ -f "${PROJECT_ROOT}/assets/icon.png" ]; then
    cp "${PROJECT_ROOT}/assets/icon.png" "${PACKAGE_DIR}/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"
fi

cat > "${PACKAGE_DIR}/DEBIAN/control" << EOF
Package: ${APP_NAME}
Version: ${APP_VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: ${MAINTAINER}
Depends: python3 (>= 3.10), python3-pip, python3-venv
Description: ${DESCRIPTION}
 Ferramenta para detectar e humanizar textos gerados por IA.
 Utiliza modelos de machine learning locais para analise.
EOF

cat > "${PACKAGE_DIR}/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

APP_DIR="/opt/detector-doppelganger"

if [ ! -d "${APP_DIR}/venv" ]; then
    python3 -m venv "${APP_DIR}/venv"
fi

"${APP_DIR}/venv/bin/pip" install --upgrade pip
"${APP_DIR}/venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

update-desktop-database /usr/share/applications || true
gtk-update-icon-cache /usr/share/icons/hicolor || true

exit 0
EOF
chmod 755 "${PACKAGE_DIR}/DEBIAN/postinst"

cat > "${PACKAGE_DIR}/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e

if [ "$1" = "purge" ]; then
    rm -rf /opt/detector-doppelganger
fi

update-desktop-database /usr/share/applications || true

exit 0
EOF
chmod 755 "${PACKAGE_DIR}/DEBIAN/postrm"

cat > "${PACKAGE_DIR}/usr/share/applications/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Version=1.0
Name=Detector de Doppelganger
Comment=${DESCRIPTION}
Exec=/opt/${APP_NAME}/venv/bin/python3 /opt/${APP_NAME}/main.py
Icon=${APP_NAME}
Terminal=false
Type=Application
Categories=Utility;TextTools;
StartupNotify=true
StartupWMClass=${APP_NAME}
Path=/opt/${APP_NAME}
EOF

dpkg-deb --build "${PACKAGE_DIR}" "${DIST_DIR}/${APP_NAME}_${APP_VERSION}_${ARCH}.deb"

echo "Pacote .deb criado: ${DIST_DIR}/${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
