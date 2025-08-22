"""
Log collection and filtering module for the Blue Team CLI Toolkit.
Supports Windows Event Logs and Linux syslog/auth.log.
"""

import os
import sys
import platform
import subprocess
from typing import List, Dict, Any
from datetime import datetime, timedelta
import utils


def get_windows_event_logs(log_type: str = "Security", lines: int = 50, filter_keyword: str = None) -> List[Dict]:
    """Collect Windows Event Logs using PowerShell."""
    try:
        # PowerShell command to get recent events
        ps_command = f"""
        Get-WinEvent -LogName {log_type} -MaxEvents {lines} | 
        Select-Object TimeCreated, Id, LevelDisplayName, Message, ProviderName |
        ConvertTo-Json -Depth 3
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            import json
            events = json.loads(result.stdout)
            
            # Filter by keyword if specified
            if filter_keyword:
                events = [
                    event for event in events 
                    if filter_keyword.lower() in event.get('Message', '').lower()
                ]
            
            return events
        else:
            utils.print_warning(f"Failed to get Windows Event Logs: {result.stderr}")
            return []
            
    except Exception as e:
        utils.print_error(f"Error collecting Windows Event Logs: {e}")
        return []


def get_linux_syslog(lines: int = 50, filter_keyword: str = None) -> List[Dict]:
    """Collect Linux syslog entries."""
    try:
        # Try different syslog locations
        syslog_paths = [
            "/var/log/syslog",
            "/var/log/messages",
            "/var/log/auth.log"
        ]
        
        logs = []
        for log_path in syslog_paths:
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines_content = f.readlines()
                    
                    # Get last N lines
                    recent_lines = lines_content[-lines:] if len(lines_content) > lines else lines_content
                    
                    for line in recent_lines:
                        if filter_keyword and filter_keyword.lower() not in line.lower():
                            continue
                            
                        # Parse syslog line
                        try:
                            parts = line.split(' ', 5)  # Split into timestamp and message
                            if len(parts) >= 6:
                                timestamp_str = ' '.join(parts[:3])
                                message = parts[5].strip()
                                
                                logs.append({
                                    'timestamp': timestamp_str,
                                    'message': message,
                                    'source': log_path
                                })
                        except:
                            # If parsing fails, just add the raw line
                            logs.append({
                                'timestamp': 'Unknown',
                                'message': line.strip(),
                                'source': log_path
                            })
                
                break  # Use the first available log file
        
        return logs
        
    except Exception as e:
        utils.print_error(f"Error collecting Linux syslog: {e}")
        return []


def get_linux_auth_log(lines: int = 50, filter_keyword: str = None) -> List[Dict]:
    """Collect Linux auth.log entries specifically."""
    try:
        auth_log_path = "/var/log/auth.log"
        if not os.path.exists(auth_log_path):
            utils.print_warning("auth.log not found")
            return []
        
        logs = []
        with open(auth_log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines_content = f.readlines()
            
            # Get last N lines
            recent_lines = lines_content[-lines:] if len(lines_content) > lines else lines_content
            
            for line in recent_lines:
                if filter_keyword and filter_keyword.lower() not in line.lower():
                    continue
                    
                # Parse auth.log line
                try:
                    parts = line.split(' ', 5)
                    if len(parts) >= 6:
                        timestamp_str = ' '.join(parts[:3])
                        message = parts[5].strip()
                        
                        logs.append({
                            'timestamp': timestamp_str,
                            'message': message,
                            'source': 'auth.log'
                        })
                except:
                    logs.append({
                        'timestamp': 'Unknown',
                        'message': line.strip(),
                        'source': 'auth.log'
                    })
        
        return logs
        
    except Exception as e:
        utils.print_error(f"Error collecting auth.log: {e}")
        return []


def analyze_logs_for_suspicious_activity(logs: List[Dict], os_type: str) -> Dict[str, Any]:
    """Analyze logs for suspicious activity patterns."""
    suspicious_patterns = {
        'windows': [
            'failed logon', 'account lockout', 'privilege escalation',
            'service installation', 'registry modification', 'process creation',
            'network connection', 'file access', 'audit failure'
        ],
        'linux': [
            'failed password', 'invalid user', 'authentication failure',
            'sudo', 'su', 'ssh', 'root login', 'permission denied',
            'connection refused', 'timeout'
        ]
    }
    
    analysis = {
        'total_entries': len(logs),
        'suspicious_entries': [],
        'failed_logins': 0,
        'privilege_escalation': 0,
        'network_anomalies': 0,
        'file_access': 0
    }
    
    patterns = suspicious_patterns.get(os_type, [])
    
    for log_entry in logs:
        message = log_entry.get('Message', log_entry.get('message', '')).lower()
        
        # Check for suspicious patterns
        for pattern in patterns:
            if pattern in message:
                analysis['suspicious_entries'].append({
                    'pattern': pattern,
                    'entry': log_entry
                })
        
        # Count specific types
        if any(term in message for term in ['failed', 'failure', 'invalid']):
            analysis['failed_logins'] += 1
        if any(term in message for term in ['privilege', 'sudo', 'su', 'elevation']):
            analysis['privilege_escalation'] += 1
        if any(term in message for term in ['network', 'connection', 'port']):
            analysis['network_anomalies'] += 1
        if any(term in message for term in ['file', 'access', 'read', 'write']):
            analysis['file_access'] += 1
    
    return analysis


def display_logs(logs: List[Dict], os_type: str):
    """Display logs in a formatted way."""
    if not logs:
        utils.print_warning("No logs found")
        return
    
    utils.print_section(f"Recent {os_type.title()} Logs")
    
    for i, log_entry in enumerate(logs, 1):
        if os_type == 'windows':
            timestamp = log_entry.get('TimeCreated', 'Unknown')
            level = log_entry.get('LevelDisplayName', 'Unknown')
            message = log_entry.get('Message', 'No message')
            provider = log_entry.get('ProviderName', 'Unknown')
            
            print(f"\n{i}. [{level}] {timestamp}")
            print(f"   Provider: {provider}")
            print(f"   Message: {message[:200]}{'...' if len(message) > 200 else ''}")
            
        else:  # Linux
            timestamp = log_entry.get('timestamp', 'Unknown')
            message = log_entry.get('message', 'No message')
            source = log_entry.get('source', 'Unknown')
            
            print(f"\n{i}. [{source}] {timestamp}")
            print(f"   {message}")


def main(args):
    """Main function for logs module."""
    utils.print_banner()
    utils.print_section("Log Collection and Analysis")
    
    os_type = args.os.lower()
    lines = args.lines
    filter_keyword = args.filter
    
    utils.print_info(f"Collecting {lines} log entries from {os_type}")
    
    logs_data = []
    
    if os_type == 'windows':
        # Collect Windows Event Logs
        security_logs = get_windows_event_logs("Security", lines, filter_keyword)
        system_logs = get_windows_event_logs("System", lines, filter_keyword)
        application_logs = get_windows_event_logs("Application", lines, filter_keyword)
        
        logs_data.extend(security_logs)
        logs_data.extend(system_logs)
        logs_data.extend(application_logs)
        
    else:  # Linux
        # Collect Linux logs
        syslog_data = get_linux_syslog(lines, filter_keyword)
        auth_log_data = get_linux_auth_log(lines, filter_keyword)
        
        logs_data.extend(syslog_data)
        logs_data.extend(auth_log_data)
    
    # Display logs
    display_logs(logs_data, os_type)
    
    # Analyze for suspicious activity
    utils.print_section("Log Analysis")
    analysis = analyze_logs_for_suspicious_activity(logs_data, os_type)
    
    print(f"\nTotal log entries: {analysis['total_entries']}")
    print(f"Suspicious entries: {len(analysis['suspicious_entries'])}")
    print(f"Failed logins: {analysis['failed_logins']}")
    print(f"Privilege escalation attempts: {analysis['privilege_escalation']}")
    print(f"Network anomalies: {analysis['network_anomalies']}")
    print(f"File access events: {analysis['file_access']}")
    
    # Show suspicious entries
    if analysis['suspicious_entries']:
        utils.print_section("Suspicious Log Entries")
        for i, entry in enumerate(analysis['suspicious_entries'][:10], 1):  # Show first 10
            pattern = entry['pattern']
            log_entry = entry['entry']
            
            if os_type == 'windows':
                message = log_entry.get('Message', 'No message')[:100]
                timestamp = log_entry.get('TimeCreated', 'Unknown')
            else:
                message = log_entry.get('message', 'No message')[:100]
                timestamp = log_entry.get('timestamp', 'Unknown')
            
            print(f"\n{i}. Pattern: {pattern}")
            print(f"   Time: {timestamp}")
            print(f"   Message: {message}...")
    
    # Export if requested
    if hasattr(args, 'export') and args.export:
        # Prepare export data with analysis
        export_data = {
            'logs': logs_data,
            'analysis': analysis,
            'summary': {
                'total_entries': analysis['total_entries'],
                'suspicious_entries': len(analysis['suspicious_entries']),
                'failed_logins': analysis['failed_logins'],
                'privilege_escalation': analysis['privilege_escalation'],
                'network_anomalies': analysis['network_anomalies'],
                'file_access': analysis['file_access']
            }
        }
        
        # Use new export functionality
        export_format = getattr(args, 'export_format', 'json')
        compress = getattr(args, 'compress', False)
        
        utils.export_report_with_metadata(
            export_data, 
            'logs', 
            export_format, 
            args.export, 
            compress
        )
    
    utils.print_success("Log collection and analysis completed")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--os', default='windows')
    parser.add_argument('--lines', type=int, default=50)
    parser.add_argument('--filter', type=str)
    parser.add_argument('--export', type=str)
    args = parser.parse_args()
    main(args)
