# Wireshark DNS Analysis Guide

## Overview

After running the DNS Troubleshooter Toolkit, the captured `.pcap` file will automatically open in Wireshark for analysis. This guide helps you understand what to look for and how to analyze the DNS traffic.

## Automatic Wireshark Integration

The toolkit automatically:
1. **Captures DNS traffic** during the simulation
2. **Opens the .pcap file** in Wireshark
3. **Provides analysis tips** for DNS traffic

## Getting Started with Wireshark Analysis

### 1. **Basic DNS Filter**
When Wireshark opens, use this filter to see only DNS traffic:
```
dns
```

### 2. **Understanding the Timeline**
The capture shows DNS traffic in chronological order:
- **Before DNS Failure**: Normal DNS queries and responses
- **During DNS Failure**: Failed queries, timeouts, retries
- **After DNS Restoration**: Successful queries resume

## Key DNS Traffic Patterns to Look For

### ✅ **Normal DNS Traffic (Before Failure)**
```
Source: Your IP → Destination: DNS Server (8.8.8.8)
Query: google.com
Response: Successful (contains IP addresses)
```

### ❌ **Failed DNS Traffic (During Failure)**
```
Source: Your IP → Destination: Invalid DNS (0.0.0.0)
Query: google.com
Response: Timeout or "Server failed" error
```

### ✅ **Restored DNS Traffic (After Fix)**
```
Source: Your IP → Destination: DNS Server (8.8.8.8)
Query: google.com
Response: Successful (contains IP addresses)
```

## Useful Wireshark Filters

### **DNS-Specific Filters:**
```
dns                    # All DNS traffic
dns.flags.rcode == 0   # Successful DNS responses
dns.flags.rcode != 0   # Failed DNS responses
dns.qry.name contains "google"  # Queries for specific domain
```

### **Time-Based Filters:**
```
frame.time >= "2025-08-14 13:30:00"  # After specific time
frame.time <= "2025-08-14 13:35:00"  # Before specific time
```

### **IP-Based Filters:**
```
ip.addr == 8.8.8.8     # Traffic to/from Google DNS
ip.addr == 0.0.0.0     # Traffic to invalid DNS (should fail)
```

## Analyzing DNS Packets

### **1. DNS Query Packet:**
- **Source**: Your computer's IP
- **Destination**: DNS server IP
- **Query Type**: Usually A (IPv4) or AAAA (IPv6)
- **Domain**: The website being resolved

### **2. DNS Response Packet:**
- **Source**: DNS server IP
- **Destination**: Your computer's IP
- **Response Code**: 
  - `0` = Success (No Error)
  - `2` = Server Failure
  - `3` = Name Error (NXDOMAIN)
  - `5` = Refused

### **3. Failed Query Indicators:**
- **No response packet** (timeout)
- **Response with error code** (server failure, refused)
- **Multiple retry attempts** (client retrying failed queries)

## Step-by-Step Analysis Process

### **Step 1: Overview**
1. Open the `.pcap` file in Wireshark
2. Apply filter: `dns`
3. Look at the timeline to understand the phases

### **Step 2: Before DNS Failure**
1. Look for successful DNS queries
2. Note the response times
3. Identify which DNS servers were working

### **Step 3: During DNS Failure**
1. Look for failed queries
2. Note timeout patterns
3. Observe retry behavior

### **Step 4: After DNS Restoration**
1. Look for successful queries resuming
2. Compare response times
3. Verify DNS server changes

## Advanced Analysis Techniques

### **1. Statistics Analysis:**
- **Statistics → Protocol Hierarchy**: See traffic breakdown
- **Statistics → DNS**: DNS-specific statistics
- **Statistics → Conversations**: IP conversation analysis

### **2. Expert Information:**
- **Analyze → Expert Information**: Shows warnings and errors
- Look for DNS-related expert messages

### **3. IO Graph:**
- **Statistics → IO Graph**: Visualize traffic patterns
- Filter by `dns` to see DNS traffic over time

## Common DNS Issues in Captures

### **1. DNS Timeouts:**
```
Symptoms: No response packets
Cause: DNS server unreachable
Solution: Check DNS server configuration
```

### **2. DNS Server Refused:**
```
Symptoms: Response with RCODE 5
Cause: DNS server rejecting queries
Solution: Check DNS server settings
```

### **3. Name Resolution Failures:**
```
Symptoms: Response with RCODE 3 (NXDOMAIN)
Cause: Domain doesn't exist
Solution: Check domain spelling
```

### **4. Server Failures:**
```
Symptoms: Response with RCODE 2
Cause: DNS server internal error
Solution: Try different DNS server
```

## Educational Value

### **What Students Learn:**
1. **DNS Protocol**: How DNS queries and responses work
2. **Network Troubleshooting**: Identifying DNS issues
3. **Packet Analysis**: Reading and interpreting network traffic
4. **Real-World Scenarios**: Practical DNS problem-solving

### **Key Concepts Demonstrated:**
- **DNS Resolution Process**: Query → Response cycle
- **Failure Modes**: Different types of DNS failures
- **Recovery Process**: How DNS restoration works
- **Network Monitoring**: Using tools to diagnose issues

## Tips for Effective Analysis

### **1. Use Color Coding:**
- Wireshark automatically color-codes packets
- DNS queries and responses have distinct colors
- Failed packets may appear in red

### **2. Follow the Timeline:**
- The capture shows the complete troubleshooting process
- Look for patterns in the timeline
- Note when failures start and stop

### **3. Compare Before/After:**
- Compare successful queries before and after
- Note differences in response times
- Look for changes in DNS servers used

### **4. Export Findings:**
- Use **File → Export → Packet Dissections** to save analysis
- Create reports for documentation
- Share findings with others

## Troubleshooting Wireshark Analysis

### **Common Issues:**

1. **"No DNS traffic found"**
   - Check if the capture file exists
   - Verify the filter syntax
   - Ensure DNS queries were made during capture

2. **"Wireshark won't open"**
   - Install Wireshark if not already installed
   - Check file permissions
   - Try opening manually: `wireshark capture_file.pcap`

3. **"Can't see packet details"**
   - Click on individual packets to see details
   - Expand the DNS section in packet details
   - Use the packet bytes view for raw data

## Conclusion

The automatic Wireshark integration makes it easy to analyze DNS traffic and understand the troubleshooting process. By following this guide, you can gain valuable insights into DNS behavior and learn practical network troubleshooting skills.

Remember: The captured traffic shows a real-world DNS failure scenario, making it an excellent learning tool for network administrators and security professionals.
