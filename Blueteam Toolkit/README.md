# Blue Team CLI Toolkit 🛡️

A comprehensive Python-based command-line toolkit for defensive security operations, designed to streamline incident response, threat hunting, and security monitoring tasks.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/blueteam-toolkit)

## 🚀 Features

### Core Modules
- **📋 Logs Collection** - Collect and analyze system logs (Windows Event Logs, Linux syslog)
- **🔍 Threat Hunting** - MITRE ATT&CK technique-based hunting + Sigma rule integration
- **🚨 Incident Response** - Live system snapshots with containment capabilities
- **🔎 IOC Scanning** - Indicator of Compromise detection with VirusTotal integration
- **🌐 Network Defense** - Connection analysis, beaconing detection, and IP blocking
- **🧠 Memory Forensics** - Process memory analysis and anomaly detection

### Advanced Features
- **🔗 SIEM Integration** - Connect to ELK, Wazuh, and Splunk for live data
- **🤖 Automation** - Schedule recurring tasks and automated reporting
- **📢 Alerting** - Multi-channel notifications (Slack, Teams, Email)
- **📊 Data Export** - Comprehensive reporting in JSON, CSV, and TXT formats
- **🛡️ Live Response** - Real-time containment (file quarantine, IP blocking, process management)

## 📦 Installation

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/blueteam-toolkit.git
cd blueteam-toolkit

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python main.py --help
```

### System Requirements
- **Python 3.8+**
- **Administrative privileges** (for advanced features)
- **Cross-platform support** (Windows, Linux, macOS)

## 🎯 Quick Examples

### Basic Operations
```bash
# Collect recent system logs
python main.py logs --os windows --lines 100

# Hunt for persistence techniques
python main.py hunt --technique T1053

# Generate incident response snapshot
python main.py ir --quarantine

# Scan for malicious IPs
python main.py ioc --type ip --value 8.8.8.8 --vt

# Analyze network connections
python main.py net --connections --beaconing
```

### Advanced Operations
```bash
# Execute Sigma rules for custom detections
python main.py hunt --sigma sigma_rules/suspicious_process_creation.yml

# Connect to SIEM and fetch alerts
python main.py siem --type elk --host localhost --alerts

# Live response containment
python main.py ir --block-ip 192.168.1.100 --kill-process 12345

# Schedule automated threat hunting
python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "09:00"

# Configure alerting system
python main.py alerts --configure --channel slack
```

## 📚 Module Documentation

### Logs Collection (`logs.py`)
Collect and analyze system logs with filtering and export capabilities.

```bash
python main.py logs --os windows --lines 100 --export logs.json
python main.py logs --os linux --filter "failed login" --export filtered_logs.csv
```

**Features:**
- Windows Event Log collection
- Linux syslog/auth.log parsing
- Keyword filtering
- Suspicious activity detection
- Multiple export formats

### Threat Hunting (`hunt.py`)
Hunt for threats using MITRE ATT&CK techniques and Sigma rules.

```bash
# MITRE ATT&CK hunting
python main.py hunt --technique T1053 --export hunt_results.json

# Sigma rule hunting
python main.py hunt --sigma sigma_rules/ --export sigma_results.json
```

**Supported Techniques:**
- T1053 - Scheduled Task/Job
- T1003 - OS Credential Dumping
- T1055 - Process Injection
- T1071 - Application Layer Protocol
- T1059 - Command and Scripting Interpreter
- T1064 - Scripted Execution
- T1083 - File and Directory Discovery
- T1016 - System Network Configuration Discovery

### Incident Response (`ir.py`)
Generate comprehensive system snapshots with live response capabilities.

```bash
# Basic IR snapshot
python main.py ir --export ir_report.json

# With containment actions
python main.py ir --quarantine --block-ip 192.168.1.100 --kill-process 12345
```

**Capabilities:**
- Process enumeration and analysis
- Network connection mapping
- File system analysis
- User account enumeration
- System information collection
- Live response containment

### IOC Scanning (`ioc.py`)
Scan for indicators of compromise across multiple data sources.

```bash
# IP address scanning
python main.py ioc --type ip --value 8.8.8.8 --vt

# File hash scanning
python main.py ioc --type hash --value "abc123..." --vt

# Domain scanning
python main.py ioc --type domain --value "malicious.com" --vt
```

**Scan Sources:**
- System logs
- DNS cache
- Running processes
- Network connections
- File system
- VirusTotal API integration

### Network Defense (`net.py`)
Analyze and secure network connections.

```bash
# List active connections
python main.py net --connections

# Detect beaconing patterns
python main.py net --beaconing

# Block malicious IPs
python main.py net --block-ip 192.168.1.100
```

**Features:**
- Active connection listing
- Beaconing pattern detection
- DNS cache inspection
- IP blocking (Windows firewall/Linux iptables)

### Memory Forensics (`mem.py`)
Analyze process memory and detect anomalies.

```bash
# Memory information
python main.py mem --info

# Process memory analysis
python main.py mem --list-procs

# Memory anomaly detection
python main.py mem --anomalies
```

**Capabilities:**
- Memory usage statistics
- Process memory mapping
- Memory anomaly detection
- Memory string scanning (Linux)
- Process memory dumping

### SIEM Integration (`siem.py`)
Connect to major SIEM platforms for live data access.

```bash
# ELK Stack integration
python main.py siem --type elk --host localhost --alerts

# Wazuh integration
python main.py siem --type wazuh --host wazuh-server --search "failed login"

# Splunk integration
python main.py siem --type splunk --host splunk-server --query "index=security"
```

**Supported SIEMs:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Wazuh
- Splunk

### Automation (`automation.py`)
Schedule recurring tasks and generate automated reports.

```bash
# Add scheduled task
python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "09:00"

# List scheduled tasks
python main.py automation --list

# Execute task manually
python main.py automation --execute --task-id "daily_hunt"
```

**Features:**
- Task scheduling (daily, weekly, hourly)
- Automated reporting
- System task integration (cron/schtasks)
- Persistent configuration

### Alerting (`alerts.py`)
Configure multi-channel alerting for security events.

```bash
# Configure Slack alerts
python main.py alerts --configure --channel slack

# Configure email alerts
python main.py alerts --configure --channel email

# Test alerting system
python main.py alerts --test --message "Test alert" --severity high
```

**Supported Channels:**
- Slack (webhooks)
- Microsoft Teams (webhooks)
- Email (SMTP)

## 🔧 Configuration

### Configuration Files
The toolkit creates several configuration files:
- `alerts_config.json` - Alerting system configuration
- `automation_config.json` - Scheduled tasks configuration
- `quarantine_log.json` - Quarantined files log

### Environment Variables
```bash
# VirusTotal API key
export VIRUSTOTAL_API_KEY="your_api_key"

# SIEM credentials
export SIEM_USERNAME="your_username"
export SIEM_PASSWORD="your_password"
```

## 📊 Data Export

All modules support comprehensive data export:

```bash
# JSON export
python main.py ir --export ir_report.json

# CSV export
python main.py logs --export logs.csv --export-format csv

# Compressed export
python main.py hunt --export hunt_results.zip --compress
```

**Export Features:**
- Multiple formats (JSON, CSV, TXT)
- Metadata inclusion
- Timestamped filenames
- ZIP compression
- Custom file paths

## 🛡️ Security Features

### Live Response Containment
- **File Quarantine** - Isolate suspicious files
- **IP Blocking** - Temporarily block malicious IPs
- **Process Management** - Kill or suspend suspicious processes
- **Automatic Cleanup** - Remove temporary blocks

### Privilege Management
- Administrative privilege detection
- Safe operation modes
- Error handling for permission issues

### Data Protection
- Secure credential storage
- HTTPS connections
- Local data handling

## 🧪 Testing

### Basic Testing
```bash
# Test all modules
python main.py logs --os windows --lines 5
python main.py hunt --technique T1053
python main.py ir
python main.py ioc --type ip --value 8.8.8.8
python main.py net --connections
python main.py mem --info
```

### Advanced Testing
```bash
# Test SIEM integration
python main.py siem --type elk --host localhost --alerts

# Test automation
python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "14:30"

# Test alerting
python main.py alerts --test --message "Test alert"
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/blueteam-toolkit.git
cd blueteam-toolkit

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## 📈 Roadmap

See [ENHANCEMENT_ROADMAP.md](ENHANCEMENT_ROADMAP.md) for detailed feature roadmap and progress.

**Completed Features:**
- ✅ Enhanced data export functionality
- ✅ Memory forensics module
- ✅ Sigma rule integration
- ✅ SIEM API integration
- ✅ Live response containment
- ✅ Automation scheduling
- ✅ Alerting notifications
- ✅ Python packaging setup

**Upcoming Features:**
- 🔄 Cross-platform expansion
- 🔄 Advanced memory forensics
- 🔄 Machine learning integration
- 🔄 Cloud platform support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MITRE ATT&CK framework for threat hunting techniques
- Sigma project for detection rules
- Open source security community
- Contributors and testers

## 📞 Support

- **Documentation**: [INSTALL.md](INSTALL.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/blueteam-toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/blueteam-toolkit/discussions)

---

**⚠️ Disclaimer**: This toolkit is designed for authorized security testing and incident response. Always ensure you have proper authorization before using these tools in any environment.
