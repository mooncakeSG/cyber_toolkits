# Quick Start Guide 🚀

Get up and running with the Cyber Security Toolkits in minutes!

## 📋 Prerequisites

- **Python 3.8+** (recommended: Python 3.9+)
- **Git** for cloning the repository
- **Administrative privileges** (for advanced features)
- **Cross-platform support** (Windows, Linux, macOS)

## ⚡ Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cyber-security-toolkits.git
cd cyber-security-toolkits
```

### 2. Install Blue Team Toolkit

```bash
cd "Blueteam Toolkit"
pip install -r requirements.txt
```

### 3. Install Red Team Toolkit

```bash
cd "../Red Team Toolkit"
pip install -r requirements.txt
```

## 🎯 Quick Examples

### Blue Team Toolkit - Basic Operations

#### Log Collection
```bash
cd "Blueteam Toolkit"

# Collect recent Windows logs
python main.py logs --os windows --lines 100

# Collect Linux logs with filtering
python main.py logs --os linux --filter "failed login"
```

#### Threat Hunting
```bash
# Hunt for scheduled tasks (MITRE ATT&CK T1053)
python main.py hunt --technique T1053

# Use Sigma rules for custom detections
python main.py hunt --sigma sigma_rules/suspicious_process_creation.yml
```

#### Incident Response
```bash
# Generate system snapshot
python main.py ir --export incident_report.json

# Live containment actions
python main.py ir --quarantine --block-ip 192.168.1.100
```

#### IOC Scanning
```bash
# Scan for malicious IP with VirusTotal
python main.py ioc --type ip --value 8.8.8.8 --vt

# Scan for file hash
python main.py ioc --type hash --value "abc123..." --vt
```

### Red Team Toolkit - Basic Operations

#### Start the Toolkit
```bash
cd "Red Team Toolkit"
python red_team_toolkit.py
```

#### Network Scanning
```
# Select: 1 - Port Scanner
# Enter target: example.com
# Select scan type: 1 (Common ports)
```

#### Web Security Testing
```
# Select: 13 - Web Vulnerability Scanner
# Enter target: https://example.com
```

#### Password Analysis
```
# Select: 6 - Password Tools
# Enter password: test123
```

## 🔧 Configuration

### Blue Team Toolkit Configuration

The Blue Team Toolkit uses environment variables for configuration:

```bash
# VirusTotal API key (optional)
export VIRUSTOTAL_API_KEY="your_api_key"

# SIEM credentials (optional)
export SIEM_USERNAME="your_username"
export SIEM_PASSWORD="your_password"
```

### Red Team Toolkit Configuration

The Red Team Toolkit creates a configuration file automatically:

```bash
# Configuration is created at: toolkit_config.ini
# Access configuration menu from main toolkit
# Select: 19 - Configuration Manager
```

## 🧪 Testing Your Installation

### Blue Team Toolkit Tests

```bash
cd "Blueteam Toolkit"

# Test log collection
python main.py logs --os windows --lines 5

# Test threat hunting
python main.py hunt --technique T1053

# Test incident response
python main.py ir

# Test IOC scanning
python main.py ioc --type ip --value 8.8.8.8
```

### Red Team Toolkit Tests

```bash
cd "Red Team Toolkit"

# Run comprehensive test suite
python test_red_team_toolkit.py

# Run specific test categories
python tests/run_tests.py all
```

## 📚 Next Steps

### Blue Team Toolkit Learning Path

1. **Start with Log Collection**
   ```bash
   python main.py logs --help
   ```

2. **Learn Threat Hunting**
   ```bash
   python main.py hunt --help
   ```

3. **Practice Incident Response**
   ```bash
   python main.py ir --help
   ```

4. **Explore SIEM Integration**
   ```bash
   python main.py siem --help
   ```

### Red Team Toolkit Learning Path

1. **Start with Network Tools**
   ```
   Select: 1 - Port Scanner
   Select: 17 - Network Mapper
   ```

2. **Learn Web Security**
   ```
   Select: 13 - Web Vulnerability Scanner
   Select: 16 - Web Scraper
   ```

3. **Practice Authentication Testing**
   ```
   Select: 15 - SSH Brute Force Tool
   Select: 6 - Password Tools
   ```

4. **Explore Plugin System**
   ```
   Select: 22 - Plugin Management
   ```

## 🛡️ Security Best Practices

### Before Using These Tools

1. **✅ Get Authorization**: Always obtain proper authorization before testing
2. **✅ Use in Lab Environment**: Test in isolated lab environments first
3. **✅ Follow Legal Guidelines**: Comply with applicable laws and regulations
4. **✅ Respect Privacy**: Respect privacy and security policies
5. **✅ Document Activities**: Keep records of all testing activities

### Safety Features

#### Blue Team Toolkit
- **Privilege Management**: Automatic privilege detection
- **Safe Defaults**: Safe operation modes
- **Error Handling**: Graceful error management

#### Red Team Toolkit
- **Sandbox Mode**: Configurable safety controls
- **Rate Limiting**: Built-in protection mechanisms
- **Resource Monitoring**: Real-time system monitoring

## 🆘 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt

# Upgrade pip if needed
python -m pip install --upgrade pip
```

#### Permission Errors
```bash
# Windows: Run as Administrator
# Linux/Mac: Use sudo
sudo python3 main.py
```

#### Network Issues
```bash
# Check firewall settings
# Verify network connectivity
# Ensure target is reachable
```

### Getting Help

- **Documentation**: Check README files in each toolkit
- **Help System**: Use `--help` flag for any command
- **Examples**: See usage examples in documentation
- **Issues**: Report problems on GitHub

## 🎓 Educational Resources

### Blue Team Learning
- **MITRE ATT&CK**: Learn about threat hunting techniques
- **Sigma Rules**: Understand detection rule development
- **Incident Response**: Study IR procedures and best practices
- **SIEM Platforms**: Learn about security monitoring

### Red Team Learning
- **Network Security**: Understand network reconnaissance
- **Web Security**: Learn about web application security
- **Penetration Testing**: Study ethical hacking methodologies
- **Security Tools**: Explore various security testing tools

## 📞 Support

### Documentation
- **[Blue Team Toolkit Documentation](Blueteam%20Toolkit/README.md)**
- **[Red Team Toolkit Documentation](Red%20Team%20Toolkit/README.md)**
- **[Project Summary](PROJECT_SUMMARY.md)**

### Community
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**🚀 You're ready to start!** 

Choose your toolkit and begin exploring the world of cybersecurity tools. Remember to use these tools responsibly and ethically. 🛡️⚔️
