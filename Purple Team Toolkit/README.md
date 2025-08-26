# Purple Team Toolkit

A comprehensive Purple Team cybersecurity toolkit that integrates Red Team attack simulations with Blue Team defensive monitoring, providing correlation and detailed reporting capabilities.

## Overview

The Purple Team Toolkit bridges the gap between offensive and defensive security by:
- **Red Team Module**: Executing controlled attack simulations
- **Blue Team Module**: Monitoring and detecting security events
- **Purple Logic**: Correlating attacks with detections and generating coverage reports

## Features

### 🔴 Red Team Capabilities
- **Reconnaissance**: Network scanning, subdomain enumeration, WHOIS lookups
- **Exploitation Testing**: Weak authentication, web application fuzzing
- **Post-Exploitation**: Lateral movement simulation, persistence mechanisms
- **Custom Payloads**: Sandboxed attack vectors for safe testing

### 🔵 Blue Team Capabilities
- **Log Collection**: Windows Event Logs, Syslog, Suricata/Zeek, Wazuh, ELK
- **Event Normalization**: Common schema for cross-platform analysis
- **Detection Engine**: Signature-based and behavioral detection
- **Alerting**: Real-time notifications and gap analysis

### 🟣 Purple Team Logic
- **Attack-Detection Mapping**: Correlate Red Team activities with Blue Team detections
- **Coverage Analysis**: Identify detection gaps and blind spots
- **Scoring System**: Quantitative assessment of defensive posture
- **Visual Reporting**: Interactive dashboards and detailed reports

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd purple_team_toolkit

# Install dependencies
pip install -r requirements.txt

# Configure settings
cp configs/settings.json.example configs/settings.json
# Edit configs/settings.json with your environment settings
```

### Basic Usage

```bash
# List available scenarios
python -m purple_team_toolkit list-scenarios

# Run a scenario with sandbox mode
python -m purple_team_toolkit run-scenario --scenario configs/scenarios/basic_recon.yaml --sandbox

# Generate a report
python -m purple_team_toolkit report --format html --output reports/scenario_report.html
```

## CLI Commands

### `run-scenario`
Execute a full attack and defense scenario.

**Options:**
- `--scenario FILE`: Path to scenario configuration file
- `--sandbox`: Enable sandbox mode for safe testing
- `--verbose`: Enable detailed logging

**Example:**
```bash
python -m purple_team_toolkit run-scenario --scenario configs/scenarios/web_attack.yaml --sandbox --verbose
```

### `report`
Generate scenario detection and coverage reports.

**Options:**
- `--format json|csv|html|pdf`: Output format
- `--output FILE`: Output file path

**Example:**
```bash
python -m purple_team_toolkit report --format html --output reports/coverage_report.html
```

### `list-scenarios`
List all available predefined attack-defense scenarios.

**Example:**
```bash
python -m purple_team_toolkit list-scenarios
```

## Configuration

### Settings (`configs/settings.json`)
```json
{
  "sandbox_mode": true,
  "rate_limiting": true,
  "confirmation_required": true,
  "log_level": "INFO",
  "output_directory": "reports/",
  "plugins_directory": "plugins/"
}
```

### Scenarios (`configs/scenarios/`)
YAML-based scenario definitions:
```yaml
name: "Basic Reconnaissance"
description: "Network discovery and enumeration"
red_team:
  - module: "recon"
    technique: "nmap_scan"
    target: "192.168.1.0/24"
blue_team:
  - module: "network_monitoring"
    detection: "port_scan_detection"
purple_logic:
  correlation_rules:
    - attack: "nmap_scan"
      expected_detection: "port_scan_detection"
```

## Safety Features

- **Sandbox Mode**: Isolated testing environment
- **Rate Limiting**: Prevent overwhelming target systems
- **Confirmation Required**: Manual approval for destructive operations
- **Full Audit Logging**: Complete activity tracking

## Integration

The toolkit integrates with existing Red Team and Blue Team tools:
- **Red Team**: Leverages existing attack frameworks
- **Blue Team**: Connects to SIEM and monitoring solutions
- **MITRE ATT&CK**: Maps activities to framework techniques

## Project Structure

```
purple_team_toolkit/
├── cli/                    # Command-line interface
├── red_team/              # Attack simulation modules
├── blue_team/             # Defensive monitoring modules
├── purple_logic/          # Correlation and analysis
├── configs/               # Configuration files
├── reports/               # Generated reports
├── plugins/               # Extensible plugin system
├── docs/                  # Documentation
└── tests/                 # Test suite
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Web-based dashboard UI
- [ ] Automated scenario scheduling
- [ ] API endpoints for external integration
- [ ] Community ruleset repository
- [ ] Machine learning-based detection enhancement

## Support

For questions and support, please open an issue on the project repository.
