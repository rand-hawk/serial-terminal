# Simple Serial Terminal

A feature-rich GUI application for serial communication with comprehensive data formatting options, built with Python and Tkinter.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## Features

### 🔌 Connection Management
- **COM Port Detection**: Automatic discovery and listing of available serial ports
- **Flexible Settings**: Configurable baud rate, data bits, parity, stop bits, and timeout
- **Real-time Status**: Connection status indicator with color-coded feedback
- **Easy Connect/Disconnect**: Single-click connection management

### 📊 Multiple Data Formats
- **Text Mode**: Standard text input/output with UTF-8 encoding
- **Hexadecimal**: Enter and view data as hex values (e.g., `0A FF 3C`)
- **Decimal**: Send and receive data as decimal byte values (e.g., `10 255 60`)
- **Binary**: Full binary representation for each byte (e.g., `00001010 11111111`)

### ⚙️ Advanced Options
- **Line Endings**: Support for CR, LF, CR+LF, or no line endings
- **Format Exclusivity**: Only one input and one output format active at a time
- **Auto-validation**: Input validation with helpful error messages
- **Control Character Display**: Visible representation of special characters

### 📝 Logging System
- **Timestamped Logs**: Automatic log file creation with unique timestamps
- **Complete Session Recording**: Captures all sent/received data and system messages
- **Structured Format**: Well-organized log files with session headers and footers
- **Enable/Disable**: Toggle logging on/off during operation

### 🎨 User Interface
- **Professional Design**: Clean, organized layout with grouped controls
- **Color-coded Terminal**: Different colors for sent data, received data, errors, and system messages
- **Real-time Display**: Live updating terminal with timestamps
- **Responsive Layout**: Resizable window with proper scaling

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Dependencies
```bash
pip install pyserial
```

### Clone Repository
```bash
git clone https://github.com/yourusername/simple-serial-terminal.git
cd simple-serial-terminal
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
1. **Run the Application**:
   ```bash
   python simple-terminal.py
   ```

2. **Select COM Port**: Choose your device from the dropdown menu

3. **Configure Settings**: Set baud rate, data bits, parity, stop bits, and timeout

4. **Connect**: Click the "Connect" button

5. **Send Data**: Enter commands in the data field and press Enter or click "Send"

### Data Format Examples

#### Text Mode (Default)
```
Hello World
```

#### Hexadecimal Mode
```
48 65 6C 6C 6F 20 57 6F 72 6C 64
0x48 0x65 0x6C 0x6C 0x6F
```

#### Decimal Mode
```
72 101 108 108 111 32 87 111 114 108 100
```

#### Binary Mode
```
01001000 01100101 01101100 01101100 01101111
```

### Line Endings
- **None**: Send data as-is
- **CR**: Append carriage return (`\r`)
- **LF**: Append line feed (`\n`)
- **CR+LF**: Append both (`\r\n`)

### Logging
Enable logging to create timestamped log files:
```
terminal_log_20250731_143025.txt
```

Log files include:
- Session start/end timestamps
- All sent and received data with timestamps
- System messages and errors
- Connection details

## Configuration

### Serial Port Settings
- **Baud Rate**: 300 to 921600 bps
- **Data Bits**: 5, 6, 7, or 8 bits
- **Parity**: None, Even, Odd, Mark, or Space
- **Stop Bits**: 1, 1.5, or 2 bits
- **Timeout**: Configurable in seconds (can be empty for no timeout)

### Default Settings
- Baud Rate: 9600
- Data Bits: 8
- Parity: None
- Stop Bits: 1
- Timeout: 1.0 seconds

## File Structure
```
simple-serial-terminal/
├── simple-terminal.py          # Main application
├── terminal.py                 # Original HP 8564E terminal (reference)
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── logs/                       # Generated log files (created automatically)
    ├── terminal_log_20250731_143025.txt
    └── terminal_log_20250731_150312.txt
```

## Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Data Formats
![Data Formats](screenshots/data-formats.png)

### Terminal Output
![Terminal Output](screenshots/terminal-output.png)

## Troubleshooting

### Common Issues

#### "No COM ports found"
- Check that your device is properly connected
- Verify device drivers are installed
- Try clicking "Refresh" to update the port list

#### Connection Errors
- Ensure the correct baud rate and settings
- Check that the port isn't being used by another application
- Verify cable connections

#### Permission Errors (Linux/macOS)
```bash
sudo usermod -a -G dialout $USER
# Log out and log back in
```

#### Invalid Data Format
- Check input format matches selected mode (hex/decimal/binary)
- Ensure values are within valid ranges (0-255 for decimal, 8 bits for binary)
- Use spaces to separate multiple values

### Debug Mode
For additional debugging information, run with:
```bash
python simple-terminal.py --debug
```

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/simple-serial-terminal.git
cd simple-serial-terminal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0 (2025-07-31)
- Initial release
- Basic serial communication
- Multiple data format support (text, hex, decimal, binary)
- Logging system
- Professional GUI interface

## Roadmap

### Planned Features
- [ ] Macro/Script support for automated command sequences
- [ ] Data export functionality (CSV, JSON)
- [ ] Custom baud rate input
- [ ] Terminal themes and customization
- [ ] Plugin system for protocol analyzers
- [ ] Real-time data visualization
- [ ] Command history with search
- [ ] Multiple simultaneous connections

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/simple-serial-terminal/issues) page
2. Create a new issue with detailed information
3. Include your OS, Python version, and error messages

## Acknowledgments

- Built with Python and Tkinter
- Uses pySerial library for serial communication
- Inspired by professional serial terminal applications
- Thanks to the open-source community for feedback and contributions

## Related Projects

- [PySerial](https://github.com/pyserial/pyserial) - Serial communication library
- [PuTTY](https://www.putty.org/) - Popular terminal emulator

---

**Made with ❤️ by [Your Name]**

*For more information, visit our [documentation](https://github.com/yourusername/simple-serial-terminal/wiki) or check out the [examples](examples/) directory.*
