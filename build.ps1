# Build script for creating Windows executable and installer
# Run this script to create both the .exe file and Windows installer

Write-Host "Building Simple Serial Terminal for Windows..." -ForegroundColor Green

# Check if PyInstaller is installed
try {
    & python -m pip show pyinstaller | Out-Null
    Write-Host "✓ PyInstaller found" -ForegroundColor Green
} catch {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    & python -m pip install pyinstaller
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "installer") { Remove-Item -Recurse -Force "installer" }

# Create directories
New-Item -ItemType Directory -Force -Path "installer" | Out-Null

# Build the executable
Write-Host "Building executable with PyInstaller..." -ForegroundColor Yellow
& python -m PyInstaller simple_terminal.spec --clean

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Executable built successfully!" -ForegroundColor Green
    
    # Check if the executable was created
    if (Test-Path "dist\SimpleSerialTerminal.exe") {
        Write-Host "✓ SimpleSerialTerminal.exe created in dist folder" -ForegroundColor Green
        
        # Copy to a simpler name for installer
        Copy-Item "dist\SimpleSerialTerminal.exe" "dist\SimpleSerialTerminal.exe"
        
        Write-Host "`nExecutable created successfully!" -ForegroundColor Green
        Write-Host "Location: $(Get-Location)\dist\SimpleSerialTerminal.exe" -ForegroundColor Cyan
        Write-Host "`nTo create the installer:" -ForegroundColor Yellow
        Write-Host "1. Install Inno Setup from: https://jrsoftware.org/isdl.php" -ForegroundColor White
        Write-Host "2. Open simple_terminal_installer.iss with Inno Setup" -ForegroundColor White
        Write-Host "3. Click Build > Compile to create the installer" -ForegroundColor White
        Write-Host "`nOr if Inno Setup is in PATH, run:" -ForegroundColor Yellow
        Write-Host "iscc simple_terminal_installer.iss" -ForegroundColor White
    } else {
        Write-Host "✗ Executable not found in expected location" -ForegroundColor Red
    }
} else {
    Write-Host "✗ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nBuild completed!" -ForegroundColor Green
