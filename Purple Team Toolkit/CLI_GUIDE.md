# Purple Team Toolkit - CLI Usage Guide

## 🚀 Quick Start

### Basic Usage
```bash
# Run the CLI
python purple_cli.py --help

# Check toolkit status
python purple_cli.py status

# List available scenarios
python purple_cli.py list-scenarios
```

## 📋 Available Commands

### Main Commands

#### `run-scenario` - Execute Full Attack-Defense Scenarios
```bash
# Basic scenario execution
python purple_cli.py run-scenario -s configs/scenarios/basic_recon.yaml

# With sandbox mode for safe testing
python purple_cli.py run-scenario -s configs/scenarios/web_attack.yaml --sandbox

# With custom output directory
python purple_cli.py run-scenario -s configs/scenarios/post_exploitation.yaml -o results/

# With timeout and parallel execution
python purple_cli.py run-scenario -s configs/scenarios/basic_recon.yaml --timeout 1800 --parallel
```

**Options:**
- `-s, --scenario`: Path to scenario configuration file (required)
- `--sandbox`: Enable sandbox mode for safe testing
- `-o, --output`: Output directory for results
- `--timeout`: Scenario timeout in seconds (default: 3600)
- `--parallel`: Execute attacks in parallel

#### `report` - Generate Reports
```bash
# Generate HTML report
python purple_cli.py report -f html -o reports/scenario_report.html

# Generate JSON report
python purple_cli.py report -f json -o reports/scenario_report.json

# Generate PDF report
python purple_cli.py report -f pdf -o reports/scenario_report.pdf

# Use custom template
python purple_cli.py report -f html -o reports/custom_report.html --template templates/custom.html
```

**Options:**
- `-f, --format`: Output format (json, csv, html, pdf)
- `-o, --output`: Output file path (required)
- `--scenario-results`: Path to scenario results file
- `--template`: Custom report template

#### `list-scenarios` - List Available Scenarios
```bash
python purple_cli.py list-scenarios
```

#### `status` - Check Toolkit Status
```bash
python purple_cli.py status
```

#### `analyze` - Coverage Analysis
```bash
# Analyze specific techniques
python purple_cli.py analyze -t 192.168.1.100 --techniques T1046 T1071

# Analyze with output file
python purple_cli.py analyze -t example.com --techniques T1046 -o analysis_results.json
```

**Options:**
- `-t, --target`: Target to analyze (required)
- `--techniques`: MITRE ATT&CK techniques to test (multiple)
- `-o, --output`: Output file for analysis

### Red Team Commands

#### `red-team recon` - Reconnaissance Operations
```bash
# Basic reconnaissance
python purple_cli.py red-team recon -t example.com

# Full reconnaissance scan
python purple_cli.py red-team recon -t 192.168.1.0/24 --scan-type full

# Stealth reconnaissance
python purple_cli.py red-team recon -t example.com --scan-type stealth -o recon_results.json
```

**Options:**
- `-t, --target`: Target IP/domain (required)
- `--scan-type`: Scan type (basic, full, stealth)
- `-o, --output`: Output file for results

#### `red-team exploit` - Exploitation Operations
```bash
# Web exploitation
python purple_cli.py red-team exploit -t http://example.com --exploit-type web

# Network exploitation
python purple_cli.py red-team exploit -t 192.168.1.100 --exploit-type network

# Social engineering with custom payload
python purple_cli.py red-team exploit -t target@example.com --exploit-type social -p custom_payload.txt
```

**Options:**
- `-t, --target`: Target URL/IP (required)
- `--exploit-type`: Exploitation type (web, network, social)
- `-p, --payload`: Custom payload

### Blue Team Commands

#### `blue-team monitor` - Security Monitoring
```bash
# Basic monitoring (5 minutes)
python purple_cli.py blue-team monitor

# Monitor specific sources
python purple_cli.py blue-team monitor -s system_logs -s network_logs

# Extended monitoring with output
python purple_cli.py blue-team monitor -d 1800 -o alerts.json
```

**Options:**
- `-s, --source`: Log sources to monitor (multiple)
- `-d, --duration`: Monitoring duration in seconds (default: 300)
- `-o, --output`: Output file for alerts

#### `blue-team hunt` - Threat Hunting
```bash
# Basic threat hunt
python purple_cli.py blue-team hunt -q "process.name == 'cmd.exe'"

# Extended timeframe hunt
python purple_cli.py blue-team hunt -q "network.connection.remote_ip == '192.168.1.100'" -t 7d
```

**Options:**
- `-q, --query`: Threat hunting query (required)
- `-t, --timeframe`: Timeframe for hunting (default: 24h)

## 🔧 Configuration

### Global Options
```bash
# Enable verbose output
python purple_cli.py --verbose run-scenario -s scenario.yaml

# Use custom configuration file
python purple_cli.py --config custom_config.json status

# Set log level
python purple_cli.py --log-level DEBUG run-scenario -s scenario.yaml
```

**Global Options:**
- `-v, --verbose`: Enable verbose output
- `-c, --config`: Configuration file path
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## 📊 Example Workflows

### 1. Basic Purple Team Assessment
```bash
# 1. Check toolkit status
python purple_cli.py status

# 2. List available scenarios
python purple_cli.py list-scenarios

# 3. Run a basic reconnaissance scenario
python purple_cli.py run-scenario -s configs/scenarios/basic_recon.yaml --sandbox

# 4. Generate a report
python purple_cli.py report -f html -o reports/basic_assessment.html
```

### 2. Advanced Red Team Operations
```bash
# 1. Perform reconnaissance
python purple_cli.py red-team recon -t target.com --scan-type full -o recon.json

# 2. Execute exploitation
python purple_cli.py red-team exploit -t http://target.com --exploit-type web

# 3. Analyze coverage
python purple_cli.py analyze -t target.com --techniques T1046 T1071 T1059
```

### 3. Blue Team Monitoring and Hunting
```bash
# 1. Start monitoring
python purple_cli.py blue-team monitor -d 3600 -o monitoring_alerts.json

# 2. Perform threat hunting
python purple_cli.py blue-team hunt -q "process.name == 'powershell.exe' AND process.args CONTAINS 'Invoke-Expression'"

# 3. Generate security report
python purple_cli.py report -f pdf -o reports/security_assessment.pdf
```

## 🛡️ Safety Features

### Sandbox Mode
Always use sandbox mode for testing:
```bash
python purple_cli.py run-scenario -s scenario.yaml --sandbox
```

### Confirmation Prompts
Destructive operations will prompt for confirmation:
```bash
python purple_cli.py red-team exploit -t target.com
# Will prompt: "Are you sure you want to execute exploitation on target.com? [y/N]"
```

### Rate Limiting
Operations are automatically rate-limited to prevent overwhelming targets.

## 📁 Output Structure

### Scenario Results
```
results/
├── scenario_results.json          # Raw scenario results
├── attack_logs/                   # Detailed attack logs
├── detection_logs/                # Detection event logs
└── correlation_data/              # Attack-defense correlation data
```

### Reports
```
reports/
├── scenario_report.html           # HTML report
├── scenario_report.pdf            # PDF report
├── coverage_analysis.json         # Coverage analysis results
└── threat_hunt_results.json       # Threat hunting results
```

## 🔍 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Run with appropriate permissions
   sudo python purple_cli.py run-scenario -s scenario.yaml
   ```

2. **Configuration Not Found**
   ```bash
   # Specify custom config
   python purple_cli.py --config /path/to/config.json status
   ```

3. **Dependencies Missing**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   ```

### Debug Mode
```bash
# Enable debug output
python purple_cli.py --log-level DEBUG --verbose run-scenario -s scenario.yaml
```

## 📚 Advanced Usage

### Custom Scenarios
Create custom scenario files in YAML format:
```yaml
name: "Custom Attack Scenario"
description: "Custom attack and defense scenario"
difficulty: "Hard"
targets:
  - "192.168.1.0/24"
red_team:
  attacks:
    - technique: "T1046"
      module: "reconnaissance"
      target: "192.168.1.1"
blue_team:
  monitoring:
    - module: "network_monitoring"
      detection: "port_scan_detection"
      sources: ["network_logs"]
```

### Batch Operations
```bash
# Run multiple scenarios
for scenario in configs/scenarios/*.yaml; do
    python purple_cli.py run-scenario -s "$scenario" --sandbox
done
```

### Integration with CI/CD
```bash
# Automated testing
python purple_cli.py run-scenario -s test_scenario.yaml --sandbox
python purple_cli.py report -f json -o test_results.json
```

## 🎯 Best Practices

1. **Always use sandbox mode for testing**
2. **Review scenarios before execution**
3. **Monitor system resources during operations**
4. **Keep detailed logs of all operations**
5. **Regularly update toolkit and dependencies**
6. **Follow responsible disclosure practices**
7. **Obtain proper authorization before testing**

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review logs with `--log-level DEBUG`
- Ensure all dependencies are installed
- Verify configuration file format

---

**🛡️ Purple Team Toolkit - Secure. Unified. Powerful.**
