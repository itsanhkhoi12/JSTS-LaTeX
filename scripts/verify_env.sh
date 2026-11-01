#!/usr/bin/env bash
# ==============================================================================
# LaTeX Cross-Platform Environment Verification Script (Linux / macOS)
# ==============================================================================
set -e

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure project shim is prioritized if needed
if [ -d "$PROJECT_ROOT/scripts/bin" ]; then
    export PATH="$PROJECT_ROOT/scripts/bin:$PATH"
fi

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}  Kiểm tra môi trường biên dịch LaTeX (XeLaTeX + Minted)  ${NC}"
echo -e "${BLUE}======================================================${NC}"

HAS_ERROR=0

check_cmd() {
    local name="$1"
    local cmd="$2"
    local install_hint="$3"
    
    printf "%-30s" "Kiểm tra $name..."
    if command -v "$cmd" >/dev/null 2>&1; then
        local version
        version=$("$cmd" --version 2>&1 | head -n 1 || true)
        echo -e "[${GREEN}OK${NC}] ($version)"
    else
        echo -e "[${RED}FAIL${NC}]"
        echo -e "  ${YELLOW}-> Gợi ý khắc phục: $install_hint${NC}"
        HAS_ERROR=1
    fi
}

# 1. Kiểm tra xelatex
check_cmd "XeLaTeX" "xelatex" "Cài đặt TeX Live (texlive-xetex hoặc MacTeX)."

# 2. Kiểm tra latexmk
check_cmd "Latexmk" "latexmk" "Cài đặt latexmk (sudo apt install latexmk hoặc tlmgr install latexmk)."

# 3. Kiểm tra minted.sty
printf "%-30s" "Kiểm tra minted.sty..."
if kpsewhich minted.sty >/dev/null 2>&1; then
    MINTED_PATH=$(kpsewhich minted.sty)
    echo -e "[${GREEN}OK${NC}] ($MINTED_PATH)"
else
    echo -e "[${RED}FAIL${NC}]"
    echo -e "  ${YELLOW}-> Gợi ý: Cài đặt gói minted (tlmgr install minted hoặc texlive-latex-extra).${NC}"
    HAS_ERROR=1
fi

# 4. Kiểm tra latexminted
printf "%-30s" "Kiểm tra latexminted..."
if command -v latexminted >/dev/null 2>&1; then
    if latexminted --version >/dev/null 2>&1; then
        MINTED_VER=$(latexminted --version 2>&1 | head -n 1)
        echo -e "[${GREEN}OK${NC}] ($MINTED_VER)"
    else
        echo -e "[${YELLOW}WARNING${NC}] (latexminted có sẵn nhưng gặp lỗi khi gọi)"
        echo -e "  ${YELLOW}-> Đang dùng bộ đệm shim tại scripts/bin/latexminted.${NC}"
    fi
else
    echo -e "[${RED}FAIL${NC}]"
    echo -e "  ${YELLOW}-> Gợi ý: Cài đặt TeX Live 2024/2025 hoặc 'pip install latexminted pygments'.${NC}"
    HAS_ERROR=1
fi

# 5. Kiểm tra font files
printf "%-30s" "Kiểm tra font SVN-Times..."
FONT_DIR="$PROJECT_ROOT/fonts"
if [ -f "$FONT_DIR/SVN-Times New Roman 2.ttf" ] && \
   [ -f "$FONT_DIR/SVN-Times New Roman 2 bold.ttf" ] && \
   [ -f "$FONT_DIR/SVN-Times New Roman 2 italic.ttf" ] && \
   [ -f "$FONT_DIR/SVN-Times New Roman 2 bold italic.ttf" ]; then
    echo -e "[${GREEN}OK${NC}] (Đủ 4 biến thể Regular, Bold, Italic, Bold-Italic)"
else
    echo -e "[${RED}FAIL${NC}] (Thiếu một hoặc nhiều file font trong thư mục fonts/)"
    HAS_ERROR=1
fi

if [ $HAS_ERROR -ne 0 ]; then
    echo -e "\n${RED}[!] Phát hiện thiếu phụ thuộc. Vui lòng khắc phục trước khi chạy kiểm tra biên dịch.${NC}"
    exit 1
fi

# 6. Thử nghiệm biên dịch test_minimal.tex
echo -e "\n${BLUE}Bắt đầu biên dịch thử nghiệm (test_minimal.tex)...${NC}"
TEST_BUILD_DIR="$PROJECT_ROOT/build/test_env"
mkdir -p "$TEST_BUILD_DIR"

cd "$PROJECT_ROOT"
if xelatex -synctex=1 -interaction=nonstopmode -shell-escape -output-directory="$TEST_BUILD_DIR" "$SCRIPT_DIR/test_minimal.tex" > "$TEST_BUILD_DIR/test_compile.log" 2>&1; then
    echo -e "[${GREEN}SUCCESS${NC}] Biên dịch thành công test_minimal.pdf!"
    echo -e "  -> File kết quả: $TEST_BUILD_DIR/test_minimal.pdf"
    echo -e "${GREEN}Môi trường sẵn sàng 100% để phát triển và biên dịch dự án!${NC}"
else
    echo -e "[${RED}ERROR${NC}] Biên dịch test_minimal thất bại!"
    echo -e "  Chi tiết lỗi ghi trong: $TEST_BUILD_DIR/test_compile.log"
    tail -n 20 "$TEST_BUILD_DIR/test_compile.log"
    exit 1
fi

