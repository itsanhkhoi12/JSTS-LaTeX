#!/usr/bin/env bash
# ==============================================================================
# Script biên dịch tài liệu LaTeX cho Linux / macOS
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Prepend project local scripts/bin to PATH if present
if [ -d "$SCRIPT_DIR/scripts/bin" ]; then
    export PATH="$SCRIPT_DIR/scripts/bin:$PATH"
fi

# Tự động tạo file metadata.tex từ metadata.example.tex nếu chưa có
if [ ! -f "metadata.tex" ] && [ -f "metadata.example.tex" ]; then
    echo "[INFO] Chưa tìm thấy metadata.tex. Khởi tạo từ template metadata.example.tex..."
    cp metadata.example.tex metadata.tex
fi

mkdir -p build

if [ "$1" = "clean" ]; then
    echo "[INFO] Đang dọn dẹp các tệp tạm..."
    latexmk -C
    rm -rf build/*
    echo "[OK] Đã dọn dẹp thư mục build."
    exit 0
elif [ "$1" = "watch" ]; then
    echo "[INFO] Chế độ giám sát liên tục (pvc mode)..."
    latexmk -pvc document.tex
else
    echo "[INFO] Đang biên dịch tài liệu document.tex -> build/document.pdf..."
    latexmk document.tex
    echo "[SUCCESS] Biên dịch hoàn tất! File đầu ra: build/document.pdf"
fi

