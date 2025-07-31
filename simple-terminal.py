#!/usr/bin/env python3
"""
Simple Serial Terminal GUI
A general-purpose GUI terminal for serial communication with customizable settings
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime
import queue
import sys

class SimpleSerialTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Serial Terminal")
        self.root.geometry("800x650")
        
        # Serial connection variables
        self.ser = None
        self.connected = False
        self.selected_port = tk.StringVar()
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        # Serial settings variables
        self.baudrate = tk.StringVar(value="9600")
        self.bytesize = tk.StringVar(value="8")
        self.parity = tk.StringVar(value="N")
        self.stopbits = tk.StringVar(value="1")
        self.timeout = tk.StringVar(value="1.0")
        
        # Line ending options
        self.line_ending = tk.StringVar(value="None")
        self.hex_input = tk.BooleanVar(value=False)
        self.hex_output = tk.BooleanVar(value=False)
        self.decimal_input = tk.BooleanVar(value=False)
        self.decimal_output = tk.BooleanVar(value=False)
        self.binary_input = tk.BooleanVar(value=False)
        self.binary_output = tk.BooleanVar(value=False)
        
        # Logging options
        self.enable_logging = tk.BooleanVar(value=False)
        self.log_file = None
        self.log_filename = None
        
        # Create GUI elements
        self.create_widgets()
        
        # Start message queue processor
        self.process_messages()
        
        # Initialize COM ports
        self.refresh_com_ports()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Terminal display gets most space
        
        # Title
        title_label = ttk.Label(main_frame, text="Simple Serial Terminal", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Connection and Settings Frame
        self.create_connection_frame(main_frame)
        
        # Command Frame
        self.create_command_frame(main_frame)
        
        # Terminal Display Frame
        self.create_terminal_frame(main_frame)
        
    def create_connection_frame(self, parent):
        """Create connection settings frame"""
        conn_frame = ttk.LabelFrame(parent, text="Connection Settings", padding="10")
        conn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # First row - COM Port and basic controls
        row1_frame = ttk.Frame(conn_frame)
        row1_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        row1_frame.columnconfigure(1, weight=1)
        
        ttk.Label(row1_frame, text="COM Port:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.port_combo = ttk.Combobox(row1_frame, textvariable=self.selected_port, 
                                      state="readonly", width=30)
        self.port_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.refresh_btn = ttk.Button(row1_frame, text="Refresh", 
                                     command=self.refresh_com_ports)
        self.refresh_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.connect_btn = ttk.Button(row1_frame, text="Connect", 
                                     command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3)
        
        # Second row - Serial settings
        row2_frame = ttk.Frame(conn_frame)
        row2_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Baud rate
        ttk.Label(row2_frame, text="Baud:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        baud_combo = ttk.Combobox(row2_frame, textvariable=self.baudrate, width=8,
                                 values=["300", "1200", "2400", "4800", "9600", "19200", 
                                        "38400", "57600", "115200", "230400", "460800", "921600"])
        baud_combo.grid(row=0, column=1, padx=(0, 15))
        
        # Data bits
        ttk.Label(row2_frame, text="Data:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        data_combo = ttk.Combobox(row2_frame, textvariable=self.bytesize, width=3,
                                 values=["5", "6", "7", "8"], state="readonly")
        data_combo.grid(row=0, column=3, padx=(0, 15))
        
        # Parity
        ttk.Label(row2_frame, text="Parity:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        parity_combo = ttk.Combobox(row2_frame, textvariable=self.parity, width=4,
                                   values=["N", "E", "O", "M", "S"], state="readonly")
        parity_combo.grid(row=0, column=5, padx=(0, 15))
        
        # Stop bits
        ttk.Label(row2_frame, text="Stop:").grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
        stop_combo = ttk.Combobox(row2_frame, textvariable=self.stopbits, width=3,
                                 values=["1", "1.5", "2"], state="readonly")
        stop_combo.grid(row=0, column=7, padx=(0, 15))
        
        # Timeout
        ttk.Label(row2_frame, text="Timeout:").grid(row=0, column=8, sticky=tk.W, padx=(0, 5))
        timeout_entry = ttk.Entry(row2_frame, textvariable=self.timeout, width=6)
        timeout_entry.grid(row=0, column=9, padx=(0, 5))
        ttk.Label(row2_frame, text="s").grid(row=0, column=10, sticky=tk.W)
        
        # Connection Status
        self.status_label = ttk.Label(conn_frame, text="Status: Disconnected", 
                                     foreground="red")
        self.status_label.grid(row=2, column=0, sticky=tk.W)
        
    def create_command_frame(self, parent):
        """Create command input frame"""
        cmd_frame = ttk.LabelFrame(parent, text="Command Input", padding="10")
        cmd_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        cmd_frame.columnconfigure(1, weight=1)
        
        # First row - Data input
        ttk.Label(cmd_frame, text="Data:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.command_entry = ttk.Entry(cmd_frame, font=('Consolas', 10))
        self.command_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.command_entry.bind('<Return>', lambda e: self.send_command())
        
        self.send_btn = ttk.Button(cmd_frame, text="Send", 
                                  command=self.send_command, state="disabled")
        self.send_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.clear_btn = ttk.Button(cmd_frame, text="Clear Terminal", 
                                   command=self.clear_terminal)
        self.clear_btn.grid(row=0, column=3)
        
        # Second row - Options
        options_frame = ttk.Frame(cmd_frame)
        options_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Line ending options
        ttk.Label(options_frame, text="Line ending:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ending_combo = ttk.Combobox(options_frame, textvariable=self.line_ending, width=8,
                                   values=["None", "CR", "LF", "CR+LF"], state="readonly")
        ending_combo.grid(row=0, column=1, padx=(0, 15))
        
        # Input format options
        input_frame = ttk.LabelFrame(options_frame, text="Input Format", padding="5")
        input_frame.grid(row=0, column=2, padx=(0, 15))
        
        hex_input_cb = ttk.Checkbutton(input_frame, text="Hex", 
                                      variable=self.hex_input,
                                      command=self.on_input_format_change)
        hex_input_cb.grid(row=0, column=0, padx=(0, 5))
        
        decimal_input_cb = ttk.Checkbutton(input_frame, text="Dec", 
                                          variable=self.decimal_input,
                                          command=self.on_input_format_change)
        decimal_input_cb.grid(row=0, column=1, padx=(0, 5))
        
        binary_input_cb = ttk.Checkbutton(input_frame, text="Bin", 
                                         variable=self.binary_input,
                                         command=self.on_input_format_change)
        binary_input_cb.grid(row=0, column=2)
        
        # Output format options
        output_frame = ttk.LabelFrame(options_frame, text="Output Format", padding="5")
        output_frame.grid(row=0, column=3, padx=(0, 15))
        
        hex_output_cb = ttk.Checkbutton(output_frame, text="Hex", 
                                       variable=self.hex_output,
                                       command=self.on_output_format_change)
        hex_output_cb.grid(row=0, column=0, padx=(0, 5))
        
        decimal_output_cb = ttk.Checkbutton(output_frame, text="Dec", 
                                           variable=self.decimal_output,
                                           command=self.on_output_format_change)
        decimal_output_cb.grid(row=0, column=1, padx=(0, 5))
        
        binary_output_cb = ttk.Checkbutton(output_frame, text="Bin", 
                                          variable=self.binary_output,
                                          command=self.on_output_format_change)
        binary_output_cb.grid(row=0, column=2)
        
        # Enable logging checkbox
        log_cb = ttk.Checkbutton(options_frame, text="Enable logging", 
                                variable=self.enable_logging,
                                command=self.toggle_logging)
        log_cb.grid(row=0, column=4, padx=(0, 15))
        
        # Log status label
        self.log_status_label = ttk.Label(options_frame, text="", font=('Arial', 8), foreground="gray")
        self.log_status_label.grid(row=0, column=5)
        
        # Info text
        info_text = "Enter data as text, hex (0A FF), decimal (10 255), or binary (00001010 11111111). Line endings are automatically added."
        ttk.Label(cmd_frame, text=info_text, font=('Arial', 8), foreground="gray").grid(
            row=2, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Log file info
        log_info_text = "Enable logging to save all terminal output to a timestamped log file."
        ttk.Label(cmd_frame, text=log_info_text, font=('Arial', 8), foreground="gray").grid(
            row=3, column=0, columnspan=4, sticky=tk.W, pady=(2, 0))
    
    def create_terminal_frame(self, parent):
        """Create terminal display frame"""
        terminal_frame = ttk.LabelFrame(parent, text="Terminal Output", padding="10")
        terminal_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        terminal_frame.columnconfigure(0, weight=1)
        terminal_frame.rowconfigure(0, weight=1)
        
        # Terminal text display
        self.terminal_text = scrolledtext.ScrolledText(
            terminal_frame, 
            wrap=tk.WORD, 
            width=100, 
            height=20, 
            font=('Consolas', 9),
            bg='black',
            fg='lime',
            insertbackground='lime'
        )
        self.terminal_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add initial welcome message
        self.display_message("=== Simple Serial Terminal ===", "SYSTEM")
        self.display_message("1. Select COM port and configure settings", "SYSTEM")
        self.display_message("2. Click Connect to establish connection", "SYSTEM")
        self.display_message("3. Enter commands in the data field and press Send or Enter", "SYSTEM")
        self.display_message("4. Use options to control line endings and hex formatting", "SYSTEM")
        self.display_message("", "SYSTEM")
    
    def refresh_com_ports(self):
        """Refresh the list of available COM ports"""
        try:
            ports = serial.tools.list_ports.comports()
            port_list = []
            
            for port in ports:
                port_description = f"{port.device} - {port.description}"
                port_list.append(port_description)
            
            if not port_list:
                port_list = ["No COM ports found"]
                
            self.port_combo['values'] = port_list
            
            # Auto-select first available port if none selected
            if port_list and port_list[0] != "No COM ports found" and not self.selected_port.get():
                self.port_combo.current(0)
                
            self.display_message(f"Found {len([p for p in port_list if p != 'No COM ports found'])} COM ports", "SYSTEM")
            
        except Exception as e:
            self.display_message(f"Error refreshing COM ports: {e}", "ERROR")
    
    def toggle_connection(self):
        """Connect or disconnect from the selected COM port"""
        if self.connected:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        """Connect to the selected COM port"""
        if not self.selected_port.get() or "No COM ports found" in self.selected_port.get():
            messagebox.showwarning("Warning", "Please select a valid COM port")
            return
        
        try:
            # Validate settings
            try:
                baudrate = int(self.baudrate.get())
                bytesize = int(self.bytesize.get())
                stopbits = float(self.stopbits.get())
                timeout = float(self.timeout.get()) if self.timeout.get() else None
            except ValueError:
                messagebox.showerror("Error", "Invalid serial port settings")
                return
            
            # Extract COM port name
            port_name = self.selected_port.get().split(' - ')[0]
            
            self.display_message(f"Connecting to {port_name}...", "SYSTEM")
            
            # Create serial connection
            self.ser = serial.Serial(
                port=port_name,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=self.parity.get(),
                stopbits=stopbits,
                timeout=timeout,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            
            if self.ser.is_open:
                self.connected = True
                self.status_label.config(text=f"Status: Connected to {port_name}", foreground="green")
                self.connect_btn.config(text="Disconnect")
                self.send_btn.config(state="normal")
                
                settings_info = f"{baudrate}-{bytesize}-{self.parity.get()}-{stopbits}, Timeout: {timeout}s"
                self.display_message(f"Successfully connected to {port_name} ({settings_info})", "SUCCESS")
                
                # Start background thread to read incoming data
                self.start_read_thread()
            else:
                self.display_message("Failed to open serial port", "ERROR")
                
        except Exception as e:
            self.display_message(f"Connection error: {e}", "ERROR")
            if self.ser and self.ser.is_open:
                self.ser.close()
    
    def disconnect(self):
        """Disconnect from the COM port"""
        try:
            # First, signal disconnection to stop the read thread
            self.connected = False
            
            # Give the read thread a moment to stop
            time.sleep(0.1)
            
            # Now close the serial port
            if self.ser and self.ser.is_open:
                self.ser.close()
            
            self.status_label.config(text="Status: Disconnected", foreground="red")
            self.connect_btn.config(text="Connect")
            self.send_btn.config(state="disabled")
            self.display_message("Disconnected", "SYSTEM")
            
        except Exception as e:
            self.display_message(f"Disconnect error: {e}", "ERROR")
    
    def toggle_logging(self):
        """Toggle logging on/off"""
        if self.enable_logging.get():
            self.start_logging()
        else:
            self.stop_logging()
    
    def start_logging(self):
        """Start logging to a timestamped file"""
        try:
            # Create timestamped filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.log_filename = f"terminal_log_{timestamp}.txt"
            
            # Open log file
            self.log_file = open(self.log_filename, 'w', encoding='utf-8')
            
            # Write header
            header = f"=== Simple Serial Terminal Log Started ===\n"
            header += f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += f"Log file: {self.log_filename}\n"
            header += "=" * 50 + "\n\n"
            self.log_file.write(header)
            self.log_file.flush()
            
            # Update status
            self.log_status_label.config(text=f"Logging to: {self.log_filename}", foreground="green")
            self.display_message(f"Logging started: {self.log_filename}", "SYSTEM")
            
        except Exception as e:
            self.enable_logging.set(False)
            self.display_message(f"Failed to start logging: {e}", "ERROR")
            self.log_status_label.config(text="Logging failed", foreground="red")
    
    def stop_logging(self):
        """Stop logging"""
        try:
            if self.log_file:
                # Write footer
                footer = f"\n" + "=" * 50 + "\n"
                footer += f"Session ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                footer += "=== Simple Serial Terminal Log Ended ===\n"
                self.log_file.write(footer)
                self.log_file.close()
                self.log_file = None
            
            # Update status
            self.log_status_label.config(text="Logging stopped", foreground="gray")
            self.display_message("Logging stopped", "SYSTEM")
            
        except Exception as e:
            self.display_message(f"Error stopping logging: {e}", "ERROR")
    
    def log_to_file(self, message):
        """Log a message to the file if logging is enabled"""
        if self.enable_logging.get() and self.log_file:
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                log_entry = f"[{timestamp}] {message}\n"
                self.log_file.write(log_entry)
                self.log_file.flush()  # Ensure immediate write
            except Exception as e:
                # If logging fails, disable it to prevent repeated errors
                self.enable_logging.set(False)
                self.stop_logging()
                self.display_message(f"Logging error, disabled: {e}", "ERROR")
    
    def on_input_format_change(self):
        """Handle input format checkbox changes - ensure only one is selected"""
        formats = [(self.hex_input, 'hex'), (self.decimal_input, 'decimal'), (self.binary_input, 'binary')]
        checked_formats = [fmt_name for fmt_var, fmt_name in formats if fmt_var.get()]
        
        if len(checked_formats) > 1:
            # If multiple are checked, uncheck all except the last one clicked
            current_format = getattr(self, '_last_input_change', 'hex')
            for fmt_var, fmt_name in formats:
                if fmt_name != current_format:
                    fmt_var.set(False)
        
        # Update last changed format
        for fmt_var, fmt_name in formats:
            if fmt_var.get():
                self._last_input_change = fmt_name
                break
    
    def on_output_format_change(self):
        """Handle output format checkbox changes - ensure only one is selected"""
        formats = [(self.hex_output, 'hex'), (self.decimal_output, 'decimal'), (self.binary_output, 'binary')]
        checked_formats = [fmt_name for fmt_var, fmt_name in formats if fmt_var.get()]
        
        if len(checked_formats) > 1:
            # If multiple are checked, uncheck all except the last one clicked
            current_format = getattr(self, '_last_output_change', 'hex')
            for fmt_var, fmt_name in formats:
                if fmt_name != current_format:
                    fmt_var.set(False)
        
        # Update last changed format
        for fmt_var, fmt_name in formats:
            if fmt_var.get():
                self._last_output_change = fmt_name
                break
    
    def send_command(self):
        """Send command from the entry field"""
        if not self.connected or not self.ser:
            messagebox.showwarning("Warning", "Not connected to any COM port")
            return
        
        command = self.command_entry.get()
        if not command:
            return
        
        try:
            # Process input based on format selection
            if self.hex_input.get():
                # Convert hex string to bytes
                try:
                    # Remove spaces and convert hex string to bytes
                    hex_string = command.replace(" ", "").replace("0x", "")
                    if len(hex_string) % 2 != 0:
                        hex_string = "0" + hex_string  # Pad with leading zero
                    data = bytes.fromhex(hex_string)
                    display_command = f"HEX: {' '.join(f'{b:02X}' for b in data)}"
                except ValueError:
                    messagebox.showerror("Error", "Invalid hex string format")
                    return
            elif self.decimal_input.get():
                # Convert decimal string to bytes
                try:
                    # Split by spaces and convert each decimal value to byte
                    decimal_values = command.strip().split()
                    byte_values = []
                    for val in decimal_values:
                        decimal_val = int(val)
                        if 0 <= decimal_val <= 255:
                            byte_values.append(decimal_val)
                        else:
                            messagebox.showerror("Error", f"Decimal value {decimal_val} is out of range (0-255)")
                            return
                    data = bytes(byte_values)
                    display_command = f"DEC: {' '.join(str(b) for b in data)}"
                except ValueError:
                    messagebox.showerror("Error", "Invalid decimal format. Use space-separated values (0-255)")
                    return
            elif self.binary_input.get():
                # Convert binary string to bytes
                try:
                    # Split by spaces and convert each binary value to byte
                    binary_values = command.strip().split()
                    byte_values = []
                    for val in binary_values:
                        # Remove any '0b' prefix and validate binary format
                        binary_val = val.replace("0b", "")
                        if not all(c in '01' for c in binary_val):
                            messagebox.showerror("Error", f"Invalid binary value: {val}. Use only 0s and 1s")
                            return
                        if len(binary_val) > 8:
                            messagebox.showerror("Error", f"Binary value {val} is too long (max 8 bits)")
                            return
                        if len(binary_val) == 0:
                            messagebox.showerror("Error", f"Empty binary value: {val}")
                            return
                        # Pad to 8 bits if necessary
                        binary_val = binary_val.zfill(8)
                        decimal_val = int(binary_val, 2)
                        byte_values.append(decimal_val)
                    data = bytes(byte_values)
                    display_command = f"BIN: {' '.join(f'{b:08b}' for b in data)}"
                except ValueError:
                    messagebox.showerror("Error", "Invalid binary format. Use space-separated 8-bit values (e.g., 01001000)")
                    return
            else:
                # Regular text input
                data = command.encode('utf-8')
                display_command = command
            
            # Add line ending if selected
            if self.line_ending.get() == "CR":
                data += b'\r'
            elif self.line_ending.get() == "LF":
                data += b'\n'
            elif self.line_ending.get() == "CR+LF":
                data += b'\r\n'
            
            # Send data
            self.ser.write(data)
            
            # Display sent command
            ending_info = f" + {self.line_ending.get()}" if self.line_ending.get() != "None" else ""
            self.display_message(f"SENT: {display_command}{ending_info}", "SENT")
            
            self.command_entry.delete(0, tk.END)  # Clear the entry field
            
        except Exception as e:
            self.display_message(f"Send error: {e}", "ERROR")
    
    def start_read_thread(self):
        """Start background thread to read incoming data"""
        def read_serial():
            while self.connected and self.ser and self.ser.is_open:
                try:
                    # Check if still connected before attempting to read
                    if not self.connected:
                        break
                        
                    if self.ser.in_waiting > 0:
                        data = self.ser.read(self.ser.in_waiting)
                        if data:
                            self.message_queue.put(("RECEIVED_DATA", data))
                    time.sleep(0.05)  # Small delay to prevent excessive CPU usage
                except Exception as e:
                    # Only report error if we're still supposed to be connected
                    if self.connected:
                        self.message_queue.put(("ERROR", f"Read error: {e}"))
                    break
        
        read_thread = threading.Thread(target=read_serial, daemon=True)
        read_thread.start()
    
    def display_message(self, message, msg_type="INFO"):
        """Display a message in the terminal with timestamp and color coding"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Include milliseconds
        
        # Color coding based on message type
        colors = {
            "SENT": "cyan",
            "RECEIVED": "lime",
            "ERROR": "red",
            "SUCCESS": "green",
            "SYSTEM": "yellow",
            "INFO": "white"
        }
        
        color = colors.get(msg_type, "white")
        formatted_message = f"[{timestamp}] {msg_type}: {message}\n"
        
        # Log to file if enabled
        self.log_to_file(f"{msg_type}: {message}")
        
        # Add to message queue for thread-safe GUI updates
        self.message_queue.put(("DISPLAY", formatted_message, color))
    
    def clear_terminal(self):
        """Clear the terminal display"""
        self.terminal_text.delete(1.0, tk.END)
        self.display_message("Terminal cleared", "SYSTEM")
    
    def process_messages(self):
        """Process messages from the queue (runs in main thread)"""
        try:
            while True:
                message_data = self.message_queue.get_nowait()
                
                if message_data[0] == "DISPLAY":
                    _, formatted_message, color = message_data
                    # Insert text with color
                    self.terminal_text.insert(tk.END, formatted_message)
                    # Apply color to the last line
                    line_start = self.terminal_text.index("end-2c linestart")
                    line_end = self.terminal_text.index("end-1c")
                    self.terminal_text.tag_add(color, line_start, line_end)
                    self.terminal_text.tag_config(color, foreground=color)
                    self.terminal_text.see(tk.END)
                    
                elif message_data[0] == "RECEIVED_DATA":
                    _, data = message_data
                    if self.hex_output.get():
                        # Display as hex
                        hex_string = ' '.join(f'{b:02X}' for b in data)
                        self.display_message(f"HEX: {hex_string}", "RECEIVED")
                    elif self.decimal_output.get():
                        # Display as decimal
                        decimal_string = ' '.join(str(b) for b in data)
                        self.display_message(f"DEC: {decimal_string}", "RECEIVED")
                    elif self.binary_output.get():
                        # Display as binary
                        binary_string = ' '.join(f'{b:08b}' for b in data)
                        self.display_message(f"BIN: {binary_string}", "RECEIVED")
                    else:
                        # Display as text (with error handling for non-printable chars)
                        try:
                            text = data.decode('utf-8', errors='replace')
                            # Replace control characters with readable representations
                            text = text.replace('\r', '\\r').replace('\n', '\\n').replace('\t', '\\t')
                            self.display_message(f"TEXT: {text}", "RECEIVED")
                        except:
                            # Fallback to hex if decoding fails
                            hex_string = ' '.join(f'{b:02X}' for b in data)
                            self.display_message(f"HEX: {hex_string}", "RECEIVED")
                            
                elif message_data[0] == "ERROR":
                    _, message = message_data
                    self.display_message(message, "ERROR")
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)
    
    def on_closing(self):
        """Handle window closing"""
        # Stop logging if active
        if self.enable_logging.get():
            self.stop_logging()
        self.disconnect()
        self.root.destroy()

def main():
    """Main function to run the terminal GUI"""
    root = tk.Tk()
    app = SimpleSerialTerminal(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
