# Enhanced Red Team Toolkit v2.8

A comprehensive collection of penetration testing and red team tools designed for educational purposes and authorized security testing.

## 🚀 Phase 7 Testing & Quality Assurance (v2.7)

### New Features Added:
- **Enhanced Test Suite**: Comprehensive unit, integration, validation, and safety tests
- **Quality Assurance System**: Centralized QA management with test result tracking
- **Error Handling & Recovery**: Graceful error handling with automatic cleanup
- **Safe Mode Management**: Configurable safety settings for destructive operations
- **Safe Defaults**: Automatic safety limits and validation for all operations
- **Error Analysis**: Comprehensive error pattern analysis and statistics
- **QA Reports**: Detailed quality assurance reports with metrics and recommendations

### Technical Improvements:
- **Unit Testing Framework**: Comprehensive testing for all modules and functions
- **Integration Testing**: End-to-end workflow testing with mocked dependencies
- **Validation Testing**: Input validation and data integrity testing
- **Safety Testing**: Destructive operation safety and rate limiting tests
- **Error Recovery**: Automatic cleanup and graceful exit on failures
- **Input Validation**: Enhanced validation for all user inputs and data
- **Safety Measures**: Built-in protections against destructive operations

## 🚀 Phase 8 Extensibility & Advanced Features (v2.8)

### New Features Added:
- **Plugin System**: Load external Python scripts as modules with auto-detection
- **Task Scheduler**: Run scans at intervals or on-demand with comprehensive management
- **Sandbox Mode**: Destructive tools restricted to lab testing with safety controls
- **Plugin Management**: Complete plugin lifecycle management (load, unload, execute)
- **Scheduled Tasks**: Automated task execution with history tracking
- **Lab Network Management**: Configurable lab network restrictions
- **Safety Validation**: Comprehensive operation safety checking

### Technical Improvements:
- **Dynamic Plugin Loading**: Runtime plugin discovery and loading
- **Task Scheduling**: Flexible interval-based and one-time task execution
- **Sandbox Enforcement**: Network-based and operation-based safety restrictions
- **Plugin Metadata**: Automatic extraction and management of plugin information
- **Task History**: Comprehensive tracking of scheduled task execution
- **Safety Configuration**: Configurable safety limits and network restrictions
- **Extensibility Framework**: Foundation for future toolkit expansion

## 🚀 Phase 6 Reporting (v2.6)

### New Features Added:
- **Enhanced Reporting System**: Comprehensive reporting and export capabilities
- **Auto-Reports**: Automatic .txt reports per tool in /reports directory
- **Multi-Format Export**: Support for TXT, JSON, HTML, and PDF report formats
- **Session Management**: Organized timestamped reports by session
- **Network Graphs**: Visual graphs for port scans, services, and findings timeline
- **Report Browser**: Browse and manage report files with cleanup capabilities
- **Session Summary**: Comprehensive session summary with statistics

### Technical Improvements:
- **Jinja2 Templates**: Professional HTML report generation with custom styling
- **WeasyPrint Integration**: PDF report generation from HTML templates
- **Matplotlib Graphs**: Visual data representation for network scan results
- **Pandas Integration**: Data analysis and timeline processing
- **Logging Integration**: Comprehensive error, warning, and success event tracking
- **Report Manager**: Centralized reporting system with session tracking

## 🚀 Phase 3 Web & Auth Tools (v2.3)

### New Features Added:
- **Enhanced Web Scraper**: Multi-page scraping with email/URL harvesting and comprehensive reconnaissance
- **Enhanced Web Vulnerability Scanner**: Advanced SQLi/XSS payloads with file upload vulnerability detection
- **Enhanced SSH Brute Force Tool**: Thread pool support with multi-username testing and attempt limits
- **Enhanced Password Tools**: Entropy calculation, advanced generation modes, and wordlist mutation
- **Enhanced Payload Encoder/Decoder**: Base64, URL, hex, ROT13, binary, HTML encoding with multiple format support

### Technical Improvements:
- **Multi-Page Crawling**: Intelligent web crawling with depth control and data extraction
- **Advanced Payload Testing**: Comprehensive SQL injection and XSS testing with progress tracking
- **Thread Pool Architecture**: Improved performance for authentication testing
- **Entropy Analysis**: Mathematical password strength assessment
- **Wordlist Mutation**: Advanced password variation generation with leetspeak and case variations

## 🚀 Phase 2 Networking & Scanning Tools (v2.2)

### New Features Added:
- **Enhanced Port Scanner**: Multi-threaded scanning with Quick/Common/Full modes and service fingerprinting
- **Network Mapper**: Subnet discovery with host and service enumeration capabilities
- **Advanced DNS Tools**: Comprehensive DNS operations including subdomain enumeration and zone transfer testing
- **Enhanced ARP Spoofing**: Multiple modes (Standard, Stealth, Aggressive, Detection Test) with firewall/IDS detection
- **Firewall/IDS Detection**: TTL and ICMP analysis to detect protection mechanisms

### Technical Improvements:
- **Service Fingerprinting**: Banner grabbing and service identification for common ports
- **Multi-threaded Operations**: Improved performance for network scanning tasks
- **Detection Monitoring**: Real-time monitoring for firewall and IDS responses
- **Comprehensive Reporting**: Detailed reports for all network reconnaissance activities

## 🚀 Phase 1 Core Enhancements (v2.1)

### New Features Added:
- **Interactive CLI**: Rich terminal interface with colored output and progress bars
- **Configuration Management**: Persistent settings with CLI config menu
- **Enhanced Logging**: Rotating log files with configurable levels
- **Progress Bars**: Visual feedback for long-running operations
- **Keyboard Shortcuts**: Quick navigation and exit options
- **Error Handling**: Improved error recovery and user feedback
- **Input Validation**: Enhanced input handling with confirmation dialogs

### Technical Improvements:
- **Rich Library**: Advanced terminal UI with tables, panels, and colors
- **TQDM Integration**: Progress tracking for operations
- **Config Persistence**: Settings saved to `toolkit_config.ini`
- **Log Rotation**: Automatic log file management
- **Input Validation**: Robust error handling and user confirmation

## 🛠️ Tools Overview

### Core Tools (Original)
1. **Port Scanner** - Multi-threaded port discovery
2. **Enhanced Payload Encoder/Decoder** - Multiple encoding methods
3. **Hash Generator** - Multiple hash algorithms
4. **Hash Identifier** - Hash type detection
5. **DNS Tools** - DNS lookup and enumeration
6. **Password Tools** - Strength analysis and generation
7. **Banner Grabber** - Service banner extraction
8. **Wordlist Mutator** - Password list generation
9. **File Analyzer** - Binary file analysis
10. **File Metadata Extractor** - File information extraction
11. **Network Sniffer** - Packet capture and analysis
12. **ARP Spoofing Simulator** - MITM attack simulation
13. **Web Vulnerability Scanner** - Web app security testing
14. **DDoS Simulator** - Load testing tool

### New Advanced Tools (v2.0+)
15. **SSH Brute Force Tool** - SSH authentication testing
16. **Web Scraper** - Advanced web reconnaissance
17. **Network Mapper** - Network discovery and mapping
18. **Enhanced Test Suite & QA** - Comprehensive testing and quality assurance system
19. **Configuration Manager** - Settings management
20. **Enhanced Reporting System** - Comprehensive reporting and export capabilities
21. **Plugin Management System** - Load and manage external plugins
22. **Task Scheduler** - Schedule and manage automated tasks
23. **Sandbox Mode Management** - Configure safety and lab restrictions
24. **Help System** - Built-in help and documentation
25. **Firewall/IDS Detection** - Protection mechanism testing

## 📋 Installation

### Prerequisites
- Python 3.6 or higher
- Administrator/root privileges (for some network tools)

### Quick Setup
   ```bash
# Clone or download the toolkit
git clone <repository-url>
cd Red-Team-Toolkit

# Install dependencies
   pip install -r requirements.txt

# Run the toolkit
   python red_team_toolkit.py
   ```

### Dependencies
- **exifread** - EXIF metadata extraction
- **dnspython** - DNS resolution and enumeration
- **flask** - Web server for DDoS simulator
- **flask-socketio** - WebSocket support
- **aiohttp** - Asynchronous HTTP client
- **scapy** - Network packet manipulation
- **requests** - HTTP library
- **beautifulsoup4** - HTML parsing
- **paramiko** - SSH client library
- **colorama** - Cross-platform colored terminal text
- **rich** - Modern CLI interface (Phase 1)
- **tqdm** - Progress bars (Phase 1)
- **jinja2** - HTML template engine (Phase 6)
- **weasyprint** - PDF generation (Phase 6)
- **matplotlib** - Graph generation (Phase 6)
- **pandas** - Data analysis (Phase 6)
- **unittest2** - Enhanced testing framework (Phase 7)
- **schedule** - Task scheduling (Phase 8)
- **psutil** - System and process utilities (Phase 8)

## 🎯 Usage

### Quick Start
```bash
python red_team_toolkit.py
```

### Menu Navigation
- Use number keys (1-25) to select tools
- Use '0' to exit or return to main menu
- Press Ctrl+C to interrupt operations
- Use 'h' for help information

### Phase 1 Enhanced Features
- **Rich CLI Interface**: Beautiful tables and panels (if rich library available)
- **Keyboard Shortcuts**: Quick navigation with 'q', 'quit', 'exit', 'h', 'help'
- **Enhanced Progress Bars**: Visual progress tracking with Rich/tqdm
- **Configuration Management**: Built-in CLI configuration editor
- **Comprehensive Logging**: Automatic log rotation and multiple levels
- **Better Error Handling**: Graceful error management and user feedback

### Configuration
The toolkit now includes a configuration system:
- **Automatic Setup**: Creates default config on first run
- **Persistent Settings**: Saves preferences between sessions
- **Easy Management**: Built-in configuration menu

### Example Usage

#### Port Scanning
```
Select a tool: 1
Enter target host/IP: example.com
Select scan type: 1 (Common ports)
```

#### SSH Brute Force
```
Select a tool: 15
Enter target host/IP: 192.168.1.100
Enter username: admin
Enter wordlist file path: /path/to/wordlist.txt
```

#### Network Mapping
```
Select a tool: 17
Enter network: 192.168.1.0/24
Select scan type: 1 (Quick scan)
```

#### Web Scraping
```
Select a tool: 16
Enter target URL: https://example.com
```

## 🔧 Configuration

### Configuration File
The toolkit creates `toolkit_config.ini` with the following sections:

#### [DEFAULT]
- `max_threads` - Maximum concurrent threads (default: 50)
- `default_timeout` - Default timeout in seconds (default: 5)
- `log_level` - Logging level (default: INFO)
- `save_reports` - Auto-save reports (default: true)
- `report_directory` - Reports folder (default: reports)
- `rate_limit` - Requests per minute (default: 100)
- `enable_colors` - Colored output (default: true)

#### [SCANNING]
- `port_scan_timeout` - Port scan timeout (default: 3)
- `banner_grab_timeout` - Banner grab timeout (default: 5)
- `dns_timeout` - DNS query timeout (default: 10)
- `max_ports_per_scan` - Maximum ports per scan (default: 1000)

#### [SECURITY]
- `max_brute_force_attempts` - Max brute force attempts (default: 10000)
- `max_ddos_clients` - Max DDoS clients (default: 100)
- `max_ddos_duration` - Max DDoS duration (default: 60)
- `enable_destructive_tools` - Enable destructive tools (default: false)

### Managing Configuration
Access the configuration menu from the main toolkit:
```
Select a tool: 19
```

Options:
1. **View Configuration** - Display current settings
2. **Edit Configuration** - Modify specific values
3. **Reset to Defaults** - Restore default settings
4. **Export Configuration** - Save config to file

## 🧪 Testing

### Running Tests
The toolkit includes a comprehensive test suite:
```
Select a tool: 18
```

### Test Coverage
- **Validation Functions** - IP, hostname, port, URL validation
- **Utility Functions** - Entropy calculation, file operations
- **Configuration Management** - Config loading and saving
- **Progress Bars** - Progress tracking functionality
- **Rate Limiting** - Request rate limiting
- **Hash Generation** - Hash algorithm testing
- **Encoding/Decoding** - Base64, URL, hex encoding
- **File Operations** - File handling and reporting
- **Color Support** - Terminal color functionality
- **Input Handling** - Safe input processing
- **Integration Tests** - End-to-end workflows

### Manual Testing
```bash
# Run the test suite directly
python test_red_team_toolkit.py
```

## 📊 Reporting

### Automatic Reports
The toolkit automatically generates reports for most operations:
- **Location**: `reports/` directory
- **Format**: Timestamped text files
- **Content**: Detailed operation results and findings

### Report Types
- **Scan Reports** - Port scans, network mapping
- **Attack Reports** - Brute force attempts, vulnerability scans
- **Analysis Reports** - File analysis, hash generation
- **Tool Reports** - General tool usage and results

### Custom Reports
Users can enable/disable automatic reporting in the configuration:
```
save_reports = true
report_directory = reports
```

## 🔒 Security Features

### Built-in Protections
- **Rate Limiting** - Prevents overwhelming targets
- **Input Validation** - Sanitizes all user inputs
- **Error Handling** - Graceful error management
- **Logging** - Comprehensive activity logging
- **Configuration Validation** - Safe configuration management

### Safety Warnings
All tools include appropriate warnings and disclaimers:
- Educational use only
- Authorization requirements
- Legal compliance reminders
- Ethical usage guidelines

## 🏗️ Architecture

### Modular Design
The toolkit is organized into logical modules:
- **Core Functions** - Validation, utilities, configuration
- **Network Tools** - Scanning, sniffing, mapping
- **Web Tools** - Scraping, vulnerability scanning
- **Analysis Tools** - File analysis, hash operations
- **Testing Framework** - Comprehensive test suite

### Extensibility
The modular architecture makes it easy to add new tools:
1. Add tool function to main file
2. Update main menu
3. Add corresponding tests
4. Update documentation

## 📁 File Structure

```
Red Team Toolkit/
├── red_team_toolkit.py          # Main toolkit script
├── test_red_team_toolkit.py     # Comprehensive test suite
├── requirements.txt             # Python dependencies
├── README.md                   # This documentation
├── toolkit_config.ini          # Configuration file (auto-generated)
└── reports/                    # Generated reports directory
    ├── toolkit.log             # Activity log
    ├── port_scanner_report_*.txt
    ├── network_mapper_report_*.txt
    └── ...
```

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt
```

#### Permission Errors
```bash
# Run with administrator privileges
# Windows: Run as Administrator
# Linux/Mac: sudo python3 red_team_toolkit.py
```

#### Network Tool Issues
- Ensure you have permission to scan the target
- Check firewall settings
- Verify network connectivity

#### Configuration Issues
- Delete `toolkit_config.ini` to reset to defaults
- Check file permissions
- Verify configuration syntax

### Logging
Check the log file for detailed error information:
```
reports/toolkit.log
```

## 🤝 Contributing

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**
3. **Add your improvements**
4. **Write tests for new features**
5. **Update documentation**
6. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive tests
- Update documentation
- Include appropriate warnings
- Maintain backward compatibility

### Testing Your Changes
```bash
# Run the test suite
python test_red_team_toolkit.py

# Test specific functionality
python -m unittest test_red_team_toolkit.TestValidationFunctions
```

## 📄 License

This project is provided for educational and authorized security testing purposes only.

## ⚠️ Disclaimer

The authors are not responsible for any misuse of this toolkit. Users must:
- Comply with applicable laws
- Obtain proper authorization before testing
- Use tools ethically and responsibly
- Respect privacy and security policies

## 🔄 Version History

### v2.0.0 (Current)
- Added configuration management system
- Implemented comprehensive test suite
- Enhanced UI with colors and progress bars
- Added SSH brute force tool
- Added web scraping capabilities
- Added network mapping tool
- Improved error handling and logging
- Added rate limiting protection
- Enhanced reporting system
- Modular architecture improvements

### v1.0.0 (Original)
- Basic port scanning
- Hash generation and identification
- DNS tools
- Password analysis
- File analysis
- Network sniffing
- Web vulnerability scanning
- DDoS simulation

## 📞 Support

For issues, questions, or contributions:
- Check the troubleshooting section
- Review the log files
- Run the test suite
- Submit detailed bug reports

---

**Remember**: This toolkit is for educational purposes and authorized security testing only. Always ensure you have proper authorization before using these tools.
