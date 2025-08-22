# Interface Detection in DNS Troubleshooter Toolkit

## Overview

The DNS Troubleshooter Toolkit automatically detects and uses the **primary active network interface** for DNS troubleshooting simulations. This ensures the tool works correctly regardless of whether you're using Ethernet, Wi-Fi, or other connection types.

## Supported Connection Types

### ✅ **Fully Supported:**
- **Wi-Fi (Wireless LAN)**: Primary wireless connection
- **Ethernet**: Wired network connection
- **USB Tethering**: Mobile hotspot connections
- **Virtual Private Network (VPN)**: VPN interfaces

### ⚠️ **Partially Supported:**
- **Bluetooth Tethering**: Limited support (may not work for packet capture)
- **Mobile Broadband**: 4G/5G connections (may have limitations)

### ❌ **Not Supported:**
- **Loopback (127.0.0.1)**: Local-only interface
- **Disabled interfaces**: Inactive network adapters
- **Link-local addresses (169.254.x.x)**: Self-assigned IPs

## How Interface Detection Works

### Windows Detection Logic:

1. **Primary Method**: Analyzes `ipconfig /all` output
   - Looks for interfaces with **real IP addresses** (not link-local)
   - Prioritizes interfaces with active internet connectivity
   - Skips interfaces with `169.254.x.x` addresses (link-local)

2. **Secondary Method**: Uses `netsh interface show interface`
   - Finds enabled interfaces
   - Checks for Ethernet or Wi-Fi adapters

3. **Fallback Method**: Manual interface selection
   - Uses first available adapter
   - Defaults to "Wi-Fi" if nothing else works

### Linux Detection Logic:

1. **Primary Method**: Uses `ip route` to find default gateway interface
   - Identifies the interface used for internet traffic
   - Verifies the interface is UP and has an IP address

2. **Secondary Method**: Scans all network interfaces
   - Looks for any interface with an IP address
   - Skips loopback interface (lo)

3. **Fallback Method**: Uses default interface
   - Defaults to "eth0" if nothing else works

## Interface Priority Order

### Windows:
1. **Wi-Fi** (if active with real IP)
2. **Ethernet** (if active with real IP)
3. **Other active interfaces** (USB tethering, VPN, etc.)
4. **Fallback to Wi-Fi**

### Linux:
1. **Default route interface** (usually eth0, wlan0, or similar)
2. **Any active interface** with IP address
3. **Fallback to eth0**

## Real-World Examples

### Example 1: Wi-Fi Connection
```
System has multiple interfaces:
- Wi-Fi: 192.168.1.100 (Active - real IP)
- Ethernet: 169.254.1.1 (Link-local - not connected)
- Bluetooth: 169.254.2.1 (Link-local - not connected)

Tool selects: Wi-Fi (because it has a real IP)
```

### Example 2: Ethernet Connection
```
System has multiple interfaces:
- Ethernet: 10.0.0.50 (Active - real IP)
- Wi-Fi: 169.254.1.1 (Link-local - not connected)

Tool selects: Ethernet (because it has a real IP)
```

### Example 3: USB Tethering
```
System has multiple interfaces:
- USB Ethernet: 192.168.42.100 (Active - mobile hotspot)
- Wi-Fi: 169.254.1.1 (Link-local - not connected)

Tool selects: USB Ethernet (because it has a real IP)
```

## Troubleshooting Interface Detection

### Common Issues:

1. **"No active interface found"**
   - **Cause**: No interface has a real IP address
   - **Solution**: Check network connectivity, ensure DHCP is working

2. **"Interface not found"**
   - **Cause**: Network adapter disabled or driver issues
   - **Solution**: Enable network adapter in Device Manager

3. **"Wrong interface selected"**
   - **Cause**: Multiple active interfaces
   - **Solution**: The tool automatically selects the primary one

### Manual Override:

If the tool selects the wrong interface, you can modify the script:

```python
# In detect_interface() function, add your preferred interface:
def detect_interface():
    # Force specific interface
    return "Your-Interface-Name"
```

## Technical Details

### Windows Commands Used:
- `ipconfig /all` - Detailed interface information
- `netsh interface show interface` - Interface status
- `route print` - Routing table

### Linux Commands Used:
- `ip route` - Routing table
- `ip addr show` - Interface addresses
- `ip link show` - Interface status

### Detection Criteria:
- **Interface Status**: Must be UP/enabled
- **IP Address**: Must have a real IP (not link-local)
- **Connectivity**: Should have internet access
- **DNS Capability**: Must support DNS queries

## Best Practices

1. **Ensure Network Connectivity**: Make sure you have internet access before running the tool
2. **Use Primary Connection**: Connect via your main network (Wi-Fi or Ethernet)
3. **Disable Unused Adapters**: Turn off unused network adapters to avoid confusion
4. **Check Firewall**: Ensure firewall allows DNS traffic (port 53)
5. **Run as Administrator**: Required for DNS changes on Windows

## Educational Value

Understanding interface detection helps students learn:
- **Network Interface Management**: How systems handle multiple network adapters
- **IP Address Assignment**: Difference between real IPs and link-local addresses
- **Routing**: How systems choose which interface to use for internet traffic
- **Troubleshooting**: How to identify and fix network interface issues
