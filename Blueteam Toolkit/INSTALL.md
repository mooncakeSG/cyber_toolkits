# Blue Team CLI Toolkit - Installation Guide

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Administrative privileges (for some features)
- Internet connection (for SIEM integration and VirusTotal)

### Installation Options

#### Option 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/blueteam-toolkit.git
cd blueteam-toolkit

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python main.py --help
```

#### Option 2: Pip Installation (Future)

```bash
# Install from PyPI (when available)
pip install blueteam-toolkit

# Run the toolkit
blueteam --help
# or
btk --help
```

#### Option 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/blueteam-toolkit.git
cd blueteam-toolkit

# Install in development mode
pip install -e .

# Run the toolkit
python main.py --help
```

## System Requirements

### Windows
- Windows 10/11 or Windows Server 2016+
- PowerShell 5.0+
- Administrative privileges for:
  - Windows Event Log access
  - Firewall management
  - Process management
  - File quarantine

### Linux
- Ubuntu 18.04+, CentOS 7+, or similar
- Python 3.8+
- Administrative privileges for:
  - System log access
  - iptables management
  - Process management
  - File quarantine

### macOS
- macOS 10.15+ (Catalina)
- Python 3.8+
- Administrative privileges for:
  - System log access
  - Process management
  - File quarantine

## Dependencies

### Core Dependencies
- `psutil>=5.9.0` - System and process utilities
- `requests>=2.28.0` - HTTP library for API calls
- `PyYAML>=6.0` - YAML parsing for Sigma rules
- `schedule>=1.2.0` - Task scheduling

### Optional Dependencies
- VirusTotal API key (for IOC enrichment)
- SIEM credentials (for ELK, Wazuh, Splunk integration)
- Slack/Teams webhook URLs (for notifications)
- SMTP credentials (for email alerts)

## Configuration

### Initial Setup

1. **Basic Configuration**
   ```bash
   # Test basic functionality
   python main.py logs --os windows --lines 10
   python main.py hunt --technique T1053
   python main.py ir
   ```

2. **SIEM Integration** (Optional)
   ```bash
   # Configure SIEM connection
   python main.py siem --type elk --host your-elk-server --alerts
   ```

3. **Alerting Setup** (Optional)
   ```bash
   # Configure Slack notifications
   python main.py alerts --configure --channel slack
   
   # Configure email alerts
   python main.py alerts --configure --channel email
   ```

4. **Automation Setup** (Optional)
   ```bash
   # Add scheduled tasks
   python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "14:30"
   ```

### Configuration Files

The toolkit creates several configuration files:

- `alerts_config.json` - Alerting configuration
- `automation_config.json` - Scheduled tasks
- `quarantine_log.json` - Quarantined files log

## Usage Examples

### Basic Operations

```bash
# Collect system logs
python main.py logs --os windows --lines 100 --export logs.json

# Run threat hunting
python main.py hunt --technique T1053 --export hunt_results.json

# Generate incident response snapshot
python main.py ir --quarantine --export ir_report.json

# Scan for IOCs
python main.py ioc --type ip --value 8.8.8.8 --vt --export ioc_results.json

# Network analysis
python main.py net --connections --beaconing --export network_analysis.json

# Memory forensics
python main.py mem --info --list-procs --export memory_analysis.json
```

### Advanced Operations

```bash
# Sigma rule hunting
python main.py hunt --sigma sigma_rules/suspicious_process_creation.yml

# SIEM integration
python main.py siem --type elk --host localhost --alerts --export siem_alerts.json

# Live response containment
python main.py ir --block-ip 192.168.1.100 --kill-process 12345

# Automated scheduling
python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "09:00"

# Alert testing
python main.py alerts --test --message "Test alert" --severity high
```

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**
   ```bash
   # Run as administrator (Windows)
   # Run with sudo (Linux/macOS)
   sudo python main.py ir --quarantine
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --upgrade
   ```

3. **SIEM Connection Issues**
   ```bash
   # Check network connectivity
   # Verify credentials
   # Test with curl or browser
   ```

4. **Alert Configuration Issues**
   ```bash
   # Check configuration
   python main.py alerts --config
   
   # Test alerts
   python main.py alerts --test
   ```

### Log Files

The toolkit creates log files in the current directory:
- `quarantine_log.json` - Quarantined files
- `automated_reports/` - Automated task reports
- Various export files (JSON, CSV, TXT)

### Getting Help

```bash
# General help
python main.py --help

# Module-specific help
python main.py logs --help
python main.py hunt --help
python main.py ir --help
python main.py ioc --help
python main.py net --help
python main.py mem --help
python main.py siem --help
python main.py automation --help
python main.py alerts --help
```

## Security Considerations

### Privilege Requirements

- **Administrative privileges** are required for:
  - Windows Event Log access
  - Firewall management
  - Process termination
  - File quarantine operations

### Data Handling

- **Sensitive data** may be collected during operations
- **Export files** may contain system information
- **Quarantined files** are stored locally
- **Configuration files** may contain credentials

### Network Security

- **SIEM connections** use HTTPS
- **VirusTotal API** uses HTTPS
- **Webhook URLs** should be kept secure
- **SMTP credentials** are stored in configuration

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the enhancement roadmap
3. Create an issue on GitHub
4. Check the documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
