@echo off
REM ==============================================================================
REM Script bien dich tai lieu LaTeX cho Windows (cmd / batch)
REM ==============================================================================
setlocal EnableDelayedExpansion

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM Prepend local scripts\bin to PATH if present
if exist "%PROJECT_DIR%scripts\bin" (
    set "PATH=%PROJECT_DIR%scripts\bin;%PATH%"
)

REM Khoi tao metadata.tex neu chua co
if not exist "metadata.tex" (
    if exist "metadata.example.tex" (
        echo [INFO] Chua tim thay metadata.tex. Khoi tao tu template metadata.example.tex...
        copy "metadata.example.tex" "metadata.tex" >nul
    )
)

if not exist "build" mkdir "build"

if "%1"=="clean" (
    echo [INFO] Dang don dep cac tep tam...
    latexmk -C
    del /q /s build\* >nul 2>&1
    echo [OK] Da don dep thu muc build.
    goto :eof
)

if "%1"=="watch" (
    echo [INFO] Che do giam sat lien tuc (pvc mode)...
    latexmk -pvc document.tex
    goto :eof
)

echo [INFO] Dang bien dich tai lieu document.tex -^> build/document.pdf...
latexmk document.tex
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Bien dich hoan tat! File dau ra: build/document.pdf
) else (
    echo [ERROR] Bien dich that bai. Vui long kiem tra build/document.log
)

