# DNS Troubleshooting Toolkit - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. **Choose Your Platform**

#### For Linux (Interactive - Recommended):
```bash
# Test your system first
python3 test_toolkit.py

# Run the interactive toolkit (automatically installs dependencies)
sudo python3 dns_resolve_interactive.py
```

#### For Windows (Interactive - Recommended):
```cmd
# Test your system first
python test_toolkit.py

# Run the interactive toolkit (guides through Wireshark installation)
python dns_resolve_interactive_windows.py
```

#### For Linux (Standard):
```bash
# Test your system first
python3 test_toolkit.py

# Run the toolkit (requires sudo)
sudo python3 dns_resolve.py
```

#### For Windows (Standard):
```cmd
# Test your system first
python test_toolkit.py

# Run as Administrator
python dns_resolve_windows.py
```

### 2. **What You'll See**

#### Interactive Version:
The toolkit will guide you through:
- 🔍 **Automatic dependency check and installation**
- 🌐 **Network interface selection**
- ⚙️ **Interactive configuration setup**
- 📊 **Network information display**
- 🔍 **Wireshark packet capture setup**
- ❌ **DNS failure simulation**
- 🧪 **Failed DNS resolution testing**
- 🔧 **DNS functionality restoration**
- ✅ **DNS recovery verification**
- 📊 **Capture file analysis tips**

#### Standard Version:
The toolkit will automatically:
- ✅ Display your network configuration
- 🔍 Start Wireshark packet capture
- ❌ Simulate DNS failure
- 🧪 Test failed DNS resolution
- 🔧 Restore DNS functionality
- ✅ Verify DNS recovery
- 📊 Save capture file for analysis

### 3. **Presentation Tips**

#### Before Your Demo:
1. **Test the toolkit** in your environment
2. **Have Wireshark ready** for analysis
3. **Prepare your audience** for the demonstration
4. **Backup your DNS settings** (just in case)

#### During Your Demo:
1. **Explain each step** as it happens
2. **Point out the color coding**:
   - 🟢 Green = Success
   - 🟡 Yellow = Warning
   - 🔴 Red = Error
   - 🔵 Blue = Information
3. **Show the real-time output**
4. **Demonstrate the packet capture**

#### After Your Demo:
1. **Open the capture file** in Wireshark
2. **Show DNS queries** and responses
3. **Explain the troubleshooting process**
4. **Discuss real-world applications**

## 📋 Prerequisites

### Linux Requirements:
- Python 3.6+
- Wireshark CLI tools (`tshark`)
- systemd-resolved
- DNS utilities (`dig`, `nslookup`)
- Root privileges

### Windows Requirements:
- Python 3.6+
- Wireshark (for packet capture)
- Administrator privileges
- PowerShell execution enabled

## 🔧 Installation

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip wireshark-cli systemd-resolved dnsutils iputils-ping
```

### Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Download Wireshark from [wireshark.org](https://www.wireshark.org/download.html)
3. Run PowerShell as Administrator and execute:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
   ```

## 🎯 Demo Scenarios

### Basic DNS Troubleshooting:
- Shows DNS failure simulation
- Demonstrates recovery process
- Provides packet capture for analysis

### Advanced Analysis:
- Use Wireshark filters: `dns`
- Look for failed queries: `dns.flags.rcode != 0`
- Analyze timing and retry patterns

### Custom Scenarios:
- Modify DNS servers in the script
- Add custom domain tests
- Create specific failure scenarios

## 🔍 Analysis Guide

### Wireshark Filters:
```
# All DNS traffic
dns

# Failed DNS queries
dns.flags.rcode != 0

# Specific DNS server
ip.addr == 123.123.123.123

# DNS query types
dns.qry.type == 1  # A records
dns.qry.type == 28 # AAAA records
```

### What to Look For:
1. **Failed DNS queries** (NXDOMAIN responses)
2. **DNS server timeouts**
3. **Retry attempts** and intervals
4. **Query patterns** before/after failure
5. **Response times** and performance impact

## ⚠️ Safety Notes

### Safe Usage:
- ✅ Only use on authorized networks
- ✅ Test in isolated environments first
- ✅ Backup network settings before running
- ✅ Restore original settings after demonstration

### Network Impact:
- ⏱️ Minimal disruption (short duration)
- 🔄 Automatic restoration of DNS settings
- 🎯 Controlled failure simulation
- 📊 Real-time monitoring and capture

## 🆘 Troubleshooting

### Common Issues:

#### Linux:
- **Permission denied**: Run with `sudo`
- **tshark not found**: Install `wireshark-cli`
- **resolvectl not found**: Install `systemd-resolved`

#### Windows:
- **Access denied**: Run as Administrator
- **tshark not found**: Install Wireshark
- **PowerShell errors**: Check execution policy

### Error Recovery:
- The toolkit includes automatic error handling
- Failed steps are logged with clear messages
- The script continues even if some components fail
- Capture files are preserved even on errors

## 📞 Support

### Quick Help:
1. **Run the test script**: `python test_toolkit.py`
2. **Check the README**: `README.md`
3. **Verify prerequisites**: See installation section
4. **Test in isolation**: Use a test environment first

### Getting Help:
- Check the comprehensive README.md
- Review the test script output
- Ensure all prerequisites are met
- Test with administrator/root privileges

---

**Ready to demonstrate DNS troubleshooting? Let's go! 🚀**
