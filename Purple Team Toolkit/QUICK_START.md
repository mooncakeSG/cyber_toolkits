# Purple Team Toolkit - Quick Start Guide

This guide will help you get up and running with the Purple Team Toolkit in minutes.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Network access for installing dependencies
- Administrative privileges (for some features)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd purple_team_toolkit
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install the Package (Optional)

```bash
pip install -e .
```

## Basic Usage

### 1. List Available Scenarios

```bash
python -m purple_team_toolkit list-scenarios
```

This will show you all available predefined attack-defense scenarios.

### 2. Run a Basic Scenario

```bash
python -m purple_team_toolkit run-scenario \
  --scenario configs/scenarios/basic_recon.yaml \
  --sandbox \
  --output reports/
```

This runs a basic reconnaissance scenario in sandbox mode and saves results to the reports directory.

### 3. Generate a Report

```bash
python -m purple_team_toolkit report \
  --format html \
  --output reports/scenario_report.html
```

This generates an HTML report from the latest scenario results.

## Configuration

### 1. Edit Settings

Copy and modify the default settings:

```bash
cp configs/settings.json configs/my_settings.json
# Edit configs/my_settings.json with your preferences
```

### 2. Use Custom Configuration

```bash
python -m purple_team_toolkit run-scenario \
  --scenario configs/scenarios/basic_recon.yaml \
  --config configs/my_settings.json
```

## Sample Scenarios

### Basic Reconnaissance

Tests network discovery and enumeration:
- Nmap port scanning
- DNS enumeration
- WHOIS lookups

### Web Application Attack

Tests web application security:
- Web fuzzing
- Port scanning
- Detection correlation

### Post-Exploitation

Tests lateral movement and persistence:
- Lateral movement simulation
- Persistence mechanisms
- System monitoring

## Understanding Output

### Scenario Results

After running a scenario, you'll get:
- **Red Team Results**: Attack execution details
- **Blue Team Results**: Detection and monitoring data
- **Purple Logic Results**: Correlation analysis and coverage metrics

### Coverage Metrics

- **Detection Coverage**: Percentage of attacks detected
- **Overall Score**: Combined score (0-100)
- **MITRE ATT&CK Mapping**: Technique coverage analysis
- **Recommendations**: Actionable improvement suggestions

## Safety Features

### Sandbox Mode

Always use `--sandbox` flag for testing:
- Isolates testing environment
- Prevents accidental damage
- Safe for production environments

### Rate Limiting

Built-in rate limiting prevents:
- Overwhelming target systems
- Triggering security measures
- Network congestion

### Confirmation Required

For destructive operations:
- Manual approval required
- Clear warnings displayed
- Audit trail maintained

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Run with appropriate privileges
   sudo python -m purple_team_toolkit run-scenario --scenario configs/scenarios/basic_recon.yaml
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Nmap Not Found**
   ```bash
   # Install nmap
   # Ubuntu/Debian
   sudo apt-get install nmap
   
   # CentOS/RHEL
   sudo yum install nmap
   
   # macOS
   brew install nmap
   ```

### Logs

Check logs for detailed information:
```bash
tail -f logs/purple_team.log
```

## Next Steps

1. **Read the Documentation**: See `README.md` for comprehensive documentation
2. **Explore Scenarios**: Try different predefined scenarios
3. **Create Custom Scenarios**: Build your own attack-defense scenarios
4. **Extend Functionality**: Use the plugin system to add custom capabilities
5. **Join the Community**: Contribute and share with other security professionals

## Support

- **Documentation**: See `README.md` and `docs/` directory
- **Issues**: Report bugs and feature requests on GitHub
- **Community**: Join discussions and share experiences

## Security Notice

⚠️ **Important**: This toolkit is designed for authorized security testing only. Always:
- Obtain proper authorization before testing
- Use sandbox mode in production environments
- Follow responsible disclosure practices
- Respect privacy and data protection laws

---

Happy Purple Teaming! 🟣
