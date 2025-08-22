"""
Network defense utilities for the Blue Team CLI Toolkit.
Lists active connections, detects beaconing patterns, and provides blocking functionality.
"""

import os
import sys
import platform
import subprocess
import psutil
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import utils


def get_active_connections() -> List[Dict]:
    """Get all active network connections."""
    connections = []
    
    try:
        for conn in psutil.net_connections():
            try:
                conn_info = {
                    'fd': conn.fd,
                    'family': str(conn.family),
                    'type': str(conn.type),
                    'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    'status': conn.status,
                    'pid': conn.pid,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Get process information
                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        conn_info['process_name'] = proc.name()
                        conn_info['process_exe'] = proc.exe()
                        conn_info['process_cmdline'] = ' '.join(proc.cmdline())
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        conn_info['process_name'] = 'Unknown'
                        conn_info['process_exe'] = 'Unknown'
                        conn_info['process_cmdline'] = 'Unknown'
                else:
                    conn_info['process_name'] = 'Unknown'
                    conn_info['process_exe'] = 'Unknown'
                    conn_info['process_cmdline'] = 'Unknown'
                
                connections.append(conn_info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except Exception as e:
        utils.print_error(f"Error getting active connections: {e}")
    
    return connections


def get_dns_cache() -> List[Dict]:
    """Get DNS cache entries."""
    dns_entries = []
    
    try:
        if platform.system() == "Windows":
            # Windows DNS cache
            try:
                result = subprocess.run(
                    ["ipconfig", "/displaydns"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    current_entry = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('Record Name'):
                            if current_entry:
                                dns_entries.append(current_entry)
                            current_entry = {'record_name': line.split(':', 1)[1].strip()}
                        elif line.startswith('Record Type'):
                            current_entry['record_type'] = line.split(':', 1)[1].strip()
                        elif line.startswith('Time To Live'):
                            current_entry['ttl'] = line.split(':', 1)[1].strip()
                        elif line.startswith('Data Length'):
                            current_entry['data_length'] = line.split(':', 1)[1].strip()
                        elif line.startswith('Section'):
                            current_entry['section'] = line.split(':', 1)[1].strip()
                        elif line.startswith('A (Host) Record'):
                            current_entry['a_record'] = line.split(':', 1)[1].strip()
                        elif line.startswith('CNAME Record'):
                            current_entry['cname_record'] = line.split(':', 1)[1].strip()
                    
                    if current_entry:
                        dns_entries.append(current_entry)
                        
            except Exception as e:
                utils.print_warning(f"Error getting Windows DNS cache: {e}")
                
        else:
            # Linux DNS cache
            try:
                # Try systemd-resolved
                result = subprocess.run(
                    ["systemd-resolve", "--statistics"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    dns_entries.append({
                        'source': 'systemd-resolved',
                        'statistics': result.stdout
                    })
                    
                # Try nscd cache
                try:
                    result = subprocess.run(
                        ["nscd", "-g"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        dns_entries.append({
                            'source': 'nscd',
                            'cache_info': result.stdout
                        })
                except FileNotFoundError:
                    pass
                    
            except Exception as e:
                utils.print_warning(f"Error getting Linux DNS cache: {e}")
                
    except Exception as e:
        utils.print_error(f"Error getting DNS cache: {e}")
    
    return dns_entries


def detect_beaconing_patterns(connections: List[Dict], interval: int = 60) -> List[Dict]:
    """Detect potential beaconing patterns in network connections."""
    beaconing_patterns = []
    
    try:
        # Group connections by remote address
        remote_connections = {}
        for conn in connections:
            if conn.get('raddr') and conn.get('status') == 'ESTABLISHED':
                remote_ip = conn['raddr'].split(':')[0]
                if remote_ip not in remote_connections:
                    remote_connections[remote_ip] = []
                remote_connections[remote_ip].append(conn)
        
        # Analyze each remote IP for beaconing patterns
        for remote_ip, conns in remote_connections.items():
            if len(conns) > 1:
                # Check for regular intervals
                timestamps = [datetime.fromisoformat(conn['timestamp'].replace('Z', '+00:00')) for conn in conns]
                timestamps.sort()
                
                intervals = []
                for i in range(1, len(timestamps)):
                    interval_seconds = (timestamps[i] - timestamps[i-1]).total_seconds()
                    intervals.append(interval_seconds)
                
                # Check for consistent intervals (within 10% variance)
                if len(intervals) >= 2:
                    avg_interval = sum(intervals) / len(intervals)
                    variance = sum(abs(interval - avg_interval) for interval in intervals) / len(intervals)
                    
                    if variance < avg_interval * 0.1:  # Less than 10% variance
                        beaconing_patterns.append({
                            'remote_ip': remote_ip,
                            'connection_count': len(conns),
                            'avg_interval_seconds': round(avg_interval, 2),
                            'variance': round(variance, 2),
                            'pattern_type': 'Regular Intervals',
                            'connections': conns,
                            'severity': 'high' if avg_interval < 300 else 'medium'  # High if < 5 minutes
                        })
                
                # Check for suspicious process names
                suspicious_processes = [conn for conn in conns if utils.is_suspicious_process(conn.get('process_name', ''))]
                if suspicious_processes:
                    beaconing_patterns.append({
                        'remote_ip': remote_ip,
                        'connection_count': len(conns),
                        'suspicious_processes': len(suspicious_processes),
                        'pattern_type': 'Suspicious Processes',
                        'connections': suspicious_processes,
                        'severity': 'high'
                    })
                
                # Check for non-standard ports
                non_standard_ports = []
                for conn in conns:
                    try:
                        port = int(conn['raddr'].split(':')[1])
                        if port not in [80, 443, 22, 21, 25, 53, 110, 143, 993, 995]:  # Common ports
                            non_standard_ports.append(conn)
                    except (ValueError, IndexError):
                        pass
                
                if non_standard_ports:
                    beaconing_patterns.append({
                        'remote_ip': remote_ip,
                        'connection_count': len(conns),
                        'non_standard_ports': len(non_standard_ports),
                        'pattern_type': 'Non-Standard Ports',
                        'connections': non_standard_ports,
                        'severity': 'medium'
                    })
                    
    except Exception as e:
        utils.print_error(f"Error detecting beaconing patterns: {e}")
    
    return beaconing_patterns


def block_ip_address(ip_address: str) -> bool:
    """Block an IP address using firewall rules."""
    if not utils.is_admin():
        utils.print_error("Administrative privileges required to block IP addresses")
        return False
    
    try:
        if platform.system() == "Windows":
            # Windows firewall rule
            rule_name = f"BlockIP_{ip_address.replace('.', '_')}"
            
            # Create inbound rule
            inbound_cmd = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_Inbound",
                "dir=in",
                "action=block",
                f"remoteip={ip_address}"
            ]
            
            result = subprocess.run(inbound_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                utils.print_error(f"Failed to create inbound rule: {result.stderr}")
                return False
            
            # Create outbound rule
            outbound_cmd = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}_Outbound",
                "dir=out",
                "action=block",
                f"remoteip={ip_address}"
            ]
            
            result = subprocess.run(outbound_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                utils.print_error(f"Failed to create outbound rule: {result.stderr}")
                return False
            
            utils.print_success(f"Successfully blocked IP address {ip_address}")
            return True
            
        else:
            # Linux iptables rule
            # Block incoming traffic
            inbound_cmd = f"iptables -A INPUT -s {ip_address} -j DROP"
            result = subprocess.run(inbound_cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                utils.print_error(f"Failed to create inbound rule: {result.stderr}")
                return False
            
            # Block outgoing traffic
            outbound_cmd = f"iptables -A OUTPUT -d {ip_address} -j DROP"
            result = subprocess.run(outbound_cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                utils.print_error(f"Failed to create outbound rule: {result.stderr}")
                return False
            
            utils.print_success(f"Successfully blocked IP address {ip_address}")
            return True
            
    except Exception as e:
        utils.print_error(f"Error blocking IP address {ip_address}: {e}")
        return False


def unblock_ip_address(ip_address: str) -> bool:
    """Unblock an IP address by removing firewall rules."""
    if not utils.is_admin():
        utils.print_error("Administrative privileges required to unblock IP addresses")
        return False
    
    try:
        if platform.system() == "Windows":
            # Remove Windows firewall rules
            rule_name = f"BlockIP_{ip_address.replace('.', '_')}"
            
            # Remove inbound rule
            inbound_cmd = [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name={rule_name}_Inbound"
            ]
            
            subprocess.run(inbound_cmd, capture_output=True, text=True, timeout=30)
            
            # Remove outbound rule
            outbound_cmd = [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name={rule_name}_Outbound"
            ]
            
            subprocess.run(outbound_cmd, capture_output=True, text=True, timeout=30)
            
            utils.print_success(f"Successfully unblocked IP address {ip_address}")
            return True
            
        else:
            # Remove Linux iptables rules
            # Remove incoming traffic rule
            inbound_cmd = f"iptables -D INPUT -s {ip_address} -j DROP"
            subprocess.run(inbound_cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            # Remove outgoing traffic rule
            outbound_cmd = f"iptables -D OUTPUT -d {ip_address} -j DROP"
            subprocess.run(outbound_cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            utils.print_success(f"Successfully unblocked IP address {ip_address}")
            return True
            
    except Exception as e:
        utils.print_error(f"Error unblocking IP address {ip_address}: {e}")
        return False


def display_network_connections(connections: List[Dict]):
    """Display network connections in a formatted way."""
    if not connections:
        utils.print_warning("No network connections found")
        return
    
    utils.print_section("Active Network Connections")
    
    # Group by status
    established = [c for c in connections if c.get('status') == 'ESTABLISHED']
    listening = [c for c in connections if c.get('status') == 'LISTEN']
    other = [c for c in connections if c.get('status') not in ['ESTABLISHED', 'LISTEN']]
    
    if established:
        print(f"\nEstablished Connections ({len(established)}):")
        for i, conn in enumerate(established[:20], 1):  # Show first 20
            print(f"\n{i}. Local: {conn.get('laddr', 'Unknown')}")
            print(f"   Remote: {conn.get('raddr', 'Unknown')}")
            print(f"   Process: {conn.get('process_name', 'Unknown')} (PID: {conn.get('pid', 'Unknown')})")
            print(f"   Type: {conn.get('family', 'Unknown')}")
    
    if listening:
        print(f"\nListening Ports ({len(listening)}):")
        for i, conn in enumerate(listening[:10], 1):  # Show first 10
            print(f"\n{i}. Address: {conn.get('laddr', 'Unknown')}")
            print(f"   Process: {conn.get('process_name', 'Unknown')} (PID: {conn.get('pid', 'Unknown')})")
            print(f"   Type: {conn.get('family', 'Unknown')}")
    
    if other:
        print(f"\nOther Connections ({len(other)}):")
        for i, conn in enumerate(other[:10], 1):  # Show first 10
            print(f"\n{i}. Local: {conn.get('laddr', 'Unknown')}")
            print(f"   Remote: {conn.get('raddr', 'Unknown')}")
            print(f"   Status: {conn.get('status', 'Unknown')}")
            print(f"   Process: {conn.get('process_name', 'Unknown')} (PID: {conn.get('pid', 'Unknown')})")


def display_dns_cache(dns_entries: List[Dict]):
    """Display DNS cache entries."""
    if not dns_entries:
        utils.print_warning("No DNS cache entries found")
        return
    
    utils.print_section("DNS Cache Entries")
    
    for i, entry in enumerate(dns_entries[:20], 1):  # Show first 20
        print(f"\n{i}. Record Name: {entry.get('record_name', 'Unknown')}")
        print(f"   Record Type: {entry.get('record_type', 'Unknown')}")
        print(f"   TTL: {entry.get('ttl', 'Unknown')}")
        if entry.get('a_record'):
            print(f"   A Record: {entry['a_record']}")
        if entry.get('cname_record'):
            print(f"   CNAME Record: {entry['cname_record']}")


def display_beaconing_patterns(patterns: List[Dict]):
    """Display detected beaconing patterns."""
    if not patterns:
        utils.print_info("No beaconing patterns detected")
        return
    
    utils.print_section("Detected Beaconing Patterns")
    
    for i, pattern in enumerate(patterns, 1):
        severity_icon = "🔴" if pattern['severity'] == 'high' else "🟡"
        print(f"\n{i}. {severity_icon} {pattern['pattern_type']}")
        print(f"   Remote IP: {pattern['remote_ip']}")
        print(f"   Connection Count: {pattern['connection_count']}")
        print(f"   Severity: {pattern['severity']}")
        
        if pattern['pattern_type'] == 'Regular Intervals':
            print(f"   Average Interval: {pattern['avg_interval_seconds']} seconds")
            print(f"   Variance: {pattern['variance']} seconds")
        elif pattern['pattern_type'] == 'Suspicious Processes':
            print(f"   Suspicious Processes: {pattern['suspicious_processes']}")
        elif pattern['pattern_type'] == 'Non-Standard Ports':
            print(f"   Non-Standard Ports: {pattern['non_standard_ports']}")
        
        # Show sample connections
        sample_conns = pattern['connections'][:3]
        for j, conn in enumerate(sample_conns, 1):
            print(f"     {j}. {conn.get('raddr', 'Unknown')} - {conn.get('process_name', 'Unknown')}")


def main(args):
    """Main function for network module."""
    utils.print_banner()
    utils.print_section("Network Defense Utilities")
    
    # Get active connections
    if args.connections:
        utils.print_info("Collecting active network connections...")
        connections = get_active_connections()
        display_network_connections(connections)
    
    # Get DNS cache
    if args.dns_cache:
        utils.print_info("Collecting DNS cache...")
        dns_entries = get_dns_cache()
        display_dns_cache(dns_entries)
    
    # Detect beaconing patterns
    if args.beaconing:
        utils.print_info("Detecting beaconing patterns...")
        connections = get_active_connections()
        patterns = detect_beaconing_patterns(connections)
        display_beaconing_patterns(patterns)
    
    # Block IP address
    if args.block:
        if not utils.validate_ip(args.block):
            utils.print_error(f"Invalid IP address: {args.block}")
            return
        
        utils.print_warning(f"Attempting to block IP address: {args.block}")
        if block_ip_address(args.block):
            utils.print_success(f"IP address {args.block} has been blocked")
        else:
            utils.print_error(f"Failed to block IP address {args.block}")
    
    # If no specific action requested, show all
    if not any([args.connections, args.dns_cache, args.beaconing, args.block]):
        utils.print_info("Collecting network information...")
        
        connections = get_active_connections()
        display_network_connections(connections)
        
        dns_entries = get_dns_cache()
        display_dns_cache(dns_entries)
        
        patterns = detect_beaconing_patterns(connections)
        display_beaconing_patterns(patterns)
    
    # Export if requested
    if hasattr(args, 'export') and args.export:
        # Prepare export data
        export_data = {
            'connections': get_active_connections() if not any([args.connections, args.dns_cache, args.beaconing, args.block]) else connections,
            'dns_cache': get_dns_cache() if not any([args.connections, args.dns_cache, args.beaconing, args.block]) else dns_entries,
            'beaconing_patterns': detect_beaconing_patterns(connections) if not any([args.connections, args.dns_cache, args.beaconing, args.block]) else patterns,
            'summary': {
                'total_connections': len(connections) if 'connections' in locals() else 0,
                'established_connections': len([c for c in connections if c.get('status') == 'ESTABLISHED']) if 'connections' in locals() else 0,
                'dns_entries': len(dns_entries) if 'dns_entries' in locals() else 0,
                'beaconing_patterns': len(patterns) if 'patterns' in locals() else 0
            }
        }
        
        export_format = getattr(args, 'export_format', 'json')
        compress = getattr(args, 'compress', False)
        
        utils.export_report_with_metadata(
            export_data, 
            'net', 
            export_format, 
            args.export, 
            compress
        )
    
    utils.print_success("Network defense analysis completed")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--connections', action='store_true')
    parser.add_argument('--beaconing', action='store_true')
    parser.add_argument('--block', type=str)
    parser.add_argument('--dns-cache', action='store_true')
    args = parser.parse_args()
    main(args)
