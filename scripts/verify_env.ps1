# ==============================================================================
# LaTeX Cross-Platform Environment Verification Script (Windows PowerShell)
# ==============================================================================
$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location $ProjectRoot

# Add local scripts/bin to PATH for this process session if exists
if (Test-Path "$ProjectRoot\scripts\bin") {
    $env:PATH = "$ProjectRoot\scripts\bin;" + $env:PATH
}

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Kiem tra moi truong bien dich LaTeX (XeLaTeX + Minted)" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

$hasError = $false

function Check-Command ($label, $cmdName, $installHint) {
    Write-Host -NoNewline ("{0,-30}" -f "Kiem tra $label...")
    $cmd = Get-Command $cmdName -ErrorAction SilentlyContinue
    if ($cmd) {
        $firstLine = ""
        try {
            $ver = & $cmdName --version 2>&1 | Select-Object -First 1
            $firstLine = "($ver)"
        } catch {
            $firstLine = "($($cmd.Source))"
        }
        Write-Host "[OK] $firstLine" -ForegroundColor Green
    } else {
        Write-Host "[FAIL]" -ForegroundColor Red
        Write-Host "  -> Goi y: $installHint" -ForegroundColor Yellow
        $script:hasError = $true
    }
}

# 1. Kiem tra XeLaTeX
Check-Command "XeLaTeX" "xelatex" "Cai dat TeX Live hoac MiKTeX (khuyen nghi TeX Live)."

# 2. Kiem tra Latexmk
Check-Command "Latexmk" "latexmk" "Cai dat latexmk thong qua tlmgr: tlmgr install latexmk."

# 3. Kiem tra minted.sty
Write-Host -NoNewline ("{0,-30}" -f "Kiem tra minted.sty...")
$mintedSty = kpsewhich minted.sty 2>$null
if ($mintedSty) {
    Write-Host "[OK] ($mintedSty)" -ForegroundColor Green
} else {
    Write-Host "[FAIL]" -ForegroundColor Red
    Write-Host "  -> Goi y: tlmgr install minted" -ForegroundColor Yellow
    $hasError = $true
}

# 4. Kiem tra latexminted
Write-Host -NoNewline ("{0,-30}" -f "Kiem tra latexminted...")
$latexminted = Get-Command latexminted -ErrorAction SilentlyContinue
if ($latexminted) {
    Write-Host "[OK] ($($latexminted.Source))" -ForegroundColor Green
} else {
    Write-Host "[FAIL]" -ForegroundColor Red
    Write-Host "  -> Goi y: pip install latexminted pygments hoac cai cap nhat TeX Live 2024+" -ForegroundColor Yellow
    $hasError = $true
}

# 5. Kiem tra font files
Write-Host -NoNewline ("{0,-30}" -f "Kiem tra font SVN-Times...")
$fontDir = Join-Path $ProjectRoot "fonts"
$f1 = Join-Path $fontDir "SVN-Times New Roman 2.ttf"
$f2 = Join-Path $fontDir "SVN-Times New Roman 2 bold.ttf"
$f3 = Join-Path $fontDir "SVN-Times New Roman 2 italic.ttf"
$f4 = Join-Path $fontDir "SVN-Times New Roman 2 bold italic.ttf"

if ((Test-Path $f1) -and (Test-Path $f2) -and (Test-Path $f3) -and (Test-Path $f4)) {
    Write-Host "[OK] (Du 4 bien the font SVN-Times)" -ForegroundColor Green
} else {
    Write-Host "[FAIL] (Thieu file font trong fonts/)" -ForegroundColor Red
    $hasError = $true
}

if ($hasError) {
    Write-Host "`n[!] Phat hien thieu phu thuoc can thiet. Vui long cai dat theo huong dan trong README.md" -ForegroundColor Red
    exit 1
}

# 6. Bien dich thu nghiem test_minimal.tex
Write-Host "`nBat dau bien dich thu nghiem (test_minimal.tex)..." -ForegroundColor Cyan
$testBuildDir = Join-Path $ProjectRoot "build\test_env"
if (-not (Test-Path $testBuildDir)) {
    New-Item -ItemType Directory -Path $testBuildDir -Force | Out-Null
}

$minimalTex = Join-Path $ProjectRoot "scripts\test_minimal.tex"
$logFile = Join-Path $testBuildDir "test_compile.log"

$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "xelatex"
$pinfo.Arguments = "-synctex=1 -interaction=nonstopmode -shell-escape -output-directory=""$testBuildDir"" ""$minimalTex"""
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$p.Start() | Out-Null
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()
$p.WaitForExit()

Set-Content -Path $logFile -Value ($stdout + $stderr)

if ($p.ExitCode -eq 0) {
    Write-Host "[SUCCESS] Bien dich thanh cong test_minimal.pdf!" -ForegroundColor Green
    Write-Host "  -> File ket qua: $testBuildDir\test_minimal.pdf" -ForegroundColor Gray
    Write-Host "Moi truong da san sang 100% de lam viec!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Bien dich test_minimal that bai!" -ForegroundColor Red
    Write-Host "  Chi tiet loi trong: $logFile" -ForegroundColor Yellow
    exit 1
}

