# DNS Troubleshooter Simulation Toolkit

A comprehensive educational tool for simulating DNS troubleshooting scenarios on both Windows and Linux systems.

## Features

- **System Information Display**: Automatically detects and displays OS, CPU, RAM, storage, and network details
- **Wireshark Integration**: Automatic detection and installation of Wireshark for packet capture
- **DNS Failure Simulation**: Realistic simulation of DNS issues and resolution
- **Cross-Platform Support**: Works on both Windows and Linux systems
- **Professional Logging**: Comprehensive logging of all operations and system information
- **Educational Focus**: Designed for learning DNS troubleshooting concepts

## Files

- `enhanced_windows_version.py` - Windows version with colorama support
- `enhanced_kali_linux_version.py` - Linux version with rich library support
- `requirements.txt` - Python dependencies

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Windows Requirements**:
   - Python 3.6+
   - Administrator privileges (for real DNS changes)
   - Wireshark (optional, will be auto-detected)

3. **Linux Requirements**:
   - Python 3.6+
   - sudo privileges (for real DNS changes)
   - Wireshark (optional, will be auto-detected)

## Usage

### Windows

**Option 1: Run as Administrator (Full Simulation)**
1. Right-click on PowerShell/Command Prompt
2. Select "Run as administrator"
3. Navigate to the toolkit directory
4. Run: `python enhanced_windows_version.py`

**Option 2: Run as Regular User (Presentation Mode)**
1. Open PowerShell/Command Prompt
2. Navigate to the toolkit directory
3. Run: `python enhanced_windows_version.py`
4. Choose "Continue in presentation mode" when prompted

### Linux

**Option 1: Run with sudo (Full Simulation)**
```bash
sudo python3 enhanced_kali_linux_version.py
```

**Option 2: Run as Regular User (Presentation Mode)**
```bash
python3 enhanced_kali_linux_version.py
```

## What the Tool Does

1. **System Analysis**: Displays comprehensive system information
2. **Wireshark Check**: Verifies Wireshark installation and offers to install if missing
3. **Network Interface Detection**: Identifies the primary network interface
4. **Current State**: Shows current network configuration and DNS settings
5. **DNS Failure Simulation**: 
   - Changes DNS servers to invalid addresses
   - Demonstrates DNS resolution failure
   - Shows that IP connectivity still works
6. **DNS Restoration**: 
   - Restores DNS servers to working addresses
   - Flushes DNS cache
   - Verifies DNS resolution is working
7. **Packet Capture**: Records DNS traffic during the simulation
8. **Wireshark Analysis**: Automatically opens captured packets for analysis
9. **Logging**: Saves all operations and system information to log files

## Output Files

- `dns_toolkit_log_YYYYMMDD_HHMMSS.txt` - Complete log of all operations
- `dns_capture_interface_YYYYMMDD_HHMMSS.pcap` - Wireshark packet capture file

## Educational Value

This toolkit demonstrates:
- **DNS Resolution Process**: How DNS queries work and fail
- **Network Troubleshooting**: Systematic approach to DNS issues
- **Packet Analysis**: Using Wireshark to capture and analyze DNS traffic
- **System Administration**: Managing network interface settings
- **Logging and Documentation**: Professional approach to troubleshooting

## Safety Features

- **Administrator Check**: Warns if running without proper privileges
- **Presentation Mode**: Safe operation without admin rights
- **Automatic Restoration**: Ensures DNS is restored after simulation
- **Error Handling**: Graceful handling of missing tools or permissions
- **Wireshark Integration**: Automatically opens captured packets for analysis

## Troubleshooting

### Common Issues

1. **"Administrator privileges required"**
   - Solution: Run as Administrator or use simulation mode

2. **"Wireshark not found"**
   - Solution: Allow the tool to install Wireshark or continue without it

3. **"Interface detection failed"**
   - Solution: Check network connectivity and try again

4. **"DNS changes not taking effect"**
   - Solution: Ensure running as Administrator and wait for changes to propagate

### Getting Help

If you encounter issues:
1. Check the log file for detailed error information
2. Ensure you have the required permissions
3. Verify network connectivity
4. Check that all dependencies are installed

## License

This tool is designed for educational purposes. Use responsibly and only on systems you own or have permission to test.
