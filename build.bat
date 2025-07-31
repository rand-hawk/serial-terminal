# Simple batch file alternative to PowerShell script
@echo off
echo Building Simple Serial Terminal for Windows...

echo Checking PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist installer rmdir /s /q installer

echo Creating directories...
mkdir installer

echo Building executable with PyInstaller...
python -m PyInstaller simple_terminal.spec --clean

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Executable created successfully!
echo Location: %CD%\dist\SimpleSerialTerminal.exe
echo.
echo To create the installer:
echo 1. Install Inno Setup from: https://jrsoftware.org/isdl.php
echo 2. Open simple_terminal_installer.iss with Inno Setup
echo 3. Click Build ^> Compile to create the installer
echo.
echo Or if Inno Setup is in PATH, run:
echo iscc simple_terminal_installer.iss
echo.
echo Build completed!
pause
