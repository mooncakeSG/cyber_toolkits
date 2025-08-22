"""
IOC (Indicators of Compromise) scanner for the Blue Team CLI Toolkit.
Checks logs, DNS cache, and processes for malicious indicators.
"""

import os
import sys
import platform
import subprocess
import psutil
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import utils


def validate_ioc(ioc_type: str, value: str) -> bool:
    """Validate IOC format."""
    if ioc_type == 'ip':
        return utils.validate_ip(value)
    elif ioc_type == 'domain':
        return utils.validate_domain(value)
    elif ioc_type == 'hash':
        return utils.validate_hash(value)
    return False


def scan_logs_for_ioc(ioc_type: str, value: str) -> List[Dict]:
    """Scan system logs for IOC matches."""
    matches = []
    
    try:
        if platform.system() == "Windows":
            # Scan Windows Event Logs
            log_types = ["Security", "System", "Application"]
            
            for log_type in log_types:
                try:
                    ps_command = f"""
                    Get-WinEvent -LogName {log_type} -MaxEvents 1000 | 
                    Where-Object {{ $_.Message -like "*{value}*" }} |
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
                        
                        for event in events:
                            matches.append({
                                'source': f'Windows Event Log - {log_type}',
                                'timestamp': event.get('TimeCreated', 'Unknown'),
                                'level': event.get('LevelDisplayName', 'Unknown'),
                                'message': event.get('Message', ''),
                                'provider': event.get('ProviderName', 'Unknown'),
                                'ioc_type': ioc_type,
                                'ioc_value': value
                            })
                            
                except Exception as e:
                    utils.print_warning(f"Error scanning {log_type} logs: {e}")
                    
        else:
            # Scan Linux logs
            log_files = [
                "/var/log/syslog",
                "/var/log/messages", 
                "/var/log/auth.log",
                "/var/log/secure"
            ]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    try:
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if value.lower() in line.lower():
                                    matches.append({
                                        'source': log_file,
                                        'line_number': line_num,
                                        'timestamp': extract_timestamp_from_log(line),
                                        'message': line.strip(),
                                        'ioc_type': ioc_type,
                                        'ioc_value': value
                                    })
                    except Exception as e:
                        utils.print_warning(f"Error reading {log_file}: {e}")
                        
    except Exception as e:
        utils.print_error(f"Error scanning logs for IOC: {e}")
    
    return matches


def extract_timestamp_from_log(log_line: str) -> str:
    """Extract timestamp from log line."""
    # Common timestamp patterns
    patterns = [
        r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',  # Jan 15 10:30:45
        r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',  # 2024-01-15 10:30:45
        r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})',  # 01/15/2024 10:30:45
    ]
    
    for pattern in patterns:
        match = re.search(pattern, log_line)
        if match:
            return match.group(1)
    
    return 'Unknown'


def scan_dns_cache_for_ioc(ioc_type: str, value: str) -> List[Dict]:
    """Scan DNS cache for IOC matches."""
    matches = []
    
    try:
        if ioc_type == 'domain':
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
                        for i, line in enumerate(lines):
                            if value.lower() in line.lower():
                                # Extract context around the match
                                start = max(0, i - 5)
                                end = min(len(lines), i + 6)
                                context = '\n'.join(lines[start:end])
                                
                                matches.append({
                                    'source': 'Windows DNS Cache',
                                    'match': line.strip(),
                                    'context': context,
                                    'ioc_type': ioc_type,
                                    'ioc_value': value
                                })
                                
                except Exception as e:
                    utils.print_warning(f"Error scanning Windows DNS cache: {e}")
                    
            else:
                # Linux DNS cache (systemd-resolved)
                try:
                    result = subprocess.run(
                        ["systemd-resolve", "--statistics"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0 and value.lower() in result.stdout.lower():
                        matches.append({
                            'source': 'Linux DNS Cache',
                            'match': 'Found in systemd-resolve statistics',
                            'context': result.stdout,
                            'ioc_type': ioc_type,
                            'ioc_value': value
                        })
                        
                except Exception as e:
                    utils.print_warning(f"Error scanning Linux DNS cache: {e}")
                    
    except Exception as e:
        utils.print_error(f"Error scanning DNS cache for IOC: {e}")
    
    return matches


def scan_processes_for_ioc(ioc_type: str, value: str) -> List[Dict]:
    """Scan running processes for IOC matches."""
    matches = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'memory_info']):
            try:
                proc_info = proc.info
                
                # Check process name
                if value.lower() in proc_info['name'].lower():
                    matches.append({
                        'source': 'Process Name',
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'exe': proc_info.get('exe', 'Unknown'),
                        'cmdline': ' '.join(proc_info.get('cmdline', [])),
                        'memory_mb': round(proc_info['memory_info'].rss / 1024 / 1024, 2) if proc_info['memory_info'] else 0,
                        'ioc_type': ioc_type,
                        'ioc_value': value
                    })
                
                # Check command line arguments
                cmdline = ' '.join(proc_info.get('cmdline', []))
                if value.lower() in cmdline.lower():
                    matches.append({
                        'source': 'Process Command Line',
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'exe': proc_info.get('exe', 'Unknown'),
                        'cmdline': cmdline,
                        'memory_mb': round(proc_info['memory_info'].rss / 1024 / 1024, 2) if proc_info['memory_info'] else 0,
                        'ioc_type': ioc_type,
                        'ioc_value': value
                    })
                
                # Check executable hash if it's a hash IOC
                if ioc_type == 'hash' and proc_info.get('exe') and os.path.exists(proc_info['exe']):
                    file_hash = utils.calculate_hash(proc_info['exe'])
                    if file_hash and file_hash.lower() == value.lower():
                        matches.append({
                            'source': 'Process Executable Hash',
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'exe': proc_info['exe'],
                            'hash': file_hash,
                            'memory_mb': round(proc_info['memory_info'].rss / 1024 / 1024, 2) if proc_info['memory_info'] else 0,
                            'ioc_type': ioc_type,
                            'ioc_value': value
                        })
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        utils.print_error(f"Error scanning processes for IOC: {e}")
    
    return matches


def scan_network_connections_for_ioc(ioc_type: str, value: str) -> List[Dict]:
    """Scan network connections for IOC matches."""
    matches = []
    
    try:
        for conn in psutil.net_connections():
            try:
                # Check local address
                if conn.laddr and ioc_type == 'ip':
                    if value == conn.laddr.ip:
                        matches.append({
                            'source': 'Network Connection - Local',
                            'connection_type': str(conn.type),
                            'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'None',
                            'status': conn.status,
                            'pid': conn.pid,
                            'ioc_type': ioc_type,
                            'ioc_value': value
                        })
                
                # Check remote address
                if conn.raddr and ioc_type == 'ip':
                    if value == conn.raddr.ip:
                        matches.append({
                            'source': 'Network Connection - Remote',
                            'connection_type': str(conn.type),
                            'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'None',
                            'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}",
                            'status': conn.status,
                            'pid': conn.pid,
                            'ioc_type': ioc_type,
                            'ioc_value': value
                        })
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except Exception as e:
        utils.print_error(f"Error scanning network connections for IOC: {e}")
    
    return matches


def scan_files_for_ioc(ioc_type: str, value: str) -> List[Dict]:
    """Scan files for IOC matches."""
    matches = []
    
    try:
        # Common directories to scan
        directories = []
        if platform.system() == "Windows":
            directories = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads"),
                "C:\\Temp",
                "C:\\Windows\\Temp"
            ]
        else:
            directories = [
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~/Downloads"),
                "/tmp",
                "/var/tmp"
            ]
        
        for directory in directories:
            if os.path.exists(directory):
                try:
                    for root, dirs, filenames in os.walk(directory):
                        for filename in filenames:
                            file_path = os.path.join(root, filename)
                            
                            # Check filename
                            if value.lower() in filename.lower():
                                matches.append({
                                    'source': 'File Name',
                                    'file_path': file_path,
                                    'filename': filename,
                                    'ioc_type': ioc_type,
                                    'ioc_value': value
                                })
                            
                            # Check file hash if it's a hash IOC
                            if ioc_type == 'hash':
                                try:
                                    file_hash = utils.calculate_hash(file_path)
                                    if file_hash and file_hash.lower() == value.lower():
                                        matches.append({
                                            'source': 'File Hash',
                                            'file_path': file_path,
                                            'filename': filename,
                                            'hash': file_hash,
                                            'ioc_type': ioc_type,
                                            'ioc_value': value
                                        })
                                except Exception:
                                    continue
                                    
                except (OSError, PermissionError):
                    continue
                    
    except Exception as e:
        utils.print_error(f"Error scanning files for IOC: {e}")
    
    return matches


def enrich_ioc_with_virustotal(ioc_type: str, value: str) -> Optional[Dict]:
    """Enrich IOC with VirusTotal information."""
    if not utils.VIRUSTOTAL_API_KEY:
        utils.print_warning("VirusTotal API key not set. Set VIRUSTOTAL_API_KEY environment variable.")
        return None
    
    utils.print_info("Enriching IOC with VirusTotal...")
    vt_data = utils.virus_total_lookup(ioc_type, value)
    
    if vt_data:
        return {
            'ioc_type': ioc_type,
            'ioc_value': value,
            'vt_response_code': vt_data.get('response_code', 0),
            'vt_positives': vt_data.get('positives', 0),
            'vt_total': vt_data.get('total', 0),
            'vt_detection_ratio': f"{vt_data.get('positives', 0)}/{vt_data.get('total', 0)}",
            'vt_scan_date': vt_data.get('scan_date', 'Unknown'),
            'vt_permalink': vt_data.get('permalink', ''),
            'vt_detections': vt_data.get('scans', {})
        }
    
    return None


def display_ioc_scan_results(scan_results: Dict[str, Any]):
    """Display IOC scan results."""
    utils.print_section("IOC Scan Results")
    
    ioc_type = scan_results['ioc_type']
    ioc_value = scan_results['ioc_value']
    
    print(f"IOC Type: {ioc_type}")
    print(f"IOC Value: {ioc_value}")
    print(f"Scan Timestamp: {scan_results['timestamp']}")
    
    # Log matches
    if scan_results['log_matches']:
        utils.print_section("Log Matches")
        for i, match in enumerate(scan_results['log_matches'][:10], 1):  # Show first 10
            print(f"\n{i}. Source: {match['source']}")
            print(f"   Timestamp: {match.get('timestamp', 'Unknown')}")
            print(f"   Message: {match.get('message', '')[:200]}...")
    
    # DNS cache matches
    if scan_results['dns_matches']:
        utils.print_section("DNS Cache Matches")
        for i, match in enumerate(scan_results['dns_matches'], 1):
            print(f"\n{i}. Source: {match['source']}")
            print(f"   Match: {match['match']}")
    
    # Process matches
    if scan_results['process_matches']:
        utils.print_section("Process Matches")
        for i, match in enumerate(scan_results['process_matches'], 1):
            print(f"\n{i}. Source: {match['source']}")
            print(f"   PID: {match['pid']}")
            print(f"   Name: {match['name']}")
            print(f"   Path: {match.get('exe', 'Unknown')}")
            print(f"   Memory: {match.get('memory_mb', 0)} MB")
    
    # Network connection matches
    if scan_results['network_matches']:
        utils.print_section("Network Connection Matches")
        for i, match in enumerate(scan_results['network_matches'], 1):
            print(f"\n{i}. Source: {match['source']}")
            print(f"   Local: {match['local_addr']}")
            print(f"   Remote: {match['remote_addr']}")
            print(f"   Status: {match['status']}")
            print(f"   PID: {match['pid']}")
    
    # File matches
    if scan_results['file_matches']:
        utils.print_section("File Matches")
        for i, match in enumerate(scan_results['file_matches'], 1):
            print(f"\n{i}. Source: {match['source']}")
            print(f"   File: {match['file_path']}")
            if match.get('hash'):
                print(f"   Hash: {match['hash']}")
    
    # VirusTotal enrichment
    if scan_results.get('virustotal_data'):
        utils.print_section("VirusTotal Enrichment")
        vt_data = scan_results['virustotal_data']
        print(f"Detection Ratio: {vt_data['vt_detection_ratio']}")
        print(f"Scan Date: {vt_data['vt_scan_date']}")
        print(f"Permalink: {vt_data['vt_permalink']}")
        
        if vt_data['vt_positives'] > 0:
            utils.print_warning(f"Found {vt_data['vt_positives']} positive detections!")
            
            # Show top detections
            detections = vt_data.get('vt_detections', {})
            positive_detections = {k: v for k, v in detections.items() if v.get('detected', False)}
            
            if positive_detections:
                print("\nTop Detections:")
                for i, (av_name, av_data) in enumerate(list(positive_detections.items())[:5], 1):
                    print(f"  {i}. {av_name}: {av_data.get('result', 'Unknown')}")
    
    # Summary
    utils.print_section("Scan Summary")
    total_matches = (len(scan_results['log_matches']) + 
                    len(scan_results['dns_matches']) + 
                    len(scan_results['process_matches']) + 
                    len(scan_results['network_matches']) + 
                    len(scan_results['file_matches']))
    
    print(f"Total Matches Found: {total_matches}")
    print(f"Log Matches: {len(scan_results['log_matches'])}")
    print(f"DNS Cache Matches: {len(scan_results['dns_matches'])}")
    print(f"Process Matches: {len(scan_results['process_matches'])}")
    print(f"Network Matches: {len(scan_results['network_matches'])}")
    print(f"File Matches: {len(scan_results['file_matches'])}")
    
    if total_matches > 0:
        utils.print_warning(f"IOC {ioc_value} found in {total_matches} locations!")
    else:
        utils.print_success(f"No matches found for IOC {ioc_value}")


def main(args):
    """Main function for IOC module."""
    utils.print_banner()
    utils.print_section("IOC Scanner")
    
    ioc_type = args.type.lower()
    ioc_value = args.value
    
    # Validate IOC
    if not validate_ioc(ioc_type, ioc_value):
        utils.print_error(f"Invalid {ioc_type} format: {ioc_value}")
        return
    
    utils.print_info(f"Scanning for {ioc_type}: {ioc_value}")
    
    # Initialize scan results
    scan_results = {
        'ioc_type': ioc_type,
        'ioc_value': ioc_value,
        'timestamp': utils.format_timestamp(datetime.now().timestamp()),
        'log_matches': [],
        'dns_matches': [],
        'process_matches': [],
        'network_matches': [],
        'file_matches': [],
        'virustotal_data': None
    }
    
    # Scan logs
    if args.scan_logs:
        utils.print_info("Scanning system logs...")
        scan_results['log_matches'] = scan_logs_for_ioc(ioc_type, ioc_value)
    
    # Scan DNS cache
    utils.print_info("Scanning DNS cache...")
    scan_results['dns_matches'] = scan_dns_cache_for_ioc(ioc_type, ioc_value)
    
    # Scan processes
    if args.scan_processes:
        utils.print_info("Scanning running processes...")
        scan_results['process_matches'] = scan_processes_for_ioc(ioc_type, ioc_value)
    
    # Scan network connections
    utils.print_info("Scanning network connections...")
    scan_results['network_matches'] = scan_network_connections_for_ioc(ioc_type, ioc_value)
    
    # Scan files
    utils.print_info("Scanning files...")
    scan_results['file_matches'] = scan_files_for_ioc(ioc_type, ioc_value)
    
    # VirusTotal enrichment
    if args.vt:
        scan_results['virustotal_data'] = enrich_ioc_with_virustotal(ioc_type, ioc_value)
    
    # Display results
    display_ioc_scan_results(scan_results)
    
    # Export if requested
    if hasattr(args, 'export') and args.export:
        export_format = getattr(args, 'export_format', 'json')
        compress = getattr(args, 'compress', False)
        
        utils.export_report_with_metadata(
            scan_results, 
            'ioc', 
            export_format, 
            args.export, 
            compress
        )
    
    utils.print_success("IOC scan completed")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, choices=['ip', 'domain', 'hash'])
    parser.add_argument('--value', required=True)
    parser.add_argument('--vt', action='store_true')
    parser.add_argument('--scan-logs', action='store_true')
    parser.add_argument('--scan-processes', action='store_true')
    args = parser.parse_args()
    main(args)
