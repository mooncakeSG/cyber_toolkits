"""
Shared utility functions for the Blue Team CLI Toolkit.
"""

import json
import csv
import os
import sys
import platform
import subprocess
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import psutil

# Global configuration
DEBUG_MODE = os.getenv('BLUETEAM_DEBUG', 'false').lower() == 'true'
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')


def print_banner():
    """Print the Blue Team Toolkit banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    Blue Team CLI Toolkit                     ║
║              Defensive Security Operations                   ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_info(message: str):
    """Print an info message."""
    print(f"[+] {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"[!] {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"[ERROR] {message}")


def print_success(message: str):
    """Print a success message."""
    print(f"[✓] {message}")


def is_admin() -> bool:
    """Check if the script is running with administrative privileges."""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except:
        return False


def get_system_info() -> Dict[str, str]:
    """Get basic system information."""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "python_version": sys.version,
        "is_admin": is_admin()
    }


def export_to_json(data: Any, filename: str) -> bool:
    """Export data to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        print_success(f"Data exported to {filename}")
        return True
    except Exception as e:
        print_error(f"Failed to export to JSON: {e}")
        return False


def export_to_csv(data: List[Dict], filename: str) -> bool:
    """Export data to CSV file."""
    try:
        if not data:
            print_warning("No data to export")
            return False
            
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print_success(f"Data exported to {filename}")
        return True
    except Exception as e:
        print_error(f"Failed to export to CSV: {e}")
        return False


def generate_timestamped_filename(base_name: str, extension: str = "json") -> str:
    """Generate timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"


def export_data(data: Any, export_format: str = "json", filename: str = None, 
                compress: bool = False, base_name: str = "report") -> str:
    """
    Enhanced export function supporting multiple formats and compression.
    
    Args:
        data: Data to export
        export_format: Format to export (json, csv, txt)
        filename: Custom filename (optional)
        compress: Whether to compress the file
        base_name: Base name for timestamped files
    
    Returns:
        Path to exported file
    """
    try:
        # Generate filename if not provided
        if not filename:
            filename = generate_timestamped_filename(base_name, export_format)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # Export based on format
        if export_format.lower() == "json":
            if isinstance(data, list) and data and isinstance(data[0], dict):
                # Flatten nested data for better JSON structure
                export_data = data
            else:
                export_data = data
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
                
        elif export_format.lower() == "csv":
            if isinstance(data, list) and data and isinstance(data[0], dict):
                export_data = data
            else:
                # Convert non-list data to list format
                export_data = [{"data": str(data)}]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if export_data:
                    writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
                    writer.writeheader()
                    writer.writerows(export_data)
                    
        elif export_format.lower() == "txt":
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"{key}: {value}\n")
                elif isinstance(data, list):
                    for item in data:
                        f.write(f"{item}\n")
                else:
                    f.write(str(data))
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
        
        # Compress if requested
        if compress:
            import zipfile
            zip_filename = f"{filename}.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(filename, os.path.basename(filename))
            
            # Remove original file
            os.remove(filename)
            filename = zip_filename
        
        print_success(f"Data exported to {filename}")
        return filename
        
    except Exception as e:
        print_error(f"Failed to export data: {e}")
        return ""


def export_report_with_metadata(data: Any, report_type: str, export_format: str = "json", 
                               filename: str = None, compress: bool = False) -> str:
    """
    Export report with metadata wrapper.
    
    Args:
        data: Report data
        report_type: Type of report (ir, hunt, logs, ioc, net)
        export_format: Export format
        filename: Custom filename
        compress: Whether to compress
    
    Returns:
        Path to exported file
    """
    # Create metadata wrapper
    metadata = {
        "report_metadata": {
            "toolkit_version": "1.0.0",
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "hostname": platform.node(),
            "platform": platform.system(),
            "python_version": platform.python_version()
        },
        "report_data": data
    }
    
    base_name = f"{report_type}_report"
    return export_data(metadata, export_format, filename, compress, base_name)


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to human-readable string."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def run_command(command: str, shell: bool = True) -> tuple:
    """Run a system command and return output."""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def virus_total_lookup(ioc_type: str, value: str) -> Optional[Dict]:
    """Look up IOC in VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        print_warning("VirusTotal API key not set. Set VIRUSTOTAL_API_KEY environment variable.")
        return None
    
    try:
        if ioc_type == 'ip':
            url = f"https://www.virustotal.com/vtapi/v2/ip-address/report"
            params = {'apikey': VIRUSTOTAL_API_KEY, 'ip': value}
        elif ioc_type == 'domain':
            url = f"https://www.virustotal.com/vtapi/v2/domain/report"
            params = {'apikey': VIRUSTOTAL_API_KEY, 'domain': value}
        elif ioc_type == 'hash':
            url = f"https://www.virustotal.com/vtapi/v2/file/report"
            params = {'apikey': VIRUSTOTAL_API_KEY, 'resource': value}
        else:
            return None
            
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print_warning(f"VirusTotal API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print_warning(f"VirusTotal API request failed: {e}")
        return None


def validate_ip(ip: str) -> bool:
    """Validate IP address format."""
    import ipaddress
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_domain(domain: str) -> bool:
    """Validate domain format."""
    import re
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(pattern, domain))


def validate_hash(hash_value: str) -> bool:
    """Validate hash format (MD5, SHA1, SHA256)."""
    import re
    md5_pattern = r'^[a-fA-F0-9]{32}$'
    sha1_pattern = r'^[a-fA-F0-9]{40}$'
    sha256_pattern = r'^[a-fA-F0-9]{64}$'
    
    return (bool(re.match(md5_pattern, hash_value)) or 
            bool(re.match(sha1_pattern, hash_value)) or 
            bool(re.match(sha256_pattern, hash_value)))


def get_process_tree() -> List[Dict]:
    """Get process tree with parent-child relationships."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'ppid', 'create_time', 'memory_info']):
        try:
            proc_info = proc.info
            proc_info['children'] = []
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Build parent-child relationships
    for proc in processes:
        for child in processes:
            if child['ppid'] == proc['pid']:
                proc['children'].append(child['pid'])
    
    return processes


def calculate_hash(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
    """Calculate file hash."""
    import hashlib
    
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print_error(f"Failed to calculate hash for {file_path}: {e}")
        return None


def is_suspicious_process(process_name: str) -> bool:
    """Check if process name matches known suspicious patterns."""
    suspicious_patterns = [
        'cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe',
        'rundll32.exe', 'regsvr32.exe', 'mshta.exe', 'certutil.exe',
        'bitsadmin.exe', 'wmic.exe', 'schtasks.exe', 'at.exe',
        'net.exe', 'netstat.exe', 'ipconfig.exe', 'whoami.exe'
    ]
    
    return process_name.lower() in [p.lower() for p in suspicious_patterns]


def get_network_connections() -> List[Dict]:
    """Get all network connections."""
    connections = []
    try:
        for conn in psutil.net_connections():
            try:
                conn_info = {
                    'fd': conn.fd,
                    'family': conn.family,
                    'type': conn.type,
                    'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    'status': conn.status,
                    'pid': conn.pid
                }
                connections.append(conn_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        print_error(f"Failed to get network connections: {e}")
    
    return connections
