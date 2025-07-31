# Simple Serial Terminal v1.0.0

## 🎉 First Release

This is the first official release of Simple Serial Terminal - a user-friendly GUI application for serial communication on Windows.

## 📦 What's Included

### Windows Executable
- **SimpleSerialTerminal.exe** (~12MB) - Standalone executable
  - No Python installation required
  - All dependencies bundled
  - Ready to run on Windows 7 and later

### Windows Installer  
- **SimpleSerialTerminal_Setup_v1.0.0.exe** (~13MB) - Professional installer
  - Automatic installation to Program Files
  - Start Menu shortcut creation
  - Optional desktop shortcut
  - Built-in uninstaller
  - Includes documentation files

## ✨ Features

- **COM Port Management**: Auto-detect and connect to serial ports
- **Configurable Settings**: Baud rate, data bits, parity, stop bits, timeout
- **Multiple Data Formats**: Text, Hexadecimal, Decimal, Binary input/output
- **Line Ending Options**: CR, LF, CR+LF support
- **Real-time Logging**: Timestamped communication logs
- **Data Export**: Save logs to text files
- **Clear Interface**: Easy-to-use GUI with status indicators

## 🚀 Quick Start

### Option 1: Use the Installer (Recommended)
1. Download `SimpleSerialTerminal_Setup_v1.0.0.exe`
2. Run the installer and follow the setup wizard
3. Launch from Start Menu or desktop shortcut

### Option 2: Portable Executable
1. Download `SimpleSerialTerminal.exe`
2. Place it in any folder
3. Double-click to run

## 💻 System Requirements

- **OS**: Windows 7 or later (32-bit or 64-bit)
- **Memory**: 50MB RAM minimum
- **Storage**: 15MB free space
- **Hardware**: USB or built-in serial ports

## 🔧 Supported Hardware

- USB-to-Serial adapters (FTDI, Prolific, CH340, etc.)
- Built-in RS232 ports
- Arduino and microcontroller boards
- Industrial serial devices
- Any device using standard serial communication

## 📚 Documentation

- See README.md for detailed usage instructions
- Check BUILD_WINDOWS.md for building from source
- View examples and troubleshooting in the main documentation

## 🐛 Known Issues

- First launch may be slower due to Windows security scanning
- Some antivirus software may flag the executable (false positive)
- Port refresh required if devices are connected after startup

## 🏗️ Building from Source

This release was built using:
- Python 3.13.5
- PyInstaller 6.12.0  
- Inno Setup 6.4.2
- pySerial library

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is an open-source project. Contributions, bug reports, and feature requests are welcome on GitHub.

---

**Download the files below and start communicating with your serial devices today!**
