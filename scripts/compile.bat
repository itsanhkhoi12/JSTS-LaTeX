@echo off
REM ==============================================================================
REM LaTeX compilation script for Windows (cmd / batch)
REM ==============================================================================
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
cd /d "%ROOT_DIR%"

REM Prepend local scripts\bin to PATH if present
if exist "%SCRIPT_DIR%bin" (
    set "PATH=%SCRIPT_DIR%bin;%PATH%"
)

REM Initialize metadata.tex if not present
if not exist "metadata.tex" (
    if exist "metadata.example.tex" (
        echo [INFO] metadata.tex not found. Initializing from metadata.example.tex template...
        copy "metadata.example.tex" "metadata.tex" >nul
    )
)

if not exist "build" mkdir "build"

if "%1"=="clean" (
    echo [INFO] Cleaning temporary files...
    latexmk -C
    del /q /s build\* >nul 2>&1
    echo [OK] Cleaned build directory.
    goto :eof
)

if "%1"=="watch" (
    echo [INFO] Starting continuous compilation...
    latexmk -pvc document.tex
    goto :eof
)

echo [INFO] Compiling document.tex -^> build/document.pdf...
latexmk document.tex
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Compilation completed! Output: build/document.pdf
) else (
    echo [ERROR] Compilation failed. Please check build/document.log
)
