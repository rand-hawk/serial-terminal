# Windows Build Instructions

This directory contains files for building a Windows executable and installer for Simple Serial Terminal.

## Building the Executable

### Option 1: Using PowerShell Script
```powershell
.\build.ps1
```

### Option 2: Using Batch File
```cmd
build.bat
```

### Option 3: Manual Build
```cmd
python -m pip install pyinstaller
python -m PyInstaller simple_terminal.spec --clean
```

## Creating the Windows Installer

1. **Install Inno Setup**
   - Download from: https://jrsoftware.org/isdl.php
   - Install the compiler

2. **Build the Installer**
   - Open `simple_terminal_installer.iss` in Inno Setup
   - Click Build → Compile
   - Or run from command line: `iscc simple_terminal_installer.iss`

## Files Generated

- **Executable**: `dist\SimpleSerialTerminal.exe` (~12MB)
- **Installer**: `installer\SimpleSerialTerminal_Setup_v1.0.0.exe`

## Distribution

The generated installer includes:
- Main executable
- README and LICENSE files
- Desktop shortcut (optional)
- Start menu entry
- Uninstaller

## System Requirements

- Windows 7 or later
- No additional dependencies required (all bundled)

## Notes

- The executable is standalone and includes all Python dependencies
- First run may be slower due to extraction
- Windows Defender might scan the file on first run (normal behavior)
