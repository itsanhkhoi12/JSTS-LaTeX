#!/usr/bin/env bash
# ==============================================================================
# LaTeX compilation script for Linux / macOS
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# Prepend project local scripts/bin to PATH if present
if [ -d "$SCRIPT_DIR/bin" ]; then
    export PATH="$SCRIPT_DIR/bin:$PATH"
fi

# Automatically create metadata.tex from metadata.example.tex if not present
if [ ! -f "metadata.tex" ] && [ -f "metadata.example.tex" ]; then
    echo "[INFO] metadata.tex not found. Initializing from metadata.example.tex template..."
    cp metadata.example.tex metadata.tex
fi

mkdir -p build

if [ "$1" = "clean" ]; then
    echo "[INFO] Cleaning temporary files..."
    latexmk -C
    rm -rf build/*
    echo "[OK] Cleaned build directory."
    exit 0
elif [ "$1" = "watch" ]; then
    echo "[INFO] Starting continuous compilation (pvc mode)..."
    latexmk -pvc document.tex
else
    echo "[INFO] Compiling document.tex -> build/document.pdf..."
    latexmk document.tex
    echo "[SUCCESS] Compilation completed! Output: build/document.pdf"
fi
