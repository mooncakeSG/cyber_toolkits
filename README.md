# Cyber Security Toolkits 🛡️⚔️🟣



A comprehensive collection of offensive, defensive, and purple team cybersecurity tools designed for educational purposes and authorized security testing. This repository contains three specialized toolkits: a **Blue Team Toolkit** for defensive security operations, a **Red Team Toolkit** for penetration testing and offensive security, and a **Purple Team Toolkit** for attack-defense correlation and testing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/cyber-security-toolkits)
[![Blue Team](https://img.shields.io/badge/Blue%20Team-Complete-brightgreen.svg)](https://github.com/yourusername/cyber-security-toolkits/tree/main/Blueteam%20Toolkit)
[![Red Team](https://img.shields.io/badge/Red%20Team-v2.8-orange.svg)](https://github.com/yourusername/cyber-security-toolkits/tree/main/Red%20Team%20Toolkit)
[![Purple Team](https://img.shields.io/badge/Purple%20Team-CLI%20Ready-purple.svg)](https://github.com/yourusername/cyber-security-toolkits/tree/main/Purple%20Team%20Toolkit)

## 📋 Table of Contents

- [Overview](#overview)
- [Toolkits](#toolkits)
  - [Blue Team Toolkit](#blue-team-toolkit)
  - [Red Team Toolkit](#red-team-toolkit)
  - [Purple Team Toolkit](#purple-team-toolkit)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Security & Ethics](#security--ethics)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains three comprehensive cybersecurity toolkits designed for different aspects of security operations:

- **🛡️ Blue Team Toolkit**: Defensive security operations, incident response, and threat hunting
- **⚔️ Red Team Toolkit**: Penetration testing, vulnerability assessment, and offensive security
- **🟣 Purple Team Toolkit**: Attack-defense correlation, scenario testing, and coverage analysis

All toolkits are designed with modularity, extensibility, and professional-grade features in mind, with a focus on CLI-based operations for better performance and security.

## 🛠️ Toolkits

### 🛡️ Blue Team Toolkit

**Status**: ✅ **Production Ready** - Complete with all planned features

A comprehensive defensive security toolkit designed for incident response, threat hunting, and security monitoring operations.

#### 🚀 Key Features

- **📋 Log Collection & Analysis** - Windows Event Logs, Linux syslog, keyword filtering
- **🔍 Threat Hunting** - MITRE ATT&CK techniques + Sigma rule integration
- **🚨 Incident Response** - Live system snapshots with containment capabilities
- **🔎 IOC Scanning** - Multi-source scanning with VirusTotal integration
- **🌐 Network Defense** - Connection analysis, beaconing detection, IP blocking
- **🧠 Memory Forensics** - Process memory analysis and anomaly detection
- **🔗 SIEM Integration** - ELK, Wazuh, Splunk connectivity
- **🤖 Automation** - Scheduled tasks and automated reporting
- **📢 Alerting** - Multi-channel notifications (Slack, Teams, Email)

#### 📊 Statistics

- **11 Core Modules** with 50+ features
- **3,000+ Lines of Code**
- **Cross-Platform Support** (Windows, Linux, macOS)
- **Multiple Export Formats** (JSON, CSV, TXT with compression)
- **100% Enhancement Completion**

#### 🎯 Use Cases

```bash
# Incident Response
python main.py ir --quarantine --export incident_report.json

# Threat Hunting
python main.py hunt --technique T1053 --export hunt_results.json

# SIEM Integration
python main.py siem --type elk --host localhost --alerts

# IOC Analysis
python main.py ioc --type ip --value 8.8.8.8 --vt
```

**[📖 Full Blue Team Documentation](Blueteam%20Toolkit/README.md)**

---

### ⚔️ Red Team Toolkit

**Status**: ✅ **Production Ready** - v2.8 with advanced extensibility features

A comprehensive offensive security toolkit designed for penetration testing, vulnerability assessment, and red team operations.

#### 🚀 Key Features

- **🔍 Network Reconnaissance** - Port scanning, network mapping, DNS enumeration
- **🌐 Web Security Testing** - Vulnerability scanning, web scraping, authentication testing
- **🔐 Authentication Testing** - SSH brute force, password analysis, hash operations
- **📡 Network Attacks** - ARP spoofing, DDoS simulation, packet analysis
- **🔧 Analysis Tools** - File analysis, metadata extraction, hash identification
- **🤖 Plugin System** - Dynamic plugin loading and auto-registration
- **⏰ Task Scheduler** - Automated task execution and management
- **📊 Resource Monitoring** - Real-time system resource tracking
- **🛡️ Sandbox Mode** - Safety controls and lab network restrictions

#### 📊 Statistics

- **25+ Core Tools** with advanced features
- **12,800+ Lines of Code**
- **Plugin Architecture** with auto-discovery
- **Comprehensive Test Suite** (24 test cases)
- **Advanced Reporting** (HTML, PDF, JSON)

#### 🎯 Use Cases

```bash
# Network Scanning
python red_team_toolkit.py
# Select: 1 - Port Scanner
# Target: example.com

# Web Vulnerability Testing
python red_team_toolkit.py
# Select: 13 - Web Vulnerability Scanner
# Target: https://example.com

# Plugin Development
# Create custom tools in plugins/ directory
```

**[📖 Full Red Team Documentation](Red%20Team%20Toolkit/README.md)**

---

### 🟣 Purple Team Toolkit

**Status**: ✅ **CLI Production Ready** - Comprehensive attack-defense correlation framework

A unified CLI-based cybersecurity framework that integrates Red Team, Blue Team, and Purple Team operations for comprehensive security testing and correlation analysis.

#### 🚀 Key Features

- **🔄 Attack-Defense Correlation** - Real-time mapping of attacks to detections
- **📊 MITRE ATT&CK Integration** - Framework-based technique testing and coverage analysis
- **🎯 Scenario Execution** - Complete attack-defense scenario testing
- **📈 Coverage Analysis** - Detection gap identification and reporting
- **🛡️ Safety Controls** - Sandbox mode, confirmation prompts, rate limiting
- **📋 Rich CLI Interface** - Beautiful terminal output with progress indicators
- **📊 Multi-Format Reporting** - HTML, PDF, JSON, CSV report generation
- **🔧 Extensible Architecture** - Plugin system and custom scenarios

#### 📊 Statistics

- **15+ CLI Commands** across all toolkits
- **3 Integrated Modules** (Red, Blue, Purple Team)
- **Rich Terminal UI** with color-coded output
- **Comprehensive Documentation** with usage guides
- **Safety Features** including sandbox mode

#### 🎯 Use Cases

```bash
# Check toolkit status
python purple_cli.py status

# List available scenarios
python purple_cli.py list-scenarios

# Execute full scenario
python purple_cli.py run-scenario -s configs/scenarios/basic_recon.yaml --sandbox

# Red Team reconnaissance
python purple_cli.py red-team recon -t target.com --scan-type full

# Blue Team monitoring
python purple_cli.py blue-team monitor -d 3600 -o alerts.json

# Coverage analysis
python purple_cli.py analyze -t target.com --techniques T1046 T1071 T1059

# Generate reports
python purple_cli.py report -f html -o reports/assessment.html
```

**[📖 Full Purple Team Documentation](Purple%20Team%20Toolkit/README.md)**
**[📖 CLI Usage Guide](Purple%20Team%20Toolkit/CLI_GUIDE.md)**

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9+)
- **Administrative privileges** (for advanced features)
- **Cross-platform support** (Windows, Linux, macOS)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cyber-security-toolkits.git
cd cyber-security-toolkits

# Install Blue Team Toolkit
cd "Blueteam Toolkit"
pip install -r requirements.txt

# Install Red Team Toolkit
cd "../Red Team Toolkit"
pip install -r requirements.txt

# Install Purple Team Toolkit
cd "../Purple Team Toolkit"
pip install -r requirements.txt
```

### Basic Usage

#### Blue Team Toolkit

```bash
cd "Blueteam Toolkit"
python main.py --help
python main.py logs --os windows --lines 100
python main.py hunt --technique T1053
```

#### Red Team Toolkit

```bash
cd "Red Team Toolkit"
python red_team_toolkit.py
# Interactive menu-driven interface
```

#### Purple Team Toolkit

```bash
cd "Purple Team Toolkit"
python purple_cli.py --help
python purple_cli.py status
python purple_cli.py list-scenarios
```

## 📦 Installation

### Detailed Setup

#### Blue Team Toolkit

```bash
cd "Blueteam Toolkit"

# Install dependencies
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .

# Run with help
python main.py --help
```

#### Red Team Toolkit

```bash
cd "Red Team Toolkit"

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python red_team_toolkit.py

# Run tests
python test_red_team_toolkit.py
```

#### Purple Team Toolkit

```bash
cd "Purple Team Toolkit"

# Install dependencies
pip install -r requirements.txt

# Check toolkit status
python purple_cli.py status

# Run a basic scenario (safe mode)
python purple_cli.py run-scenario -s configs/scenarios/basic_recon.yaml --sandbox
```

### Dependencies

#### Blue Team Toolkit

- `psutil>=5.9.0` - System and process utilities
- `requests>=2.28.0` - HTTP library
- `PyYAML>=6.0` - YAML processing
- `schedule>=1.2.0` - Task scheduling

#### Red Team Toolkit

- `rich>=13.0.0` - Modern CLI interface
- `scapy>=2.4.0` - Network packet manipulation
- `beautifulsoup4>=4.9.0` - HTML parsing
- `paramiko>=2.8.0` - SSH client library
- `jinja2>=3.0.0` - Template engine
- `weasyprint>=54.0` - PDF generation
- `matplotlib>=3.5.0` - Graph generation
- `pandas>=1.3.0` - Data analysis
- And 15+ additional dependencies

#### Purple Team Toolkit

- `click>=8.1.0` - CLI framework
- `rich>=13.0.0` - Rich terminal output
- `pyyaml>=6.0` - YAML configuration
- `pandas>=2.0.0` - Data analysis
- `plotly>=5.15.0` - Interactive visualizations
- `jinja2>=3.0.0` - Report templates
- `reportlab>=4.0.0` - PDF generation
- And 10+ additional dependencies

## 🎯 Usage Examples

### Blue Team Operations

#### Incident Response

```bash
# Generate comprehensive system snapshot
python main.py ir --quarantine --export incident_report.json

# Live containment actions
python main.py ir --block-ip 192.168.1.100 --kill-process 12345
```

#### Threat Hunting

```bash
# MITRE ATT&CK hunting
python main.py hunt --technique T1053 --export hunt_results.json

# Sigma rule hunting
python main.py hunt --sigma sigma_rules/ --export sigma_results.json
```

#### Security Monitoring

```bash
# SIEM integration
python main.py siem --type elk --host localhost --alerts

# Automated monitoring
python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "09:00"
```

### Red Team Operations

#### Network Reconnaissance

```bash
# Port scanning
python red_team_toolkit.py
# Select: 1 - Port Scanner
# Enter target: example.com
# Select scan type: 1 (Common ports)

# Network mapping
python red_team_toolkit.py
# Select: 17 - Network Mapper
# Enter network: 192.168.1.0/24
```

#### Web Security Testing

```bash
# Web vulnerability scanning
python red_team_toolkit.py
# Select: 13 - Web Vulnerability Scanner
# Enter target: https://example.com

# Web scraping
python red_team_toolkit.py
# Select: 16 - Web Scraper
# Enter target: https://example.com
```

#### Authentication Testing

```bash
# SSH brute force
python red_team_toolkit.py
# Select: 15 - SSH Brute Force Tool
# Enter target: 192.168.1.100
# Enter username: admin
# Enter wordlist: /path/to/wordlist.txt
```

### Purple Team Operations

#### Complete Scenario Testing

```bash
# Run a full attack-defense scenario
python purple_cli.py run-scenario -s configs/scenarios/web_attack.yaml --sandbox

# Execute with custom output
python purple_cli.py run-scenario -s configs/scenarios/post_exploitation.yaml -o results/ --parallel
```

#### Individual Toolkit Operations

```bash
# Red Team reconnaissance
python purple_cli.py red-team recon -t target.com --scan-type full -o recon.json

# Blue Team monitoring
python purple_cli.py blue-team monitor -d 1800 -o alerts.json

# Threat hunting
python purple_cli.py blue-team hunt -q "process.name == 'powershell.exe'"
```

#### Analysis and Reporting

```bash
# Coverage analysis
python purple_cli.py analyze -t target.com --techniques T1046 T1071 T1059

# Generate comprehensive report
python purple_cli.py report -f html -o reports/security_assessment.html

# Generate PDF report
python purple_cli.py report -f pdf -o reports/security_assessment.pdf
```

## 🛡️ Security & Ethics

### ⚠️ Important Disclaimers

1. **Educational Purpose**: These toolkits are designed for educational purposes and authorized security testing only.
2. **Legal Compliance**: Users must comply with all applicable laws and regulations in their jurisdiction.
3. **Authorization Required**: Always obtain proper authorization before testing any system or network.
4. **Ethical Usage**: Use these tools responsibly and ethically, respecting privacy and security policies.

### 🔒 Built-in Safety Features

#### Blue Team Toolkit

- **Privilege Management**: Administrative privilege detection and safe operation modes
- **Data Protection**: Secure credential storage and HTTPS connections
- **Live Response**: Safe containment with automatic cleanup

#### Red Team Toolkit

- **Sandbox Mode**: Configurable safety controls and lab network restrictions
- **Rate Limiting**: Built-in protection against overwhelming targets
- **Resource Monitoring**: Real-time system resource tracking
- **Dangerous Tools**: Clear warnings and information about potentially harmful operations

#### Purple Team Toolkit

- **Sandbox Mode**: Safe testing environment for all operations
- **Confirmation Prompts**: Destructive operations require explicit approval
- **Rate Limiting**: Automatic protection against overwhelming targets
- **Audit Logging**: Complete operation tracking and documentation

### 🎓 Educational Value

These toolkits provide hands-on experience with:

- **Incident Response Procedures**
- **Threat Hunting Techniques**
- **Penetration Testing Methodologies**
- **Attack-Defense Correlation**
- **Security Tool Development**
- **Automation and Orchestration**
- **Reporting and Documentation**

## 🤝 Contributing

We welcome contributions from the security community! Please see our contributing guidelines:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/mooncakesg/cyber-security-toolkits.git
cd cyber-security-toolkits

# Set up development environment
# Blue Team Toolkit
cd "Blueteam Toolkit"
pip install -e .

# Red Team Toolkit
cd "../Red Team Toolkit"
pip install -r requirements.txt

# Purple Team Toolkit
cd "../Purple Team Toolkit"
pip install -r requirements.txt
```

### Contribution Areas

- **Bug Fixes**: Report and fix issues
- **Feature Enhancements**: Add new capabilities
- **Documentation**: Improve guides and examples
- **Testing**: Expand test coverage
- **Security**: Enhance safety features
- **CLI Improvements**: Enhance command-line interfaces

### Code Standards

- Follow **PEP 8** style guidelines
- Add comprehensive **tests** for new features
- Update **documentation** for changes
- Include appropriate **warnings** and disclaimers
- Maintain **backward compatibility**

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 📞 Support

### Documentation

- **[Blue Team Toolkit Documentation](Blueteam%20Toolkit/README.md)**
- **[Red Team Toolkit Documentation](Red%20Team%20Toolkit/README.md)**
- **[Purple Team Toolkit Documentation](Purple%20Team%20Toolkit/README.md)**
- **[Purple Team CLI Guide](Purple%20Team%20Toolkit/CLI_GUIDE.md)**
- **[Installation Guide](Blueteam%20Toolkit/INSTALL.md)**

### Issues & Discussions

- **GitHub Issues**: [Report bugs and request features](https://github.com/yourusername/cyber-security-toolkits/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/yourusername/cyber-security-toolkits/discussions)

### Community

- **Security Professionals**: Share experiences and best practices
- **Students**: Learn practical cybersecurity skills
- **Researchers**: Contribute to security tool development

## 🏆 Project Status

### Blue Team Toolkit

- ✅ **100% Complete** - All planned features implemented
- ✅ **Production Ready** - Tested and validated
- ✅ **Comprehensive Documentation** - Complete user and developer guides
- ✅ **Cross-Platform Support** - Windows, Linux, macOS

### Red Team Toolkit

- ✅ **v2.8 Production Ready** - Advanced extensibility features
- ✅ **Plugin System** - Dynamic plugin loading and auto-registration
- ✅ **Comprehensive Testing** - 24 test cases with full coverage
- ✅ **Advanced Reporting** - Multiple format support with visualizations

### Purple Team Toolkit

- ✅ **CLI Production Ready** - Comprehensive attack-defense correlation
- ✅ **15+ CLI Commands** - Full toolkit integration
- ✅ **Rich Terminal UI** - Beautiful, informative output
- ✅ **Safety Features** - Sandbox mode and confirmation prompts
- ✅ **Complete Documentation** - Usage guides and examples

## 🎉 Acknowledgments

- **MITRE ATT&CK** framework for threat hunting techniques
- **Sigma project** for detection rules
- **Open source security community** for inspiration and contributions
- **Contributors and testers** for feedback and improvements

---

**🛡️⚔️🟣 Cyber Security Toolkits** - Empowering security professionals with comprehensive offensive, defensive, and purple team tools.

**Remember**: Always use these tools responsibly, ethically, and with proper authorization. 🎓
