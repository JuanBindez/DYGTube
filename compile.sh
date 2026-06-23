#!/bin/bash

# Variáveis
EXECUTABLE_NAME="DYGTube-v8.0.0-x86_64"
PYINSTALLER_CMD="pyinstaller"
PYINSTALLER_FLAGS="--onefile --noconsole --windowed"
MAIN_FILE="main.py"

build() {
    echo "Iniciando o build com PyInstaller..."
    $PYINSTALLER_CMD --name "$EXECUTABLE_NAME" $PYINSTALLER_FLAGS "$MAIN_FILE"
}

clean() {
    echo "Cleaning files..."
    rm -rf build dist __pycache__ "$EXECUTABLE_NAME.spec"
}

# Controle de argumentos (Executa build por padrão se nenhum argumento for passado)
ACTION="${1:-build}"

case "$ACTION" in
    build)
        build
        ;;
    clean)
        clean
        ;;
    *)
        echo "Uso: $0 {build|clean}"
        exit 1
        ;;
esac